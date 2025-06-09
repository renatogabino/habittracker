# Rastreador de Hábitos - TP Engenharia de Software II

## 1. Membros do Grupo

*   Leo Soares de Oliveira Junior
*   Renato Gabino Diniz

## 2. Explicação do Sistema

O "Rastreador de Hábitos" é uma aplicação de desktop simples desenvolvida para ajudar os usuários a monitorar e manter seus hábitos diários. A interface gráfica permite uma interação intuitiva para gerenciar e visualizar o progresso.

**Funcionalidades Principais:**

*   **Adicionar Novos Hábitos:** Os usuários podem adicionar novos hábitos que desejam rastrear.
*   **Marcar Conclusão:** Para cada hábito, o usuário pode marcar se ele foi concluído ou não em uma data específica.
*   **Controle de Data:**
    *   Um controlador de data permite ao usuário navegar para datas passadas para visualizar ou registrar o status dos hábitos nesses dias.
    *   Não é possível navegar para datas futuras (posteriores ao dia atual real).
    *   Um botão "Hoje" permite retornar rapidamente à data atual.
*   **Visualização de Sequência (Streak):**
    *   Para cada hábito, a aplicação exibe a sequência atual de dias consecutivos em que o hábito foi concluído.
    *   Se um hábito foi concluído na data visualizada, a sequência inclui essa data.
    *   Se um hábito não foi concluído na data visualizada, mas possuía uma sequência ativa no dia anterior, essa sequência anterior é exibida. Caso contrário, a sequência é zero.
*   **Deletar Hábitos:** Os usuários podem remover hábitos que não desejam mais rastrear.
*   **Persistência de Dados:** As informações sobre os hábitos e suas conclusões são salvas localmente em um arquivo JSON (`habits_data.json`), permitindo que os dados persistam entre as sessões de uso da aplicação.

## 3. Tecnologias Utilizadas
*   **Linguagem de Programação:** Python 3
*   **Interface Gráfica (GUI):** Flet
    *   Um framework Python que permite criar aplicações interativas multiusuário e multiplataforma (web, desktop, mobile) de forma rápida.
*   **Testes de Unidade:** Pytest
    *   Um framework de testes para Python que facilita a escrita de testes pequenos e legíveis, mas escaláveis.
*   **Persistência de Dados:** JSON
    *   Utilizado para armazenar os dados dos hábitos de forma simples e legível.
*   **Gerenciamento de Data da Aplicação:** Módulo customizado (`app_date_manager.py`)
    *   Para controlar a data de referência dentro da aplicação, permitindo a navegação no tempo para fins de visualização e registro.
*   **Controle de Versão:** Git
*   **Hospedagem do Repositório:** GitHub
*   **Integração Contínua/Entrega Contínua (CI/CD):** GitHub Actions
    *   Configurado para executar automaticamente os testes de unidade a cada commit nos sistemas operacionais Linux, macOS e Windows, garantindo a integridade do código e facilitando a detecção precoce de regressões.
