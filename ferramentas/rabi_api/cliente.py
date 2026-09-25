"""Cliente da API externa do Sistema Rabi — só biblioteca padrão (urllib + json).

O que ele faz por você:
- acha a chave: variável de ambiente RABI_API_KEY → arquivo credenciais/rabi-api-externa.md
  (linha `api_key: rbk_...`) → erro claro em português;
- base por RABI_API_BASE (padrão: produção);
- nunca imprime a chave (mascara em logs e repr);
- leitura que falha de verdade: status fora de 2xx ou corpo vazio = exceção;
- 401 → ChaveInvalida; 403 → SemPermissao; 503 → uma nova tentativa curta e depois
  ChaveInvalida (já foi a resposta para chave inválida) — nunca repete em loop;
- 429 → espera e tenta de novo (no máximo 3 vezes);
- ler_tudo(): pagina até totalPages, normaliza os envelopes (dados | data | items | lista crua)
  e confere lidos = total;
- enviar_lote(): fatia no limite, trata 207 lendo resultados[indice] e devolve relatório;
- guarda X-ApiKey-Expires-At da última resposta.

Uso rápido:
    from ferramentas.rabi_api.cliente import ClienteRabi
    c = ClienteRabi()
    convenios = c.ler_tudo("/convenios", {"ativo": "true"})
"""
from __future__ import annotations

import datetime as _dt
import json
import os
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE_PRODUCAO = "https://api.rabisistemas.com.br/api/v1/integrations"
BASE_HOMOLOGACAO = "https://api.hmg.rabisistemas.dev/api/v1/integrations"
ARQUIVO_CREDENCIAL = os.path.join("credenciais", "rabi-api-externa.md")
# Rotas em que 401 NÃO é problema de chave (defeitos declarados no Swagger de 25/09/2026).
ROTAS_401_SEM_SER_CHAVE = re.compile(
    r"^/(parametros/desconto/colaborador/[^/]+|parametros/alcada-compra/colaborador/[^/]+|"
    r"parametros/acolhimento/atualizar-validacoes/[^/]+|faturamento/glosas/(produto|taxa|servico))$")
PADRAO_LINHA_CHAVE = re.compile(r"^\s*[-*>]?\s*`?\s*api_key\s*:\s*`?\s*(rbk_[^\s`'\"]+)", re.I | re.M)


# --------------------------------------------------------------------------- exceções

class ErroRabi(Exception):
    """Erro de chamada à API. Tem .status, .corpo (texto), .metodo e .caminho."""

    def __init__(self, mensagem: str, status: int | None = None, corpo: str = "",
                 metodo: str = "", caminho: str = ""):
        super().__init__(mensagem)
        self.status = status
        self.corpo = corpo
        self.metodo = metodo
        self.caminho = caminho

    def mensagem_servidor(self) -> str:
        try:
            dados = json.loads(self.corpo)
            if isinstance(dados, dict) and dados.get("error"):
                return str(dados["error"])
        except (ValueError, TypeError):
            pass
        return (self.corpo or "")[:300]


class ChaveAusente(ErroRabi):
    """Nenhuma chave encontrada (nem no ambiente, nem no arquivo de credenciais)."""


class ChaveInvalida(ErroRabi):
    """401 (chave ausente, errada, vencida ou revogada) ou 503 persistente."""


class SemPermissao(ErroRabi):
    """403: a chave é válida, mas não tem a permissão da rota."""


class LeituraIncompleta(ErroRabi):
    """Leitura paginada terminou com quantidade diferente do total anunciado."""


class FormatoInesperado(ErroRabi):
    """Corpo de listagem em formato que não reconhecemos."""


# --------------------------------------------------------------------------- utilidades

def mascarar(chave: str | None) -> str:
    """'rbk_abc...xyz9' -> 'rbk_…xyz9' (nunca mostra a chave inteira)."""
    if not chave:
        return "(sem chave)"
    return f"{chave[:4]}…{chave[-4:]}" if len(chave) > 12 else "rbk_…"


def ler_chave_do_arquivo(raiz: str | None = None) -> tuple[str | None, str | None]:
    """Procura credenciais/rabi-api-externa.md em raiz, no diretório atual e nos pais."""
    candidatos = []
    base = os.path.abspath(raiz or os.getcwd())
    while True:
        candidatos.append(os.path.join(base, ARQUIVO_CREDENCIAL))
        pai = os.path.dirname(base)
        if pai == base:
            break
        base = pai
    for caminho in candidatos:
        if os.path.isfile(caminho):
            with open(caminho, encoding="utf-8") as f:
                m = PADRAO_LINHA_CHAVE.search(f.read())
            if m:
                return m.group(1), caminho
    return None, None


def _contexto_ssl() -> ssl.SSLContext:
    cafile = os.environ.get("SSL_CERT_FILE") or os.environ.get("REQUESTS_CA_BUNDLE")
    if cafile and os.path.isfile(cafile):
        return ssl.create_default_context(cafile=cafile)
    return ssl.create_default_context()


def _abridor(url: str):
    host = urllib.parse.urlparse(url).hostname or ""
    handlers = [urllib.request.HTTPSHandler(context=_contexto_ssl())]
    if host in ("127.0.0.1", "localhost", "::1"):
        handlers.append(urllib.request.ProxyHandler({}))  # servidor local: sem proxy
    return urllib.request.build_opener(*handlers)


def _valor_param(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (list, tuple)):
        return ",".join(_valor_param(x) for x in v)
    return str(v)


def normalizar_envelope(corpo) -> dict:
    """Devolve {'itens': [...], 'total': int|None, 'totalPages': int|None, 'formato': str}.

    Formatos reconhecidos:
      {dados:[...], page, pageSize, total, totalPages}   (padrão desde 25/09/2026)
      {data:[...], meta:{total, totalPages|lastPage}}    (antigo /financeiro/movimentacoes)
      {message, data:[...]}                               (antigo /orcamentos)
      {items:[...], total, page, pageSize, totalPages}   (antigo /estoque/saldo-produtos)
      [...]                                               (lista crua: /tabelas-preco antigo, "Array direto")
    """
    if isinstance(corpo, list):
        return {"itens": corpo, "total": len(corpo), "totalPages": 1, "formato": "lista crua"}
    if not isinstance(corpo, dict):
        raise FormatoInesperado(f"Listagem com corpo que não é lista nem objeto: {type(corpo).__name__}")
    for chave in ("dados", "items", "data"):
        if chave not in corpo:
            continue
        valor = corpo[chave]
        if isinstance(valor, dict) and any(k in valor for k in ("dados", "items", "data")):
            interno = normalizar_envelope(valor)
            interno["formato"] = f"{chave}→{interno['formato']}"
            return interno
        if not isinstance(valor, list):
            raise FormatoInesperado(f"Campo '{chave}' não é lista")
        meta = corpo.get("meta") if isinstance(corpo.get("meta"), dict) else {}
        total = corpo.get("total", meta.get("total"))
        paginas = corpo.get("totalPages", meta.get("totalPages", meta.get("lastPage")))
        formato = {"dados": "dados", "items": "items",
                   "data": "data+meta" if meta else ("message+data" if "message" in corpo else "data")}[chave]
        return {"itens": valor,
                "total": int(total) if total is not None else None,
                "totalPages": int(paginas) if paginas is not None else None,
                "formato": formato}
    raise FormatoInesperado("Objeto sem 'dados', 'data' ou 'items' — não é uma listagem conhecida. "
                            f"Chaves: {sorted(corpo)[:10]}")


class Resposta:
    def __init__(self, status: int, texto: str, cabecalhos: dict):
        self.status = status
        self.texto = texto
        self.cabecalhos = cabecalhos

    @property
    def json(self):
        if not self.texto:
            return None
        return json.loads(self.texto)

    def __repr__(self):
        return f"<Resposta {self.status} {len(self.texto)} bytes>"


# --------------------------------------------------------------------------- cliente

class ClienteRabi:
    def __init__(self, base: str | None = None, chave: str | None = None, *, raiz: str | None = None,
                 timeout: float = 90, esperas_429=(5, 10, 20), esperas_503=(3,),
                 log=None, verbose: bool = False):
        self.base = (base or os.environ.get("RABI_API_BASE") or BASE_PRODUCAO).rstrip("/")
        self.origem_chave = "parâmetro"
        if not chave:
            chave = os.environ.get("RABI_API_KEY", "").strip() or None
            self.origem_chave = "variável de ambiente RABI_API_KEY"
        if not chave:
            chave, arquivo = ler_chave_do_arquivo(raiz)
            self.origem_chave = f"arquivo {arquivo}"
        if not chave:
            raise ChaveAusente(
                "Não achei a chave da API do Rabi. Configure o segredo de ambiente RABI_API_KEY "
                "(preferido) ou registre a linha 'api_key: rbk_...' em credenciais/rabi-api-externa.md "
                "no repo da clínica. Passo a passo: conhecimento/api-externa/chave-e-token.md.")
        if not chave.startswith("rbk_"):
            raise ChaveInvalida("A chave não começa com 'rbk_' — confira se copiou a chave certa "
                                f"(origem: {self.origem_chave}).")
        self._chave = chave
        self.timeout = timeout
        self.esperas_429 = tuple(esperas_429)[:3]
        self.esperas_503 = tuple(esperas_503)
        self.validade: str | None = None  # X-ApiKey-Expires-At da última resposta
        self.ultima_resposta: Resposta | None = None
        self.ultima_leitura: dict | None = None
        self._log = log if log is not None else (lambda m: print(m, file=sys.stderr)) if verbose else (lambda m: None)

    def __repr__(self):
        return f"<ClienteRabi base={self.base} chave={mascarar(self._chave)}>"

    @property
    def chave_mascarada(self) -> str:
        return mascarar(self._chave)

    # ------------------------------------------------------------------ validade
    def dias_restantes(self, agora: _dt.datetime | None = None) -> int | None:
        if not self.validade:
            return None
        try:
            fim = _dt.datetime.fromisoformat(self.validade.replace("Z", "+00:00"))
        except ValueError:
            return None
        if fim.tzinfo is None:
            fim = fim.replace(tzinfo=_dt.timezone.utc)
        agora = agora or _dt.datetime.now(_dt.timezone.utc)
        return (fim - agora).days

    # ------------------------------------------------------------------ HTTP cru
    def requisicao(self, metodo: str, caminho: str, params: dict | None = None, corpo=None,
                   cabecalhos: dict | None = None, levantar: bool = True) -> Resposta:
        """Faz a chamada. Com levantar=True, status ≥ 400 vira exceção (401/403/503 específicas)."""
        metodo = metodo.upper()
        url = self.base + (caminho if caminho.startswith("/") else "/" + caminho)
        if params:
            limpos = {k: _valor_param(v) for k, v in params.items() if v is not None}
            url += ("&" if "?" in url else "?") + urllib.parse.urlencode(limpos)
        dados = None
        hdr = {"Authorization": f"Bearer {self._chave}", "Accept": "application/json"}
        if corpo is not None:
            dados = json.dumps(corpo, ensure_ascii=False).encode("utf-8")
            hdr["Content-Type"] = "application/json"
        hdr.update(cabecalhos or {})

        tentativas_429 = list(self.esperas_429)
        tentativas_503 = list(self.esperas_503)
        while True:
            req = urllib.request.Request(url, data=dados, method=metodo, headers=hdr)
            try:
                with _abridor(url).open(req, timeout=self.timeout) as r:
                    resp = Resposta(r.status, r.read().decode("utf-8", "replace"), dict(r.headers.items()))
            except urllib.error.HTTPError as e:
                resp = Resposta(e.code, e.read().decode("utf-8", "replace") if e.fp else "", dict(e.headers.items()))
            except urllib.error.URLError as e:
                raise ErroRabi(f"Sem conexão com a API ({metodo} {caminho}): {e.reason}",
                               metodo=metodo, caminho=caminho) from None
            self.ultima_resposta = resp
            exp = {k.lower(): v for k, v in resp.cabecalhos.items()}.get("x-apikey-expires-at")
            if exp:
                self.validade = exp
            self._log(f"{metodo} {caminho} -> {resp.status} ({len(resp.texto)} bytes)")
            if resp.status == 429 and tentativas_429:
                espera = tentativas_429.pop(0)
                self._log(f"429: outro lote em andamento; esperando {espera}s e tentando de novo")
                time.sleep(espera)
                continue
            if resp.status == 503 and tentativas_503:
                espera = tentativas_503.pop(0)
                self._log(f"503: tentando de novo uma vez em {espera}s")
                time.sleep(espera)
                continue
            break
        if levantar and resp.status >= 400:
            self._levantar(resp, metodo, caminho)
        return resp

    def _levantar(self, resp: Resposta, metodo: str, caminho: str):
        base = ErroRabi("", resp.status, resp.texto, metodo, caminho)
        msg_srv = base.mensagem_servidor()
        onde = f"{metodo} {caminho}"
        if resp.status == 401 and ROTAS_401_SEM_SER_CHAVE.match(caminho.split("?")[0]):
            raise ErroRabi(
                f"401 em {onde}, mas nesta rota o 401 é defeito conhecido da API (não é a chave): "
                f"'{msg_srv}'. Nas rotas POST /parametros/desconto|alcada-compra/colaborador e "
                "acolhimento/atualizar-validacoes a chave de API sempre recebe 401 — faça pela tela. "
                "Nas rotas PUT /faturamento/glosas/*, 401 = motivoGlosado inexistente. "
                "Ver conhecimento/api-externa/defeitos-conhecidos.md.",
                resp.status, resp.texto, metodo, caminho)
        if resp.status == 401:
            raise ChaveInvalida(
                f"401 em {onde}: a API recusou a chave (ausente, errada, vencida ou revogada). "
                f"Servidor: '{msg_srv}'. Não vou repetir. Peça chave nova ao time Rabi pelo mesmo canal "
                f"em que a chave foi gerada (chave atual: {mascarar(self._chave)}, origem: {self.origem_chave}). "
                "Atenção: nas rotas PUT /faturamento/glosas/* um motivo de glosa inválido também devolve 401.",
                resp.status, resp.texto, metodo, caminho)
        if resp.status == 403:
            m = re.search(r"'([A-Za-z]+:[a-z]+)'", msg_srv)
            perm = m.group(1) if m else "(ver a rota no Swagger)"
            raise SemPermissao(
                f"403 em {onde}: a chave não tem a permissão {perm}. Peça ao time Rabi uma chave que inclua "
                "essa permissão (lista em conhecimento/api-externa/chave-e-token.md).",
                resp.status, resp.texto, metodo, caminho)
        if resp.status == 503:
            raise ChaveInvalida(
                f"503 em {onde} depois de nova tentativa: a API não conseguiu validar a chave. Pelo Swagger "
                "de 25/09 isso é falha de rede/tempo, mas até 24/09 era a resposta para chave inválida. "
                "Não vou repetir em loop: confira a chave e, se ela estiver certa, avise o time Rabi.",
                resp.status, resp.texto, metodo, caminho)
        raise ErroRabi(f"{resp.status} em {onde}: {msg_srv}", resp.status, resp.texto, metodo, caminho)

    # ------------------------------------------------------------------ verbos
    def get(self, caminho: str, params: dict | None = None):
        """Leitura. Falha se status ≠ 2xx ou corpo vazio. Devolve o JSON (pode ser null/0/lista/objeto)."""
        resp = self.requisicao("GET", caminho, params)
        if not resp.texto.strip():
            raise ErroRabi(f"Leitura vazia (0 bytes) em GET {caminho} com status {resp.status}: "
                           "leitura vazia é leitura falha — não conclua nada com ela.",
                           resp.status, "", "GET", caminho)
        try:
            dados = resp.json
        except ValueError:
            raise FormatoInesperado(f"GET {caminho} devolveu corpo que não é JSON", resp.status,
                                    resp.texto[:300], "GET", caminho) from None
        if dados == 401 and caminho.startswith("/agendamentos/motivo-cancelamento"):
            raise ErroRabi("GET /agendamentos/motivo-cancelamento devolveu 200 com o número 401 no corpo: "
                           "é erro de banco disfarçado (defeito conhecido). Tente mais tarde.",
                           resp.status, resp.texto, "GET", caminho)
        return dados

    def post(self, caminho: str, corpo=None, params: dict | None = None, cabecalhos: dict | None = None):
        return self._escrita("POST", caminho, corpo, params, cabecalhos)

    def put(self, caminho: str, corpo=None, params: dict | None = None):
        return self._escrita("PUT", caminho, corpo, params)

    def patch(self, caminho: str, corpo=None, params: dict | None = None):
        return self._escrita("PATCH", caminho, corpo, params)

    def delete(self, caminho: str, params: dict | None = None):
        return self._escrita("DELETE", caminho, None, params)

    def _escrita(self, metodo, caminho, corpo, params, cabecalhos=None):
        """Devolve o JSON da resposta (ou None se vazio). Status ≥ 400 vira exceção."""
        resp = self.requisicao(metodo, caminho, params, corpo, cabecalhos)
        try:
            return resp.json
        except ValueError:
            return resp.texto

    # ------------------------------------------------------------------ leitura completa
    def ler_tudo(self, caminho: str, params: dict | None = None, *, page_size: int = 200,
                 conferir_total: bool = True, max_paginas: int = 5000) -> list:
        """Lê todas as páginas de uma listagem e devolve a lista completa de itens.

        Percorre por totalPages (não pelo tamanho da página). Confere lidos = total quando o
        total é informado (LeituraIncompleta se não bater; desligue com conferir_total=False só
        onde a rota avisa que filtra depois de paginar, como GET /orcamentos sem pacienteId).
        """
        params = dict(params or {})
        params.setdefault("pageSize", page_size)
        pagina = int(params.pop("page", 1))
        itens: list = []
        total = paginas = None
        formato = None
        while True:
            corpo = self.get(caminho, {**params, "page": pagina})
            env = normalizar_envelope(corpo)
            formato = formato or env["formato"]
            itens.extend(env["itens"])
            total = env["total"] if env["total"] is not None else total
            paginas = env["totalPages"] if env["totalPages"] is not None else paginas
            if env["formato"] == "lista crua":
                break  # sem paginação declarada
            if paginas is not None:
                if pagina >= paginas:
                    break
            elif total is not None:
                if len(itens) >= total or not env["itens"]:
                    break
            elif len(env["itens"]) < int(params["pageSize"]):
                break
            pagina += 1
            if pagina > max_paginas:
                raise LeituraIncompleta(f"Mais de {max_paginas} páginas em {caminho}; parei por segurança.")
        self.ultima_leitura = {"caminho": caminho, "lidos": len(itens), "total": total,
                               "paginas": paginas, "formato": formato}
        if conferir_total and total is not None and len(itens) != total:
            raise LeituraIncompleta(
                f"GET {caminho}: li {len(itens)} itens, mas a API anunciou total={total}. "
                "Não conclua nada com esta leitura; leia de novo (pode ter havido gravação no meio).",
                None, "", "GET", caminho)
        return itens

    # ------------------------------------------------------------------ lotes
    def enviar_lote(self, caminho: str, chave_corpo: str, itens: list, tamanho: int = 50, *,
                    metodo: str = "POST", extras: dict | None = None) -> dict:
        """Envia itens em fatias de `tamanho` (50 nos /bulk, 200 nas abas do convênio e
        /tabelas-preco/produtos/bulk, 100 em /nfse/tomadores/bulk e PUT /convenios/{id}/colaboradores).

        Uma fatia por vez (a API recusa lotes simultâneos com 429). Lê o 207 item a item.
        Devolve relatório: {'enviados', 'ok', 'erros', 'nao_processados', 'resultados', 'lotes',
        'reenviar'} — 'reenviar' tem só os itens ERRO/NAO_PROCESSADO (nunca reenvie o lote inteiro).
        Se uma fatia inteira falhar (4xx), levanta ErroRabi com .relatorio parcial.
        """
        if tamanho < 1:
            raise ValueError("tamanho deve ser ≥ 1")
        rel = {"enviados": 0, "ok": 0, "erros": [], "nao_processados": [], "resultados": [],
               "lotes": [], "reenviar": []}
        for inicio in range(0, len(itens), tamanho):
            fatia = itens[inicio:inicio + tamanho]
            corpo = {**(extras or {}), chave_corpo: fatia}
            try:
                resp = self.requisicao(metodo, caminho, corpo=corpo)
            except ErroRabi as e:
                e.relatorio = rel
                rel["lotes"].append({"inicio": inicio, "quantidade": len(fatia), "status": e.status})
                raise
            dados = None
            try:
                dados = resp.json
            except ValueError:
                pass
            rel["enviados"] += len(fatia)
            rel["lotes"].append({"inicio": inicio, "quantidade": len(fatia), "status": resp.status})
            resultados = dados.get("resultados") if isinstance(dados, dict) else None
            if resultados is None:
                if resp.status == 207:
                    raise ErroRabi(f"207 em {metodo} {caminho} sem 'resultados' — não dá para saber o que gravou.",
                                   resp.status, resp.texto, metodo, caminho)
                rel["ok"] += len(fatia)
                continue
            vistos = set()
            for r in resultados:
                idx = int(r.get("indice", -1))
                vistos.add(idx)
                global_idx = inicio + idx
                linha = {**r, "indice_global": global_idx}
                rel["resultados"].append(linha)
                status = str(r.get("status", "")).upper()
                if status in ("CRIADO", "ATUALIZADO", "OK", "SUCESSO"):
                    rel["ok"] += 1
                elif status == "NAO_PROCESSADO":
                    rel["nao_processados"].append(linha)
                    rel["reenviar"].append(fatia[idx] if 0 <= idx < len(fatia) else None)
                else:
                    rel["erros"].append(linha)
                    rel["reenviar"].append(fatia[idx] if 0 <= idx < len(fatia) else None)
            for idx in range(len(fatia)):  # item sem resultado = não confirmado
                if idx not in vistos:
                    linha = {"indice": idx, "indice_global": inicio + idx, "status": "SEM_RESULTADO"}
                    rel["nao_processados"].append(linha)
                    rel["reenviar"].append(fatia[idx])
        return rel


def resumo_lote(rel: dict) -> str:
    """Texto curto para mostrar ao usuário (sem dados pessoais)."""
    linhas = [f"Enviados: {rel['enviados']} · OK: {rel['ok']} · Erro: {len(rel['erros'])} · "
              f"Não processados: {len(rel['nao_processados'])}"]
    for e in rel["erros"][:20]:
        linhas.append(f"  - item {e['indice_global']}: {e.get('erro') or e.get('status')}")
    if len(rel["erros"]) > 20:
        linhas.append(f"  … e mais {len(rel['erros']) - 20}")
    return "\n".join(linhas)
