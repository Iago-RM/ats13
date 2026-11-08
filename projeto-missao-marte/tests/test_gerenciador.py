import pytest
from src.gerenciador_recursos import (
    OxigenioInsuficienteError,
    NivelEmergenciaInvalidoError
)
from src.servico_telemetria import ServicoTelemetriaEspacial

class TestGerenciadorRecursos:

    @pytest.mark.parametrize(
        "num_astronautas, o2_por_pessoa, agua_por_pessoa, esperado_o2, esperado_agua",
        [
            (2, 2.5, 3.0, 5.0, 6.0),
            (4, 2.0, 2.5, 8.0, 10.0),
            (5, 3.0, 4.0, 15.0, 20.0),
        ]
    )
    def test_calculo_consumo_diario_parametrizado(
        self, gerenciador, num_astronautas, o2_por_pessoa, agua_por_pessoa, esperado_o2, esperado_agua
    ):
        gerenciador.num_astronautas = num_astronautas
        consumo = gerenciador.calcular_consumo_diario(o2_por_pessoa, agua_por_pessoa)
        
        assert consumo["oxigenio"] == esperado_o2
        assert consumo["agua"] == esperado_agua

    def test_processar_consumo_diario_sucesso(self, gerenciador):
        estoque_inicial_o2 = gerenciador.estoque_oxigenio
        consumo = gerenciador.calcular_consumo_diario()
        
        gerenciador.processar_consumo_diario()
        
        assert gerenciador.estoque_oxigenio == estoque_inicial_o2 - consumo["oxigenio"]

    def test_processar_consumo_diario_oxigenio_insuficiente(self, gerenciador):
        gerenciador.estoque_oxigenio = 2.0  # Menor que o consumo de 4 astronautas (10.0)
        
        with pytest.raises(OxigenioInsuficienteError, match="Estoque de oxigênio insuficiente"):
            gerenciador.processar_consumo_diario()

    def test_aplicar_taxa_emergencia_invalida(self, gerenciador):
        with pytest.raises(NivelEmergenciaInvalidoError):
            gerenciador.aplicar_taxa_emergencia(fator_multiplicador=0)

    def test_aplicar_racionamento_invalido(self, gerenciador):
        with pytest.raises(ValueError):
            gerenciador.aplicar_racionamento(percentual_cota=1.5)

    # --- Testes com Mocks (Requisito 2) ---
    def test_aplicar_taxa_emergencia_dispara_alerta_crise(self, gerenciador, mocker):
        mock_telemetria = mocker.Mock(spec=ServicoTelemetriaEspacial)
        gerenciador.estoque_oxigenio = 5.0
        fator_multiplicador = 4.0  # Demanda = 40.0 (> 5.0)
        
        with pytest.raises(OxigenioInsuficienteError, match="Oxigênio insuficiente durante taxa de emergência!"):
            gerenciador.aplicar_taxa_emergencia(
                fator_multiplicador=fator_multiplicador, 
                telemetria_servico=mock_telemetria
            )
        
        mock_telemetria.enviar_alerta_crise.assert_called_once_with(5.0, 40.0)

    def test_aplicar_taxa_emergencia_sem_crise_nao_dispara_alerta(self, gerenciador, mocker):
        mock_telemetria = mocker.Mock(spec=ServicoTelemetriaEspacial)
        gerenciador.estoque_oxigenio = 100.0
        fator_multiplicador = 2.0  # Demanda = 20.0 (<= 100.0)
        
        novo_estoque = gerenciador.aplicar_taxa_emergencia(
            fator_multiplicador=fator_multiplicador, 
            telemetria_servico=mock_telemetria
        )
        
        assert novo_estoque == 80.0
        mock_telemetria.enviar_alerta_crise.assert_not_called()