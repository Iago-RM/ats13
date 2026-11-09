import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestPainelE2E:

    @pytest.fixture(autouse=True)
    def setup_screenshot(self, browser, request):
        """Captura automaticamente a tela em caso de falha no teste (Requisito 3)."""
        yield
        if request.node.rep_call.failed:
            os.makedirs("tests/screenshots", exist_ok=True)
            screenshot_path = f"tests/screenshots/{request.node.name}.png"
            browser.save_screenshot(screenshot_path)

    @pytest.fixture(autouse=True)
    def hook_report(self, request):
        yield
        request.node.rep_call = getattr(request.node, "rep_call", None)

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(item, call):
        outcome = yield
        rep = outcome.get_result()
        setattr(item, "rep_call", rep)

    def test_solicitacao_cota_oxigenio_web(self, browser):
        # Obtém o caminho absoluto do arquivo painel.html
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        painel_path = os.path.fspath(os.path.join(base_dir, "src", "web", "painel.html"))
        
        # Abre o painel HTML no browser
        browser.get(f"file:///{painel_path}")

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