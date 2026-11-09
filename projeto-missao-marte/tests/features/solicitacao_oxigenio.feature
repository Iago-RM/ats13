Feature: Solicitação e Controle de Oxigênio no ECLSS Marte
  Como um engenheiro ou astronauta do habitat
  Quero gerenciar e solicitar cotas de oxigênio
  Para garantir a sobrevivência da tripulação em condições normais e de crise

  Scenario: Solicitação bem-sucedida de cota extra de oxigênio
    Given que o habitat possui um estoque inicial de 500.0 litros de oxigênio
    When eu solicito a adição de uma cota extra de 50.0 litros de oxigênio
    Then o estoque atualizado de oxigênio deve ser 550.0 litros

  Scenario: Tentativa de aplicação de taxa de emergência com oxigênio insuficiente
    Given que o habitat possui um estoque crítico de 5.0 litros de oxigênio
    When eu aplico uma taxa de emergência com fator multiplicador de 4.0
    Then o sistema deve disparar um alerta de crise e lançar uma exceção de oxigênio insuficiente