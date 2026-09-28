#!/usr/bin/env python3
"""Aprendizados da clínica para o kit: rascunho → filtro de privacidade → link de envio.

Roda DENTRO do repo da clínica (o kit fica em `.kit/`):

    python3 .kit/ferramentas/kit/filtrar_aprendizado.py novo --titulo "…" --tipo calculo
    python3 .kit/ferramentas/kit/filtrar_aprendizado.py filtrar contribuicoes-kit/AAAA-MM-DD-NN-tema.md
    python3 .kit/ferramentas/kit/filtrar_aprendizado.py enviado contribuicoes-kit/… --issue 12
    python3 .kit/ferramentas/kit/filtrar_aprendizado.py indice

- `novo`: cria o rascunho no formato fixo (numeração do dia) e atualiza o índice.
- `filtrar`: procura dado da clínica ou dado pessoal. Achou → lista (valor
  mascarado) e sai 1; nada é enviado. Limpo → marca "filtrado", imprime o
  texto final e o LINK pré-preenchido do formulário de issue do kit (o humano
  lê e clica "Submit new issue"). Sai 0.
- `enviado`: registra o número da issue aberta (status "enviado #N").
- `indice`: refaz `contribuicoes-kit/00-INDICE.md` a partir dos arquivos.

O filtro também é usado pelo kit (`coletar_aprendizados.py`) como 2ª trava.
Só stdlib. Códigos: 0 ok · 1 bloqueado pelo filtro · 2 erro de uso.
"""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import quote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _comum import RAIZ_KIT, hoje, ler_versao, slugificar  # noqa: E402

REPO_KIT = "fmunizmcorp/implantarabi-ia"
FORMULARIO = "aprendizado-clinica.yml"
PASTA = "contribuicoes-kit"
LIMITE_URL = 7500  # o GitHub recusa URLs muito longas (~8 KB)
TIPOS = {
    "calculo": "Cálculo / conversão de valores",
    "regra": "Correção de regra do kit",
    "api": "Comportamento real da API",
    "processo": "Processo / conversa / ritual",
    "ferramenta": "Ferramenta (script do kit)",
}
STATUS_ABERTOS = ("rascunho", "filtrado")
# Só os aprendizados datados (AAAA-MM-DD-NN-tema.md); nunca o 00-INDICE.md.
PADRAO_ARQ = "[12][0-9][0-9][0-9]-[01][0-9]-[0-3][0-9]-*.md"

# Seções do arquivo ↔ campos do formulário de issue (ids em .github/ISSUE_TEMPLATE/).
SECOES = [
    ("O que o kit diz", "kit_diz"),
    ("O que acontece de verdade", "realidade"),
    ("Regra proposta", "regra"),
    ("Como detectar", "detectar"),
    ("Evidência (só o tipo, nunca o conteúdo)", "evidencia"),
]
CAMPOS_CABECALHO = [("Tipo", "tipo"), ("Arquivo do kit afetado", "arquivo_kit"),
                    ("Versão do kit", "versao_kit")]

# ---------------------------------------------------------------------------
# Filtro de privacidade
# ---------------------------------------------------------------------------
PADROES = [
    ("chave da API", re.compile(r"rbk_[A-Za-z0-9_-]{3,}")),
    ("token do GitHub", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{10,}|github_pat_[A-Za-z0-9_]{10,})")),
    ("CPF", re.compile(r"(?<!\d)(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})(?!\d)")),
    ("CNPJ", re.compile(r"(?<!\d)(\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}|\d{14})(?!\d)")),
    ("e-mail", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
    ("telefone", re.compile(r"(?<!\d)\(?\d{2}\)?\s?9?\d{4}[-\s]\d{4}(?!\d)")),
    ("CEP", re.compile(r"(?<!\d)\d{5}-\d{3}(?!\d)")),
    ("ID interno do Rabi", re.compile(
        r"\b(?:id|ID|Id)\b\s*[:=#]?\s*\d{2,}"              # id: 212 / ID 212
        r"|\b[a-z][A-Za-z]*(?:Id|ID|Ids)\b[\"']?\s*[:=]\s*\[?\s*\"?\d+"  # servicoId": 4521, convenioId=77
        r"|/[a-z-]+/\d{2,}(?![\w.-])")),                     # /convenios/212

    ("senha", re.compile(r"\bsenha\s*[:=]\s*\S+", re.I)),
]
# Número com cara de dinheiro (187,43 · 1.234,56 · R$ 90) ou percentual com casa decimal (12,5%).
VALOR = re.compile(r"(?:R\$\s*\d[\d.]*(?:,\d+)?|(?<![\d.,])\d{1,3}(?:\.\d{3})*,\d{2}(?![\d%])|(?<![\d.,])\d+,\d+\s?%)")
MARCA_EXEMPLO = re.compile(r"^\W{0,3}\(exemplo\)", re.I)
URL = re.compile(r"https?://[^\s)>\]`'\"]+")
DOMINIO = re.compile(r"(?<![@\w./])(?:www\.)?[\w-]+(?:\.[\w-]+)*\.(?:com|com\.br|net|org|org\.br|med\.br|br)\b", re.I)
HOSTS_OK = ("rabisistemas.com.br", "gov.br", "ans.gov.br", "anvisa.gov.br", "github.com")
GITHUB_OK = (f"github.com/{REPO_KIT}".lower(),)
PALAVRAS_GENERICAS = {
    "clinica", "clinicas", "centro", "medico", "medica", "medicos", "saude", "instituto",
    "hospital", "consultorio", "especialidades", "integrada", "integrado", "servicos", "ltda",
    "eireli", "grupo", "rede", "unidade", "diagnostico", "imagem", "odontologia", "exemplo",
    # especialidades e termos comuns (não identificam ninguém sozinhos)
    "cardiologia", "dermatologia", "pediatria", "ortopedia", "ginecologia", "obstetricia",
    "oftalmologia", "oncologia", "neurologia", "urologia", "endocrinologia", "gastroenterologia",
    "psiquiatria", "psicologia", "fisioterapia", "nutricao", "radiologia", "laboratorio",
    "vacinas", "infusao", "infusoes", "reumatologia", "pneumologia", "nefrologia", "hematologia",
    "otorrinolaringologia", "mastologia", "geriatria", "medicina", "vida", "bem", "estar",
    "familia", "mulher", "crianca", "sorriso", "especializada", "especializado", "policlinica",
    "ambulatorio", "day", "care", "center", "health", "doutor", "doutora", "dra", "dr",
}
DOMINIOS_OK = ("rabisistemas.com.br", "gov.br", "github.com")


def _sem_acento(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


def mascarar(valor: str) -> str:
    v = valor.strip()
    return v[:3] + "…" if len(v) > 4 else "…"


def termos_da_clinica(repo: Path | None) -> list[str]:
    """Nome, slug e nomes cadastrados em dados/ (para o filtro nunca deixar sair)."""
    if not repo:
        return []
    termos: set[str] = set()
    estado = repo / "ESTADO.md"
    if estado.is_file():
        m = re.search(r"^- \*\*Clínica:\*\*\s*(.+?)\s*$", estado.read_text(encoding="utf-8", errors="replace"), re.M)
        if m and "<" not in m.group(1):
            nome = m.group(1).strip()
            termos.add(nome)
            termos.add(slugificar(nome))
            for palavra in re.findall(r"[\wÀ-ÿ]+", nome):
                if len(palavra) >= 4 and _sem_acento(palavra) not in PALAVRAS_GENERICAS:
                    termos.add(palavra)
    try:
        url = subprocess.run(["git", "-C", str(repo), "remote", "get-url", "origin"],
                             capture_output=True, text=True, timeout=10).stdout.strip()
        if url:
            termos.add(re.sub(r"\.git$", "", url.rstrip("/")).rsplit("/", 1)[-1])
    except (OSError, subprocess.SubprocessError):
        pass
    nomes: set[str] = set()
    dados = repo / "dados"
    if dados.is_dir():
        for arq in dados.rglob("*.csv"):
            nomes |= _nomes_do_csv(arq)
        for arq in dados.rglob("*.md"):
            nomes |= _nomes_do_md(arq)
    for extra in ("PAPEIS.md", "diretrizes-da-equipe.md"):
        if (repo / extra).is_file():
            nomes |= _nomes_do_md(repo / extra)
    for nome in nomes:
        termos.add(nome)
        partes = [p for p in re.findall(r"[\wÀ-ÿ]+", nome) if len(p) >= 4 and _sem_acento(p) not in PALAVRAS_GENERICAS]
        termos.update(partes)  # "Ana Rocha" também bloqueia "Rocha"
    return sorted((t for t in termos if len(t) >= 4 and _sem_acento(t) not in PALAVRAS_GENERICAS),
                  key=len, reverse=True)


_COL_NOME = re.compile(r"nome|raz[aã]o|fantasia|profissional|colaborador|respons[aá]vel|contato", re.I)
_CAMPO_MD = re.compile(r"\*\*(?:Nome|Raz[aã]o social|Nome fantasia|Profissional|Colaborador|Respons[aá]vel|"
                       r"Contato|Dono|Implantador|Quem)[^*]*:\*\*\s*([^|\n<>`]{4,80})", re.I)


def _nomes_do_csv(arq: Path) -> set[str]:
    nomes: set[str] = set()
    try:
        texto = arq.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return nomes
    try:
        dialeto = csv.Sniffer().sniff(texto[:4096], delimiters=";,\t|")
    except csv.Error:
        dialeto = csv.excel
        dialeto.delimiter = ";" if texto.count(";") > texto.count(",") else ","
    try:
        for linha in csv.DictReader(texto.splitlines(), dialect=dialeto):
            for col, val in linha.items():
                if col and val and _COL_NOME.search(col) and len(val.strip()) >= 4:
                    nomes.add(val.strip())
    except csv.Error:
        pass
    return nomes


def _nomes_do_md(arq: Path) -> set[str]:
    try:
        texto = arq.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    nomes = {m.group(1).strip().rstrip(".,;") for m in _CAMPO_MD.finditer(texto)}
    # tabelas de pessoas (PAPEIS.md): células com 2+ palavras capitalizadas
    for cel in re.findall(r"\|\s*([A-ZÀ-Ý][a-zà-ÿ]+(?:\s+(?:d[aeo]s?\s+)?[A-ZÀ-Ý][a-zà-ÿ]+)+)\s*(?=\|)", texto):
        nomes.add(cel.strip())
    return {n for n in nomes if n and "<" not in n}


def filtrar_texto(texto: str, termos: list[str] = ()) -> list[str]:
    """Devolve a lista de problemas (vazia = limpo). Nunca devolve o valor inteiro."""
    problemas: list[str] = []
    termos_norm = [(t, _sem_acento(t)) for t in termos]
    for n, linha in enumerate(texto.splitlines(), 1):
        sem = _sem_acento(linha)
        for nome, rx in PADROES:
            for m in rx.finditer(linha):
                problemas.append(f"linha {n}: {nome} ({mascarar(m.group(0))})")
        for m in VALOR.finditer(linha):
            if not MARCA_EXEMPLO.search(linha[m.end():m.end() + 25]):
                problemas.append(f"linha {n}: valor/percentual ({mascarar(m.group(0))}) sem '(exemplo)' logo depois "
                                 "— use valor genérico e escreva '(exemplo)' colado ao número")
        sem_urls = URL.sub(" ", linha)
        for m in DOMINIO.finditer(sem_urls):
            d = m.group(0).lower().lstrip("w.") if m.group(0).lower().startswith("www.") else m.group(0).lower()
            if not any(d == h or d.endswith("." + h) for h in DOMINIOS_OK):
                problemas.append(f"linha {n}: endereço/site ({mascarar(m.group(0))}); só sites públicos do Rabi/gov")
        for m in URL.finditer(linha):
            u = m.group(0).rstrip(".,;")
            host = (urlparse(u).hostname or "").lower()
            if not any(host == h or host.endswith("." + h) for h in HOSTS_OK):
                problemas.append(f"linha {n}: link externo ({host or mascarar(u)}); só links públicos do Rabi/ANS/gov")
            elif host.endswith("github.com") and not any(g in u.lower() for g in GITHUB_OK):
                problemas.append(f"linha {n}: link de outro repositório do GitHub (pode ser o da clínica)")
            elif host == "app.rabisistemas.com.br" and re.search(r"/\d{2,}", u):
                problemas.append(f"linha {n}: link de tela do Rabi com ID")
        for original, norm in termos_norm:
            if norm and re.search(r"(?<![a-z0-9])" + re.escape(norm) + r"(?![a-z0-9])", sem):
                problemas.append(f"linha {n}: nome/identificador da clínica ou de pessoa ({mascarar(original)})")
    return problemas


# ---------------------------------------------------------------------------
# Arquivo de aprendizado
# ---------------------------------------------------------------------------
def ler_aprendizado(caminho: Path) -> dict[str, str]:
    texto = caminho.read_text(encoding="utf-8")
    dados: dict[str, str] = {"titulo": "", "status": ""}
    m = re.search(r"^# (.+)$", texto, re.M)
    if m:
        dados["titulo"] = m.group(1).strip()
    for rotulo, chave in CAMPOS_CABECALHO + [("Status", "status"), ("Issue", "issue")]:
        m = re.search(rf"^- \*\*{re.escape(rotulo)}:\*\*\s*(.*)$", texto, re.M)
        dados[chave] = m.group(1).strip() if m else ""
    partes = re.split(r"^## ", texto, flags=re.M)
    for parte in partes[1:]:
        cab, _, corpo = parte.partition("\n")
        for rotulo, chave in SECOES:
            if cab.strip().lower() == rotulo.lower():
                dados[chave] = re.sub(r"<!--.*?-->", "", corpo, flags=re.S).strip()
    return dados


def texto_enviavel(d: dict[str, str]) -> str:
    """Só o que vai para a issue (o filtro roda sobre isto)."""
    linhas = [d.get("titulo", "")]
    for _, chave in CAMPOS_CABECALHO:
        linhas.append(d.get(chave, ""))
    for _, chave in SECOES:
        linhas.append(d.get(chave, ""))
    return "\n".join(linhas)


def faltando(d: dict[str, str]) -> list[str]:
    obrig = [("titulo", "título")] + [(c, r) for r, c in SECOES[:4]] + [("tipo", "Tipo")]
    return [r for c, r in obrig if not d.get(c, "").strip()]


def link_issue(d: dict[str, str]) -> str:
    params = {"template": FORMULARIO, "title": f"[aprendizado] {d['titulo']}"}
    for _, chave in CAMPOS_CABECALHO + SECOES:
        if d.get(chave):
            params[chave] = d[chave]
    qs = "&".join(f"{k}={quote(v, safe='')}" for k, v in params.items())
    return f"https://github.com/{REPO_KIT}/issues/new?{qs}"


def trocar_campo(caminho: Path, rotulo: str, valor: str) -> None:
    texto = caminho.read_text(encoding="utf-8")
    rx = re.compile(rf"^(- \*\*{re.escape(rotulo)}:\*\*).*$", re.M)
    if rx.search(texto):
        texto = rx.sub(lambda m: f"{m.group(1)} {valor}", texto, count=1)
    else:
        texto = re.sub(r"^(# .+\n)", rf"\1- **{rotulo}:** {valor}\n", texto, count=1, flags=re.M)
    caminho.write_text(texto, encoding="utf-8")


# ---------------------------------------------------------------------------
# Índice da fila
# ---------------------------------------------------------------------------
CAB_INDICE = """# Aprendizados para o kit — fila desta clínica

> Gerado por `.kit/ferramentas/kit/filtrar_aprendizado.py indice`. Não edite à mão.
> O que é e como enviar: `.kit/prompts/08-contribuir-com-o-kit.md`.
> **Nada aqui leva dado da clínica**: só o método (cálculo, regra, API, processo).

| Arquivo | Título | Tipo | Status |
|---|---|---|---|
"""


def refazer_indice(repo: Path) -> Path:
    pasta = repo / PASTA
    pasta.mkdir(exist_ok=True)
    linhas = []
    for arq in sorted(pasta.glob(PADRAO_ARQ)):
        d = ler_aprendizado(arq)
        titulo = d["titulo"].replace("|", "/")
        linhas.append(f"| [{arq.name}]({arq.name}) | {titulo} | {d.get('tipo', '')} | {d.get('status', '')} |")
    indice = pasta / "00-INDICE.md"
    indice.write_text(CAB_INDICE + ("\n".join(linhas) + "\n" if linhas else "| — | (fila vazia) | — | — |\n"),
                      encoding="utf-8")
    return indice


def pendentes(repo: Path) -> int:
    pasta = repo / PASTA
    if not pasta.is_dir():
        return 0
    return sum(1 for a in pasta.glob(PADRAO_ARQ)
               if ler_aprendizado(a).get("status", "").split(" ")[0] in STATUS_ABERTOS)


MODELO_ARQ = """# {titulo}
- **Tipo:** {tipo}
- **Arquivo do kit afetado:** {arquivo}
- **Versão do kit:** {versao}
- **Status:** rascunho
- **Criado em:** {data}

<!-- REGRA: nada da clínica. Sem nome, CNPJ, CPF, pessoa, ID do Rabi, valor
contratado, link do repo. Use valores genéricos marcados como "exemplo". -->

## O que o kit diz

## O que acontece de verdade

## Regra proposta

## Como detectar

## Evidência (só o tipo, nunca o conteúdo)
"""


def raiz_kit_de(repo: Path) -> Path:
    kit = repo / ".kit"
    return kit if (kit / "VERSION").is_file() else RAIZ_KIT


def cmd_novo(args) -> int:
    repo = Path(args.repo).resolve()
    if args.tipo not in TIPOS:
        print(f"ERRO: --tipo deve ser um de: {', '.join(TIPOS)}", file=sys.stderr)
        return 2
    pasta = repo / PASTA
    pasta.mkdir(exist_ok=True)
    data = hoje()
    n = 1 + sum(1 for _ in pasta.glob(f"{data}-*.md"))
    arq = pasta / f"{data}-{n:02d}-{slugificar(args.titulo)[:50]}.md"
    arq.write_text(MODELO_ARQ.format(titulo=args.titulo.strip(), tipo=TIPOS[args.tipo],
                                     arquivo=args.arquivo or "(qual arquivo do kit?)",
                                     versao=ler_versao(raiz_kit_de(repo)), data=data), encoding="utf-8")
    refazer_indice(repo)
    print(f"Rascunho criado: {arq.relative_to(repo)} (preencha as seções e rode `filtrar`).")
    return 0


def cmd_filtrar(args) -> int:
    repo = Path(args.repo).resolve()
    arq = Path(args.arquivo)
    arq = arq if arq.is_absolute() else (repo / arq)
    if not arq.is_file():
        print(f"ERRO: não achei {arq}", file=sys.stderr)
        return 2
    d = ler_aprendizado(arq)
    falta = faltando(d)
    if falta:
        print("INCOMPLETO: preencha antes de enviar: " + ", ".join(falta))
        return 1
    problemas = filtrar_texto(texto_enviavel(d), termos_da_clinica(repo))
    if problemas:
        print(f"BLOQUEADO: {len(problemas)} problema(s) de privacidade. Generalize e rode de novo:")
        for p in problemas:
            print("  -", p)
        return 1
    link = link_issue(d)
    trocar_campo(arq, "Status", f"filtrado ({hoje()})")
    refazer_indice(repo)
    print("LIMPO: nenhum dado da clínica encontrado.")
    print("=== TEXTO QUE VAI SAIR (mostre ao usuário antes) ===")
    print(f"Título: [aprendizado] {d['titulo']}")
    for rotulo, chave in CAMPOS_CABECALHO + SECOES:
        print(f"-- {rotulo}:\n{d.get(chave, '')}")
    print("=== LINK (o usuário abre, confere e clica em 'Submit new issue') ===")
    if len(link) > LIMITE_URL:
        print(f"https://github.com/{REPO_KIT}/issues/new?template={FORMULARIO}")
        print("AVISO: texto longo demais para o link; abra o formulário acima e cole cada campo do texto.")
    else:
        print(link)
    return 0


def cmd_enviado(args) -> int:
    repo = Path(args.repo).resolve()
    arq = Path(args.arquivo)
    arq = arq if arq.is_absolute() else (repo / arq)
    if not arq.is_file():
        print(f"ERRO: não achei {arq}", file=sys.stderr)
        return 2
    trocar_campo(arq, "Status", f"enviado #{args.issue} ({hoje()})")
    trocar_campo(arq, "Issue", f"https://github.com/{REPO_KIT}/issues/{args.issue}")
    refazer_indice(repo)
    print(f"Registrado: {arq.name} → issue #{args.issue}")
    return 0


def cmd_indice(args) -> int:
    indice = refazer_indice(Path(args.repo).resolve())
    print(f"Índice refeito: {indice}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Aprendizados da clínica para o kit (com filtro de privacidade).")
    ap.add_argument("--repo", default=".", help="raiz do repo da clínica (padrão: pasta atual)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("novo", help="cria um rascunho")
    p.add_argument("--titulo", required=True)
    p.add_argument("--tipo", required=True, help=" · ".join(TIPOS))
    p.add_argument("--arquivo", help="arquivo do kit afetado")
    p = sub.add_parser("filtrar", help="filtra e gera o link de envio")
    p.add_argument("arquivo")
    p = sub.add_parser("enviado", help="registra a issue aberta")
    p.add_argument("arquivo")
    p.add_argument("--issue", required=True, type=int)
    sub.add_parser("indice", help="refaz o índice da fila")
    args = ap.parse_args(argv)
    return {"novo": cmd_novo, "filtrar": cmd_filtrar, "enviado": cmd_enviado, "indice": cmd_indice}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
