"""Casos de teste T1–T26 do manual + invariantes + circularidade.

Fonte: https://www.rabisistemas.com.br/manual/precos/guia-ia.html#casos-de-teste
(números exatos do manual) e
https://www.rabisistemas.com.br/manual/precos/arvore-de-decisao.html#exemplos.

Convenção do manual: item = (valor · Zerar · Utiliza). "—" no valor
convertido = vazio (None). Onde o manual não dá um número (custo, valor do
subserviço), usamos um valor ilustrativo e dizemos isso no docstring.
"""
import pytest

from ferramentas.conversao.modelo import (
    Catalogo, ConfigItem, Convenio, PoliticaTipoProduto, Produto, Servico, Taxa, Vinculo,
    FONTE_FIXO,
)
from ferramentas.conversao import motor as m


# --------------------------------------------------------------------------- helpers

def prod(id_, valor, custo=10.0, **kw):
    """Produto com preço de casa = ``valor`` (fonte fixa)."""
    return Produto(id=id_, nome=kw.pop("nome", f"Produto {id_}"), custo=custo,
                   preco_venda_tabela=valor, fonte_preco=FONTE_FIXO, **kw)


def taxa(id_, valor, **kw):
    return Taxa(id=id_, nome=kw.pop("nome", f"Taxa {id_}"), valor_cadastro=valor, **kw)


def serv(id_, valor=0.0, somar=False, itens=(), **kw):
    return Servico(id=id_, nome=kw.pop("nome", f"Serviço {id_}"), valor_cadastro=valor, somar_itens=somar,
                   itens=[Vinculo(t, i, q) for (t, i, q) in itens], **kw)


def cfg(id_, utiliza=True, zerar=False, pacote=False, conv=None, **kw):
    return ConfigItem(id=id_, utiliza=utiliza, zerar=zerar, pacote=pacote, valor_convertido=conv, **kw)


def montar(servicos, produtos=(), taxas=(), cs=(), cp=(), ct=(), **kw_conv):
    cat = Catalogo(servicos={s.id: s for s in servicos}, produtos={p.id: p for p in produtos},
                   taxas={t.id: t for t in taxas})
    c = Convenio(id=1, nome="Convênio A", servicos={x.id: x for x in cs}, produtos={x.id: x for x in cp},
                 taxas={x.id: x for x in ct}, **kw_conv)
    return cat, c


def servico_simples(somar, pacote, conv, valor_fixo=100.0, itens_prod=()):
    """Serviço 1 com produtos (id, valor, zerar, utiliza)."""
    produtos = [prod(pid, v) for (pid, v, _, _) in itens_prod]
    s = serv(1, valor=0.0 if somar else valor_fixo, somar=somar,
             itens=[("produto", pid, 1) for (pid, _, _, _) in itens_prod])
    cs = [cfg(1, pacote=pacote, conv=conv)]
    cp = [cfg(pid, utiliza=u, zerar=z) for (pid, _, z, u) in itens_prod]
    return montar([s], produtos, cs=cs, cp=cp)


# --------------------------------------------------------------------------- casos

def t1():
    cat, c = servico_simples(False, False, None, 100, [(10, 50, False, True)])
    assert m.valor(cat, c, 1) == 150


def t2():
    cat, c = servico_simples(False, True, None, 100, [(10, 50, True, True)])
    assert m.valor(cat, c, 1) == 100


def t3():
    cat, c = servico_simples(False, True, None, 100, [(10, 50, False, True)])
    assert m.valor(cat, c, 1) == 150


def t4():
    cat, c = servico_simples(False, True, 90.0, 100, [(10, 50, False, True)])
    assert m.valor(cat, c, 1) == 140


def t5():
    cat, c = servico_simples(True, False, None, itens_prod=[(10, 3000, True, True)])
    assert m.valor(cat, c, 1) == 3000  # zerar ignorado (não é pacote)


def t6():
    cat, c = servico_simples(True, False, 266.16, itens_prod=[(10, 3000, False, True)])
    assert m.valor(cat, c, 1) == pytest.approx(3266.16)


def t7():
    """somar T · pacote T · convertido vazio → não é pacote fechado; nada zerado.
    O manual não diz o Zerar do produto além de T; o sub (fixo 80) vai com Zerar ✔
    para provar que também não é lido."""
    p = prod(10, 135.42)
    sub = serv(2, 80.0)
    s = serv(1, 0.0, True, [("produto", 10, 1), ("subservico", 2, 1)])
    cat, c = montar([s, sub], [p], cs=[cfg(1, pacote=True), cfg(2, zerar=True)], cp=[cfg(10, zerar=True)])
    r = m.calcular_servico(cat, c, 1)
    assert not r.pacote_fechado
    assert r.total == pytest.approx(215.42)
    assert all(l.conta for l in r.arvore.filhos)


def t8():
    cat, c = servico_simples(True, True, 3506.53, itens_prod=[(10, 3000, True, True)])
    assert m.valor(cat, c, 1) == pytest.approx(3506.53)


def t9():
    cat, c = servico_simples(True, False, None, itens_prod=[(10, 3000, False, False)])
    r = m.calcular_servico(cat, c, 1)
    assert r.total == 0
    assert r.arvore.filhos[0].motivo == m.NAO_UTILIZA


def t10():
    """Sub com Utiliza=F contendo produto: sub e produto fora; custo do produto conta.
    Valores ilustrativos: produto 70 (custo 25), sub fixo 40."""
    p = prod(10, 70, custo=25)
    sub = serv(2, 40.0, itens=[("produto", 10, 1)])
    s = serv(1, 0.0, True, [("subservico", 2, 1)])
    cat, c = montar([s, sub], [p], cs=[cfg(1), cfg(2, utiliza=False)], cp=[cfg(10)])
    r = m.calcular_servico(cat, c, 1)
    ls = {(l.tipo, l.id): l for l in r.linhas}
    assert r.total == 0
    assert ls[("subservico", 2)].motivo == m.NAO_UTILIZA and not ls[("subservico", 2)].conta
    assert ls[("produto", 10)].motivo == m.PAI_FORA and not ls[("produto", 10)].conta
    assert r.custo == 25  # custo conta


def t11():
    """Orçamento com a configuração de T8, usou 2 (composição 1): 3506,53 + 3000 (excedente)."""
    cat, c = servico_simples(True, True, 3506.53, itens_prod=[(10, 3000, True, True)])
    c.pago_no_ato = True
    o = m.orcamento(cat, c, [{"tipo": "servico", "id": 1, "usados": {"produto:10": 2}}])
    assert o.total == pytest.approx(6506.53)
    lp = [l for l in o.linhas if l.tipo == "produto"][0]
    assert lp.qtd_cobrada == 1 and lp.valor == 3000


def t12():
    cat, c = servico_simples(False, False, 0.0, 100, [(10, 50, False, True)])
    r = m.calcular_servico(cat, c, 1)
    assert r.base == 0  # zero é zero; não desce para o cadastro
    assert r.total == 50
    assert m.quatro_linhas(cat, c, 1)["proprio"] == 0


def t13():
    """Farol consolidado: A (receita 50, custo 100 → vermelha) + B (500/100 → verde),
    régua 100/120 → 550/200 = 275% VERDE. Montado como orçamento: custo vem de produto
    da composição sem Utiliza (receita 0, custo conta)."""
    pa, pb = prod(10, 1, custo=100), prod(11, 1, custo=100)
    a = serv(1, 50.0, itens=[("produto", 10, 1)])
    b = serv(2, 500.0, itens=[("produto", 11, 1)])
    cat, c = montar([a, b], [pa, pb], cs=[cfg(1), cfg(2)], cp=[cfg(10, utiliza=False), cfg(11, utiliza=False)],
                    pago_no_ato=True)
    o = m.orcamento(cat, c, [{"tipo": "servico", "id": 1}, {"tipo": "servico", "id": 2}])
    assert o.por_servico[1]["farol"] == m.VERMELHO
    assert o.por_servico[2]["farol"] == m.VERDE
    assert o.indice == pytest.approx(275.0)
    assert o.farol == m.VERDE


def t14():
    """Produto sem Utiliza (casa 80, custo 60) + serviço com receita 100 e custo 40 →
    100/100 = 100% → ≤ Vermelho = VERMELHO (bloqueia). O serviço: fixo 100 com um
    produto de custo 40 sem Utiliza (ilustrativo)."""
    p = prod(10, 80, custo=60)
    p2 = prod(11, 5, custo=40)
    s = serv(1, 100.0, itens=[("produto", 11, 1)])
    cat, c = montar([s], [p, p2], cs=[cfg(1)], cp=[cfg(10, utiliza=False), cfg(11, utiliza=False)],
                    pago_no_ato=True)
    o = m.orcamento(cat, c, [{"tipo": "servico", "id": 1}, {"tipo": "produto", "id": 10}])
    lp = [l for l in o.linhas if l.tipo == "produto" and l.id == 10][0]
    assert lp.valor == 0 and lp.custo == 60
    assert o.total == 100 and o.custo == 100
    assert o.indice == pytest.approx(100.0)
    assert o.farol == m.VERMELHO
    # variante do manual: item sem custo → ROXO
    cat.produtos[10].custo = None
    assert m.orcamento(cat, c, [{"tipo": "servico", "id": 1}, {"tipo": "produto", "id": 10}]).farol == m.ROXO


def t15():
    """Raiz Pacote ✔ · combinado 0,01 · sub "aplicação" Zerar ✔ contendo taxa 73,99 Zerar ✘.
    Sub com valor fixo ilustrativo 20 (é zerado; só a linha dele sai)."""
    tx = taxa(20, 73.99)
    sub = serv(2, 20.0, itens=[("taxa", 20, 1)])
    s = serv(1, 100.0, False, [("subservico", 2, 1)])
    cat, c = montar([s, sub], taxas=[tx], cs=[cfg(1, pacote=True, conv=0.01), cfg(2, zerar=True)],
                    ct=[cfg(20, zerar=False)])
    r = m.calcular_servico(cat, c, 1)
    ls = {(l.tipo, l.id): l for l in r.linhas}
    assert r.total == pytest.approx(74.00)
    assert ls[("subservico", 2)].motivo == m.ZERADO_EM_PACOTE and ls[("subservico", 2)].valor_efetivo == 0
    assert ls[("taxa", 20)].conta


def t16():
    p = prod(10, 30)
    sub = serv(2, 40.0, itens=[("produto", 10, 1)])
    s = serv(1, 100.0, False, [("subservico", 2, 1)])
    cat, c = montar([s, sub], [p], cs=[cfg(1, pacote=True), cfg(2, zerar=False)], cp=[cfg(10, zerar=True)])
    r = m.calcular_servico(cat, c, 1)
    assert r.total == 140
    assert {(l.tipo, l.id): l for l in r.linhas}[("produto", 10)].motivo == m.ZERADO_EM_PACOTE


def t17():
    p = prod(10, 20)
    sub = serv(2, 80.0, itens=[("produto", 10, 1)])
    s = serv(1, 0.0, True, [("subservico", 2, 1)])
    cat, c = montar([s, sub], [p], cs=[cfg(1), cfg(2)], cp=[cfg(10)])
    assert m.valor(cat, c, 1) == 100


def t18():
    cat, c = servico_simples(False, False, None, 100, [(10, 50, False, True)])
    c.pago_no_ato = True
    o = m.orcamento(cat, c, [{"tipo": "servico", "id": 1, "usados": {"produto:10": 2}}])
    assert o.total == 200  # quantidade inteira


def t19():
    cat, c = servico_simples(False, False, None, 100, [(10, 80, False, False)])
    cat.produtos[10].custo = 60
    c.pago_no_ato = True
    o = m.orcamento(cat, c, [{"tipo": "servico", "id": 1}])
    lp = [l for l in o.linhas if l.tipo == "produto"][0]
    assert lp.valor == 0 and lp.motivo == m.NAO_UTILIZA
    assert o.custo == 60  # custo conta no Farol


def t20():
    cat, c = servico_simples(True, False, 266.16, itens_prod=[(10, 3000, False, True)])
    r = m.calcular_servico(cat, c, 1)
    assert r.base == pytest.approx(266.16)  # linha ✅
    assert r.total == pytest.approx(3266.16)  # Farol / linha do serviço em Farol › Itens
    assert r.arvore.receita == pytest.approx(3266.16)


def t21():
    s = serv(1, 100.0, nome="Consulta", codigo_tuss="10101012")
    cat, c = montar([s], cs=[cfg(1, nome="", codigo="X1")])
    t = m.textos_servico(s, c)
    assert t["nome"] == "Consulta" and t["codigo"] == "X1"


def t22():
    p = Produto(id=10, nome="Medicamento", tipo_produto="MEDICAMENTO", custo=5, preco_venda_tabela=60,
                fonte_preco=FONTE_FIXO, precos_tabela={"Tabela Referência": {"PRECO_1": 50}})
    cat, c = montar([], [p], cp=[cfg(10)])
    c.politicas["MEDICAMENTO"] = PoliticaTipoProduto("MEDICAMENTO", "Tabela Referência", "PRECO_1", 10)
    assert m.valor_produto(p, c).valor == pytest.approx(55.00)


def _t23_25(pacote, zerar_taxa):
    p, tx = prod(10, 50), taxa(20, 30)
    s = serv(1, 100.0, False, [("produto", 10, 1), ("taxa", 20, 1)])
    return montar([s], [p], [tx], cs=[cfg(1, pacote=pacote, conv=100.0)], cp=[cfg(10, zerar=True)],
                  ct=[cfg(20, zerar=zerar_taxa)])


def t23():
    cat, c = _t23_25(False, True)
    assert m.quatro_linhas(cat, c, 1)["total"] == 180


def t24():
    cat, c = _t23_25(True, True)
    assert m.quatro_linhas(cat, c, 1)["total"] == 100


def t25():
    cat, c = _t23_25(True, False)
    assert m.quatro_linhas(cat, c, 1)["total"] == 130


def t26():
    p = prod(10, 900, nome="Medicamento exemplo")
    sub = serv(2, 80.0, nome="Aplicação")
    s = serv(1, 0.0, True, [("produto", 10, 1), ("subservico", 2, 1)], nome="Medicamento aplicado")
    cat, c = montar([s, sub], [p], cs=[cfg(1), cfg(2)], cp=[cfg(10)])
    q = m.quatro_linhas(cat, c, 1)
    assert q["proprio"] == 0
    assert q["proprio_explicacao"] == "0,00 (sem preço próprio: itens cobrados à parte)"
    assert q["total"] == 980
    assert q["casa_rotulo"] == "(soma dos itens)" and q["casa"] == 980
    assert m.calcular_servico(cat, c, 1).total == 980  # = Farol


CASOS = {f"T{i}": globals()[f"t{i}"] for i in range(1, 27)}


@pytest.mark.parametrize("caso", list(CASOS), ids=list(CASOS))
def test_caso_manual(caso):
    CASOS[caso]()


# --------------------------------------------------------------------------- exemplos numéricos

def _exemplo_composto():
    """arvore-de-decisao.html#exemplo-composto (Convênio Beta)."""
    med = Produto(10, "Medicamento X", tipo_produto="MEDICAMENTO", custo=30, preco_venda_tabela=70,
                  fonte_preco=FONTE_FIXO, precos_tabela={"Tabela Interna": {"PRECO_1": 50}}, tabela87=20)
    ser = prod(11, 1.5, custo=0.5, nome="Seringa")
    soro = prod(12, 4.0, custo=3.0, nome="Soro")
    tx = taxa(20, 40.0, nome="Taxa de sala")
    s = serv(1, 100.0, False, [("produto", 10, 1), ("produto", 11, 1), ("produto", 12, 1), ("taxa", 20, 1)])
    cat, c = montar([s], [med, ser, soro], [tx], cs=[cfg(1, conv=90.0)],
                    cp=[cfg(10), cfg(11, conv=2.0), cfg(12, utiliza=False)], ct=[cfg(20, conv=35.0)])
    c.politicas["MEDICAMENTO"] = PoliticaTipoProduto("MEDICAMENTO", "Tabela Interna", "PRECO_1", 10)
    return cat, c


def test_exemplo_composto_beta():
    cat, c = _exemplo_composto()
    r = m.calcular_servico(cat, c, 1)
    ls = {(l.tipo, l.id): l for l in r.linhas}
    assert ls[("produto", 10)].receita == 55 and ls[("produto", 10)].farol == m.VERDE
    assert round(ls[("produto", 10)].indice) == 183
    assert ls[("produto", 11)].receita == 2 and round(ls[("produto", 11)].indice) == 400
    assert ls[("produto", 12)].receita == 0 and not ls[("produto", 12)].conta
    assert ls[("taxa", 20)].receita == 35
    assert r.base == 90 and r.total == 182 and r.custo == 33.5
    assert round(r.indice) == 543 and r.farol == m.VERDE


def test_exemplo_composto_variante_pacote():
    cat, c = _exemplo_composto()
    c.servicos[1].pacote = True
    c.produtos[11].zerar = True
    c.taxas[20] = cfg(20, conv=35.0, zerar=True)
    r = m.calcular_servico(cat, c, 1)
    assert r.total == 145 and r.base == 90 and r.custo == 33.5
    assert round(r.indice) == 433


def test_exemplo_subservico_540():
    """arvore-de-decisao.html#arvore-subservico: 500 + 0 + 40 + 0 = 540."""
    tx, mat = taxa(20, 40.0), prod(10, 10.0)
    ap = serv(2, 80.0, itens=[("taxa", 20, 1), ("produto", 10, 1)], nome="Aplicação")
    s = serv(1, 0.0, False, [("subservico", 2, 1)])
    cat, c = montar([s, ap], [mat], [tx], cs=[cfg(1, pacote=True, conv=500.0), cfg(2, zerar=True)],
                    cp=[cfg(10, zerar=True)], ct=[cfg(20, zerar=False)])
    assert m.valor(cat, c, 1) == 540


def test_exemplo_simples_consulta():
    s = serv(1, 300.0, nome="Consulta", codigo_tuss="10101012", tipo_atendimento=4)
    cat, c = montar([s], cs=[cfg(1, conv=180.0, nome="CONSULTA ELETIVA", tipo_atendimento=5)])
    r = m.calcular_servico(cat, c, 1)
    assert r.base == 180 and r.total == 180 and r.farol is None  # custo zero esperado: sem roxo
    t = m.textos_servico(s, c)
    assert t["nome"] == "CONSULTA ELETIVA" and t["codigo"] == "10101012" and t["tipo_atendimento"] == 5
    c.servicos[1] = cfg(1)
    assert m.calcular_servico(cat, c, 1).base == 300
    assert m.tipo_atendimento_efetivo(s, c) == 4


# --------------------------------------------------------------------------- produto: herança e FK

def test_produto_convertido_nao_herda_fk():
    p = Produto(10, "P", tipo_produto="MAT", custo=1, preco_venda_tabela=60, fonte_preco=FONTE_FIXO, fator_k=50)
    cat, c = montar([], [p], cp=[cfg(10, conv=40.0)])
    c.politicas["MAT"] = PoliticaTipoProduto("MAT", None, None, 30)
    assert m.valor_produto(p, c).valor == 40  # FK da política/cadastro NÃO se aplica
    c.produtos[10].fator_k = 10
    assert m.valor_produto(p, c).valor == 44


def test_produto_heranca_campo_a_campo_e_fixo_sem_fk():
    p = Produto(10, "P", tipo_produto="MAT", custo=1, preco_venda_tabela=60, fonte_preco=FONTE_FIXO,
                ultima_compra=20, fator_k=5)
    cat, c = montar([], [p], cp=[cfg(10, fator_k=0.0)])  # FK 0 na linha: não desce
    c.politicas["MAT"] = PoliticaTipoProduto("MAT", "PRECO DA ULTIMA COMPRA", None, 50)
    assert m.valor_produto(p, c).valor == 20  # fonte da política, FK 0 da linha
    c.produtos[10].fator_k = None
    assert m.valor_produto(p, c).valor == 30  # FK 50 da política
    c.politicas["MAT"] = PoliticaTipoProduto("MAT", None, None, 50)
    assert m.valor_produto(p, c).valor == 60  # fonte do cadastro = FIXO: sem FK
    c.produtos[10].valor_convertido = 0.0
    assert m.valor_produto(p, c).valor == 0  # 0,00 = gratuito


def test_produto_sem_fonte_zero_e_roxo_consolidado():
    p = Produto(10, "P", custo=5)
    s = serv(1, 100.0, itens=[("produto", 10, 1)])
    cat, c = montar([s], [p], cs=[cfg(1)], cp=[cfg(10)])
    pr = m.valor_produto(p, c)
    assert pr.valor == 0 and pr.sem_preco
    o = m.orcamento(cat, c, [{"tipo": "servico", "id": 1}])
    assert o.farol == m.ROXO


def test_taxa_zero_explicito():
    tx = taxa(20, 40)
    cat, c = montar([], taxas=[tx], ct=[cfg(20, conv=0.0)])
    assert m.valor_taxa(tx, c).valor == 0
    c.taxas[20].valor_convertido = None
    assert m.valor_taxa(tx, c).valor == 40


# --------------------------------------------------------------------------- invariantes

def _codigos(achados):
    return {a.codigo for a in achados}


def test_I1_item_sem_utiliza():
    cat, c = servico_simples(False, False, None, 100, [(10, 50, False, False)])
    assert "I1" in _codigos(m.validar_invariantes(cat, c))


def test_I2_pacote_sem_zerar():
    cat, c = servico_simples(False, True, None, 100, [(10, 50, False, True)])
    assert "I2" in _codigos(m.validar_invariantes(cat, c))


def test_I3_valor_duplicado_raiz_sub():
    sub = serv(2, 0.0, True)
    s = serv(1, 0.0, True, [("subservico", 2, 1)])
    cat, c = montar([s, sub], cs=[cfg(1, conv=50.0), cfg(2, conv=50.0)])
    assert "I3" in _codigos(m.validar_invariantes(cat, c))


def test_I4_zero_um_centavo():
    cat, c = servico_simples(False, False, 0.01, 100)
    ach = [a for a in m.validar_invariantes(cat, c) if a.codigo == "I4"]
    assert ach and ach[0].nivel == "ERRO"


def test_I5_produto_sem_custo():
    cat, c = servico_simples(False, False, None, 100, [(10, 50, False, True)])
    cat.produtos[10].custo = None
    assert "I5" in _codigos(m.validar_invariantes(cat, c))
    assert m.calcular_servico(cat, c, 1).farol == m.ROXO


def test_I6_receita_por_tipo_fecha():
    cat, c = _exemplo_composto()
    r = m.calcular_servico(cat, c, 1)
    assert sum(r.receita_por_tipo.values()) == pytest.approx(r.total)
    assert r.receita_por_tipo == {"servico": 90, "produto": 57, "taxa": 35}
    assert "I6" not in _codigos(m.validar_invariantes(cat, c))


def test_I7_somar_com_valor_cadastro():
    cat, c = servico_simples(True, False, None, itens_prod=[(10, 50, False, True)])
    cat.servicos[1].valor_cadastro = 10
    assert "I7" in _codigos(m.validar_invariantes(cat, c))


def test_I8_somar_sem_nada_que_conta():
    cat, c = servico_simples(True, False, None, itens_prod=[(10, 50, False, False)])
    assert "I8" in _codigos(m.validar_invariantes(cat, c))


def test_I9_fixo_com_composicao_sem_pacote():
    cat, c = servico_simples(False, False, None, 100, [(10, 50, False, True)])
    assert "I9" in _codigos(m.validar_invariantes(cat, c))


def test_I10_sub_zerado_com_item_sem_zerar():
    tx = taxa(20, 73.99)
    sub = serv(2, 20.0, itens=[("taxa", 20, 1)])
    s = serv(1, 100.0, False, [("subservico", 2, 1)])
    cat, c = montar([s, sub], taxas=[tx], cs=[cfg(1, pacote=True), cfg(2, zerar=True)], ct=[cfg(20)])
    assert "I10" in _codigos(m.validar_invariantes(cat, c))


def test_I11_I13_linha_check_base_e_sigma_total():
    cat, c = servico_simples(True, False, 266.16, itens_prod=[(10, 3000, False, True)])
    r = m.calcular_servico(cat, c, 1)
    q = m.quatro_linhas(cat, c, 1)
    assert q["proprio"] == r.base == r.arvore.base
    assert q["total"] == r.total == r.arvore.receita  # Σ = receita do Farol


def test_I12_combinado_sem_pacote_com_zerar():
    cat, c = _t23_25(False, True)
    assert "I12" in _codigos(m.validar_invariantes(cat, c))
    cat, c = _t23_25(True, True)
    assert "I12" not in _codigos(m.validar_invariantes(cat, c))


def test_zerar_sem_pacote_aviso():
    cat, c = servico_simples(False, False, None, 100, [(10, 50, True, True)])
    assert "ZERAR_SEM_PACOTE" in _codigos(m.validar_invariantes(cat, c))


def test_pacote_sem_efeito_em_somar_sem_valor():
    cat, c = servico_simples(True, True, None, itens_prod=[(10, 50, True, True)])
    assert "PACOTE_SEM_EFEITO" in _codigos(m.validar_invariantes(cat, c))
    assert m.valor(cat, c, 1) == 50


# --------------------------------------------------------------------------- circularidade

def test_circularidade_cortada_e_detectada():
    a = serv(1, 10.0, itens=[("subservico", 2, 1)])
    b = serv(2, 5.0, itens=[("subservico", 1, 1)])
    cat, c = montar([a, b], cs=[cfg(1), cfg(2)])
    assert m.detectar_ciclos(cat) == [[1, 2, 1]]
    r = m.calcular_servico(cat, c, 1)  # termina (corta pelo caminho visitado)
    assert r.total == 15
    assert any("ciclo" in x for x in r.avisos)
    assert "CICLO" in _codigos(m.validar_invariantes(cat, c))
    o = m.orcamento(cat, c, [{"tipo": "servico", "id": 1}])
    assert o.total == 15


def test_quantidades_multiplicam():
    p = prod(10, 10.0, custo=4)
    sub = serv(2, 5.0, itens=[("produto", 10, 3)])
    s = serv(1, 0.0, True, [("subservico", 2, 2)])
    cat, c = montar([s, sub], [p], cs=[cfg(1), cfg(2)], cp=[cfg(10)])
    r = m.calcular_servico(cat, c, 1)
    assert r.total == 2 * (5 + 3 * 10)
    assert r.custo == 2 * 3 * 4
