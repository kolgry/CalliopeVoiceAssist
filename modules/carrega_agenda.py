import datetime
import pandas as pd
import os

agora = datetime.datetime.now()
hora_atual = agora.hour
minuto_atual = agora.minute
data_atual = agora.date()
ano_atual = agora.year

planilha_agenda = 'agenda.xlsx'

if not os.path.exists(planilha_agenda):
    print(f"[INFO] Arquivo {planilha_agenda} não encontrado. Criando agenda vazia...")
    agenda = pd.DataFrame()
else:
    agenda = pd.read_excel(planilha_agenda)


def converter_data(valor):
    try:
        if isinstance(valor, datetime.datetime):
            return valor.date()

        if isinstance(valor, str) and '-' in valor:
            valor_com_ano = f"{valor}-{ano_atual}"
            return datetime.datetime.strptime(valor_com_ano, '%d-%b-%Y').date()

        return pd.to_datetime(valor).date()
    except:
        return None


agenda['data_convertida'] = agenda['data'].apply(converter_data)

descricao, responsavel, hora_agenda = [], [], []

for index, row in agenda.iterrows():
    if row["data_convertida"] is None or pd.isna(row["data_convertida"]):
        continue

    data = row["data_convertida"]

    # Converter hora
    try:
        hora_completa = datetime.datetime.strptime(str(row['hora']), '%H:%M:%S')
        hora = hora_completa.hour
    except:
        continue

    if data_atual == data:
        if hora >= hora_atual:
            descricao.append(row['descricao'])
            responsavel.append(row['responsavel'])
            hora_agenda.append(row['hora'])


def carrega_agenda():
    if descricao:
        return descricao, responsavel, hora_agenda
    else:
        return False