"""Foto (antes/depois) de um recurso do Rabi e diff campo a campo.

Toda gravação no Rabi segue o ritual: foto antes → prévia → aprovação → grava → foto depois + diff.

CLI (a partir da raiz do repo):
    python3 -m ferramentas.rabi_api.foto antes  --caminho /convenios/12/servicos --destino provas/S10/conv-a/2026-10-01
    python3 -m ferramentas.rabi_api.foto depois --caminho /convenios/12/servicos --destino provas/S10/conv-a/2026-10-01
    python3 -m ferramentas.rabi_api.foto diff   --destino provas/S10/conv-a/2026-10-01
    python3 -m ferramentas.rabi_api.foto diff   --antes a.json --depois b.json [--saida diff.txt]

Opções de foto: --param chave=valor (repetível), --unico (GET simples, sem paginar),
--sem-mascara (não recomendado: grava dados pessoais sem máscara).

LGPD: por padrão, campos de dado pessoal (cpf, rg, e-mail, telefone, celular, data de nascimento…)
são mascarados; em /pacientes, /atendimentos, /agendamentos, /orcamentos e /nfse/tomadores o nome
também. A chave da API nunca é gravada.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys

from .cliente import ClienteRabi, FormatoInesperado

CAMPOS_PESSOAIS = {
    "cpf", "cpfmae", "rg", "numerodocumento", "email", "telefone", "celular", "telefonefornecedor",
    "datadenascimento", "datanascimento", "nomemae", "nomepai", "cns", "numerodacarterinha",
    "numerodacarteirinha", "carteirinha", "senha", "conteudo", "logradouro", "endereco_linha",
}
ROTAS_COM_PACIENTE = ("/pacientes", "/atendimentos", "/agendamentos", "/orcamentos", "/nfse/tomadores")
MASCARA = "***"


def mascarar_pessoais(obj, mascarar_nome: bool = False):
    if isinstance(obj, dict):
        novo = {}
        for k, v in obj.items():
            kl = k.lower()
            if kl in CAMPOS_PESSOAIS or (mascarar_nome and kl in ("nome", "nomesocial", "primeironome", "sobrenome")):
                novo[k] = MASCARA if v not in (None, "") else v
            else:
                novo[k] = mascarar_pessoais(v, mascarar_nome)
        return novo
    if isinstance(obj, list):
        return [mascarar_pessoais(x, mascarar_nome) for x in obj]
    return obj


def foto(cliente: ClienteRabi, caminho: str, destino_dir: str, nome: str, params: dict | None = None,
         *, paginar: bool = True, mascarar: bool = True) -> str:
    """Lê o recurso (paginando tudo, se for listagem) e grava destino_dir/nome.json. Devolve o caminho."""
    if paginar:
        try:
            dados = cliente.ler_tudo(caminho, params)
            meta_leitura = cliente.ultima_leitura
        except FormatoInesperado:
            dados = cliente.get(caminho, params)  # não é listagem: leitura simples
            meta_leitura = {"formato": "objeto"}
    else:
        dados = cliente.get(caminho, params)
        meta_leitura = {"formato": "objeto"}
    if mascarar:
        dados = mascarar_pessoais(dados, caminho.startswith(ROTAS_COM_PACIENTE))
    conteudo = {
        "meta": {
            "caminho": caminho, "params": params or {}, "base": cliente.base,
            "lido_em": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "leitura": meta_leitura, "mascarado": mascarar,
            "validade_chave": cliente.validade,
        },
        "dados": dados,
    }
    os.makedirs(destino_dir, exist_ok=True)
    arq = os.path.join(destino_dir, nome if nome.endswith(".json") else nome + ".json")
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(conteudo, f, ensure_ascii=False, indent=2, sort_keys=True)
    return arq


# --------------------------------------------------------------------------- diff

def _dados(x):
    if isinstance(x, dict) and "dados" in x and (set(x) <= {"meta", "dados"}):
        return x["dados"]
    return x


def _chave_item(item):
    if isinstance(item, dict):
        for k in ("id", "servicoId", "produtoId", "taxaId", "planoId", "especialidadeId", "colaboradorId",
                  "item_id", "servico_id", "produto_id"):
            if k in item and item[k] is not None:
                extra = item.get("servico_raiz_id")
                return (k, item[k], extra) if extra is not None else (k, item[k])
    return None


def _fmt(v) -> str:
    s = json.dumps(v, ensure_ascii=False, sort_keys=True)
    return s if len(s) <= 120 else s[:117] + "…"


def _diff(a, b, caminho: str, saida: list):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            sub = f"{caminho}.{k}" if caminho else k
            if k not in a:
                saida.append(f"+ {sub}: {_fmt(b[k])}")
            elif k not in b:
                saida.append(f"- {sub}: {_fmt(a[k])}")
            else:
                _diff(a[k], b[k], sub, saida)
        return
    if isinstance(a, list) and isinstance(b, list):
        chaves_a = [_chave_item(x) for x in a]
        chaves_b = [_chave_item(x) for x in b]
        if all(chaves_a) and all(chaves_b) and len(set(chaves_a)) == len(a) and len(set(chaves_b)) == len(b):
            ma, mb = dict(zip(chaves_a, a)), dict(zip(chaves_b, b))
            for ch in list(dict.fromkeys(chaves_a + chaves_b)):
                rot = f"{caminho}[{ch[0]}={ch[1]}" + (f",raiz={ch[2]}" if len(ch) > 2 else "") + "]"
                if ch not in ma:
                    saida.append(f"+ {rot} (novo): {_fmt(mb[ch])}")
                elif ch not in mb:
                    saida.append(f"- {rot} (sumiu): {_fmt(ma[ch])}")
                else:
                    _diff(ma[ch], mb[ch], rot, saida)
            return
        for i in range(max(len(a), len(b))):
            rot = f"{caminho}[{i}]"
            if i >= len(a):
                saida.append(f"+ {rot}: {_fmt(b[i])}")
            elif i >= len(b):
                saida.append(f"- {rot}: {_fmt(a[i])}")
            else:
                _diff(a[i], b[i], rot, saida)
        return
    if a != b:
        saida.append(f"~ {caminho or '(raiz)'}: {_fmt(a)} → {_fmt(b)}")


def diff(antes, depois) -> str:
    """Diferença campo a campo em texto legível. Aceita os JSON das fotos ou dados crus."""
    linhas: list[str] = []
    _diff(_dados(antes), _dados(depois), "", linhas)
    ignorar = re.compile(r"\.(updatedAt|updated_at)\b|^(updatedAt)")
    mudancas = [l for l in linhas if not ignorar.search(l)]
    so_datas = len(linhas) - len(mudancas)
    cab = (f"Diferenças: {len(mudancas)} (+ novo · - sumiu · ~ mudou)"
           + (f"; {so_datas} só de updatedAt omitidas" if so_datas else ""))
    if not mudancas:
        return cab + "\nNenhuma diferença de conteúdo."
    return cab + "\n" + "\n".join(mudancas)


# --------------------------------------------------------------------------- CLI

def _params(lista):
    out = {}
    for p in lista or []:
        if "=" not in p:
            raise SystemExit(f"--param precisa ser chave=valor (recebi {p!r})")
        k, v = p.split("=", 1)
        out[k] = v
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python3 -m ferramentas.rabi_api.foto", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("acao", choices=["antes", "depois", "diff"])
    ap.add_argument("--caminho", help="rota, ex.: /convenios/12/servicos")
    ap.add_argument("--destino", help="pasta da prova (grava antes.json / depois.json / diff.txt)")
    ap.add_argument("--nome", help="nome do arquivo (padrão: antes/depois)")
    ap.add_argument("--param", action="append", help="parâmetro de consulta chave=valor (repetível)")
    ap.add_argument("--unico", action="store_true", help="GET simples, sem paginar")
    ap.add_argument("--sem-mascara", action="store_true", help="não mascarar dados pessoais (evite)")
    ap.add_argument("--antes", help="arquivo antes (diff)")
    ap.add_argument("--depois", help="arquivo depois (diff)")
    ap.add_argument("--saida", help="arquivo de saída do diff (padrão: <destino>/diff.txt)")
    a = ap.parse_args(argv)

    if a.acao in ("antes", "depois"):
        if not a.caminho or not a.destino:
            ap.error("antes/depois precisam de --caminho e --destino")
        c = ClienteRabi()
        arq = foto(c, a.caminho, a.destino, a.nome or a.acao, _params(a.param),
                   paginar=not a.unico, mascarar=not a.sem_mascara)
        info = c.ultima_leitura or {}
        print(f"Foto gravada: {arq} (lidos={info.get('lidos', '?')}, total={info.get('total', '?')})")
        return 0

    antes = a.antes or (os.path.join(a.destino, "antes.json") if a.destino else None)
    depois = a.depois or (os.path.join(a.destino, "depois.json") if a.destino else None)
    if not antes or not depois:
        ap.error("diff precisa de --destino ou de --antes e --depois")
    with open(antes, encoding="utf-8") as f:
        ja = json.load(f)
    with open(depois, encoding="utf-8") as f:
        jd = json.load(f)
    texto = diff(ja, jd)
    saida = a.saida or (os.path.join(a.destino, "diff.txt") if a.destino else None)
    if saida:
        with open(saida, "w", encoding="utf-8") as f:
            f.write(texto + "\n")
        print(f"Diff gravado: {saida}")
    print(texto)
    return 0


if __name__ == "__main__":
    sys.exit(main())
