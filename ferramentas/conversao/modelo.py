"""Modelo de dados do motor de conversão de valores (preços por convênio).

Fonte: manual oficial, Preços e Conversão de Valores
(https://www.rabisistemas.com.br/manual/precos/guia-ia.html#algoritmo e
https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#tabela-mestra).
Conferido em 2026-09-25 · Kit v0.1.0.

Regra de ouro representada aqui: **vazio ≠ zero**.
Todo campo "convertido" é ``Optional``: ``None`` = vazio (desce de nível);
``0.0`` = zero de verdade (não desce).

Os três níveis:
  nível 3 = o item dentro do convênio (``ConfigItem``, linha 🔁);
  nível 2 = política do convênio por tipo de produto (``PoliticaTipoProduto``;
            só vale para o preço de produto);
  nível 1 = catálogo (``Servico``, ``Produto``, ``Taxa``, linha 🔒).
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional

# Tipos de vínculo aceitos na composição de um serviço.
TIPOS_VINCULO = ("produto", "taxa", "subservico", "equipamento")

# Fontes de preço de produto (nomes como aparecem na tela).
FONTE_FIXO = "PRECO FIXO CADASTRADO"
FONTE_ULTIMA_COMPRA = "PRECO DA ULTIMA COMPRA"
FONTE_ULTIMA_PESQUISA = "PRECO DA ULTIMA PESQUISA"
FONTE_MEDIO = "PRECO MEDIO DE COMPRA"
FONTES_FIXAS = (FONTE_FIXO, FONTE_ULTIMA_COMPRA, FONTE_ULTIMA_PESQUISA, FONTE_MEDIO)
# Qualquer outro nome de fonte = tabela de preços interna (Preço 1/2/3).

TIPOS_PRECIFICACAO = ("PRECO_1", "PRECO_2", "PRECO_3")


def _opt_float(v) -> Optional[float]:
    """Converte para float preservando vazio. '' e None viram None; 0 fica 0.0."""
    if v is None:
        return None
    if isinstance(v, str):
        s = v.strip()
        if s == "":
            return None
        if "," in s:
            s = s.replace(".", "").replace(",", ".")
        return float(s)
    return float(v)


def _opt_str(v) -> Optional[str]:
    """Texto em branco conta como vazio (desce de nível)."""
    if v is None:
        return None
    s = str(v)
    return s if s.strip() != "" else None


@dataclass
class Vinculo:
    """Um item da composição de um serviço (aba Produtos/Taxas/Servicos/Equipamentos)."""
    tipo: str  # produto | taxa | subservico | equipamento
    id: int
    quantidade: float = 1.0

    def __post_init__(self):
        if self.tipo == "servico":
            self.tipo = "subservico"
        if self.tipo not in TIPOS_VINCULO:
            raise ValueError(f"tipo de vínculo inválido: {self.tipo!r}")


@dataclass
class Servico:
    """Serviço do catálogo (Configurações › Serviços)."""
    id: int
    nome: str
    valor_cadastro: float = 0.0
    somar_itens: bool = False  # "Definir preço do serviço pelos itens"
    itens: List[Vinculo] = field(default_factory=list)
    ativo: bool = True
    descricao: Optional[str] = None
    codigo: Optional[str] = None
    codigo_tuss: Optional[str] = None
    tipo_codigo: Optional[int] = None
    tabela87: Optional[int] = None
    tipo_atendimento: Optional[int] = None


@dataclass
class Produto:
    """Produto do catálogo (Estoque › Produtos; preço e custo na aba Estoque)."""
    id: int
    nome: str
    tipo_produto: Optional[str] = None
    custo: Optional[float] = None  # custo unitário para o Farol; None = sem custo (roxo)
    preco_venda_tabela: Optional[float] = None  # "Preço de venda tabela"
    fonte_preco: Optional[str] = None  # nome da fonte (FONTES_FIXAS) ou nome da tabela interna
    tipo_precificacao: Optional[str] = None  # PRECO_1 | PRECO_2 | PRECO_3
    fator_k: Optional[float] = None  # percentual (15 = +15%)
    ultima_compra: Optional[float] = None
    ultima_pesquisa: Optional[float] = None
    preco_medio: Optional[float] = None
    # valores do produto nas tabelas internas: {nome_tabela: {PRECO_1: v, ...}}
    precos_tabela: Dict[str, Dict[str, float]] = field(default_factory=dict)
    # código do produto em cada tabela de fonte de preço: {nome_tabela: codigo}
    codigos_tabela: Dict[str, str] = field(default_factory=dict)
    ativo: bool = True
    descricao: Optional[str] = None
    codigo: Optional[str] = None
    tipo_codigo: Optional[int] = None
    tabela87: Optional[int] = None


@dataclass
class Taxa:
    """Taxa do catálogo (Configurações › Taxas). Sem Fator K, sem política, sem custo."""
    id: int
    nome: str
    valor_cadastro: float = 0.0
    ativo: bool = True
    descricao: Optional[str] = None
    codigo: Optional[str] = None
    tipo_codigo: Optional[int] = None
    tabela87: Optional[int] = None


@dataclass
class ConfigItem:
    """Item dentro do convênio (nível 3, linha 🔁). Um por serviço/produto/taxa.

    ``utiliza`` nasce ``False`` (padrão de vínculo novo). ``pacote`` só existe
    para serviço. ``zerar`` é por item × convênio (não por vínculo).
    """
    id: int
    utiliza: bool = False
    valor_convertido: Optional[float] = None  # None = vazio; 0.0 = zero de verdade
    pacote: bool = False
    zerar: bool = False
    fator_k: Optional[float] = None  # só produto
    fonte_preco: Optional[str] = None  # só produto
    tipo_precificacao: Optional[str] = None  # só produto
    nome: Optional[str] = None
    descricao: Optional[str] = None
    codigo: Optional[str] = None  # código no convênio (nível 3)
    codigo_convenio: Optional[str] = None  # só serviço: "código do convênio"
    tipo_codigo: Optional[int] = None
    tabela87: Optional[int] = None
    tipo_atendimento: Optional[int] = None  # só serviço
    parcelas: Optional[int] = None  # só serviço
    autorizacao_previa: Optional[bool] = None
    retorno: Optional[bool] = None


@dataclass
class PoliticaTipoProduto:
    """Nível 2: Política de Preço por Tipo de Produto (Dados do convênio)."""
    tipo_produto: str
    fonte_preco: Optional[str] = None
    tipo_precificacao: Optional[str] = None
    fator_k: Optional[float] = None
    ativa: bool = True


@dataclass
class Convenio:
    id: int
    nome: str
    servicos: Dict[int, ConfigItem] = field(default_factory=dict)
    produtos: Dict[int, ConfigItem] = field(default_factory=dict)
    taxas: Dict[int, ConfigItem] = field(default_factory=dict)
    politicas: Dict[str, PoliticaTipoProduto] = field(default_factory=dict)
    limite_parcelas: Optional[int] = None
    pago_no_ato: bool = False
    parametro_vermelho: float = 100.0  # Configurações › Parâmetros › Valores
    parametro_amarelo: float = 120.0


@dataclass
class Catalogo:
    servicos: Dict[int, Servico] = field(default_factory=dict)
    produtos: Dict[int, Produto] = field(default_factory=dict)
    taxas: Dict[int, Taxa] = field(default_factory=dict)

    def item(self, tipo: str, id_: int):
        if tipo == "produto":
            return self.produtos.get(id_)
        if tipo == "taxa":
            return self.taxas.get(id_)
        if tipo in ("subservico", "servico"):
            return self.servicos.get(id_)
        return None


# ---------------------------------------------------------------------------
# Leitura de cenário JSON (ver exemplos/cenario-convenio-a.json)
# ---------------------------------------------------------------------------

def _config_from_dict(d: dict) -> ConfigItem:
    return ConfigItem(
        id=int(d["id"]),
        utiliza=bool(d.get("utiliza", False)),
        valor_convertido=_opt_float(d.get("valor_convertido")),
        pacote=bool(d.get("pacote", False)),
        zerar=bool(d.get("zerar", False)),
        fator_k=_opt_float(d.get("fator_k")),
        fonte_preco=_opt_str(d.get("fonte_preco")),
        tipo_precificacao=_opt_str(d.get("tipo_precificacao")),
        nome=_opt_str(d.get("nome")),
        descricao=_opt_str(d.get("descricao")),
        codigo=_opt_str(d.get("codigo")),
        codigo_convenio=_opt_str(d.get("codigo_convenio")),
        tipo_codigo=d.get("tipo_codigo"),
        tabela87=d.get("tabela87"),
        tipo_atendimento=d.get("tipo_atendimento"),
        parcelas=d.get("parcelas"),
        autorizacao_previa=d.get("autorizacao_previa"),
        retorno=d.get("retorno"),
    )


def catalogo_from_dict(d: dict) -> Catalogo:
    cat = Catalogo()
    for s in d.get("servicos", []):
        itens = [Vinculo(i["tipo"], int(i["id"]), float(i.get("quantidade", 1))) for i in s.get("itens", [])]
        cat.servicos[int(s["id"])] = Servico(
            id=int(s["id"]), nome=s["nome"], valor_cadastro=float(s.get("valor_cadastro", 0) or 0),
            somar_itens=bool(s.get("somar_itens", False)), itens=itens, ativo=bool(s.get("ativo", True)),
            descricao=s.get("descricao"), codigo=s.get("codigo"), codigo_tuss=s.get("codigo_tuss"),
            tipo_codigo=s.get("tipo_codigo"), tabela87=s.get("tabela87"),
            tipo_atendimento=s.get("tipo_atendimento"))
    for p in d.get("produtos", []):
        cat.produtos[int(p["id"])] = Produto(
            id=int(p["id"]), nome=p["nome"], tipo_produto=p.get("tipo_produto"),
            custo=_opt_float(p.get("custo")), preco_venda_tabela=_opt_float(p.get("preco_venda_tabela")),
            fonte_preco=_opt_str(p.get("fonte_preco")), tipo_precificacao=_opt_str(p.get("tipo_precificacao")),
            fator_k=_opt_float(p.get("fator_k")), ultima_compra=_opt_float(p.get("ultima_compra")),
            ultima_pesquisa=_opt_float(p.get("ultima_pesquisa")), preco_medio=_opt_float(p.get("preco_medio")),
            precos_tabela={k: {kk: float(vv) for kk, vv in v.items()} for k, v in (p.get("precos_tabela") or {}).items()},
            codigos_tabela=dict(p.get("codigos_tabela") or {}), ativo=bool(p.get("ativo", True)),
            descricao=p.get("descricao"), codigo=p.get("codigo"), tipo_codigo=p.get("tipo_codigo"),
            tabela87=p.get("tabela87"))
    for t in d.get("taxas", []):
        cat.taxas[int(t["id"])] = Taxa(
            id=int(t["id"]), nome=t["nome"], valor_cadastro=float(t.get("valor_cadastro", 0) or 0),
            ativo=bool(t.get("ativo", True)), descricao=t.get("descricao"), codigo=t.get("codigo"),
            tipo_codigo=t.get("tipo_codigo"), tabela87=t.get("tabela87"))
    return cat


def convenio_from_dict(d: dict) -> Convenio:
    c = Convenio(
        id=int(d.get("id", 0)), nome=d.get("nome", ""),
        limite_parcelas=d.get("limite_parcelas"), pago_no_ato=bool(d.get("pago_no_ato", False)),
        parametro_vermelho=float(d.get("parametro_vermelho", 100)),
        parametro_amarelo=float(d.get("parametro_amarelo", 120)))
    for k in ("servicos", "produtos", "taxas"):
        alvo = getattr(c, k)
        for item in d.get(k, []):
            cfg = _config_from_dict(item)
            alvo[cfg.id] = cfg
    for p in d.get("politicas", []):
        c.politicas[p["tipo_produto"]] = PoliticaTipoProduto(
            tipo_produto=p["tipo_produto"], fonte_preco=_opt_str(p.get("fonte_preco")),
            tipo_precificacao=_opt_str(p.get("tipo_precificacao")), fator_k=_opt_float(p.get("fator_k")),
            ativa=bool(p.get("ativa", True)))
    return c


def cenario_from_dict(d: dict):
    """Lê ``{"catalogo": {...}, "convenio": {...}}`` e devolve (Catalogo, Convenio)."""
    return catalogo_from_dict(d.get("catalogo", {})), convenio_from_dict(d.get("convenio", {}))


def para_dict(obj) -> dict:
    return asdict(obj)
