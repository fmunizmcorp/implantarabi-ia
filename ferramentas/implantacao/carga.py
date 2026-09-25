"""Carga genérica de cadastros no Rabi seguindo o RITUAL DE 5 PASSOS.

  1) previa  — foto ANTES + casamento com o que já existe + prévia legível (nada é gravado)
  2) (humano aprova na conversa — a sessão registra a aprovação em historico/requisitos/raw/)
  3) gravar  — grava SÓ o plano aprovado (novos via /bulk em fatias; alterações via GET→merge→PUT
               com o objeto completo), guarda resposta crua, foto DEPOIS e diff.

Exemplos (a partir da raiz do repo da clínica):
  python3 .kit/ferramentas/implantacao/carga.py previa --recurso taxas --sprint S05 \
      --entrada dados/taxas/taxas.json --casar-por codigoTaxa
  python3 .kit/ferramentas/implantacao/carga.py gravar --plano provas/S05/taxas/<data>/plano.json \
      --aprovado-por "Implantador X na conversa de 25/09" [--apenas-primeiro] [--incluir-alteracoes]

Entrada: JSON (lista de objetos no formato do corpo da API) ou CSV ';' com cabeçalho = campos da API
(coluna 'origem' é obrigatória e NÃO é enviada à API). Regras: um lote por vez; primeiro item de um
bloco novo deve ser provado antes do restante (--apenas-primeiro); pacientes exigem --lgpd-ciente.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import sys
import unicodedata
from pathlib import Path

RAIZ_KIT = Path(__file__).resolve().parents[2]
if str(RAIZ_KIT) not in sys.path:
    sys.path.insert(0, str(RAIZ_KIT))

from ferramentas.rabi_api.cliente import ClienteRabi, ErroRabi, resumo_lote  # noqa: E402
from ferramentas.rabi_api import foto as _foto  # noqa: E402

# recurso → (listagem, bulk, chave do corpo, limite, campo id)
RECURSOS = {
    "empresas": ("/empresas", None, None, 1, "id"),
    "depositos": ("/depositos", "/depositos/bulk", "depositos", 50, "id"),
    "locais": ("/locais", None, None, 1, "id"),
    "operadoras": ("/operadoras", "/operadoras/bulk", "operadoras", 50, "id"),
    "fornecedores": ("/fornecedores", "/fornecedores/bulk", "fornecedores", 50, "id"),
    "fabricantes": ("/fabricantes", "/fabricantes/bulk", "fabricantes", 50, "id"),
    "taxas": ("/taxas", "/taxas/bulk", "taxas", 50, "id"),
    "produtos": ("/produtos", "/produtos/bulk", "produtos", 50, "id"),
    "equipamentos": ("/equipamentos", "/equipamentos/bulk", "equipamentos", 50, "id"),
    "servicos": ("/servicos", "/servicos/bulk", "servicos", 50, "id"),
    "colaboradores": ("/colaboradores", "/colaboradores/bulk", "colaboradores", 50, "id"),
    "convenios": ("/convenios", "/convenios/bulk", "convenios", 50, "id"),
    "pacientes": ("/pacientes", "/pacientes/bulk", "pacientes", 50, "id"),
}
PROIBIDOS = {"financeiro", "estoque", "nfse"}  # nunca por esta ferramenta (exigem ordem escrita e rotas próprias)


def _norm(v) -> str:
    t = unicodedata.normalize("NFD", str(v if v is not None else ""))
    return "".join(c for c in t if unicodedata.category(c) != "Mn").strip().lower()


def _ler_entrada(caminho: Path) -> list[dict]:
    if caminho.suffix.lower() == ".json":
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        return dados if isinstance(dados, list) else dados.get("itens", [])
    with caminho.open(encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f, delimiter=";"))
    itens = []
    for l in linhas:
        item = {}
        for k, v in l.items():
            if k is None or v is None or v == "":
                continue
            v = v.strip()
            if v.lower() in ("true", "sim", "s"):
                v = True
            elif v.lower() in ("false", "nao", "não", "n"):
                v = False
            else:
                try:
                    v = int(v) if v.isdigit() else float(v.replace(",", ".")) if v.replace(",", "", 1).replace(".", "", 1).isdigit() else v
                except ValueError:
                    pass
            if "." in k:  # campo aninhado ex.: endereco.cep
                a, b = k.split(".", 1)
                item.setdefault(a, {})[b] = v
            else:
                item[k] = v
        itens.append(item)
    return itens


def _comparar(novo: dict, atual: dict) -> list[tuple[str, object, object]]:
    difs = []
    for k, v in novo.items():
        if k == "origem":
            continue
        if isinstance(v, dict) and isinstance(atual.get(k), dict):
            difs += [(f"{k}.{a}", b, c) for a, b, c in _comparar(v, atual[k])]
        elif _norm(atual.get(k)) != _norm(v):
            difs.append((k, atual.get(k), v))
    return difs


def previa(cli: ClienteRabi, recurso: str, entrada: Path, casar_por: str, sprint: str, repo: Path) -> Path:
    listar, *_ = RECURSOS[recurso]
    pasta = repo / "provas" / sprint / recurso / _dt.datetime.now().strftime("%Y%m%d-%H%M")
    arq_antes = _foto.foto(cli, listar, str(pasta), "antes")
    existentes = json.loads(Path(arq_antes).read_text(encoding="utf-8"))["dados"]
    indice = {}
    for e in existentes:
        indice.setdefault(_norm(e.get(casar_por)), []).append(e)
    itens = _ler_entrada(entrada)
    plano = {"recurso": recurso, "sprint": sprint, "casar_por": casar_por, "entrada": str(entrada),
             "criar": [], "alterar": [], "iguais": [], "ambiguos": [], "sem_origem": [], "pasta": str(pasta)}
    linhas_md = [f"# Prévia — {recurso} ({sprint})", "",
                 f"Fonte: `{entrada}` · já existentes no Rabi: **{len(existentes)}** · itens na entrada: **{len(itens)}**", "",
                 "| # | item | situação | o que muda (de → para) | origem |", "|---|---|---|---|---|"]
    for n, item in enumerate(itens, 1):
        chave = _norm(item.get(casar_por))
        nome = item.get("nome") or item.get("razaoSocial") or item.get("taxas") or item.get(casar_por)
        origem = item.get("origem", "")
        if not origem:
            plano["sem_origem"].append(item)
            linhas_md.append(f"| {n} | {nome} | ❌ SEM ORIGEM — não entra | — | — |")
            continue
        achados = indice.get(chave, []) if chave else []
        if len(achados) > 1:
            plano["ambiguos"].append({"item": item, "candidatos": [a.get("id") for a in achados]})
            linhas_md.append(f"| {n} | {nome} | ⚠️ {len(achados)} registros iguais no Rabi — decidir | — | {origem} |")
        elif achados:
            atual = achados[0]
            difs = _comparar(item, atual)
            ativo = "" if atual.get("ativo", True) else " (INATIVO no Rabi)"
            if difs:
                plano["alterar"].append({"id": atual.get("id"), "item": item, "difs": difs})
                muda = "; ".join(f"{k}: {a!s} → {b!s}" for k, a, b in difs[:6]) + (" …" if len(difs) > 6 else "")
                linhas_md.append(f"| {n} | {nome} | ✏️ existe{ativo}, muda | {muda} | {origem} |")
            else:
                plano["iguais"].append(atual.get("id"))
                linhas_md.append(f"| {n} | {nome} | ✅ já existe igual{ativo} — nada a fazer | — | {origem} |")
        else:
            plano["criar"].append(item)
            linhas_md.append(f"| {n} | {nome} | ➕ novo | — | {origem} |")
    linhas_md += ["", f"**Resumo:** criar {len(plano['criar'])} · alterar {len(plano['alterar'])} · "
                  f"iguais {len(plano['iguais'])} · ambíguos {len(plano['ambiguos'])} · sem origem {len(plano['sem_origem'])}",
                  "", "Nada foi gravado. Para gravar, a sessão precisa da aprovação do usuário."]
    (pasta / "previa.md").write_text("\n".join(linhas_md) + "\n", encoding="utf-8")
    (pasta / "plano.json").write_text(json.dumps(plano, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n".join(linhas_md))
    print(f"\nPlano: {pasta / 'plano.json'}")
    return pasta / "plano.json"


def gravar(cli: ClienteRabi, plano_arq: Path, aprovado_por: str, apenas_primeiro: bool,
           incluir_alteracoes: bool, lgpd_ciente: bool) -> int:
    plano = json.loads(plano_arq.read_text(encoding="utf-8"))
    recurso = plano["recurso"]
    listar, bulk, chave, limite, campo_id = RECURSOS[recurso]
    if recurso == "pacientes" and not lgpd_ciente:
        print("Pacientes: rode com --lgpd-ciente (lote pequeno, conferência por amostra, sem extrato no repo).")
        return 2
    pasta = Path(plano["pasta"])
    criar = [{k: v for k, v in i.items() if k != "origem"} for i in plano["criar"]]
    alterar = plano["alterar"] if incluir_alteracoes else []
    if apenas_primeiro:
        criar, alterar = criar[:1], (alterar[:1] if not criar else [])
    respostas: dict = {"aprovado_por": aprovado_por, "em": _dt.datetime.now().isoformat(timespec="seconds"),
                       "criacao": None, "alteracoes": []}
    codigo = 0
    try:
        if criar:
            if bulk:
                rel = cli.enviar_lote(bulk, chave, criar, limite)
                respostas["criacao"] = rel
                print(resumo_lote(rel))
                codigo = 1 if rel["reenviar"] else 0
            else:
                respostas["criacao"] = [cli.post(listar, i) for i in criar]
        for alt in alterar:  # PUT = sobrescrita: GET → merge → PUT objeto completo
            atual = cli.get(f"{listar}/{alt['id']}")
            atual = atual.get("dados", atual) if isinstance(atual, dict) else atual
            novo = {**atual, **{k: v for k, v in alt["item"].items() if k != "origem"}}
            respostas["alteracoes"].append({"id": alt["id"], "resposta": cli.put(f"{listar}/{alt['id']}", novo)})
    except ErroRabi as e:
        respostas["erro"] = str(e)
        codigo = 2
        print(f"ERRO: {e}")
    finally:
        (pasta / "resposta.json").write_text(json.dumps(respostas, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        arq_depois = _foto.foto(cli, listar, str(pasta), "depois")
        antes = json.loads((pasta / "antes.json").read_text(encoding="utf-8"))
        depois = json.loads(Path(arq_depois).read_text(encoding="utf-8"))
        texto = _foto.diff(antes, depois)
        (pasta / "diff.txt").write_text(texto + "\n", encoding="utf-8")
        print(texto)
        print(f"\nProvas em {pasta} (antes.json, resposta.json, depois.json, diff.txt). "
              "Atualize a sprint e o ESTADO.md, faça commit+push e mostre o diff ao usuário.")
    return codigo


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("previa")
    p.add_argument("--recurso", required=True, choices=sorted(RECURSOS))
    p.add_argument("--entrada", required=True)
    p.add_argument("--casar-por", default="nome")
    p.add_argument("--sprint", required=True)
    p.add_argument("--repo", default=".")
    g = sub.add_parser("gravar")
    g.add_argument("--plano", required=True)
    g.add_argument("--aprovado-por", required=True, help="quem aprovou e onde (fica na prova)")
    g.add_argument("--apenas-primeiro", action="store_true")
    g.add_argument("--incluir-alteracoes", action="store_true")
    g.add_argument("--lgpd-ciente", action="store_true")
    a = ap.parse_args(argv)
    cli = ClienteRabi()
    if a.cmd == "previa":
        previa(cli, a.recurso, Path(a.entrada), a.casar_por, a.sprint, Path(a.repo))
        return 0
    return gravar(cli, Path(a.plano), a.aprovado_por, a.apenas_primeiro, a.incluir_alteracoes, a.lgpd_ciente)


if __name__ == "__main__":
    raise SystemExit(main())
