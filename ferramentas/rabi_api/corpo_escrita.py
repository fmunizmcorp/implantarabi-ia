"""Monta o corpo dos PUT de /servicos e /produtos (e o corpo PARCIAL das rotas parciais).

Dois modos, conforme a rota (conhecimento/api-externa/convencoes.md §4):

1) PARCIAL — `corpo_parcial(recurso, mudancas, leitura=None)`: rotas que o Rabi declara parciais
   desde 01–02/10/2026 (rabi-api `7d16cd50`/`49362b61`): servicos, convenios, pacientes (+ carteira),
   colaboradores, grades, orcamentos, movimentações, guias, contas-caixa. Campo omitido MANTÉM;
   `null` LIMPA; lista omitida mantém; lista enviada SUBSTITUI (`[]` apaga). Aqui o corpo leva SÓ o
   que muda; listas vazias são recusadas sem `permitir_lista_vazia`; `null` e listas aparecem em
   `resumo_parcial()` para a prévia. É o modo padrão do kit nessas rotas.

2) COMPLETO — `corpo_put_servico` / `corpo_put_produto`: GET → corpo completo do schema de escrita.
   Obrigatório em /produtos (o PUT de produto não declara parcial = sobrescreve) e útil em /servicos
   quando se quer reenviar o cadastro inteiro. A leitura usa nomes diferentes da escrita:
   - serviço: `somarItens` (leitura) × `somarItems` (escrita); objetos aninhados × IDs;
   - produto: `permitirEstoqueNegativo` × `estoquePodeNegativar`; `Fabricante`/`TipoProduto`/… × ids.
   TODO campo do schema de escrita (`ServicoCreate` / `ProdutoCreate`) tem de ser resolvido — pela
   leitura ou por `complementos` (`None` explícito = limpar). Faltou algum → `CampoDeEscritaAusente`.

Forma REAL da leitura:
- `GET /servicos/{id}` (desde 13/10/2026, Swagger 22/11): traz tudo com os nomes do PUT —
  `documentos` ([{id}]), `produtoIds` (id ou {id, quantidade, valorUnitario em reais}),
  `equipamentoIds`, `servicoTaxa` ([{taxaId, quantidade}]), `especialidadesId`,
  `servicosRelacionados` ([{servicoId, quantidade}], também `composicao`), `somarItems`/`somarItens`,
  `tipoAtendimento`, `perfilFiscalId`. "Ler e reenviar sem alterar não muda nada." Leituras antigas
  (25–28/09, sem produtos/taxas/equipamentos) seguem aceitas com `complementos`.
- Produto da composição enviado SEM `valorUnitario` mantém o valor que já tinha (desde 02/10).
- `GET /produtos/{id}` traz `Fabricante`, `TipoProduto`, `UnidadeDeMedida` e `deposito` aninhados;
  não traz princípio ativo, CD, tipo de código, tabela 87, última pesquisa, fornecedores nem anexos.
- Produto (02/10): `codigoEAN` texto 8/12/13/14 dígitos, `codigoNCM` texto 8 dígitos (número perde
  zero à esquerda), `codigoProduto` até 10 caracteres (letras, números, `. - /`). Validado aqui.

Colaborador: desde 13/10 o GET traz `perguntasIds`, `vinculoRepasse` e `mensagem` no formato do PUT,
e o PUT é parcial — use `corpo_parcial("colaboradores", ...)` com só o que muda.

Uso:
    from ferramentas.rabi_api.corpo_escrita import corpo_parcial, resumo_parcial
    atual = c.get("/servicos/46")
    corpo = corpo_parcial("servicos", {"valor": 40.0}, leitura=atual)   # {"valor": 40.0}
    print(resumo_parcial(corpo))                                         # vai na prévia
    c.put("/servicos/46", corpo)
"""
from __future__ import annotations

from typing import Any, Callable, Iterable

# Campos do schema de escrita (conferidos contra o spec pelo teste test_corpo_escrita.py).
CAMPOS_SERVICO = (
    "nome", "descricao", "codigo", "codigoTUSS", "valor", "tempoServico", "somarItems",
    "linkAuxiliar", "preparamentos", "preparo", "tipoServicoId", "tipoCodigoId", "tipoGuiaId",
    "tabelaANS87ID", "regimeDeAtendimentoId", "tipoAtendimento", "servicoTaxa",
    "especialidadesId", "produtoIds", "equipamentoIds",
    "servicosRelacionados", "habilitarAgendamentoOnline", "apenasComColaboradorDesignado",
    "documentos", "perfilFiscalId",
)
OBRIGATORIOS_SERVICO = ("nome", "descricao")
# Campos novos (13/10/2026) que leituras antigas não trazem: como o PUT de serviço é parcial,
# omiti-los MANTÉM o valor atual — no modo completo, ficam fora do corpo em vez de dar erro.
OMITIVEIS_SERVICO = ("documentos", "perfilFiscalId")

CAMPOS_PRODUTO = (
    "nome", "codigoProduto", "codigoEAN", "codigoNCM", "apresentacao", "contendo", "depositoId",
    "tipoProdutoId", "fabricanteId", "principioAtivoId", "unidadeDeMedidaId", "cdId",
    "tipoCodigoId", "tabelaANS87ID", "estoquePodeNegativar", "prazoDeReposicao",
    "precoUltimaPesquisa", "dataUltimaPesquisa", "fornecedores", "anexos",
)
OBRIGATORIOS_PRODUTO = (
    "nome", "codigoProduto", "apresentacao", "contendo", "depositoId", "tipoProdutoId",
    "fabricanteId", "unidadeDeMedidaId", "prazoDeReposicao",
)

_AUSENTE = object()


class CampoDeEscritaAusente(ValueError):
    """Algum campo do corpo de escrita não pôde ser resolvido (ou veio inválido)."""

    def __init__(self, recurso: str, faltam: list[str], problemas: list[str] | None = None):
        self.recurso, self.faltam, self.problemas = recurso, list(faltam), list(problemas or [])
        partes = []
        if self.faltam:
            partes.append(
                f"PUT de {recurso}: a leitura não traz {len(self.faltam)} campo(s) que a escrita "
                f"exige: {', '.join(self.faltam)}. No modo completo, omitir apagaria (produto) ou "
                "deixaria o corpo incompleto. Informe-os "
                "em `complementos` (valor do cadastro do repo; `None` explícito só se for para limpar)."
            )
        partes += self.problemas
        super().__init__(" ".join(partes))


def _desembrulhar(leitura: Any) -> dict:
    if isinstance(leitura, dict) and isinstance(leitura.get("dados"), dict):
        return leitura["dados"]
    if isinstance(leitura, dict) and isinstance(leitura.get("data"), dict):
        return leitura["data"]
    if not isinstance(leitura, dict):
        raise TypeError("leitura precisa ser o objeto (dict) devolvido pelo GET do item")
    return leitura


# ---------- resolvedores: cada um devolve o valor ou _AUSENTE ----------

def _direto(*nomes: str) -> Callable[[dict], Any]:
    def r(d: dict) -> Any:
        for n in nomes:
            if n in d:
                return d[n]
        return _AUSENTE
    return r


def _id_de(*nomes: str) -> Callable[[dict], Any]:
    """Campo que pode vir como id (int/str) ou como objeto aninhado {id, ...}."""
    def r(d: dict) -> Any:
        for n in nomes:
            if n not in d:
                continue
            v = d[n]
            if v is None or isinstance(v, (int, str)):
                return v
            if isinstance(v, dict):
                if "id" in v:
                    return v["id"]
                raise CampoDeEscritaAusente("?", [], [f"'{n}' veio como objeto sem 'id': {sorted(v)}"])
            raise CampoDeEscritaAusente("?", [], [f"'{n}' em formato inesperado: {type(v).__name__}"])
        return _AUSENTE
    return r


def _item_para_id(el: Any, chave_id: str, aninhados: Iterable[str], origem: str) -> Any:
    if isinstance(el, (int, str)):
        return el
    if not isinstance(el, dict):
        raise CampoDeEscritaAusente("?", [], [f"item de '{origem}' em formato inesperado: {el!r}"])
    if chave_id in el:
        return el[chave_id]
    for a in aninhados:
        sub = el.get(a)
        if isinstance(sub, dict) and "id" in sub:
            return sub["id"]
    outros_ids = [k for k in el if k != "id" and k.endswith("Id")]
    if "id" in el and not outros_ids:
        return el["id"]  # o próprio objeto da entidade
    raise CampoDeEscritaAusente(
        "?", [], [f"item de '{origem}' é ambíguo (linha de vínculo sem '{chave_id}'): chaves {sorted(el)}"])


def _lista_ids(chaves: Iterable[str], chave_id: str, aninhados: Iterable[str]) -> Callable[[dict], Any]:
    def r(d: dict) -> Any:
        for n in chaves:
            if n not in d:
                continue
            v = d[n]
            if v is None:
                return []
            if not isinstance(v, list):
                raise CampoDeEscritaAusente("?", [], [f"'{n}' deveria ser lista: {type(v).__name__}"])
            return [_item_para_id(el, chave_id, aninhados, n) for el in v]
        return _AUSENTE
    return r


def _lista_objetos(chaves: Iterable[str], chave_id: str, aninhados: Iterable[str],
                   chaves_id_alternativas: Iterable[str] = ()) -> Callable[[dict], Any]:
    """Lista de vínculos com QUANTIDADE ({<chave_id>, quantidade}); preserva a quantidade lida.

    Desde 28/09/2026 a API externa aceita ID puro ou objeto em `servicosRelacionados` e
    `servicoTaxa` — reduzir a ID perderia a quantidade (viraria 1)."""
    alternativas = tuple(chaves_id_alternativas)

    def r(d: dict) -> Any:
        for n in chaves:
            if n not in d:
                continue
            v = d[n]
            if v is None:
                return []
            if isinstance(v, dict):  # formato antigo: um só vínculo (ex.: taxaServico: {id, ...})
                v = [v]
            if not isinstance(v, list):
                raise CampoDeEscritaAusente("?", [], [f"'{n}' deveria ser lista: {type(v).__name__}"])
            saida = []
            for el in v:
                if isinstance(el, (int, str)):
                    saida.append({chave_id: el, "quantidade": 1})
                    continue
                if not isinstance(el, dict):
                    raise CampoDeEscritaAusente("?", [], [f"item de '{n}' em formato inesperado: {el!r}"])
                ident = next((el[k] for k in (chave_id, *alternativas) if k in el), None)
                if ident is None:
                    for a in aninhados:
                        sub = el.get(a)
                        if isinstance(sub, dict) and "id" in sub:
                            ident = sub["id"]
                            break
                if ident is None and "id" in el and not [k for k in el if k != "id" and k.endswith("Id")]:
                    ident = el["id"]  # o próprio objeto da entidade
                if ident is None:
                    raise CampoDeEscritaAusente(
                        "?", [], [f"item de '{n}' sem '{chave_id}': chaves {sorted(el)}"])
                saida.append({chave_id: ident, "quantidade": el.get("quantidade", 1)})
            return saida
        return _AUSENTE
    return r


def _lista_produtos(chaves: Iterable[str]) -> Callable[[dict], Any]:
    """`produtoIds`: id puro, ou {id, quantidade, valorUnitario} — preserva quantidade e valor lidos.

    Itens que vêm como id puro (ou como linha de vínculo sem quantidade/valor) saem como id puro,
    como antes; itens com quantidade ≠ 1 ou `valorUnitario` saem como objeto (reduzir a id faria a
    quantidade voltar a 1)."""
    ids = _lista_ids(chaves, "produtoId", ("produto", "Produto"))

    def r(d: dict) -> Any:
        for n in chaves:
            if n not in d:
                continue
            v = d[n]
            if v is None:
                return []
            if not isinstance(v, list):
                raise CampoDeEscritaAusente("?", [], [f"'{n}' deveria ser lista: {type(v).__name__}"])
            base = ids({n: v})
            saida = []
            for el, ident in zip(v, base):
                extra = {}
                if isinstance(el, dict):
                    if el.get("quantidade") not in (None, 1):
                        extra["quantidade"] = el["quantidade"]
                    if el.get("valorUnitario") is not None:
                        extra["valorUnitario"] = el["valorUnitario"]
                saida.append({"id": ident, **extra} if extra else ident)
            return saida
        return _AUSENTE
    return r


def _documentos(d: dict) -> Any:
    for n in ("documentos", "ServicoDocumento", "servicoDocumento"):
        if n not in d:
            continue
        v = d[n] or []
        return [{"id": _item_para_id(el, "documentoId", ("documento", "Documento"), n)} for el in v]
    return _AUSENTE


def _anexos(d: dict) -> Any:
    if "anexos" not in d:
        return _AUSENTE
    v = d["anexos"] or []
    return [{"nome": a.get("nome"), "caminhoArquivo": a.get("caminhoArquivo")} for a in v]


MAPA_SERVICO: dict[str, Callable[[dict], Any]] = {
    "nome": _direto("nome"),
    "descricao": _direto("descricao"),
    "codigo": _direto("codigo"),
    "codigoTUSS": _direto("codigoTUSS"),
    "valor": _direto("valor"),
    "tempoServico": _direto("tempoServico"),
    "somarItems": _direto("somarItems", "somarItens"),
    "linkAuxiliar": _direto("linkAuxiliar"),
    "preparamentos": _direto("preparamentos"),
    "preparo": _direto("preparo"),
    "tipoServicoId": _id_de("tipoServicoId", "tipoServico", "TipoServico"),
    "tipoCodigoId": _id_de("tipoCodigoId", "tipoCodigo", "TipoCodigo"),
    "tipoGuiaId": _id_de("tipoGuiaId", "tipoGuia", "TipoGuia"),
    "tabelaANS87ID": _id_de("tabelaANS87ID", "tabelaANS87Id", "tabelaANS87", "TabelaANS87"),
    "regimeDeAtendimentoId": _id_de("regimeDeAtendimentoId", "regimeDeAtendimento", "RegimeDeAtendimento"),
    "tipoAtendimento": _id_de("tipoAtendimento", "tipoAtendimentoId", "TipoAtendimento"),
    "servicoTaxa": _lista_objetos(("servicoTaxa", "TaxaServico", "taxaServico", "taxas"),
                                  "taxaId", ("taxa", "Taxa")),
    "especialidadesId": _lista_ids(
        ("especialidadesId", "ServicoEspecialidade", "servicoEspecialidade", "especialidades"),
        "especialidadeId", ("especialidade", "Especialidade")),
    "produtoIds": _lista_produtos(("produtoIds", "ServicoProduto", "servicoProduto", "produtos")),
    "equipamentoIds": _lista_ids(
        ("equipamentoIds", "ServicoEquipamento", "servicoEquipamento", "equipamentos"),
        "equipamentoId", ("equipamento", "Equipamento")),
    "servicosRelacionados": _lista_objetos(
        ("servicosRelacionados", "ServicoRelacionado", "servicoRelacionado", "composicao"),
        "servicoId", ("servicoRelacionado", "ServicoRelacionado", "servicoFilho"),
        chaves_id_alternativas=("servicoRelacionadoId", "servicoFilhoId")),
    "habilitarAgendamentoOnline": _direto("habilitarAgendamentoOnline"),
    "apenasComColaboradorDesignado": _direto("apenasComColaboradorDesignado"),
    "documentos": _documentos,
    "perfilFiscalId": _direto("perfilFiscalId"),
}

MAPA_PRODUTO: dict[str, Callable[[dict], Any]] = {
    "nome": _direto("nome"),
    "codigoProduto": _direto("codigoProduto"),
    "codigoEAN": _direto("codigoEAN"),
    "codigoNCM": _direto("codigoNCM"),
    "apresentacao": _direto("apresentacao"),
    "contendo": _direto("contendo"),
    "depositoId": _id_de("depositoId", "deposito", "Deposito"),
    "tipoProdutoId": _id_de("tipoProdutoId", "TipoProduto", "tipoProduto"),
    "fabricanteId": _id_de("fabricanteId", "Fabricante", "fabricante"),
    "principioAtivoId": _id_de("principioAtivoId", "PrincipioAtivo", "principioAtivo"),
    "unidadeDeMedidaId": _id_de("unidadeDeMedidaId", "UnidadeDeMedida", "unidadeDeMedida"),
    "cdId": _id_de("cdId", "cd", "Cd"),
    "tipoCodigoId": _id_de("tipoCodigoId", "tipoCodigo", "TipoCodigo"),
    "tabelaANS87ID": _id_de("tabelaANS87ID", "tabelaANS87Id", "tabelaANS87", "TabelaANS87"),
    "estoquePodeNegativar": _direto("estoquePodeNegativar", "permitirEstoqueNegativo"),
    "prazoDeReposicao": _direto("prazoDeReposicao"),
    "precoUltimaPesquisa": _direto("precoUltimaPesquisa"),
    "dataUltimaPesquisa": _direto("dataUltimaPesquisa"),
    "fornecedores": _lista_ids(
        ("fornecedores", "ProdutoFornecedor", "produtoFornecedor", "Fornecedores"),
        "fornecedorId", ("fornecedor", "Fornecedor")),
    "anexos": _anexos,
}


def _converter(recurso: str, leitura: Any, complementos: dict | None,
               campos: tuple, obrigatorios: tuple, mapa: dict, omitiveis: tuple = ()) -> dict:
    d = _desembrulhar(leitura)
    complementos = dict(complementos or {})
    desconhecidos = sorted(k for k in complementos if k not in campos)
    if desconhecidos:
        raise CampoDeEscritaAusente(recurso, [], [
            f"`complementos` tem nome(s) que não existem no schema de escrita de {recurso}: "
            f"{', '.join(desconhecidos)} (a API ignoraria e apagaria o campo certo; ex.: "
            "'somarItens' → 'somarItems')."])
    corpo: dict = {}
    faltam: list[str] = []
    problemas: list[str] = []
    for campo in campos:
        if campo in complementos:
            corpo[campo] = complementos[campo]
            continue
        try:
            v = mapa[campo](d)
        except CampoDeEscritaAusente as e:
            problemas += [f"{campo}: {p}" for p in e.problemas]
            continue
        if v is _AUSENTE:
            if campo not in omitiveis:
                faltam.append(campo)
        else:
            corpo[campo] = v
    for campo in obrigatorios:
        if campo in corpo and corpo[campo] in (None, ""):
            problemas.append(f"{campo} é obrigatório na escrita e está vazio.")
    if faltam or problemas:
        raise CampoDeEscritaAusente(recurso, faltam, problemas)
    return corpo


_RE_EAN = __import__("re").compile(r"^(\d{8}|\d{12,14})$")
_RE_NCM = __import__("re").compile(r"^\d{8}$")
_RE_COD = __import__("re").compile(r"^[A-Za-z0-9./-]{1,10}$")


def problemas_codigos_produto(corpo: dict) -> list[str]:
    """Regras de 02/10/2026 (rabi-api `f3b63493`): EAN e NCM como TEXTO, código do produto ≤ 10."""
    prob = []
    for campo, regra, texto in (("codigoEAN", _RE_EAN, "8, 12, 13 ou 14 dígitos"),
                                ("codigoNCM", _RE_NCM, "exatamente 8 dígitos")):
        v = corpo.get(campo)
        if v is None or v == "":
            continue
        if not isinstance(v, str):
            prob.append(f"{campo} deve ir como TEXTO com {texto} (número perde zero à esquerda): {v!r}")
        elif not regra.match(v):
            prob.append(f"{campo} inválido — precisa de {texto}: {v!r}")
    v = corpo.get("codigoProduto")
    if isinstance(v, str) and v and not _RE_COD.match(v):
        prob.append(f"codigoProduto até 10 caracteres (letras, números, ponto, hífen ou barra): {v!r}")
    return prob


def corpo_put_servico(leitura: dict, complementos: dict | None = None) -> dict:
    """GET /servicos/{id} → corpo completo do PUT /servicos/{id} (schema ServicoCreate)."""
    return _converter("servicos", leitura, complementos, CAMPOS_SERVICO, OBRIGATORIOS_SERVICO, MAPA_SERVICO,
                      OMITIVEIS_SERVICO)


def corpo_put_produto(leitura: dict, complementos: dict | None = None) -> dict:
    """GET /produtos/{id} → corpo completo do PUT /produtos/{id} (schema ProdutoCreate)."""
    corpo = _converter("produtos", leitura, complementos, CAMPOS_PRODUTO, OBRIGATORIOS_PRODUTO, MAPA_PRODUTO)
    prob = problemas_codigos_produto(corpo)
    if prob:
        raise CampoDeEscritaAusente("produtos", [], prob + [
            "Se o código veio assim da leitura (cadastro antigo), mande-o como texto em `complementos` "
            "(ex.: complementos={'codigoEAN': '07891234567895'}) — confirme o zero à esquerda no documento."])
    return corpo


# ---------------------------------------------------------------- modo PARCIAL
# Rotas que o Rabi declara parciais (Swagger 22/11/2026 + código deploy_prd). Nas demais, PUT completo.
RECURSOS_PARCIAIS = {
    "servicos", "convenios", "pacientes", "colaboradores", "grades-colaborador",
    "grades-equipamento", "orcamentos", "financeiro/movimentacoes", "faturamento/guias",
    "financeiro/contas-caixa", "pacientes/convenios",
}
# Leitura em CENTAVOS e escrita em REAIS (Swagger 22/11): comparar com o GET daria resultado errado
# (40 centavos ≠ R$ 40,00) — nesses recursos o corpo parcial NÃO é filtrado pela leitura.
RECURSOS_LEITURA_EM_CENTAVOS = {"orcamentos", "financeiro/movimentacoes", "faturamento/guias"}
# Nomes de leitura que a escrita de serviço NÃO aceita (mandar = a API ignora → mudança perdida).
_LEITURA_SERVICO = {"somarItens": "somarItems", "tipoServico": "tipoServicoId", "tipoCodigo": "tipoCodigoId",
                    "ServicoEspecialidade": "especialidadesId", "composicao": "servicosRelacionados"}
# Listas de convênio que, enviadas incompletas, desativam unidades / apagam políticas.
_LISTAS_SENSIVEIS = {"convenios": ("unidadesIds", "politicasPorTipoProduto")}


class CorpoParcialInvalido(ValueError):
    """O corpo parcial pedido tem campo desconhecido, nome de leitura, lista vazia sem permissão etc."""


def _igual(a: Any, b: Any) -> bool:
    """Igualdade estrita: mesmo tipo e mesmo valor (em Python True == 1 e 1 == 1.0)."""
    if isinstance(a, bool) or isinstance(b, bool) or type(a) is not type(b):
        if not (isinstance(a, (int, float)) and isinstance(b, (int, float))
                and not isinstance(a, bool) and not isinstance(b, bool)):
            return False
    return a == b


def corpo_parcial(recurso: str, mudancas: dict, leitura: Any = None,
                  permitir_lista_vazia: Iterable[str] = (), listas_conferidas: Iterable[str] = (),
                  permitir_objeto: Iterable[str] = ()) -> dict:
    """Corpo de PUT PARCIAL com só o que muda (convencoes.md §4.1).

    - `recurso` precisa estar em RECURSOS_PARCIAIS (produto, taxa, local… → use o modo completo);
    - em `servicos`, os nomes têm de ser os do schema de escrita (ex.: `somarItems`, não `somarItens`);
    - com `leitura` (o GET), tira do corpo o que já está igual — só vai o que de fato muda;
    - lista `[]` só passa se o campo estiver em `permitir_lista_vazia` (apaga TODOS os vínculos);
    - em convênio, `unidadesIds`/`politicasPorTipoProduto` só passam se estiverem em
      `listas_conferidas` (conferidos contra a régua: lista enviada é a lista completa) — mesmo
      que iguais à leitura;
    - objeto aninhado (ex.: `endereco`, `vinculoRepasse`) só passa se estiver em `permitir_objeto`
      e for o objeto COMPLETO: não há medição de que o Rabi mescle objeto parcial;
    - em orçamentos, movimentações e guias a leitura vem em CENTAVOS: não se compara com ela.
    """
    if recurso not in RECURSOS_PARCIAIS:
        raise CorpoParcialInvalido(
            f"PUT de {recurso} não é parcial (não declarado) — campo omitido seria apagado. Use o "
            "objeto completo (corpo_put_produto para produtos; GET + mudanças para os demais).")
    if not isinstance(mudancas, dict) or not mudancas:
        raise CorpoParcialInvalido("mudancas vazias: não há o que gravar.")
    mudancas = {k: v for k, v in mudancas.items() if k != "origem"}
    prob = []
    if recurso == "servicos":
        for k in mudancas:
            if k in _LEITURA_SERVICO:
                prob.append(f"'{k}' é nome de LEITURA; na escrita é '{_LEITURA_SERVICO[k]}'.")
            elif k not in CAMPOS_SERVICO:
                prob.append(f"'{k}' não existe no schema de escrita de serviço (a API ignoraria).")
    permitidas = set(permitir_lista_vazia)
    for k, v in mudancas.items():
        if isinstance(v, list) and not v and k not in permitidas:
            prob.append(f"'{k}': [] APAGA todos os vínculos. Se é isso mesmo, passe permitir_lista_vazia=('{k}',).")
    objetos_ok = set(permitir_objeto)
    for k, v in mudancas.items():
        if isinstance(v, dict) and k not in objetos_ok:
            prob.append(f"'{k}' é objeto aninhado: mande o objeto COMPLETO (o Rabi pode não mesclar) e "
                        f"passe permitir_objeto=('{k}',).")
    conferidas = set(listas_conferidas)
    for k in _LISTAS_SENSIVEIS.get(recurso, ()):
        if k in mudancas and k not in conferidas:
            prob.append(f"'{k}' enviado é a lista COMPLETA (o que ficar fora é desativado/apagado). "
                        f"Confira contra a régua e passe listas_conferidas=('{k}',).")
    if prob:
        raise CorpoParcialInvalido(" ".join(prob))
    if leitura is not None and recurso not in RECURSOS_LEITURA_EM_CENTAVOS:
        d = _desembrulhar(leitura)
        iguais = [k for k, v in mudancas.items() if k in d and _igual(d[k], v)]
        mudancas = {k: v for k, v in mudancas.items() if k not in iguais}
        if not mudancas:
            raise CorpoParcialInvalido("Tudo o que foi pedido já está igual no Rabi: nada a gravar.")
    return mudancas


def resumo_parcial(corpo: dict, recurso: str = "") -> list[str]:
    """Linhas para a PRÉVIA: o que muda, o que será LIMPO (null) e as listas que SUBSTITUEM."""
    linhas = []
    for k, v in corpo.items():
        if v is None and recurso == "servicos" and k == "valor":
            linhas.append("valor: null → R$ 0,00 (no serviço, valor null vira 0)")
        elif v is None:
            linhas.append(f"{k}: será LIMPO (null)")
        elif isinstance(v, list):
            linhas.append(f"{k}: lista SUBSTITUI os vínculos atuais por {len(v)} item(ns)"
                          + (" — APAGA todos" if not v else ""))
        else:
            linhas.append(f"{k}: → {v!r}")
    return linhas


CONVERSORES = {"servicos": corpo_put_servico, "produtos": corpo_put_produto}
