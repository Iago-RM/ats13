import pytest
from src.gerenciador_recursos import GerenciadorRecursosMarte
from src.servico_telemetria import ServicoTelemetriaEspacial

@pytest.fixture(scope="session")
def parametros_iniciais_habitat():
    """Fixture global de módulo/sessão com parâmetros padrão do habitat."""
    return {
        "estoque_oxigenio_inicial": 500.0,
        "estoque_agua_inicial": 1000.0,
        "num_astronautas_padrao": 4
    }

@pytest.fixture
def gerenciador(parametros_iniciais_habitat):
    """Fixture de escopo function com preparação e limpeza (yield)."""
    # Setup
    gerenciador_instancia = GerenciadorRecursosMarte(
        estoque_oxigenio=parametros_iniciais_habitat["estoque_oxigenio_inicial"],
        estoque_agua=parametros_iniciais_habitat["estoque_agua_inicial"],
        num_astronautas=parametros_iniciais_habitat["num_astronautas_padrao"]
    )
    yield gerenciador_instancia
    # Tear down / limpeza pós-teste (se necessário)
    del gerenciador_instancia

@pytest.fixture
def servico_telemetria():
    return ServicoTelemetriaEspacial()