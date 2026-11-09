import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.gerenciador_recursos import GerenciadorRecursosMarte
from src.servico_telemetria import ServicoTelemetriaEspacial

@pytest.fixture(scope="session")
def parametros_iniciais_habitat():
    return {
        "estoque_oxigenio_inicial": 500.0,
        "estoque_agua_inicial": 1000.0,
        "num_astronautas_padrao": 4
    }

@pytest.fixture
def gerenciador(parametros_iniciais_habitat):
    gerenciador_instancia = GerenciadorRecursosMarte(
        estoque_oxigenio=parametros_iniciais_habitat["estoque_oxigenio_inicial"],
        estoque_agua=parametros_iniciais_habitat["estoque_agua_inicial"],
        num_astronautas=parametros_iniciais_habitat["num_astronautas_padrao"]
    )
    yield gerenciador_instancia
    del gerenciador_instancia

@pytest.fixture
def servico_telemetria():
    return ServicoTelemetriaEspacial()

@pytest.fixture
def browser():
    """Fixture para gerenciar o ciclo de vida do WebDriver em modo headless (Requisito 3)."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1280, 720)
    
    yield driver
    
    driver.quit()