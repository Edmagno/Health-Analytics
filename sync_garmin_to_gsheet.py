import gspread
import pandas as pd
from garminconnect import Garmin
from datetime import date, timedelta
import os

# --- CONFIGURAÇÕES E CREDENCIAIS ---
# Para testar localmente, preencha suas informações aqui.
# Lembre-se que depois vamos mover isso para os "Secrets".

GARMIN_EMAIL = "edmagnogomes@gmail.com"
GARMIN_PASSWORD = "Ed!!88013785"

# O nome da sua planilha no Google Drive
NOME_DA_PLANILHA = "Healthy Analytics"
# O nome da aba/página específica da planilha
NOME_DA_ABA = "DadosGarmin"

# Caminho para o seu arquivo de credenciais do Google, dentro da pasta 'secrets'
# O 'os.path.join' garante que o caminho funcione em qualquer sistema operacional
GOOGLE_CREDENTIALS_FILE = os.path.join("secrets", "credentials.json")


# --- FUNÇÃO PRINCIPAL ---
def coletar_e_salvar_dados_garmin():
    """
    Conecta ao Garmin, busca os dados do dia anterior, e salva em uma
    nova linha no Google Sheets.
    """
    
    # Define a data de ontem para garantir que todos os dados do dia foram sincronizados
    data_alvo = date.today() - timedelta(days=1)
    data_str = data_alvo.isoformat()
    
    print(f"Iniciando coleta de dados do Garmin para a data: {data_str}")

    try:
        # 1. CONECTAR E BUSCAR DADOS DO GARMIN
        print("Conectando ao Garmin...")
        client = Garmin(GARMIN_EMAIL, GARMIN_PASSWORD)
        client.login()
        print("Conexão com o Garmin bem-sucedida!")

        # Busca as estatísticas gerais do dia
        stats = client.get_stats(data_str)
        
        # Pega dados específicos que queremos
        passos = stats.get('totalSteps', 0)
        calorias = stats.get('totalKilocalories', 0)
        
        # Busca dados de sono e converte para horas
        sono_data = client.get_sleep_data(data_str)
        segundos_sono = sono_data.get('totalSleepSeconds', 0)
        horas_sono = round(segundos_sono / 3600, 2) if segundos_sono else 0
        
        # Busca Body Battery (VERSÃO CORRIGIDA E MAIS ROBUSTA)
        bb_data = client.get_body_battery(data_str)
        body_battery_max = 0 # Define um valor padrão
        if bb_data: # Primeiro, checa se a lista de dados não está vazia
            # Agora, cria uma lista apenas com os valores que REALMENTE existem
            niveis_validos = [item['bodyBatteryLevel'] for item in bb_data if item and 'bodyBatteryLevel' in item]
            if niveis_validos: # Se encontrarmos algum valor válido na lista
                body_battery_max = max(niveis_validos)

        # Busca Frequência Cardíaca em Repouso
        hr_data = client.get_heart_rates(data_str)
        fc_repouso = hr_data.get('restingHeartRate', 0)

        print("Dados coletados do Garmin:")
        print(f"- Passos: {passos}")
        print(f"- Calorias: {calorias}")
        print(f"- Horas de Sono: {horas_sono}")
        print(f"- Body Battery Máx: {body_battery_max}")
        print(f"- FC Repouso: {fc_repouso}")

        # 2. CONECTAR E ESCREVER NO GOOGLE SHEETS
        print("\nConectando ao Google Sheets...")
        gc = gspread.service_account(filename=GOOGLE_CREDENTIALS_FILE)
        spreadsheet = gc.open(NOME_DA_PLANILHA)
        worksheet = spreadsheet.worksheet(NOME_DA_ABA)
        print("Conexão com o Google Sheets bem-sucedida!")

        # Prepara a nova linha na ordem correta dos cabeçalhos
        nova_linha = [
            data_str,
            passos,
            calorias,
            horas_sono,
            body_battery_max,
            fc_repouso
        ]

        # Adiciona a nova linha à planilha
        worksheet.append_row(nova_linha)
        
        print(f"\nSUCESSO! Nova linha de dados adicionada à planilha '{NOME_DA_PLANILHA}'.")

    except Exception as e:
        print(f"\nERRO: Ocorreu um problema durante o processo: {e}")

# --- EXECUÇÃO DO SCRIPT ---
if __name__ == "__main__":
    coletar_e_salvar_dados_garmin()