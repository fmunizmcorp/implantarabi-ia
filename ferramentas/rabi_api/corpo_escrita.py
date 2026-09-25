"""Converte a forma de LEITURA (GET) na forma de ESCRITA (corpo do PUT) — /servicos e /produtos.

Por que existe: o `PUT /servicos/{id}` e o `PUT /produtos/{id}` SOBRESCREVEM o cadastro, e a
leitura usa nomes e formatos diferentes da escrita. Exemplos (spec de 25/09/2026 + implantação
real):
- serviço: a leitura traz `somarItens` (com N); a escrita exige `somarItems` (com S);
- a leitura traz objetos aninhados (`tipoServico: {id, nome}`, `ServicoEspecialidade: [...]`,
  `TipoProduto: {id, nome}`, `Fabricante`, `deposito`, `UnidadeDeMedida`); a escrita exige IDs
  (`tipoServicoId`, `especialidadesId`, `tipoProdutoId`, `fabricanteId`, `depositoId`…);
- produto: a leitura traz `permitirEstoqueNegativo`; a escrita exige `estoquePodeNegativar`.
Mandar o GET de volta no PUT faz a API ignorar os nomes de leitura e APAGAR os campos (numa
implantação real o valor de um serviço foi a R$ 0,00 e a especialidade sumiu).

Regra desta ferramenta: TODO campo do schema de escrita (`ServicoCreate` / `ProdutoCreate`) tem
de ser resolvido — pela leitura (com os apelidos conhecidos) ou por `complementos` (valor
explícito; `None` explícito = "quero limpar"). Se algum não puder ser resolvido, levanta
`CampoDeEscritaAusente` listando TODOS os que faltam. Nunca omite em silêncio.

Uso:
    from ferramentas.rabi_api.corpo_escrita import corpo_put_servico
    atual = c.get("/servicos/46")
    corpo = corpo_put_servico(atual, complementos={"valor": 40.0})   # aplica a mudança
    c.put("/servicos/46", corpo)

Forma REAL medida em produção (GET de 25/09/2026; testes em test_corpo_escrita.py):
- `GET /servicos/{id}` traz os ids no primeiro nível (`tipoServicoId`, `tipoCodigoId`, `tipoGuiaId`,
  `tipoAtendimentoId`, `regimeDeAtendimentoId`, `tabelaANS87ID`), `codigoTUSS`, `tempoServico`,
  `somarItens` e `valor`, mas **NÃO traz** a composição (`produtoIds`, `taxaServicoId`,
  `valorTaxaServico`, `servicosRelacionados`, `equipamentoIds`), as especialidades
  (`especialidadesId`) nem `preparo`. Esses vêm SEMPRE por `complementos`: do dicionário de IDs /
  da foto da prova da criação (S08). Nunca "reenvie vazio".
- `GET /produtos/{id}` traz `Fabricante`, `TipoProduto`, `UnidadeDeMedida` e `deposito` aninhados
  (convertidos para ids aqui) e `permitirEstoqueNegativo`; não traz princípio ativo, CD, tipo de
  código, tabela 87, última pesquisa, fornecedores nem anexos (→ `complementos`).

Colaborador NÃO tem conversor: o GET de colaborador não traz `conselho`, `vinculoRepasse`,
`mensagem` nem `uf`/`conselhoProfissionalId` de cada especialidade, que o `ColaboradorCreate`
exige. Monte o corpo do PUT de colaborador a partir do cadastro do repo (dados da S09).
"""
from __future__ import annotations

from typing import Any, Callable, Iterable

# Campos do schema de escrita (conferidos contra o spec pelo teste test_corpo_escrita.py).
CAMPOS_SERVICO = (
    "nome", "descricao", "codigo", "codigoTUSS", "valor", "tempoServico", "somarItems",
    "linkAuxiliar", "preparamentos", "preparo", "tipoServicoId", "tipoCodigoId", "tipoGuiaId",
    "tabelaANS87ID", "regimeDeAtendimentoId", "tipoAtendimento", "taxaServicoId",
    "valorTaxaServico", "especialidadesId", "produtoIds", "equipamentoIds",
    "servicosRelacionados", "habilitarAgendamentoOnline", "apenasComColaboradorDesignado",
)
OBRIGATORIOS_SERVICO = ("nome", "descricao")

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
                f"exige: {', '.join(self.faltam)}. O PUT sobrescreve — omitir apagaria. Informe-os "
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
    "taxaServicoId": _id_de("taxaServicoId", "taxaServico", "TaxaServico"),
    "valorTaxaServico": _direto("valorTaxaServico"),
    "especialidadesId": _lista_ids(
        ("especialidadesId", "ServicoEspecialidade", "servicoEspecialidade", "especialidades"),
        "especialidadeId", ("especialidade", "Especialidade")),
    "produtoIds": _lista_ids(
        ("produtoIds", "ServicoProduto", "servicoProduto", "produtos"),
        "produtoId", ("produto", "Produto")),
    "equipamentoIds": _lista_ids(
        ("equipamentoIds", "ServicoEquipamento", "servicoEquipamento", "equipamentos"),
        "equipamentoId", ("equipamento", "Equipamento")),
    "servicosRelacionados": _lista_ids(
        ("servicosRelacionados", "ServicoRelacionado", "servicoRelacionado"),
        "servicoRelacionadoId", ("servicoRelacionado", "ServicoRelacionado", "servicoFilho")),
    "habilitarAgendamentoOnline": _direto("habilitarAgendamentoOnline"),
    "apenasComColaboradorDesignado": _direto("apenasComColaboradorDesignado"),
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
               campos: tuple, obrigatorios: tuple, mapa: dict) -> dict:
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
            faltam.append(campo)
        else:
            corpo[campo] = v
    for campo in obrigatorios:
        if campo in corpo and corpo[campo] in (None, ""):
            problemas.append(f"{campo} é obrigatório na escrita e está vazio.")
    if faltam or problemas:
        raise CampoDeEscritaAusente(recurso, faltam, problemas)
    return corpo


def corpo_put_servico(leitura: dict, complementos: dict | None = None) -> dict:
    """GET /servicos/{id} → corpo completo do PUT /servicos/{id} (schema ServicoCreate)."""
    return _converter("servicos", leitura, complementos, CAMPOS_SERVICO, OBRIGATORIOS_SERVICO, MAPA_SERVICO)


def corpo_put_produto(leitura: dict, complementos: dict | None = None) -> dict:
    """GET /produtos/{id} → corpo completo do PUT /produtos/{id} (schema ProdutoCreate)."""
    return _converter("produtos", leitura, complementos, CAMPOS_PRODUTO, OBRIGATORIOS_PRODUTO, MAPA_PRODUTO)


CONVERSORES = {"servicos": corpo_put_servico, "produtos": corpo_put_produto}
