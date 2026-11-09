Projeto Missão Marte: ECLSS (Environmental Control and Life Support System)

Suíte de testes automatizados para validação do módulo de controle e monitoramento do habitat espacial de Marte, desenvolvida em Python utilizando pytest, Mocks (pytest-mock), automação Web E2E com Selenium WebDriver em modo headless, BDD com a sintaxe Gherkin (pytest-bdd) e Integração Contínua via GitHub Actions com medição de cobertura de código (pytest-cov).

🚀 Como Executar Localmente

1. Clonar o Repositório

git clone https://github.com/Iago-RM/ats13
cd projeto-missao-marte


2. Criar e Ativar o Ambiente Virtual

# Criar o ambiente virtual
python -m venv venv

# Ativar no Windows (PowerShell/CMD)
venv\Scripts\activate

# Ativar no Linux / macOS
source venv/bin/activate


3. Instalar as Dependências

pip install -r requirements.txt


4. Executar a Suíte de Testes

Para rodar a suíte completa de testes unitários, mocks, Selenium E2E e BDD exibindo o relatório de cobertura no terminal:

pytest --cov=src --cov-report=term-missing


🛠️ Tecnologias e Frameworks Utilizados

Linguagem: Python 3.10+

Testes Unitários e Integração: pytest (com Fixtures e Parametrização)

Isolamento e Mocks: pytest-mock (com MagicMock e validações de chamadas)

Automação Web E2E: selenium (Chrome em modo Headless)

BDD (Behavior-Driven Development): pytest-bdd (Sintaxe Gherkin com @given, @when, @then)

Cobertura de Código: pytest-cov

Integração Contínua: GitHub Actions (.github/workflows/pipeline.yml)

📂 Estrutura Recomendada do Repositório

projeto-missao-marte/
├── .github/
│   └── workflows/
│       └── pipeline.yml
├── features/
│   └── solicitacao_oxigenio.feature
├── src/
│   ├── __init__.py
│   ├── gerenciador_recursos.py
│   ├── servico_telemetria.py
│   └── web/
│       └── painel.html
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_gerenciador.py
│   ├── test_selenium_e2e.py
│   └── test_bdd.py
├── requirements.txt
└── README.md


📋 Requisitos do Sistema Sob Teste (SUT)

GerenciadorRecursosMarte: Regra de negócio responsável por validar estoques de oxigênio e água, calcular consumo por astronauta/dia, taxas de emergência e racionamento.

ServicoTelemetriaEspacial: Serviço externo responsável por enviar relatórios de status e disparar alertas de crise para a Terra.

Painel ControleWeb: Interface Web (painel.html) para solicitação de cota extra de oxigênio pelos astronautas.