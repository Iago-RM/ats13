import os
from pathlib import Path
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestPainelE2E:

    @pytest.fixture(autouse=True)
    def setup_screenshot(self, browser, request):
        """Captura automaticamente a tela em caso de falha no teste (Requisito 3)."""
        yield
        if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
            os.makedirs("tests/screenshots", exist_ok=True)
            screenshot_path = f"tests/screenshots/{request.node.name}.png"
            browser.save_screenshot(screenshot_path)

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        rep = outcome.get_result()
        setattr(item, "rep_call", rep)

    def test_solicitacao_cota_oxigenio_web(self, browser):
        # Usa pathlib para gerar a URL do arquivo local de forma segura para o browser
        base_dir = Path(__file__).resolve().parent.parent
        painel_path = base_dir / "web" / "painel.html"
        url_file = painel_path.as_uri()  # Converte corretamente para file:///...
        
        # Abre o painel HTML no browser
        browser.get(url_file)

        # Espera explícita para garantir que o campo de entrada está carregado no DOM
        wait = WebDriverWait(browser, 10)
        input_cota = wait.until(EC.presence_of_element_located((By.ID, "cota-extra")))
        btn_solicitar = wait.until(EC.element_to_be_clickable((By.ID, "btn-solicitar")))

        # Interage com o formulário preenchendo a cota extra
        input_cota.send_keys("50.0")
        btn_solicitar.click()

        # Espera explícita até a mensagem de sucesso aparecer atualizando o DOM
        mensagem_sucesso = wait.until(
            EC.visibility_of_element_located((By.ID, "mensagem"))
        )
        
        assert "Sucesso! Cota de 50L de oxigênio aprovada." in mensagem_sucesso.text

        # Verifica se o nível de oxigênio atualizou na tela para 550.0
        nivel_o2 = browser.find_element(By.ID, "nivel-oxigenio").text
        assert nivel_o2 == "550.0"