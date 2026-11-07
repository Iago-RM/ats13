import pytest
from src.gerenciador_recursos import (
    OxigenioInsuficienteError,
    NivelEmergenciaInvalidoError
)

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