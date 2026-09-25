"""Importa planilha/CSV de sistema anterior ou do cliente para o formato do kit.

Fluxo (nada é gravado no Rabi aqui — só prepara dados com ORIGEM):
 1) sugerir:  python3 importar_planilha.py sugerir --entrada lista.csv --alvo colaboradores
        → imprime/grava um mapa JSON coluna_origem → campo_kit (por semelhança de nome)
 2) a IA revisa o mapa com o usuário (confirma coluna a coluna quando houver dúvida)
 3) aplicar:  python3 importar_planilha.py aplicar --entrada lista.csv --mapa mapa.json --saida dados/colaboradores/colaboradores.csv
        → CSV normalizado (UTF-8, ';') com colunas do alvo + 'origem' (arquivo:linha),
          CPF/CNPJ/CEP/telefone limpos e validados, duplicados sinalizados.
Aceita CSV (',' ';' tab ou '|', detecção automática, UTF-8 ou latin-1) e XLSX (se openpyxl instalado).
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

# Campos do kit por alvo (nomes próximos dos campos da API externa).
ALVOS: dict[str, list[str]] = {
    "empresas": ["razaoSocial", "nomeFantasia", "cnpj", "cnes", "cep", "endereco", "numero", "complemento", "bairro", "cidade", "uf", "telefone", "email"],
    "locais": ["nome", "empresa", "tipoLocal", "observacao"],
    "operadoras": ["nomeFantasia", "razaoSocial", "cnpj", "registroANS", "telefone", "email", "plano"],
    "fornecedores": ["nome", "razaoSocial", "cnpj", "telefone", "email"],
    "fabricantes": ["nome"],
    "taxas": ["taxas", "codigoTaxa", "tipoTaxa", "valor"],
    "produtos": ["nome", "codigoProduto", "apresentacao", "contendo", "unidadeDeMedida", "tipoProduto", "fabricante", "principioAtivo", "ean", "registroAnvisa", "custo"],
    "equipamentos": ["nome", "descricao", "local"],
    "servicos": ["nome", "codigo", "tipoCodigo", "tipoServico", "duracaoMinutos", "valor", "especialidade"],
    "colaboradores": ["nome", "cpf", "dataDeNascimento", "sexo", "email", "telefone", "celular", "cep", "endereco", "numero", "bairro", "cidade", "uf", "conselho", "numeroConselho", "ufConselho", "cbo", "especialidade", "rqe"],
    "pacientes": ["nome", "cpf", "dataDeNascimento", "sexo", "email", "telefone", "celular", "cep", "endereco", "numero", "bairro", "cidade", "uf", "convenio", "plano", "carteirinha", "validadeCarteirinha"],
    "precos-convenio": ["tipo", "nome_convenio", "codigo", "valor_combinado", "observacao"],
}
SINONIMOS = {
    "cpf": ["cpf", "documento", "doc"], "cnpj": ["cnpj"], "cep": ["cep"], "uf": ["uf", "estado"],
    "dataDeNascimento": ["nascimento", "data nasc", "dt nasc", "datanascimento"],
    "celular": ["celular", "whatsapp", "cel"], "telefone": ["telefone", "fone", "tel"],
    "email": ["email", "e-mail"], "carteirinha": ["carteirinha", "carteira", "matricula", "numero carteira"],
    "numeroConselho": ["crm", "numero conselho", "registro"], "conselho": ["conselho"],
    "razaoSocial": ["razao social", "razao"], "nomeFantasia": ["fantasia", "nome fantasia"],
    "valor": ["valor", "preco", "preço"], "valor_combinado": ["valor", "preco", "preço"],
    "codigo": ["codigo", "cod", "tuss"], "registroANS": ["ans", "registro ans"],
}
PII = {"pacientes"}


def sem_acento(t: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", str(t)) if unicodedata.category(c) != "Mn").lower().strip()


def so_digitos(t) -> str:
    return re.sub(r"\D", "", str(t or ""))


def cpf_valido(c: str) -> bool:
    c = so_digitos(c)
    if len(c) != 11 or c == c[0] * 11:
        return False
    for n in (9, 10):
        s = sum(int(c[i]) * (n + 1 - i) for i in range(n))
        if int(c[n]) != (s * 10 % 11) % 10:
            return False
    return True


def cnpj_valido(c: str) -> bool:
    c = so_digitos(c)
    if len(c) != 14 or c == c[0] * 14:
        return False
    def dv(base, pesos):
        s = sum(int(a) * b for a, b in zip(base, pesos)); r = s % 11
        return "0" if r < 2 else str(11 - r)
    p1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    d1 = dv(c[:12], p1); d2 = dv(c[:12] + d1, [6] + p1)
    return c[12:] == d1 + d2


def ler_tabela(caminho: Path) -> tuple[list[str], list[list[str]]]:
    if caminho.suffix.lower() in (".xlsx", ".xlsm"):
        try:
            import openpyxl  # type: ignore
        except ImportError:
            raise SystemExit("Para XLSX instale openpyxl (pip install openpyxl) ou exporte a planilha como CSV.")
        wb = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
        ws = wb.worksheets[0]
        linhas = [["" if v is None else str(v) for v in r] for r in ws.iter_rows(values_only=True)]
    else:
        bruto = caminho.read_bytes()
        try:
            texto = bruto.decode("utf-8-sig")
        except UnicodeDecodeError:
            texto = bruto.decode("latin-1")
        amostra = texto[:5000]
        try:
            dialeto = csv.Sniffer().sniff(amostra, delimiters=",;\t|")
        except csv.Error:
            dialeto = csv.excel
            dialeto.delimiter = ";" if amostra.count(";") > amostra.count(",") else ","
        linhas = list(csv.reader(io.StringIO(texto), dialeto))
    linhas = [l for l in linhas if any(str(c).strip() for c in l)]
    if not linhas:
        raise SystemExit(f"{caminho}: sem linhas")
    return [str(c).strip() for c in linhas[0]], linhas[1:]


def sugerir_mapa(cabecalho: list[str], alvo: str) -> dict[str, str | None]:
    campos = ALVOS[alvo]
    mapa: dict[str, str | None] = {}
    usados = set()
    for col in cabecalho:
        nc = sem_acento(col)
        melhor, nota = None, 0.0
        for campo in campos:
            candidatos = [campo] + SINONIMOS.get(campo, [])
            for cand in candidatos:
                r = SequenceMatcher(None, nc, sem_acento(cand)).ratio()
                if sem_acento(cand) in nc:
                    r = max(r, 0.9)
                if r > nota:
                    melhor, nota = campo, r
        mapa[col] = melhor if nota >= 0.6 and melhor not in usados else None
        if mapa[col]:
            usados.add(mapa[col])
    return mapa


def normalizar_valor(campo: str, v: str) -> tuple[str, str]:
    """Devolve (valor_normalizado, aviso)."""
    v = str(v or "").strip()
    if not v:
        return "", ""
    if campo == "cpf":
        d = so_digitos(v).zfill(11)
        return d, "" if cpf_valido(d) else "CPF inválido"
    if campo == "cnpj":
        d = so_digitos(v).zfill(14)
        return d, "" if cnpj_valido(d) else "CNPJ inválido"
    if campo == "cep":
        d = so_digitos(v)
        return d, "" if len(d) == 8 else "CEP com tamanho errado"
    if campo in ("telefone", "celular"):
        d = so_digitos(v)
        return d, "" if len(d) in (10, 11) else "telefone sem DDD ou incompleto"
    if campo in ("valor", "valor_combinado", "custo"):
        t = v.replace("R$", "").strip()
        if "," in t:
            t = t.replace(".", "").replace(",", ".")
        try:
            return f"{float(t):.2f}", ""
        except ValueError:
            return v, "valor não numérico"
    if campo in ("dataDeNascimento", "validadeCarteirinha"):
        m = re.match(r"(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})$", v)
        if m:
            d, mth, y = m.groups(); y = ("19" + y if int(y) > 30 else "20" + y) if len(y) == 2 else y
            return f"{y}-{int(mth):02d}-{int(d):02d}", ""
        if re.match(r"\d{4}-\d{2}-\d{2}", v):
            return v[:10], ""
        return v, "data em formato desconhecido"
    if campo == "uf":
        return v.upper()[:2] if len(v) <= 3 else v, ""
    return v, ""


CHAVE_DEDUP = {"cpf", "cnpj", "codigo", "codigoProduto", "ean"}


def aplicar(entrada: Path, mapa: dict, alvo: str, saida: Path) -> dict:
    cab, linhas = ler_tabela(entrada)
    campos = ALVOS[alvo]
    idx = {col: i for i, col in enumerate(cab)}
    vistos: dict[tuple, int] = {}
    saida.parent.mkdir(parents=True, exist_ok=True)
    resumo = {"linhas": 0, "avisos": 0, "duplicados": 0}
    with saida.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(campos + ["origem", "avisos"])
        for n, lin in enumerate(linhas, start=2):
            reg = {c: "" for c in campos}
            avisos = []
            for col, campo in mapa.items():
                if campo and col in idx and idx[col] < len(lin):
                    val, av = normalizar_valor(campo, lin[idx[col]])
                    reg[campo] = val
                    if av:
                        avisos.append(f"{campo}: {av}")
            chave = next(((c, reg[c]) for c in campos if c in CHAVE_DEDUP and reg.get(c)), None)
            if chave is None and reg.get(campos[0]):
                chave = (campos[0], sem_acento(reg[campos[0]]))
            if chave in vistos:
                avisos.append(f"duplicado da linha {vistos[chave]}")
                resumo["duplicados"] += 1
            elif chave:
                vistos[chave] = n
            resumo["linhas"] += 1
            resumo["avisos"] += bool(avisos)
            w.writerow([reg[c] for c in campos] + [f"{entrada.name}:linha {n}", " | ".join(avisos)])
    return resumo


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("sugerir"); s1.add_argument("--entrada", required=True); s1.add_argument("--alvo", required=True, choices=sorted(ALVOS)); s1.add_argument("--mapa")
    s2 = sub.add_parser("aplicar"); s2.add_argument("--entrada", required=True); s2.add_argument("--mapa", required=True); s2.add_argument("--saida", required=True); s2.add_argument("--alvo")
    a = ap.parse_args(argv)
    if a.cmd == "sugerir":
        cab, linhas = ler_tabela(Path(a.entrada))
        mapa = sugerir_mapa(cab, a.alvo)
        doc = {"alvo": a.alvo, "mapa": mapa}
        print(f"{len(linhas)} linhas; colunas → campos (None = ignorar ou perguntar ao usuário):")
        for k, v in mapa.items():
            print(f"  {k!r:35} → {v}")
        faltando = [c for c in ALVOS[a.alvo] if c not in mapa.values()]
        if faltando:
            print("Campos do alvo sem coluna correspondente:", ", ".join(faltando))
        if a.mapa:
            Path(a.mapa).write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
            print("Mapa gravado em", a.mapa)
        return 0
    doc = json.loads(Path(a.mapa).read_text(encoding="utf-8"))
    alvo = a.alvo or doc["alvo"]
    if alvo in PII:
        print("ATENÇÃO LGPD: saída contém dado pessoal — grave só em dados/pacientes/ (fora do git) e nunca em prova/relatório.", file=sys.stderr)
    r = aplicar(Path(a.entrada), doc["mapa"], alvo, Path(a.saida))
    print(f"{r['linhas']} linhas gravadas em {a.saida}; {r['avisos']} com aviso; {r['duplicados']} duplicadas.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
