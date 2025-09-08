# 📊 Healthy Analytics: Dashboard de Saúde e Produtividade

Este repositório contém o código para um dashboard pessoal e inteligente, projetado para unificar e analisar dados de saúde do Garmin Connect com outras fontes de dados, como Notion e Google Sheets. O projeto inclui um pipeline de dados automatizado e utiliza a API do Google Gemini para gerar insights.

## ✨ Visão Geral do Projeto

O objetivo deste projeto é criar uma visão 360º de métricas pessoais, combinando dados de atividade física, bem-estar e produtividade. A solução é composta por duas partes principais:

1.  **Pipeline de Dados Automatizado (Backend):** Um script Python que roda diariamente para extrair dados do Garmin e armazená-los de forma estruturada no Google Sheets.
2.  **Dashboard Interativo (Frontend):** Uma aplicação web construída com Streamlit que visualiza os dados e utiliza IA para fornecer análises e resumos.

## ⚙️ Arquitetura da Solução

*A arquitetura foi projetada para ser robusta, escalável e de baixo custo (totalmente gratuita).*

![Diagrama da Arquitetura](URL_DA_IMAGEM_DA_ARQUITETURA_AQUI)  ## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Coleta de Dados:**
    * `garminconnect` (para a API não oficial do Garmin)
    * `requests`
* **Armazenamento:** Google Sheets
* **Manipulação de Dados:** Pandas
* **Automação (Scheduler):** GitHub Actions
* **Dashboard:** Streamlit
* **Inteligência Artificial:** Google Gemini API
* **Controle de Versão:** Git & GitHub

## 🚀 Como Executar o Projeto Localmente

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Edmagno/Health-Analytics.git](https://github.com/Edmagno/Health-Analytics.git)
    cd Health-Analytics
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure suas credenciais:**
    * Renomeie o arquivo `secrets/example.credentials.json` para `secrets/credentials.json` e preencha com suas chaves da API do Google.
    * Adicione suas credenciais do Garmin e Gemini diretamente no script (ou configure variáveis de ambiente).

5.  **Execute o script de sincronização (se necessário):**
    ```bash
    python sync_garmin_to_gsheet.py
    ```

6.  **Inicie o dashboard:**
    ```bash
    streamlit run app.py
    ```

## 📈 Próximos Passos do Projeto

- [ ] Integrar a leitura de dados do Notion.
- [ ] Implementar a chamada para a API do Gemini para gerar insights diários.
- [ ] Adicionar mais visualizações e gráficos no dashboard Streamlit.
- [ ] Fazer o deploy da aplicação no Streamlit Community Cloud.