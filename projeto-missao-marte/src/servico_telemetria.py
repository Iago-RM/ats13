class ServicoTelemetriaEspacial:
    def enviar_relatorio_status(self, status_dict: dict) -> bool:
        # Simulação de envio de dados via rede para a Terra
        # Em produção, realizaria uma chamada HTTP/Socket
        return True

    def enviar_alerta_crise(self, estoque_atual: float, demanda: float) -> str:
        # Simulação de disparo de alerta crítico
        return f"ALERTA CRÍTICO: Estoque {estoque_atual} abaixo da demanda {demanda}."