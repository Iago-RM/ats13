class OxigenioInsuficienteError(Exception):
    """Exceção lançada quando não há oxigênio suficiente para o consumo ou emergência."""
    pass


class NivelEmergenciaInvalidoError(Exception):
    """Exceção lançada quando o nível de emergência informado é inválido."""
    pass


class GerenciadorRecursosMarte:
    def __init__(self, estoque_oxigenio: float, estoque_agua: float, num_astronautas: int):
        self.estoque_oxigenio = estoque_oxigenio
        self.estoque_agua = estoque_agua
        self.num_astronautas = num_astronautas

    def calcular_consumo_diario(self, consumo_por_astronauta_o2: float = 2.5, consumo_por_astronauta_agua: float = 3.0):
        total_o2 = self.num_astronautas * consumo_por_astronauta_o2
        total_agua = self.num_astronautas * consumo_por_astronauta_agua
        return {"oxigenio": total_o2, "agua": total_agua}

    def processar_consumo_diario(self):
        consumo = self.calcular_consumo_diario()
        if self.estoque_oxigenio < consumo["oxigenio"]:
            raise OxigenioInsuficienteError("Estoque de oxigênio insuficiente para o consumo diário.")
        
        self.estoque_oxigenio -= consumo["oxigenio"]
        self.estoque_agua -= consumo["agua"]
        return True

    def aplicar_taxa_emergencia(self, fator_multiplicador: float, telemetria_servico=None):
        if fator_multiplicador <= 0:
            raise NivelEmergenciaInvalidoError("O fator multiplicador de emergência deve ser maior que zero.")
        
        consumo_base = self.calcular_consumo_diario()["oxigenio"]
        consumo_emergencia = consumo_base * fator_multiplicador

        if self.estoque_oxigenio < consumo_emergencia:
            if telemetria_servico:
                telemetria_servico.enviar_alerta_crise(self.estoque_oxigenio, consumo_emergencia)
            raise OxigenioInsuficienteError("Oxigênio insuficiente durante taxa de emergência!")

        self.estoque_oxigenio -= consumo_emergencia
        return self.estoque_oxigenio

    def aplicar_racionamento(self, percentual_cota: float):
        if not (0 < percentual_cota <= 1):
            raise ValueError("O percentual de cota deve estar entre 0 e 1.")
        self.estoque_oxigenio *= percentual_cota
        self.estoque_agua *= percentual_cota