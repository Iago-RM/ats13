import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from src.gerenciador_recursos import GerenciadorRecursosMarte, OxigenioInsuficienteError
from src.servico_telemetria import ServicoTelemetriaEspacial

# Carrega o arquivo .feature correspondente
scenarios('../tests/features/solicitacao_oxigenio.feature')

@pytest.fixture
def contexto_teste():
    return {
        "gerenciador": None,
        "telemetria": ServicoTelemetriaEspacial(),
        "excecao_capturada": None
    }

@given(parsers.parse("que o habitat possui um estoque inicial de {estoque:f} litros de oxigênio"))
def estoque_inicial_normal(contexto_teste, estoque):
    contexto_teste["gerenciador"] = GerenciadorRecursosMarte(
        estoque_oxigenio=estoque, estoque_agua=1000.0, num_astronautas=4
    )

@given(parsers.parse("que o habitat possui um estoque crítico de {estoque:f} litros de oxigênio"))
def estoque_inicial_critico(contexto_teste, estoque):
    contexto_teste["gerenciador"] = GerenciadorRecursosMarte(
        estoque_oxigenio=estoque, estoque_agua=1000.0, num_astronautas=4
    )

@when(parsers.parse("eu solicito a adição de uma cota extra de {qtd:f} litros de oxigênio"))
def solicitar_cota_extra(contexto_teste, qtd):
    gerenciador = contexto_teste["gerenciador"]
    gerenciador.estoque_oxigenio += qtd

@when(parsers.parse("eu aplico uma taxa de emergência com fator multiplicador de {fator:f}"))
def aplicar_taxa_emergencia(contexto_teste, fator):
    gerenciador = contexto_teste["gerenciador"]
    telemetria = contexto_teste["telemetria"]
    try:
        gerenciador.aplicar_taxa_emergencia(fator_multiplicador=fator, telemetria_servico=telemetria)
    except OxigenioInsuficienteError as e:
        contexto_teste["excecao_capturada"] = e

@then(parsers.parse("o estoque atualizado de oxigênio deve ser {esperado:f} litros"))
def verificar_estoque_atualizado(contexto_teste, esperado):
    assert contexto_teste["gerenciador"].estoque_oxigenio == esperado

@then("o sistema deve disparar um alerta de crise e lançar uma exceção de oxigênio insuficiente")
def verificar_alerta_e_excecao(contexto_teste):
    assert contexto_teste["excecao_capturada"] is not None
    assert isinstance(contexto_teste["excecao_capturada"], OxigenioInsuficienteError)