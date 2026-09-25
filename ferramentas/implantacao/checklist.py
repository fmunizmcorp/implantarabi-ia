"""Leitura dos checklists de sprint do repo da clínica (sprints/Sxx*.md).

Formato esperado da tabela: | # | item | status | origem | prova | observação |
Status válidos: pendente, coletado, confirmado, gravado, conferido, n/a, bloqueado.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

STATUS_VALIDOS = ("pendente", "coletado", "confirmado", "gravado", "conferido", "n/a", "bloqueado")
# peso de avanço de cada status (conferido = 100%)
PESO = {"pendente": 0, "bloqueado": 0, "coletado": 0.25, "confirmado": 0.5, "gravado": 0.75, "conferido": 1.0}


@dataclass
class Item:
    numero: str
    item: str
    status: str
    origem: str = ""
    prova: str = ""
    observacao: str = ""


@dataclass
class Sprint:
    codigo: str
    nome: str
    arquivo: Path
    itens: list[Item] = field(default_factory=list)
    avisos: list[str] = field(default_factory=list)

    @property
    def considerados(self) -> list[Item]:
        return [i for i in self.itens if i.status != "n/a"]

    @property
    def percentual(self) -> int:
        base = self.considerados
        if not base:
            return 0
        return round(100 * sum(PESO.get(i.status, 0) for i in base) / len(base))

    def contagem(self) -> dict[str, int]:
        c = {s: 0 for s in STATUS_VALIDOS}
        for i in self.itens:
            c[i.status] = c.get(i.status, 0) + 1
        return c

    @property
    def situacao(self) -> str:
        base = self.considerados
        if not base:
            return "sem itens"
        if any(i.status == "bloqueado" for i in base):
            return "bloqueada"
        if all(i.status == "conferido" for i in base):
            return "concluída"
        if all(i.status == "pendente" for i in base):
            return "não iniciada"
        return "em andamento"


def _normaliza(txt: str) -> str:
    t = txt.strip().lower()
    for a, b in (("ã", "a"), ("á", "a"), ("ç", "c"), ("õ", "o"), ("é", "e"), ("ê", "e"), ("í", "i"), ("ó", "o")):
        t = t.replace(a, b)
    return t


def _celulas(linha: str) -> list[str]:
    linha = linha.strip()
    if linha.startswith("|"):
        linha = linha[1:]
    if linha.endswith("|"):
        linha = linha[:-1]
    return [c.strip() for c in linha.split("|")]


def ler_sprint(arquivo: Path) -> Sprint:
    texto = arquivo.read_text(encoding="utf-8")
    m = re.search(r"^#\s*(S\d{2}[a-z]?)\s*[—-]\s*(.+)$", texto, re.M)
    codigo = m.group(1) if m else arquivo.stem.split("-")[0]
    nome = m.group(2).split(" · ")[0].strip() if m else arquivo.stem
    sp = Sprint(codigo=codigo, nome=nome, arquivo=arquivo)
    linhas = texto.splitlines()
    cab = None
    for ln in linhas:
        if not ln.strip().startswith("|"):
            cab = None
            continue
        cels = _celulas(ln)
        norm = [_normaliza(c) for c in cels]
        if "status" in norm and "item" in norm:
            cab = {nome_col: idx for idx, nome_col in enumerate(norm)}
            continue
        if cab is None or set(ln.replace("|", "").strip()) <= set("-: "):
            continue
        def col(n: str) -> str:
            idx = cab.get(n)
            return cels[idx] if idx is not None and idx < len(cels) else ""
        status = _normaliza(col("status")) or "pendente"
        status = {"nao se aplica": "n/a", "na": "n/a", "a fazer": "pendente"}.get(status, status)
        if status not in STATUS_VALIDOS:
            sp.avisos.append(f"status desconhecido '{col('status')}' no item '{col('item')}' — tratado como pendente")
            status = "pendente"
        sp.itens.append(Item(col("#"), col("item"), status, col("origem"), col("prova"),
                             col("observacao")))
    return sp


def ler_sprints(repo: Path) -> list[Sprint]:
    pasta = Path(repo) / "sprints"
    arquivos = sorted(p for p in pasta.glob("S*.md") if re.match(r"S\d{2}", p.name))
    return [ler_sprint(a) for a in arquivos]
