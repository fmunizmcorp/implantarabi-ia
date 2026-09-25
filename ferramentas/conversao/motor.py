"""Motor de conversão de valores por convênio — implementa as árvores do manual.

Fonte primária (prevalece sobre este código):
  https://www.rabisistemas.com.br/manual/precos/guia-ia.html#algoritmo
  (2.1 produto, 2.2 taxa, 2.3 base, 2.4 serviço composto, 2.5 orçamento,
   2.6/2.7 Farol e Farol consolidado, 2.8 tipo de atendimento, 2.9 textos,
   2.10 Farol › Itens, 2.11 quatro linhas)
  https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#arvores
Conferido em 2026-09-25 · Vale para: produção desde 23–24/09/2026 · Kit v0.1.0.

O motor é uma PREVISÃO para conferir antes/depois de gravar. Quem manda é o
Rabi: depois de gravar, compare com ``conferir_farol.py``.

Decisões de leitura (documentadas no README, seção "Interpretações"):
  * valores unitários de produto com Fator K são arredondados a centavos;
  * produto com custo ``None`` ou ``<= 0`` conta como "sem custo" (roxo);
  * "sem preço" = produto com Utiliza cuja cadeia não achou fonte nem valor;
  * valores das linhas-filhas de um subserviço são por 1 unidade do pai;
  * a linha 🔒 de serviço que soma itens = Σ q × preço de casa (recursivo).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional, Tuple

from .modelo import (
    Catalogo, ConfigItem, Convenio, Produto, Servico, Taxa,
    FONTE_FIXO, FONTE_MEDIO, FONTE_ULTIMA_COMPRA, FONTE_ULTIMA_PESQUISA,
)

# Motivos oficiais (aba Farol › Itens, coluna "Conta no total = Não").
NAO_UTILIZA = "NAO_UTILIZA_NO_CONVENIO"
ZERADO_EM_PACOTE = "ZERADO_EM_PACOTE"
PAI_FORA = "PAI_FORA_DO_TOTAL"
# Motivos do kit (não existem na tela; usados só para explicar).
EQUIPAMENTO = "EQUIPAMENTO_SEM_VALOR"
CICLO = "CICLO_CORTADO"
NAO_CADASTRADO = "ITEM_NAO_ENCONTRADO_NO_CATALOGO"

VERDE, AMARELO, VERMELHO, ROXO = "VERDE", "AMARELO", "VERMELHO", "ROXO"


def r2(v: Optional[float]) -> Optional[float]:
    return None if v is None else round(v + 0.0, 2)


# ---------------------------------------------------------------------------
# 2.1 Produto
# ---------------------------------------------------------------------------

@dataclass
class PrecoItem:
    valor: float
    origem: str  # CONVERTIDO | FONTE | SEM_FONTE | CADASTRO (taxa)
    fonte: Optional[str] = None
    tipo_precificacao: Optional[str] = None
    fator_k: Optional[float] = None
    sem_preco: bool = False
    detalhe: str = ""


def _primeiro(*vals):
    """Primeiro valor preenchido. Texto em branco ('') conta como vazio; 0 não."""
    for v in vals:
        if v is None or (isinstance(v, str) and v.strip() == ""):
            continue
        return v
    return None


def valor_produto(p: Produto, c: Optional[Convenio]) -> PrecoItem:
    """Valor unitário do produto no convênio (árvore 3.2). ``c=None`` = preço de casa."""
    cp: Optional[ConfigItem] = c.produtos.get(p.id) if c else None
    if cp is not None and cp.valor_convertido is not None:
        fk = cp.fator_k if cp.fator_k is not None else 0.0  # SÓ o Fator K da própria linha
        v = r2(cp.valor_convertido * (1 + fk / 100.0))
        return PrecoItem(v, "CONVERTIDO", fator_k=cp.fator_k,
                         detalhe=f"valor convertido {cp.valor_convertido} × (1+{fk}/100)")
    pol = None
    if c and p.tipo_produto and p.tipo_produto in c.politicas and c.politicas[p.tipo_produto].ativa:
        pol = c.politicas[p.tipo_produto]
    fonte = _primeiro(cp.fonte_preco if cp else None, pol.fonte_preco if pol else None, p.fonte_preco)
    tipo = _primeiro(cp.tipo_precificacao if cp else None, pol.tipo_precificacao if pol else None,
                     p.tipo_precificacao)
    fk = _primeiro(cp.fator_k if cp else None, pol.fator_k if pol else None, p.fator_k, 0.0)
    if fonte is None:
        return PrecoItem(0.0, "SEM_FONTE", sem_preco=True, detalhe="sem valor convertido e sem fonte de preço")
    mult = 1 + fk / 100.0
    if fonte == FONTE_FIXO:  # SEM Fator K
        v = p.preco_venda_tabela
        return PrecoItem(r2(v or 0.0), "FONTE", fonte, tipo, None, sem_preco=v is None,
                         detalhe="Preço de venda tabela (fixo, sem Fator K)")
    base = {FONTE_ULTIMA_COMPRA: p.ultima_compra, FONTE_ULTIMA_PESQUISA: p.ultima_pesquisa,
            FONTE_MEDIO: p.preco_medio}
    if fonte in base:
        v = base[fonte]
        return PrecoItem(r2((v or 0.0) * mult), "FONTE", fonte, tipo, fk, sem_preco=v is None,
                         detalhe=f"{fonte} {v} × (1+{fk}/100)")
    # tabela de preços interna
    v = (p.precos_tabela.get(fonte) or {}).get(tipo) if tipo else None
    if not v:
        v = p.preco_venda_tabela
    return PrecoItem(r2((v or 0.0) * mult), "FONTE", fonte, tipo, fk, sem_preco=not v,
                     detalhe=f"tabela {fonte}/{tipo} {v} × (1+{fk}/100)")


# ---------------------------------------------------------------------------
# 2.2 Taxa
# ---------------------------------------------------------------------------

def valor_taxa(t: Taxa, c: Optional[Convenio]) -> PrecoItem:
    ct = c.taxas.get(t.id) if c else None
    if ct is not None and ct.valor_convertido is not None:
        return PrecoItem(r2(ct.valor_convertido), "CONVERTIDO")
    return PrecoItem(r2(t.valor_cadastro or 0.0), "CADASTRO")


# ---------------------------------------------------------------------------
# 2.3 base e pacote fechado
# ---------------------------------------------------------------------------

def base(s: Servico, c: Convenio) -> float:
    """Valor próprio (linha ✅ e linha de procedimento do XML)."""
    sc = c.servicos.get(s.id)
    if sc is not None and sc.valor_convertido is not None:
        return r2(sc.valor_convertido)  # inclusive 0: zero é zero
    return 0.0 if s.somar_itens else r2(s.valor_cadastro or 0.0)


def pacote_fechado(s: Servico, c: Convenio) -> bool:
    sc = c.servicos.get(s.id)
    if sc is None or not sc.pacote:
        return False
    return (not s.somar_itens) or (sc.valor_convertido is not None)


def cor_farol(indice: Optional[float], c: Convenio) -> Optional[str]:
    if indice is None:
        return None
    if indice <= c.parametro_vermelho:
        return VERMELHO
    if indice <= c.parametro_amarelo:
        return AMARELO
    return VERDE


def _sem_custo(p: Produto) -> bool:
    return p.custo is None or p.custo <= 0


# ---------------------------------------------------------------------------
# 2.4 / 2.10 serviço composto e Farol › Itens
# ---------------------------------------------------------------------------

@dataclass
class Linha:
    """Uma linha da árvore (como na aba Farol › Itens)."""
    tipo: str  # servico | subservico | produto | taxa | equipamento
    id: int
    nome: str
    caminho: str
    quantidade: float = 1.0
    valor_unitario: Optional[float] = None  # produto/taxa: preço no convênio
    base: Optional[float] = None  # serviço/subserviço: valor próprio
    valor_efetivo: float = 0.0  # valor da própria linha considerado na conta (0 se fora)
    receita: float = 0.0  # produto/taxa: = valor_efetivo; subserviço/raiz: total da subárvore
    custo: float = 0.0
    sem_custo: bool = False
    sem_preco: bool = False
    tem_produto: bool = False
    conta: bool = True
    motivo: Optional[str] = None
    utiliza: Optional[bool] = None
    zerar: Optional[bool] = None
    indice: Optional[float] = None
    farol: Optional[str] = None
    origem_preco: Optional[str] = None
    filhos: List["Linha"] = field(default_factory=list)

    def percorrer(self):
        yield self
        for f in self.filhos:
            yield from f.percorrer()


@dataclass
class ResultadoServico:
    servico_id: int
    nome: str
    utiliza: bool
    base: float  # linha ✅
    total: float  # linha Σ = receita do Farol = valor(S, C)
    custo: float
    indice: Optional[float]
    farol: Optional[str]
    pacote_fechado: bool
    casa: float  # linha 🔒
    casa_rotulo: str
    combinado: Optional[float]  # linha 🔁
    receita_por_tipo: Dict[str, float]
    arvore: Linha
    avisos: List[str] = field(default_factory=list)

    @property
    def linhas(self) -> List[Linha]:
        return list(self.arvore.percorrer())


class _Ctx:
    def __init__(self, cat: Catalogo, c: Convenio):
        self.cat, self.c = cat, c
        self.avisos: List[str] = []


def _cfg(c: Convenio, tipo: str, id_: int) -> Optional[ConfigItem]:
    return {"produto": c.produtos, "taxa": c.taxas, "subservico": c.servicos}.get(tipo, {}).get(id_)


def _avaliar(ctx: _Ctx, s: Servico, zera_ctx: bool, visitados: Tuple[int, ...], fora: bool,
             linha: Linha) -> Dict[str, float]:
    """Preenche ``linha`` (serviço/subserviço) com filhos, total e custo (por 1 unidade).

    Devolve receita por tipo {servico, produto, taxa} por unidade.
    """
    c, cat = ctx.c, ctx.cat
    b = base(s, c)
    zera = zera_ctx or pacote_fechado(s, c)
    total = 0.0 if fora else b
    por_tipo = {"servico": 0.0 if fora else b, "produto": 0.0, "taxa": 0.0}
    custo = 0.0
    sem_custo = sem_preco = tem_produto = False
    for v in s.itens:
        obj = cat.item(v.tipo, v.id)
        cam = f"{linha.caminho} > {getattr(obj, 'nome', v.id)}"
        if v.tipo == "equipamento":
            linha.filhos.append(Linha("equipamento", v.id, str(v.id), cam, v.quantidade,
                                      conta=False, motivo=EQUIPAMENTO))
            continue
        if obj is None:
            ctx.avisos.append(f"{cam}: {v.tipo} {v.id} não está no catálogo")
            linha.filhos.append(Linha(v.tipo, v.id, str(v.id), cam, v.quantidade, conta=False,
                                      motivo=NAO_CADASTRADO))
            continue
        cfg = _cfg(c, v.tipo, v.id)
        utiliza = bool(cfg and cfg.utiliza)
        zerar = bool(cfg and cfg.zerar)
        motivo = PAI_FORA if fora else (None if utiliza else NAO_UTILIZA)
        zerado = motivo is None and zera and zerar
        q = v.quantidade
        if v.tipo == "subservico":
            if v.id in visitados:
                ctx.avisos.append(f"{cam}: ciclo detectado (serviço {v.id} já está no caminho) — cortado")
                linha.filhos.append(Linha("subservico", v.id, obj.nome, cam, q, conta=False, motivo=CICLO))
                continue
            sub = Linha("subservico", v.id, obj.nome, cam, q, utiliza=utiliza, zerar=zerar)
            pt = _avaliar(ctx, obj, zera, visitados + (v.id,), motivo is not None, sub)
            sb = base(obj, c)
            sub.base = sb
            contrib = 0.0 if motivo else (sub.receita - (sb if zerado else 0.0))
            if motivo is None and zerado:
                pt = dict(pt, servico=pt["servico"] - sb)
            sub.receita = r2(q * contrib)
            sub.valor_efetivo = 0.0 if (motivo or zerado) else r2(q * sb)
            sub.custo = r2(q * sub.custo)
            sub.conta = motivo is None and not zerado
            sub.motivo = motivo or (ZERADO_EM_PACOTE if zerado else None)
            sub.indice = (sub.receita / sub.custo * 100) if sub.custo > 0 else None
            sub.farol = ROXO if sub.sem_custo else cor_farol(sub.indice, c)
            linha.filhos.append(sub)
            total += q * contrib
            if motivo is None:
                for k in por_tipo:
                    por_tipo[k] += q * pt[k]
            custo += sub.custo
            sem_custo |= sub.sem_custo
            sem_preco |= sub.sem_preco
            tem_produto |= sub.tem_produto
            continue
        # produto ou taxa
        preco = valor_produto(obj, c) if v.tipo == "produto" else valor_taxa(obj, c)
        entra = motivo is None and not zerado
        efetivo = r2(q * preco.valor) if entra else 0.0
        li = Linha(v.tipo, v.id, obj.nome, cam, q, valor_unitario=preco.valor, valor_efetivo=efetivo,
                   receita=efetivo, conta=entra, motivo=motivo or (ZERADO_EM_PACOTE if zerado else None),
                   utiliza=utiliza, zerar=zerar, origem_preco=preco.origem)
        if v.tipo == "produto":
            li.tem_produto = True
            li.sem_custo = _sem_custo(obj)
            li.sem_preco = utiliza and preco.sem_preco and not fora
            li.custo = 0.0 if li.sem_custo else r2(q * obj.custo)
            li.indice = (li.receita / li.custo * 100) if li.custo > 0 else None
            li.farol = ROXO if li.sem_custo else cor_farol(li.indice, c)
            custo += li.custo
            sem_custo |= li.sem_custo
            sem_preco |= li.sem_preco
            tem_produto = True
        linha.filhos.append(li)
        total += efetivo
        if entra:
            por_tipo[v.tipo] += efetivo
    linha.base = b
    linha.receita = r2(total)
    linha.valor_efetivo = 0.0 if fora else b
    linha.custo = r2(custo)
    linha.sem_custo, linha.sem_preco, linha.tem_produto = sem_custo, sem_preco, tem_produto
    return por_tipo


def casa_servico(cat: Catalogo, s: Servico, _visit: Tuple[int, ...] = ()) -> float:
    """Linha 🔒: soma dos itens a preço de casa (se soma itens) ou Valor do cadastro."""
    if not s.somar_itens:
        return r2(s.valor_cadastro or 0.0)
    tot = 0.0
    for v in s.itens:
        obj = cat.item(v.tipo, v.id)
        if obj is None or v.tipo == "equipamento":
            continue
        if v.tipo == "produto":
            tot += v.quantidade * valor_produto(obj, None).valor
        elif v.tipo == "taxa":
            tot += v.quantidade * (obj.valor_cadastro or 0.0)
        elif v.id not in _visit:
            tot += v.quantidade * casa_servico(cat, obj, _visit + (s.id,))
    return r2(tot)


def calcular_servico(cat: Catalogo, c: Convenio, servico_id: int) -> ResultadoServico:
    """valor(S, C) com a árvore completa, custo, Farol e as 4 linhas."""
    s = cat.servicos[servico_id]
    ctx = _Ctx(cat, c)
    sc = c.servicos.get(s.id)
    raiz = Linha("servico", s.id, s.nome, s.nome, 1.0, utiliza=bool(sc and sc.utiliza),
                 zerar=bool(sc and sc.zerar))
    pt = _avaliar(ctx, s, False, (s.id,), False, raiz)
    raiz.indice = (raiz.receita / raiz.custo * 100) if raiz.custo > 0 else None
    raiz.farol = ROXO if raiz.sem_custo else cor_farol(raiz.indice, c)
    if s.somar_itens and sc is not None and sc.valor_convertido is None:
        pass  # linha ✅ = 0,00 "sem preço próprio: itens cobrados à parte" — não é erro
    return ResultadoServico(
        servico_id=s.id, nome=s.nome, utiliza=bool(sc and sc.utiliza), base=raiz.base,
        total=raiz.receita, custo=raiz.custo, indice=r2(raiz.indice), farol=raiz.farol,
        pacote_fechado=pacote_fechado(s, c), casa=casa_servico(cat, s),
        casa_rotulo="(soma dos itens)" if s.somar_itens else "",
        combinado=sc.valor_convertido if sc else None,
        receita_por_tipo={k: r2(v) for k, v in pt.items()}, arvore=raiz, avisos=ctx.avisos)


def valor(cat: Catalogo, c: Convenio, servico_id: int) -> float:
    return calcular_servico(cat, c, servico_id).total


def quatro_linhas(cat: Catalogo, c: Convenio, servico_id: int) -> Dict[str, object]:
    """Coluna Valor do serviço (2.11): 🔒 casa, 🔁 combinado, ✅ próprio, Σ total."""
    r = calcular_servico(cat, c, servico_id)
    s = cat.servicos[servico_id]
    expl = ""
    if s.somar_itens and r.combinado is None:
        expl = "0,00 (sem preço próprio: itens cobrados à parte)"
    return {"casa": r.casa, "casa_rotulo": r.casa_rotulo, "combinado": r.combinado,
            "proprio": r.base, "proprio_explicacao": expl, "total": r.total}


def calcular_convenio(cat: Catalogo, c: Convenio, so_ativos: bool = False) -> List[ResultadoServico]:
    out = []
    for sid, s in sorted(cat.servicos.items()):
        if so_ativos and not s.ativo:
            continue
        out.append(calcular_servico(cat, c, sid))
    return out


def farol_produto(cat: Catalogo, c: Convenio, produto_id: int) -> Dict[str, object]:
    """Farol de um produto sozinho (aba Farol › Produtos)."""
    p = cat.produtos[produto_id]
    pr = valor_produto(p, c)
    if _sem_custo(p):
        return {"receita": pr.valor, "custo": None, "indice": None, "farol": ROXO}
    ind = pr.valor / p.custo * 100
    return {"receita": pr.valor, "custo": r2(p.custo), "indice": r2(ind), "farol": cor_farol(ind, c)}


# ---------------------------------------------------------------------------
# 2.8 / 2.9 tipo de atendimento e textos
# ---------------------------------------------------------------------------

def tipo_atendimento_efetivo(s: Servico, c: Convenio):
    sc = c.servicos.get(s.id)
    return _primeiro(sc.tipo_atendimento if sc else None, s.tipo_atendimento)


def textos_servico(s: Servico, c: Convenio) -> Dict[str, object]:
    sc = c.servicos.get(s.id) or ConfigItem(id=s.id)
    return {
        "nome": _primeiro(sc.nome, s.nome),
        "descricao": _primeiro(sc.descricao, s.descricao),
        "codigo": _primeiro(sc.codigo, sc.codigo_convenio, s.codigo, s.codigo_tuss),
        "tipo_codigo": _primeiro(sc.tipo_codigo, s.tipo_codigo),
        "tabela87": _primeiro(sc.tabela87, s.tabela87),
        "tipo_atendimento": tipo_atendimento_efetivo(s, c),
        "parcelas": _primeiro(sc.parcelas, c.limite_parcelas),
    }


def textos_produto(p: Produto, c: Convenio) -> Dict[str, object]:
    cp = c.produtos.get(p.id) or ConfigItem(id=p.id)
    fonte = valor_produto(p, c).fonte
    return {
        "nome": _primeiro(cp.nome, p.nome),
        "descricao": _primeiro(cp.descricao, p.descricao),
        "codigo": _primeiro(cp.codigo, p.codigos_tabela.get(fonte) if fonte else None, p.codigo),
        "tipo_codigo": _primeiro(cp.tipo_codigo, p.tipo_codigo),
        "tabela87": _primeiro(cp.tabela87, p.tabela87),
    }


def textos_taxa(t: Taxa, c: Convenio) -> Dict[str, object]:
    ct = c.taxas.get(t.id) or ConfigItem(id=t.id)
    return {
        "nome": _primeiro(ct.nome, t.nome),
        "descricao": _primeiro(ct.descricao, t.descricao),
        "codigo": _primeiro(ct.codigo, t.codigo),
        "tipo_codigo": _primeiro(ct.tipo_codigo, t.tipo_codigo),
        "tabela87": _primeiro(ct.tabela87, t.tabela87),
    }


# ---------------------------------------------------------------------------
# 2.7 Farol consolidado
# ---------------------------------------------------------------------------

@dataclass
class Parte:
    receita: float
    custo: float
    sem_custo: bool = False
    sem_preco: bool = False
    tem_produto: bool = False


def farol_consolidado(partes: Iterable[Parte], c: Convenio) -> Dict[str, object]:
    partes = list(partes)
    receita = sum(p.receita for p in partes)
    custo = sum(p.custo for p in partes)
    if any(p.sem_custo or p.sem_preco for p in partes):
        return {"receita": r2(receita), "custo": r2(custo), "indice": None, "farol": ROXO}
    if custo <= 0:
        return {"receita": r2(receita), "custo": 0.0, "indice": None, "farol": None}
    ind = receita / custo * 100
    return {"receita": r2(receita), "custo": r2(custo), "indice": r2(ind), "farol": cor_farol(ind, c)}


# ---------------------------------------------------------------------------
# 2.5 Orçamento
# ---------------------------------------------------------------------------

@dataclass
class LinhaOrcamento:
    tipo: str
    id: int
    nome: str
    caminho: str
    qtd_composicao: float
    qtd_usada: float
    qtd_cobrada: float
    preco_unitario: float
    valor: float
    custo: float
    sem_custo: bool = False
    sem_preco: bool = False
    motivo: Optional[str] = None
    servico_raiz: Optional[int] = None


@dataclass
class ResultadoOrcamento:
    linhas: List[LinhaOrcamento]
    total: float
    custo: float
    indice: Optional[float]
    farol: Optional[str]
    por_servico: Dict[int, Dict[str, object]]
    avisos: List[str] = field(default_factory=list)


def _orc_servico(ctx: _Ctx, s: Servico, mult: float, usados: Dict[str, float], zera_ctx: bool,
                 visitados: Tuple[int, ...], fora: bool, zerado_proprio: bool, raiz: int,
                 caminho: str, out: List[LinhaOrcamento]):
    c, cat = ctx.c, ctx.cat
    b = base(s, c)
    val = 0.0 if (fora or zerado_proprio) else r2(b * mult)
    tipo = "servico" if len(visitados) == 1 else "subservico"
    out.append(LinhaOrcamento(tipo, s.id, s.nome, caminho, mult, mult, mult, b, val, 0.0,
                              motivo=(PAI_FORA if fora and tipo == "subservico" else None) or
                              (ZERADO_EM_PACOTE if zerado_proprio else None), servico_raiz=raiz))
    zera = zera_ctx or pacote_fechado(s, c)
    for v in s.itens:
        obj = cat.item(v.tipo, v.id)
        if obj is None or v.tipo == "equipamento":
            continue
        cam = f"{caminho} > {obj.nome}"
        cfg = _cfg(c, v.tipo, v.id)
        utiliza = bool(cfg and cfg.utiliza)
        zerar = bool(cfg and cfg.zerar)
        motivo = PAI_FORA if fora else (None if utiliza else NAO_UTILIZA)
        comp = mult * v.quantidade
        if v.tipo == "subservico":
            if v.id in visitados:
                ctx.avisos.append(f"{cam}: ciclo cortado")
                continue
            pos = len(out)
            _orc_servico(ctx, obj, comp, usados, zera, visitados + (v.id,), motivo is not None,
                         motivo is None and zera and zerar, raiz, cam, out)
            if motivo == NAO_UTILIZA:
                out[pos].motivo = NAO_UTILIZA  # a linha do próprio subserviço
            continue
        usada = usados.get(f"{v.tipo}:{v.id}", comp)
        preco = valor_produto(obj, c) if v.tipo == "produto" else valor_taxa(obj, c)
        embute = comp > 0 and zera and zerar and motivo is None
        if motivo is not None:
            cobrada, vl = 0.0, 0.0  # sem Utiliza: linha a R$ 0,00 (custo conta)
        else:
            cobrada = max(0.0, usada - comp) if embute else usada
            vl = r2(cobrada * preco.valor)
        custo, sc_, sp = 0.0, False, False
        if v.tipo == "produto":
            sc_ = _sem_custo(obj)
            custo = 0.0 if sc_ else r2(usada * obj.custo)
            sp = utiliza and not fora and preco.sem_preco
        out.append(LinhaOrcamento(v.tipo, v.id, obj.nome, cam, comp, usada, cobrada, preco.valor, vl, custo,
                                  sc_, sp, motivo or (ZERADO_EM_PACOTE if embute else None), raiz))


def orcamento(cat: Catalogo, c: Convenio, pedido: List[dict]) -> ResultadoOrcamento:
    """Orçamento (regra transacional 2.5) + Farol consolidado (2.7).

    ``pedido``: lista de ``{"tipo": "servico"|"produto"|"taxa", "id": N,
    "quantidade": 1, "usados": {"produto:10": 2}}``. ``usados`` informa a
    quantidade realmente usada de um item da composição (padrão = a da
    composição). Produto/taxa avulsos entram pelo preço do convênio.
    """
    ctx = _Ctx(cat, c)
    if not c.pago_no_ato:
        ctx.avisos.append("orçamento só existe para convênio 'Pago no ato do atendimento' (conta feita mesmo assim)")
    linhas: List[LinhaOrcamento] = []
    for item in pedido:
        tipo, id_, q = item.get("tipo", "servico"), int(item["id"]), float(item.get("quantidade", 1))
        if tipo == "servico":
            s = cat.servicos[id_]
            sc = c.servicos.get(id_)
            if not (sc and sc.utiliza):
                ctx.avisos.append(f"serviço {s.nome}: convênio não Utiliza — a tela não o ofereceria")
            _orc_servico(ctx, s, q, item.get("usados", {}), False, (id_,), False, False, id_, s.nome, linhas)
            continue
        obj = cat.item(tipo, id_)
        cfg = _cfg(c, tipo, id_)
        utiliza = bool(cfg and cfg.utiliza)
        preco = valor_produto(obj, c) if tipo == "produto" else valor_taxa(obj, c)
        vl = r2(q * preco.valor) if utiliza else 0.0
        custo, sc_ = 0.0, False
        if tipo == "produto":
            sc_ = _sem_custo(obj)
            custo = 0.0 if sc_ else r2(q * obj.custo)
        linhas.append(LinhaOrcamento(tipo, id_, obj.nome, obj.nome, q, q, q if utiliza else 0.0, preco.valor, vl,
                                     custo, sc_, utiliza and preco.sem_preco,
                                     None if utiliza else NAO_UTILIZA, None))
    partes = [Parte(l.valor, l.custo, l.sem_custo, l.sem_preco, l.tipo == "produto") for l in linhas]
    cons = farol_consolidado(partes, c)
    por_serv: Dict[int, Dict[str, object]] = {}
    for sid in dict.fromkeys(l.servico_raiz for l in linhas if l.servico_raiz is not None):
        ls = [l for l in linhas if l.servico_raiz == sid]
        por_serv[sid] = farol_consolidado(
            [Parte(l.valor, l.custo, l.sem_custo, l.sem_preco, l.tipo == "produto") for l in ls], c)
    return ResultadoOrcamento(linhas, cons["receita"], cons["custo"], cons["indice"], cons["farol"],
                              por_serv, ctx.avisos)


# ---------------------------------------------------------------------------
# Circularidade e invariantes
# ---------------------------------------------------------------------------

def detectar_ciclos(cat: Catalogo) -> List[List[int]]:
    """Lista ciclos de subserviços (A contém B que contém A). Cada ciclo é a lista de ids."""
    ciclos, vistos = [], set()

    def dfs(sid, caminho):
        s = cat.servicos.get(sid)
        if s is None:
            return
        for v in s.itens:
            if v.tipo != "subservico":
                continue
            if v.id in caminho:
                ciclo = caminho[caminho.index(v.id):] + [v.id]
                chave = frozenset(ciclo)
                if chave not in vistos:
                    vistos.add(chave)
                    ciclos.append(ciclo)
                continue
            dfs(v.id, caminho + [v.id])

    for sid in sorted(cat.servicos):
        dfs(sid, [sid])
    return ciclos


@dataclass
class Achado:
    codigo: str  # I1..I13, CICLO, ZERAR_SEM_PACOTE...
    nivel: str  # ERRO | AVISO
    item: str
    mensagem: str


def _iter_comp(cat: Catalogo, s: Servico, visit=()):
    """Todos os vínculos (tipo, id) da árvore de s, com o serviço pai."""
    for v in s.itens:
        yield s, v
        if v.tipo == "subservico" and v.id not in visit and v.id in cat.servicos:
            yield from _iter_comp(cat, cat.servicos[v.id], visit + (s.id,))


def validar_invariantes(cat: Catalogo, c: Convenio) -> List[Achado]:
    """Invariantes I1–I13 que dá para checar só com catálogo + configuração."""
    out: List[Achado] = []
    for ciclo in detectar_ciclos(cat):
        out.append(Achado("CICLO", "ERRO", " > ".join(map(str, ciclo)), "subserviços em ciclo"))
    # I4 — 0,01
    for nome_aba, aba in (("servico", c.servicos), ("produto", c.produtos), ("taxa", c.taxas)):
        for cfg in aba.values():
            if cfg.valor_convertido is not None and abs(cfg.valor_convertido - 0.01) < 1e-9:
                out.append(Achado("I4", "ERRO", f"{nome_aba} {cfg.id}",
                                  "valor 0,01 — marcador antigo de 'sem valor'. Deixe vazio (ou confirme preço simbólico)"))
    # I5 — produto utilizado sem custo
    for pid, cfg in c.produtos.items():
        p = cat.produtos.get(pid)
        if cfg.utiliza and p is not None and _sem_custo(p):
            out.append(Achado("I5", "AVISO", f"produto {p.nome}", "utilizado sem custo → Farol roxo"))
    pais_com_pacote = set()
    for sid, s in cat.servicos.items():
        sc = c.servicos.get(sid)
        if sc and sc.utiliza and pacote_fechado(s, c):
            pais_com_pacote.add(sid)
    # itens em algum pacote fechado (direto ou em ancestral)
    em_pacote = set()

    def marcar(s, dentro, visit=()):
        dentro = dentro or s.id in pais_com_pacote
        for v in s.itens:
            if dentro:
                em_pacote.add((v.tipo, v.id))
            if v.tipo == "subservico" and v.id in cat.servicos and v.id not in visit:
                marcar(cat.servicos[v.id], dentro, visit + (s.id,))
    for sid in pais_com_pacote:
        marcar(cat.servicos[sid], True)
    for sid, s in sorted(cat.servicos.items()):
        sc = c.servicos.get(sid)
        if not (sc and sc.utiliza):
            continue
        nome = f"serviço {s.nome}"
        # I1
        for pai, v in _iter_comp(cat, s):
            if v.tipo == "equipamento":
                continue
            cfg = _cfg(c, v.tipo, v.id)
            if not (cfg and cfg.utiliza):
                out.append(Achado("I1", "AVISO", f"{nome} > {v.tipo} {v.id}",
                                  "item da composição sem Utiliza (custo sem receita). Confirme que o convênio não cobre"))
        # I7
        if s.somar_itens and (s.valor_cadastro or 0) != 0:
            out.append(Achado("I7", "AVISO", nome, "soma itens com Valor do cadastro ≠ 0"))
        r = calcular_servico(cat, c, sid)
        # I8
        if s.somar_itens and sc.valor_convertido is None and not any(
                l.conta for l in r.arvore.filhos if l.tipo in ("produto", "taxa", "subservico")):
            out.append(Achado("I8", "AVISO", nome, "soma itens sem nenhum item que conta e sem valor convertido"))
        tem_comp = any(v.tipo != "equipamento" for v in s.itens)
        # I9
        if not s.somar_itens and tem_comp and not sc.pacote:
            out.append(Achado("I9", "AVISO", nome,
                              "preço fixo com composição e sem Pacote: os itens entram por cima. Confirme com a clínica"))
        # I12
        if sc.valor_convertido is not None and not sc.pacote and tem_comp:
            if any((_cfg(c, v.tipo, v.id) or ConfigItem(id=0)).zerar for _, v in _iter_comp(cat, s)):
                out.append(Achado("I12", "AVISO", nome,
                                  "valor combinado não é pacote: há itens com Zerar mas o serviço não tem Pacote"))
        # Pacote sem efeito
        if sc.pacote and s.somar_itens and sc.valor_convertido is None:
            out.append(Achado("PACOTE_SEM_EFEITO", "AVISO", nome,
                              "Pacote marcado em serviço que soma itens sem valor convertido: não muda nada"))
        # I2 parcial
        if pacote_fechado(s, c) and tem_comp and not any(
                (_cfg(c, v.tipo, v.id) or ConfigItem(id=0)).zerar for _, v in _iter_comp(cat, s)):
            out.append(Achado("I2", "AVISO", nome, "pacote fechado sem nenhum item com Zerar: tudo é cobrado por cima"))
        # I10
        if pacote_fechado(s, c):
            for pai, v in _iter_comp(cat, s):
                cfg = _cfg(c, v.tipo, v.id)
                if v.tipo == "subservico" and cfg and cfg.zerar and cfg.utiliza:
                    sub = cat.servicos.get(v.id)
                    if sub and any(not (_cfg(c, w.tipo, w.id) or ConfigItem(id=0)).zerar
                                   for w in sub.itens if w.tipo in ("produto", "taxa")):
                        out.append(Achado("I10", "AVISO", f"{nome} > {sub.nome}",
                                          "subserviço zerado com itens sem Zerar: esses itens continuam cobrados"))
        # I3 heurística
        if sc.valor_convertido is not None:
            for v in s.itens:
                cfg = _cfg(c, v.tipo, v.id)
                if v.tipo == "subservico" and cfg and cfg.utiliza and cfg.valor_convertido is not None \
                        and abs(cfg.valor_convertido - sc.valor_convertido) < 0.005 and cfg.valor_convertido > 0:
                    out.append(Achado("I3", "AVISO", nome, f"mesmo valor na raiz e no subserviço {v.id}: receita em dobro?"))
        # I6 / I11 / I13 — coerência interna do cálculo
        soma = sum(r.receita_por_tipo.values())
        if abs(soma - r.total) > 0.011:
            out.append(Achado("I6", "ERRO", nome, f"receita {r.total} ≠ serviços+produtos+taxas {soma}"))
    # zerar sem pacote acima (vale para todo o convênio)
    for tipo, aba in (("produto", c.produtos), ("taxa", c.taxas), ("subservico", c.servicos)):
        for cfg in aba.values():
            if cfg.zerar and (tipo, cfg.id) not in em_pacote and any(
                    (v.tipo, v.id) == (tipo, cfg.id) for s in cat.servicos.values() for v in s.itens):
                out.append(Achado("ZERAR_SEM_PACOTE", "AVISO", f"{tipo} {cfg.id}",
                                  "Zerar marcado, mas o item não está em nenhum pacote fechado: não tem efeito"))
    return out
