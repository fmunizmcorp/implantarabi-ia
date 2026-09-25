"""Monta os corpos dos PUT das abas do convênio a partir de ``precos-<slug>.csv``.

Uso:
  python3 .kit/ferramentas/conversao/montar_convenio.py precos-convenio-a.csv \\
      --convenio-id 12 --saida saida/ [--catalogo cenario.json] [--atual atual.json] \\
      [--fontes fontes.json] [--unico]

Rotas (spec openapi-2026-09-25.json, todas upsert, até 200 itens por chamada):
  PUT /convenios/{id}/produtos  {"produtos": [ConvenioProdutoItem]}
  PUT /convenios/{id}/taxas     {"taxas":    [ConvenioTaxaItem]}
  PUT /convenios/{id}/servicos  {"servicos": [ConvenioServicoItem]}

Semântica das células do CSV (vazio ≠ zero):
  * ``valor_combinado`` e ``fator_k`` vazios = "sem regra" → enviados como
    ``null`` (a API LIMPA o campo). ``manter`` = não enviar (fica como está).
    ``0`` / ``0,00`` = zero de verdade. ``0,01`` = ERRO (marcador proibido).
  * caixas (utiliza, pacote, zerar, autorizacao_previa, retorno): vazio =
    não enviar (mantém). Aceita s/n, sim/não, true/false, 1/0, x.
  * textos e ids (nome_convenio, codigo, *_id, parcelas): vazio = não enviar.
    ``limpar`` em ``tipo_atendimento_id`` envia ``null``.
  * ``origem`` é OBRIGATÓRIA (de onde veio o dado: contrato, tabela, e-mail…).

Ordem de gravação (manual, arvore-de-decisao.html#checklist): Utiliza →
valores → textos/códigos → tipo de atendimento → Pacote e Zerar. Por padrão
gera uma fase por etapa; ``--unico`` gera tudo numa fase só.
Saída: ``manifesto.json`` (sequência das chamadas), os lotes ``*.json`` e
``previa.md`` (tabela item · campo · de → para · porquê) para o humano aprovar.
Quem grava é o cliente ``ferramentas/rabi_api`` (ClienteRabi.put/enviar_lote).
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

if __package__ in (None, ""):
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
    __package__ = "ferramentas.conversao"

from .modelo import ConfigItem, Convenio, cenario_from_dict, TIPOS_PRECIFICACAO  # noqa: E402
from . import motor  # noqa: E402

COLUNAS = ["tipo", "id_rabi", "nome_rabi", "nome_convenio", "descricao_convenio", "codigo", "tipo_codigo_id", "tabela87_id",
           "tipo_atendimento_id", "utiliza", "valor_combinado", "pacote", "zerar", "autorizacao_previa",
           "retorno", "fator_k", "fonte_preco", "tipo_precificacao", "parcelas", "origem", "observacao"]
OBRIGATORIAS = ["tipo", "id_rabi", "origem"]
LOTE_MAX = 200
MANTER, LIMPAR = "manter", "limpar"
MANTER_SINAIS = {"manter", "="}  # "=" (convenção do documento 10) e "manter" são equivalentes

ABA = {"servico": "servicos", "produto": "produtos", "taxa": "taxas"}
CHAVE_ID = {"servico": "servicoId", "produto": "produtoId", "taxa": "taxaId"}
# coluna do CSV -> campo da API, por tipo (conferido no spec 2026-09-25)
MAPA = {
    "servico": {"utiliza": "utiliza", "valor_combinado": "valorInternoConvenio", "parcelas": "parcelasMaximas",
                "nome_convenio": "nomeConversao", "descricao_convenio": "descricaoConvenio",
                "codigo": "codigo", "tipo_codigo_id": "tipoCodigoId",
                "tabela87_id": "tabela87ANSId", "autorizacao_previa": "autorizacaoPrevia",
                "retorno": "retornoServico", "tipo_atendimento_id": "tipoAtendimentoId",
                "pacote": "pacote", "zerar": "zerarValor"},
    "produto": {"utiliza": "utiliza", "valor_combinado": "valorUnitarioConversao", "fator_k": "fatorK",
                "fonte_preco": "fontePrecoCompraOptionsId", "tipo_precificacao": "tipoPrecificacao",
                "parcelas": "parcelasMaximas", "nome_convenio": "nomeConversao",
                "descricao_convenio": "descricaoConversao", "codigo": "codigoConversao",
                "tipo_codigo_id": "tipoCodigoId", "tabela87_id": "tabela87ANSId", "zerar": "zerarValor"},
    "taxa": {"utiliza": "utiliza", "valor_combinado": "valorConvertido", "nome_convenio": "nomeConvertido",
             "descricao_convenio": "descricaoConvertida",
             "codigo": "codigo", "tipo_codigo_id": "tipoCodigoId", "tabela87_id": "tabela87ANSId",
             "zerar": "zerarValor"},
}
FASES = [
    ("1-utiliza", {"utiliza"}),
    ("2-valores", {"valorInternoConvenio", "valorUnitarioConversao", "valorConvertido", "fatorK",
                   "fontePrecoCompraOptionsId", "tipoPrecificacao", "parcelasMaximas"}),
    ("3-textos", {"nomeConversao", "nomeConvertido", "codigo", "codigoConversao", "tipoCodigoId",
                  "tabela87ANSId", "autorizacaoPrevia", "retornoServico"}),
    ("4-tipo-atendimento", {"tipoAtendimentoId"}),
    ("5-pacote-zerar", {"pacote", "zerarValor"}),
]
ORDEM_ABAS = ["produto", "taxa", "servico"]


@dataclass
class Achado:
    nivel: str  # ERRO | AVISO
    linha: int
    item: str
    mensagem: str


@dataclass
class LinhaPreco:
    num: int
    tipo: str
    id: int
    nome_rabi: str
    origem: str
    observacao: str
    campos: Dict[str, object] = field(default_factory=dict)  # campo da API -> valor (None = null)
    cfg: Dict[str, object] = field(default_factory=dict)  # para o motor


# --------------------------------------------------------------------------- parsing

def parse_decimal_br(txt: str) -> float:
    """'1.234,56' -> 1234.56 · '266,16' -> 266.16 · '3506.53' -> 3506.53."""
    s = txt.strip().replace("R$", "").replace(" ", "")
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    return float(s)


def parse_bool(txt: str) -> Optional[bool]:
    s = txt.strip().lower()
    if s == "" or s == MANTER:
        return None
    if s in ("s", "sim", "true", "1", "x", "v", "✔", "✓", "yes", "y"):
        return True
    if s in ("n", "nao", "não", "false", "0", "✘", "no", "-"):
        return False
    raise ValueError(f"caixa inválida: {txt!r} (use sim/não)")


def parse_tipo_prec(txt: str) -> str:
    s = txt.strip().upper().replace("PREÇO", "PRECO").replace(" ", "_")
    if s in ("1", "2", "3"):
        s = f"PRECO_{s}"
    if s not in TIPOS_PRECIFICACAO:
        raise ValueError(f"tipo_precificacao inválido: {txt!r} (PRECO_1, PRECO_2 ou PRECO_3)")
    return s


def _fmt_fk(v: float) -> str:
    """fatorK vai como texto no spec ("10,5")."""
    t = f"{v:.4f}".rstrip("0").rstrip(".")
    return t.replace(".", ",")


def ler_csv(caminho: str, fontes: Optional[Dict[str, int]] = None) -> Tuple[List[LinhaPreco], List[Achado]]:
    fontes = fontes or {}
    fontes_rev = {v: k for k, v in fontes.items()}
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        texto = f.read()
    primeira = texto.splitlines()[0] if texto else ""
    delim = ";" if primeira.count(";") > primeira.count(",") else ","
    leitor = csv.DictReader(io.StringIO(texto), delimiter=delim)
    faltando = [c for c in OBRIGATORIAS if c not in (leitor.fieldnames or [])]
    achados: List[Achado] = []
    if faltando:
        return [], [Achado("ERRO", 1, "cabeçalho", f"colunas obrigatórias ausentes: {faltando}")]
    desconhecidas = [c for c in leitor.fieldnames if c not in COLUNAS]
    if desconhecidas:
        achados.append(Achado("AVISO", 1, "cabeçalho", f"colunas ignoradas: {desconhecidas}"))
    linhas: List[LinhaPreco] = []
    vistos = set()
    for n, row in enumerate(leitor, start=2):
        row = {k: (v or "").strip() for k, v in row.items() if k}
        if not any(row.values()):
            continue
        tipo = row.get("tipo", "").lower().replace("ç", "c")
        item = f"{tipo} {row.get('id_rabi', '?')} {row.get('nome_rabi', '')}".strip()

        def erro(msg):
            achados.append(Achado("ERRO", n, item, msg))

        def aviso(msg):
            achados.append(Achado("AVISO", n, item, msg))

        if tipo not in ABA:
            erro(f"tipo inválido {row.get('tipo')!r} (servico|produto|taxa)")
            continue
        try:
            id_ = int(row.get("id_rabi", ""))
        except ValueError:
            erro("id_rabi precisa ser o número do item no Rabi")
            continue
        if not row.get("origem"):
            erro("linha sem origem: diga de onde veio o dado (contrato, tabela, e-mail…) — linha rejeitada")
            continue
        if (tipo, id_) in vistos:
            erro("item repetido no CSV")
            continue
        vistos.add((tipo, id_))
        lp = LinhaPreco(n, tipo, id_, row.get("nome_rabi", ""), row["origem"], row.get("observacao", ""))
        mapa = MAPA[tipo]
        ok = True
        for col in COLUNAS:
            txt = row.get(col, "")
            if col in ("tipo", "id_rabi", "nome_rabi", "origem", "observacao"):
                continue
            if txt == "" and col not in ("valor_combinado", "fator_k"):
                continue
            if col not in mapa:
                if txt != "":
                    erro(f"coluna {col} não existe na aba {ABA[tipo]} do convênio")
                    ok = False
                continue
            campo = mapa[col]
            try:
                if col in ("utiliza", "pacote", "zerar", "autorizacao_previa", "retorno"):
                    b = parse_bool(txt)
                    if b is None:
                        continue
                    lp.campos[campo] = b
                    lp.cfg[{"autorizacao_previa": "autorizacao_previa", "retorno": "retorno"}.get(col, col)] = b
                elif col in ("valor_combinado", "fator_k"):
                    if txt.lower() in MANTER_SINAIS:
                        continue
                    if txt == "":
                        lp.campos[campo] = None  # vazio: limpa (sem regra, desce de nível)
                        lp.cfg["valor_convertido" if col == "valor_combinado" else col] = None
                        continue
                    v = parse_decimal_br(txt)
                    if col == "valor_combinado":
                        if abs(v - 0.01) < 1e-9:
                            erro("0,01 não pode ser usado (marcador antigo de 'sem valor'): deixe vazio, "
                                 "ou 0 se for gratuito")
                            ok = False
                        if v < 0:
                            erro("valor negativo")
                            ok = False
                        lp.campos[campo] = round(v, 2)
                        lp.cfg["valor_convertido"] = round(v, 2)
                    else:
                        if not -100 <= v <= 2000:
                            erro("fator_k fora de −100 a 2000 (é percentual: 15 = +15%)")
                            ok = False
                        lp.campos[campo] = _fmt_fk(v)
                        lp.cfg["fator_k"] = v
                elif col == "fonte_preco":
                    if txt.isdigit():
                        lp.campos[campo] = int(txt)
                        lp.cfg["fonte_preco"] = fontes_rev.get(int(txt), f"fonte#{txt}")
                    elif txt in fontes:
                        lp.campos[campo] = int(fontes[txt])
                        lp.cfg["fonte_preco"] = txt
                    else:
                        erro(f"fonte_preco {txt!r} sem id: informe o número ou passe --fontes com o mapa nome→id")
                        ok = False
                elif col == "tipo_precificacao":
                    lp.campos[campo] = lp.cfg["tipo_precificacao"] = parse_tipo_prec(txt)
                elif col == "tipo_atendimento_id" and txt.lower() == LIMPAR:
                    lp.campos[campo] = None
                    lp.cfg["tipo_atendimento"] = None
                elif col in ("tipo_codigo_id", "tabela87_id", "tipo_atendimento_id", "parcelas"):
                    v = int(txt)
                    lp.campos[campo] = v
                    lp.cfg[{"tipo_codigo_id": "tipo_codigo", "tabela87_id": "tabela87",
                            "tipo_atendimento_id": "tipo_atendimento"}.get(col, col)] = v
                else:  # textos
                    lp.campos[campo] = txt
                    lp.cfg[{"nome_convenio": "nome"}.get(col, col)] = txt
            except ValueError as e:
                erro(f"{col}: {e}")
                ok = False
        if not ok:
            continue
        # avisos por linha
        if lp.campos.get("utiliza") is False and any(
                lp.campos.get(k) not in (None,) for k in ("valorInternoConvenio", "valorUnitarioConversao",
                                                          "valorConvertido")):
            aviso("Utiliza = não com valor preenchido: sem Utiliza o convênio não cobre o item (valor sem efeito)")
        linhas.append(lp)
    return linhas, achados


# --------------------------------------------------------------------------- validação cruzada

def aplicar_no_convenio(linhas: List[LinhaPreco], base: Optional[Convenio] = None) -> Convenio:
    """Sobrepõe as linhas do CSV numa configuração de convênio (para o motor)."""
    c = base or Convenio(id=0, nome="")
    for lp in linhas:
        aba = getattr(c, ABA[lp.tipo])
        cfg = aba.get(lp.id) or ConfigItem(id=lp.id)
        for k, v in lp.cfg.items():
            setattr(cfg, k, v)
        aba[lp.id] = cfg
    return c


def validar_linhas(linhas: List[LinhaPreco], cenario: Optional[dict]) -> List[Achado]:
    out: List[Achado] = []
    tem_pacote = any(lp.campos.get("pacote") for lp in linhas)
    if cenario is None:
        for lp in linhas:
            nome = f"{lp.tipo} {lp.id} {lp.nome_rabi}".strip()
            if lp.campos.get("zerarValor") and not tem_pacote:
                out.append(Achado("AVISO", lp.num, nome, "Zerar marcado, mas nenhum serviço do CSV tem Pacote: "
                                  "Zerar só age dentro de pacote fechado (confira com --catalogo)"))
            if lp.tipo == "servico" and lp.campos.get("valorInternoConvenio") is not None \
                    and not lp.campos.get("pacote"):
                out.append(Achado("AVISO", lp.num, nome, "valor combinado não é pacote: sem Pacote os itens "
                                  "somam por cima. Se o contrato é preço fechado, marque Pacote + Zerar nos inclusos"))
        return out
    cat, conv = cenario_from_dict(cenario)
    conv = aplicar_no_convenio(linhas, conv)
    for lp in linhas:
        obj = cat.item("subservico" if lp.tipo == "servico" else lp.tipo, lp.id)
        if obj is None:
            out.append(Achado("AVISO", lp.num, f"{lp.tipo} {lp.id}", "id não encontrado no catálogo informado"))
        elif lp.nome_rabi and obj.nome.strip().lower() != lp.nome_rabi.strip().lower():
            out.append(Achado("AVISO", lp.num, f"{lp.tipo} {lp.id}",
                              f"nome_rabi {lp.nome_rabi!r} ≠ catálogo {obj.nome!r}: confira o id"))
        if lp.tipo == "servico" and obj is not None and lp.campos.get("valorInternoConvenio") is not None \
                and not conv.servicos[lp.id].pacote and any(v.tipo != "equipamento" for v in obj.itens):
            msg = ("valor combinado não é pacote: serviço soma itens e sem Pacote os itens somam por cima"
                   if obj.somar_itens else
                   "valor combinado não é pacote: a composição entra por cima; se o preço já inclui itens, "
                   "marque Pacote + Zerar nos inclusos")
            out.append(Achado("AVISO", lp.num, f"servico {lp.id} {obj.nome}", msg))
    for a in motor.validar_invariantes(cat, conv):
        if a.codigo == "I4":
            continue  # 0,01 já é ERRO na leitura
        out.append(Achado(a.nivel, 0, a.item, f"{a.codigo}: {a.mensagem}"))
    return out


# --------------------------------------------------------------------------- geração

def _corpo_item(lp: LinhaPreco, campos: Optional[set] = None) -> Optional[dict]:
    corpo = {CHAVE_ID[lp.tipo]: lp.id}
    for k, v in lp.campos.items():
        if campos is None or k in campos:
            corpo[k] = v
    return corpo if len(corpo) > 1 else None


def gerar_lotes(linhas: List[LinhaPreco], convenio_id: int, unico: bool = False) -> List[dict]:
    """Devolve a sequência de chamadas: [{ordem, fase, aba, metodo, caminho, corpo, itens}]."""
    fases = [("completo", None)] if unico else FASES
    chamadas = []
    ordem = 0
    for nome_fase, campos in fases:
        for tipo in ORDEM_ABAS:
            itens = [c for c in (_corpo_item(lp, campos) for lp in linhas if lp.tipo == tipo) if c]
            for i in range(0, len(itens), LOTE_MAX):
                ordem += 1
                lote = itens[i:i + LOTE_MAX]
                chamadas.append({"ordem": ordem, "fase": nome_fase, "aba": ABA[tipo], "metodo": "PUT",
                                 "caminho": f"/convenios/{convenio_id}/{ABA[tipo]}",
                                 "corpo": {ABA[tipo]: lote}, "itens": len(lote),
                                 "lote": i // LOTE_MAX + 1})
    return chamadas


# --------------------------------------------------------------------------- prévia

def _lista(obj) -> list:
    if obj is None:
        return []
    if isinstance(obj, list):
        return obj
    for k in ("dados", "data", "items", "itens"):
        if isinstance(obj.get(k), list):
            return obj[k]
    return []


def ler_atual(caminho: str) -> Dict[Tuple[str, int], dict]:
    """``{"servicos": <GET>, "produtos": <GET>, "taxas": <GET>}`` (envelope ou lista)."""
    with open(caminho, encoding="utf-8") as f:
        d = json.load(f)
    out = {}
    for tipo, aba in ABA.items():
        for reg in _lista(d.get(aba)):
            if CHAVE_ID[tipo] in reg:
                out[(tipo, int(reg[CHAVE_ID[tipo]]))] = reg
    return out


def fmt(v, campo: str = "") -> str:
    if v is None:
        return "vazio"
    if isinstance(v, bool):
        return "sim" if v else "não"
    if isinstance(v, (int, float)) and campo in ("valorInternoConvenio", "valorUnitarioConversao",
                                                 "valorConvertido"):
        s = f"{float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {s}"
    return str(v)


def _igual(a, b, campo) -> bool:
    if a is None or b is None:
        return a is None and b is None
    if campo == "fatorK":
        try:
            return abs(parse_decimal_br(str(a)) - parse_decimal_br(str(b))) < 1e-9
        except ValueError:
            return str(a) == str(b)
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool):
        return abs(float(a) - float(b)) < 0.005
    return a == b


def montar_previa(linhas: List[LinhaPreco], achados: List[Achado], atual: Optional[Dict] = None,
                  convenio_id: int = 0, chamadas: Optional[List[dict]] = None) -> str:
    out = [f"# Prévia — convênio {convenio_id}", ""]
    out.append("> Gerada por `ferramentas/conversao/montar_convenio.py`. Nada foi gravado. "
               "Aprove antes de enviar.")
    out.append("")
    erros = [a for a in achados if a.nivel == "ERRO"]
    avisos = [a for a in achados if a.nivel == "AVISO"]
    out.append(f"**Itens no CSV:** {len(linhas)} · **Erros:** {len(erros)} · **Avisos:** {len(avisos)}")
    out.append("")
    if achados:
        out += ["## Erros e avisos", "", "| Nível | Linha | Item | Mensagem |", "|---|---|---|---|"]
        for a in erros + avisos:
            out.append(f"| {a.nivel} | {a.linha or '—'} | {a.item} | {a.mensagem} |")
        out.append("")
    out += ["## Mudanças (de → para)", ""]
    if atual is None:
        out += ["_Sem foto do estado atual (`--atual`): a coluna **de** não pôde ser calculada._", ""]
    out += ["| Item | Campo | De | Para | Porquê |", "|---|---|---|---|---|"]
    iguais = 0
    for lp in linhas:
        reg = (atual or {}).get((lp.tipo, lp.id))
        nome = f"{lp.tipo} {lp.id} {lp.nome_rabi}".strip()
        pq = lp.origem + (f" — {lp.observacao}" if lp.observacao else "")
        for campo, para in lp.campos.items():
            if atual is None:
                de = "?"
            elif reg is None:
                de = "(vínculo novo)"
            else:
                if _igual(reg.get(campo), para, campo):
                    iguais += 1
                    continue
                de = fmt(reg.get(campo), campo)
            out.append(f"| {nome} | {campo} | {de} | {fmt(para, campo)} | {pq} |")
    if atual is not None:
        out += ["", f"Campos já iguais ao atual (não mudam): {iguais}."]
    if chamadas:
        out += ["", "## Sequência de envio", "", "| # | Fase | Chamada | Itens |", "|---|---|---|---|"]
        for ch in chamadas:
            out.append(f"| {ch['ordem']} | {ch['fase']} | {ch['metodo']} {ch['caminho']} (lote {ch['lote']}) "
                       f"| {ch['itens']} |")
    out += ["", "Vazio em valor = **sem regra** (sobe de nível); 0,00 = **zero de verdade**. "
            "Valor combinado **não** é pacote: preço fechado = valor + Pacote + Zerar nos inclusos."]
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- CLI

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="CSV de preços do convênio → corpos dos PUT + prévia")
    ap.add_argument("csv")
    ap.add_argument("--convenio-id", type=int, required=True)
    ap.add_argument("--saida", required=True, help="pasta de saída")
    ap.add_argument("--catalogo", help="cenário JSON (catálogo + convênio atual) para validar composição")
    ap.add_argument("--atual", help="JSON {servicos, produtos, taxas} com o GET atual (para o de → para)")
    ap.add_argument("--fontes", help="JSON {nome da fonte de preço: id}")
    ap.add_argument("--unico", action="store_true", help="uma fase só (sem separar Utiliza/valores/…)")
    a = ap.parse_args(argv)
    fontes = json.load(open(a.fontes, encoding="utf-8")) if a.fontes else None
    linhas, achados = ler_csv(a.csv, fontes)
    cenario = json.load(open(a.catalogo, encoding="utf-8")) if a.catalogo else None
    achados += validar_linhas(linhas, cenario)
    atual = ler_atual(a.atual) if a.atual else None
    os.makedirs(a.saida, exist_ok=True)
    erros = [x for x in achados if x.nivel == "ERRO"]
    chamadas = [] if erros else gerar_lotes(linhas, a.convenio_id, a.unico)
    with open(os.path.join(a.saida, "previa.md"), "w", encoding="utf-8") as f:
        f.write(montar_previa(linhas, achados, atual, a.convenio_id, chamadas))
    manifesto = []
    for ch in chamadas:
        arq = f"{ch['ordem']:02d}-{ch['fase']}-{ch['aba']}-lote-{ch['lote']:03d}.json"
        with open(os.path.join(a.saida, arq), "w", encoding="utf-8") as f:
            json.dump(ch["corpo"], f, ensure_ascii=False, indent=1)
        manifesto.append({k: ch[k] for k in ("ordem", "fase", "aba", "metodo", "caminho", "itens", "lote")}
                         | {"arquivo": arq})
    with open(os.path.join(a.saida, "manifesto.json"), "w", encoding="utf-8") as f:
        json.dump({"convenio_id": a.convenio_id, "erros": len(erros), "chamadas": manifesto}, f,
                  ensure_ascii=False, indent=1)
    for x in achados:
        print(f"{x.nivel}: linha {x.linha or '—'} · {x.item} · {x.mensagem}")
    if erros:
        print(f"{len(erros)} erro(s): nenhum lote gerado. Corrija o CSV. Prévia em {os.path.join(a.saida, 'previa.md')}")
        return 2
    print(f"OK: {len(linhas)} itens, {len(chamadas)} chamada(s). Prévia em {os.path.join(a.saida, 'previa.md')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
