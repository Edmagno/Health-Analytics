import gspread
import pandas as pd
from garminconnect import Garmin
from datetime import date, timedelta
import os
import json

# --- CONFIGURAÇÕES E CREDENCIAIS (VERSÃO SEGURA PARA AUTOMAÇÃO) ---

# O script vai buscar as credenciais diretamente dos "Secrets" do GitHub Actions.
# Se esses Secrets não existirem, os valores serão vazios.
GARMIN_EMAIL = os.environ.get("GARMIN_EMAIL")
GARMIN_PASSWORD = os.environ.get("GARMIN_PASSWORD")
GCP_CREDENTIALS_JSON = os.environ.get("GCP_CREDENTIALS")

# Nomes da planilha e da aba
NOME_DA_PLANILHA = "Healthy Analytics"
NOME_DA_ABA = "DadosGarmin"


# --- FUNÇÃO PARA AUTENTICAR NO GOOGLE SHEETS ---
def autenticar_google_sheets():
    """
    Autentica no Google Sheets usando as credenciais fornecidas pelo
    GitHub Actions.
    """
    print("Autenticando no Google Sheets...")
    if not GCP_CREDENTIALS_JSON:
        print("ERRO: O segredo GCP_CREDENTIALS não foi encontrado. Abortando.")
        return None
        
    credentials_dict = json.loads(GCP_CREDENTIALS_JSON)
    return gspread.service_account_from_dict(credentials_dict)


# --- FUNÇÃO PRINCIPAL ---
def coletar_e_salvar_dados_garmin():
    """
    Conecta ao Garmin, busca os dados do dia anterior, e salva em uma
    nova linha no Google Sheets.
    """
    # Verifica se as credenciais do Garmin foram carregadas
    if not GARMIN_EMAIL or not GARMIN_PASSWORD:
        print("ERRO: As credenciais do Garmin (GARMIN_EMAIL, GARMIN_PASSWORD) não foram encontradas nos Secrets. Abortando.")
        return

    # Define a data de ontem
    data_alvo = date.today() - timedelta(days=1)
    data_str = data_alvo.isoformat()
    
    print(f"Iniciando coleta de dados do Garmin para a data: {data_str}")

    try:
        # 1. CONECTAR E BUSCAR DADOS DO GARMIN
        print("Conectando ao Garmin...")
        client = Garmin(GARMIN_EMAIL, GARMIN_PASSWORD)
        client.login()
        print("Conexão com o Garmin bem-sucedida!")

        # ... (O resto do código de coleta de dados permanece exatamente o mesmo)
        stats = client.get_stats(data_str)
        passos = stats.get('totalSteps', 0)
        calorias = stats.get('totalKilocalories', 0)
        
        sono_data = client.get_sleep_data(data_str)
        segundos_sono = sono_data.get('totalSleepSeconds', 0)
        horas_sono = round(segundos_sono / 3600, 2) if segundos_sono else 0
        
        bb_data = client.get_body_battery(data_str)
        body_battery_max = 0
        if bb_data:
            niveis_validos = [item['bodyBatteryLevel'] for item in bb_data if item and 'bodyBatteryLevel' in item]
            if niveis_validos:
                body_battery_max = max(niveis_validos)

        hr_data = client.get_heart_rates(data_str)
        fc_repouso = hr_data.get('restingHeartRate', 0)

        print("Dados coletados do Garmin:")
        print(f"- Passos: {passos}, Calorias: {calorias}, Sono: {horas_sono}h, Body Battery: {body_battery_max}, FC Repouso: {fc_repouso}")

        # 2. CONECTAR E ESCREVER NO GOOGLE SHEETS
        gc = autenticar_google_sheets()
        if not gc: # Se a autenticação falhar, para o script
            return
            
        spreadsheet = gc.open(NOME_DA_PLANILHA)