"""Monta o ``cenario.json`` que o simulador exige a partir das FOTOS lidas da API.

O simulador (``python3 -m ferramentas.conversao.simulador <cenario.json> --csv precos-<slug>.csv``)
precisa de ``{"catalogo": {...}, "convenio": {...}}`` (formato de ``modelo.cenario_from_dict``).
Esta ferramenta converte as leituras da API externa nesse formato e **lista as lacunas**:
o que a API não devolve e precisa vir do repo da clínica (régua, cadastro da S06/S08).

Entradas (todas JSON; envelope ``{dados: [...]}``, ``{data: [...]}`` ou lista crua):

  --servicos      GET /servicos/{id} de cada serviço (lista) — ou GET /servicos
  --produtos      GET /produtos (ou /produtos/{id} de cada)
  --taxas         GET /taxas
  --conv-servicos GET /convenios/{id}/servicos     (todas as páginas)
  --conv-produtos GET /convenios/{id}/produtos
  --conv-taxas    GET /convenios/{id}/taxas
  --politicas     políticas por tipo de produto TIRADAS DA RÉGUA (a API NÃO devolve
                  politicasPorTipoProduto): lista de
                  {"tipo_produto" | "tipoProdutoId", "fonte_preco" (nome ou id), "tipo_precificacao",
                   "fator_k", "ativa"}
  opcionais:
  --farol-produtos GET /convenios/{id}/farol/produtos  → custo do produto (aba Estoque)
  --ultima-compra  {"<produtoId>": GET /estoque/ultima-compra/{id}, ...}
  --tabelas-preco  [{"tabela": "<nome>", "resposta": GET /tabelas-preco/produtos?id=<id>}, ...]
  --precificacao   GET /tabelas-preco/precificacao  → nome da fonte de preço por id
  --parametros     GET /parametros/orcamento        → limites vermelho/amarelo do Farol
  --composicao     {"<servicoId>": [{"tipo": "produto|taxa|subservico|equipamento", "id", "quantidade"}]}
                   (árvore da S08) — usada quando o GET do serviço não traz a composição
  --complemento-produtos {"<produtoId>": {"custo", "preco_venda_tabela", "fonte_preco",
                   "tipo_precificacao", "fator_k", "ultima_pesquisa", "preco_medio"}} (aba Estoque;
                   a API não devolve estes campos)

Saída: ``cenario.json`` (com ``_lacunas``) e, na tela, a lista de lacunas.
Uso:
  python3 -m ferramentas.conversao.montar_cenario --convenio-id 12 --nome "Convênio A" \\
      --servicos fotos/servicos.json --produtos fotos/produtos.json --taxas fotos/taxas.json \\
      --conv-servicos fotos/conv-servicos.json --conv-produtos fotos/conv-produtos.json \\
      --conv-taxas fotos/conv-taxas.json --politicas dados/convenios/convenio-a/politicas.json \\
      --saida dados/convenios/convenio-a/cenario.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Optional

RAIZ_KIT = Path(__file__).resolve().parents[2]
if str(RAIZ_KIT) not in sys.path:
    sys.path.insert(0, str(RAIZ_KIT))

from ferramentas.conversao.modelo import cenario_from_dict  # noqa: E402
from ferramentas.rabi_api.corpo_escrita import MAPA_SERVICO, CampoDeEscritaAusente, _AUSENTE  # noqa: E402

CAMPOS_PRODUTO_ESTOQUE = ("custo", "preco_venda_tabela", "fonte_preco", "tipo_precificacao", "fator_k",
                          "ultima_pesquisa", "preco_medio")


def lista(resposta: Any) -> list:
    """Normaliza envelope da API (dados | data | items | lista crua | objeto único)."""
    if resposta is None:
        return []
    if isinstance(resposta, list):
        return resposta
    if isinstance(resposta, dict):
        for k in ("dados", "data", "items"):
            if isinstance(resposta.get(k), list):
                return resposta[k]
        return [resposta]
    raise TypeError(f"formato inesperado: {type(resposta).__name__}")


def _pega(d: dict, *nomes, padrao=None):
    for n in nomes:
        if n in d:
            return d[n]
    return padrao


def _id_aninhado(d: dict, *nomes):
    v = _pega(d, *nomes)
    if isinstance(v, dict):
        return v.get("id")
    return v


def _nome_aninhado(d: dict, *nomes):
    v = _pega(d, *nomes)
    if isinstance(v, dict):
        return v.get("nome") or v.get("descricao")
    return v


def _composicao_do_get(s: dict) -> Optional[list]:
    """Composição a partir do GET do serviço (mesmos apelidos do conversor de escrita).

    Devolve None se o GET não traz composição nenhuma. Quantidade: usa ``quantidade`` quando o
    vínculo traz; senão 1.
    """
    achou = False
    itens = []
    for campo, tipo in (("produtoIds", "produto"), ("servicosRelacionados", "subservico"),
                        ("equipamentoIds", "equipamento")):
        v = MAPA_SERVICO[campo](s)
        if v is _AUSENTE:
            continue
        achou = True
        itens += [{"tipo": tipo, "id": int(i), "quantidade": 1} for i in v]
    tx = MAPA_SERVICO["taxaServicoId"](s)
    if tx is not _AUSENTE:
        achou = True
        if tx is not None:
            itens.append({"tipo": "taxa", "id": int(tx), "quantidade": 1})
    # quantidade, quando o vínculo de produto a traz
    for chave in ("ServicoProduto", "servicoProduto", "produtos"):
        for el in s.get(chave) or []:
            if isinstance(el, dict) and "quantidade" in el:
                pid = el.get("produtoId") or (el.get("produto") or {}).get("id")
                for it in itens:
                    if it["tipo"] == "produto" and it["id"] == pid:
                        it["quantidade"] = float(el["quantidade"])
    return itens if achou else None


def montar_cenario(fotos: dict, politicas: list, *, convenio_id: int = 0, nome: str = "",
                   composicao: Optional[dict] = None,
                   complemento_produtos: Optional[dict] = None) -> tuple[dict, list[str]]:
    """Monta o cenário. ``fotos`` = {nome_da_entrada: resposta da API}. Devolve (cenario, lacunas)."""
    lacunas: list[str] = []
    composicao = {str(k): v for k, v in (composicao or {}).items()}
    complemento_produtos = {str(k): v for k, v in (complemento_produtos or {}).items()}

    # fonte de preço: id → nome (fontePrecoId de /tabelas-preco/precificacao; não confirmado)
    fontes = {}
    for op in lista(fotos.get("precificacao")):
        if "fontePrecoId" in op:
            fontes[op["fontePrecoId"]] = op.get("nome")
    if fontes:
        lacunas.append("fontePrecoCompraOptionsId foi lido como o `fontePrecoId` de "
                       "/tabelas-preco/precificacao (provável, NÃO confirmado): grave 1 item em homologação.")

    def nome_fonte(v):
        if v is None or isinstance(v, str):
            return v
        if v in fontes:
            return fontes[v]
        lacunas.append(f"fonte de preço id {v} sem nome (faltou --precificacao): o motor tratará como tabela.")
        return str(v)

    # ---- catálogo: serviços
    servicos = []
    for s in lista(fotos.get("servicos")):
        sid = int(s["id"])
        try:
            itens = _composicao_do_get(s)
        except CampoDeEscritaAusente as e:
            lacunas.append(f"serviço {sid}: composição ambígua no GET ({e}); use --composicao.")
            itens = None
        if str(sid) in composicao:
            itens = composicao[str(sid)]
        elif itens is None:
            lacunas.append(f"serviço {sid} ({s.get('nome')}): o GET não trouxe a composição — informe em "
                           "--composicao (árvore da S08); sem isso ele entra SEM itens.")
            itens = []
        somar = _pega(s, "somarItens", "somarItems")
        if somar is None:
            lacunas.append(f"serviço {sid}: 'somarItens' ausente no GET — assumido false.")
        servicos.append({
            "id": sid, "nome": s.get("nome") or s.get("descricao") or f"Serviço {sid}",
            "valor_cadastro": float(s.get("valor") or 0), "somar_itens": bool(somar),
            "ativo": bool(s.get("ativo", True)), "descricao": s.get("descricao"),
            "codigo": s.get("codigo"), "codigo_tuss": s.get("codigoTUSS"),
            "tipo_codigo": _id_aninhado(s, "tipoCodigoId", "tipoCodigo", "TipoCodigo"),
            "tabela87": _id_aninhado(s, "tabelaANS87ID", "tabelaANS87Id", "tabelaANS87"),
            "tipo_atendimento": _id_aninhado(s, "tipoAtendimento", "tipoAtendimentoId", "TipoAtendimento"),
            "itens": itens,
        })

    # ---- catálogo: produtos
    custo_farol = {int(x["produto_id"]): x.get("custo") for x in lista(fotos.get("farol_produtos"))
                   if "produto_id" in x}
    ultima = {str(k): v for k, v in (fotos.get("ultima_compra") or {}).items()}
    precos_tab: dict[int, dict] = {}
    for bloco in fotos.get("tabelas_preco") or []:
        for linha in lista(bloco.get("resposta")):
            tpi = linha.get("tabelaPrecoInterna") or {}
            vals = {f"PRECO_{n}": tpi.get(f"precificacao{n}") for n in (1, 2, 3)
                    if tpi.get(f"precificacao{n}") is not None}
            if vals and "id" in linha:
                precos_tab.setdefault(int(linha["id"]), {})[bloco["tabela"]] = vals
    tipo_nome: dict[Any, str] = {}
    produtos = []
    for p in lista(fotos.get("produtos")):
        pid = int(p["id"])
        tp_nome = _nome_aninhado(p, "TipoProduto", "tipoProduto")
        tp_id = _id_aninhado(p, "tipoProdutoId", "TipoProduto", "tipoProduto")
        if tp_id is not None and tp_nome:
            tipo_nome[tp_id] = tp_nome
        comp = complemento_produtos.get(str(pid), {})
        item = {"id": pid, "nome": p.get("nome") or f"Produto {pid}", "tipo_produto": tp_nome,
                "ativo": bool(p.get("ativo", True)), "codigo": p.get("codigoProduto"),
                "tipo_codigo": _id_aninhado(p, "tipoCodigoId", "tipoCodigo"),
                "tabela87": _id_aninhado(p, "tabelaANS87ID", "tabelaANS87Id", "tabelaANS87"),
                "precos_tabela": precos_tab.get(pid, {})}
        uc = ultima.get(str(pid))
        if isinstance(uc, dict) and uc.get("ultimaCompraUnitaria"):
            item["ultima_compra"] = uc["ultimaCompraUnitaria"]  # 0 = sem dado (a rota nunca dá 404)
        for campo in CAMPOS_PRODUTO_ESTOQUE:
            if campo in comp:
                item[campo] = comp[campo]
        if "custo" not in item and custo_farol.get(pid) is not None:
            item["custo"] = custo_farol[pid]
        if item.get("fonte_preco") is not None:
            item["fonte_preco"] = nome_fonte(item["fonte_preco"])
        faltam = [c for c in ("custo", "fonte_preco") if item.get(c) is None]
        if faltam:
            lacunas.append(f"produto {pid} ({item['nome']}): sem {', '.join(faltam)} (aba Estoque; a API não "
                           "devolve) — informe em --complemento-produtos ou --farol-produtos.")
        produtos.append(item)

    # ---- catálogo: taxas
    taxas = [{"id": int(t["id"]), "nome": _pega(t, "taxas", "nome", padrao=f"Taxa {t['id']}"),
              "valor_cadastro": float(t.get("valor") or 0), "ativo": bool(t.get("ativo", True)),
              "descricao": t.get("descricao"), "codigo": _pega(t, "codigoTaxa", "codigo")}
             for t in lista(fotos.get("taxas"))]

    # ---- convênio (nível 3)
    conv_serv = [{
        "id": int(x["servicoId"]), "utiliza": bool(x.get("utiliza", False)),
        "valor_convertido": x.get("valorInternoConvenio"), "pacote": bool(x.get("pacote", False)),
        "zerar": bool(x.get("zerarValor", False)), "nome": x.get("nomeConversao"),
        "descricao": x.get("descricaoConvenio"), "codigo": x.get("codigo"),
        "codigo_convenio": x.get("codigoConvenio"), "tipo_codigo": x.get("tipoCodigoId"),
        "tabela87": x.get("tabela87ANSId"), "tipo_atendimento": x.get("tipoAtendimentoId"),
        "parcelas": x.get("parcelasMaximas"), "autorizacao_previa": x.get("autorizacaoPrevia"),
        "retorno": x.get("retornoServico"),
    } for x in lista(fotos.get("conv_servicos"))]
    conv_prod = [{
        "id": int(x["produtoId"]), "utiliza": bool(x.get("utiliza", False)),
        "valor_convertido": x.get("valorUnitarioConversao"), "zerar": bool(x.get("zerarValor", False)),
        "fator_k": x.get("fatorK"), "fonte_preco": nome_fonte(x.get("fontePrecoCompraOptionsId")),
        "tipo_precificacao": x.get("tipoPrecificacao"), "nome": x.get("nomeConversao"),
        "descricao": x.get("descricaoConversao"), "codigo": x.get("codigoConversao"),
        "tipo_codigo": x.get("tipoCodigoId"), "tabela87": x.get("tabela87ANSId"),
    } for x in lista(fotos.get("conv_produtos"))]
    conv_tax = [{
        "id": int(x["taxaId"]), "utiliza": bool(x.get("utiliza", False)),
        "valor_convertido": x.get("valorConvertido"), "zerar": bool(x.get("zerarValor", False)),
        "nome": x.get("nomeConvertido"), "descricao": x.get("descricaoConvertida"),
        "codigo": x.get("codigo"), "tipo_codigo": x.get("tipoCodigoId"), "tabela87": x.get("tabela87ANSId"),
    } for x in lista(fotos.get("conv_taxas"))]

    # ---- políticas (nível 2) — vêm da régua, não da API
    pols = []
    if not politicas:
        lacunas.append("sem políticas por tipo de produto: a API NÃO devolve politicasPorTipoProduto — "
                       "informe --politicas a partir da régua contratual (S10a).")
    for pol in politicas or []:
        tp = pol.get("tipo_produto")
        if tp is None and "tipoProdutoId" in pol:
            tp = tipo_nome.get(pol["tipoProdutoId"])
            if tp is None:
                lacunas.append(f"política com tipoProdutoId {pol['tipoProdutoId']} sem nome correspondente "
                               "nos produtos lidos — ignorada.")
                continue
        pols.append({"tipo_produto": tp, "fonte_preco": nome_fonte(pol.get("fonte_preco")),
                     "tipo_precificacao": pol.get("tipo_precificacao"), "fator_k": pol.get("fator_k"),
                     "ativa": bool(pol.get("ativa", True))})

    par = lista(fotos.get("parametros"))
    par = par[0] if par and isinstance(par[0], dict) else {}
    vermelho, amarelo = par.get("parametroVermelho"), par.get("parametroAmarelo")
    if vermelho is None or amarelo is None:
        lacunas.append("limites do Farol não lidos (--parametros = GET /parametros/orcamento): "
                       "usados 100/120 — confira na tela.")
    cenario = {
        "_leia": "Gerado por ferramentas/conversao/montar_cenario.py a partir das fotos da API. "
                 "Veja _lacunas antes de confiar na previsão.",
        "_lacunas": lacunas,
        "catalogo": {"servicos": servicos, "produtos": produtos, "taxas": taxas},
        "convenio": {"id": convenio_id, "nome": nome, "servicos": conv_serv, "produtos": conv_prod,
                     "taxas": conv_tax, "politicas": pols,
                     "parametro_vermelho": vermelho if vermelho is not None else 100,
                     "parametro_amarelo": amarelo if amarelo is not None else 120},
    }
    cenario_from_dict(cenario)  # garante que o simulador consegue ler
    return cenario, lacunas


def _ler(caminho: Optional[str]):
    if not caminho:
        return None
    return json.loads(Path(caminho).read_text(encoding="utf-8"))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--convenio-id", type=int, required=True)
    ap.add_argument("--nome", default="")
    for opc in ("servicos", "produtos", "taxas", "conv-servicos", "conv-produtos", "conv-taxas"):
        ap.add_argument(f"--{opc}", required=True)
    ap.add_argument("--politicas", required=True, help="políticas da régua (JSON); lista vazia [] se não houver")
    for opc in ("farol-produtos", "ultima-compra", "tabelas-preco", "precificacao", "parametros",
                "composicao", "complemento-produtos"):
        ap.add_argument(f"--{opc}")
    ap.add_argument("--saida", required=True)
    a = ap.parse_args(argv)
    fotos = {k.replace("-", "_"): _ler(getattr(a, k.replace("-", "_")))
             for k in ("servicos", "produtos", "taxas", "conv-servicos", "conv-produtos", "conv-taxas",
                       "farol-produtos", "ultima-compra", "tabelas-preco", "precificacao", "parametros")}
    cenario, lacunas = montar_cenario(fotos, _ler(a.politicas) or [], convenio_id=a.convenio_id, nome=a.nome,
                                      composicao=_ler(a.composicao),
                                      complemento_produtos=_ler(a.complemento_produtos))
    Path(a.saida).parent.mkdir(parents=True, exist_ok=True)
    Path(a.saida).write_text(json.dumps(cenario, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"Cenário salvo em {a.saida}: {len(cenario['catalogo']['servicos'])} serviços, "
          f"{len(cenario['catalogo']['produtos'])} produtos, {len(cenario['catalogo']['taxas'])} taxas.")
    if lacunas:
        print(f"\n{len(lacunas)} LACUNA(S) — a previsão só vale depois de resolvê-las:")
        for x in lacunas:
            print(f"- {x}")
    print(f"\nPróximo: python3 -m ferramentas.conversao.simulador {a.saida} --csv precos-<slug>.csv --invariantes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
