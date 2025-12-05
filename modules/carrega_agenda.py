import datetime
import pandas as pd

# Obter data e hora atuais
agora = datetime.datetime.now()
hora_atual = agora.hour
minuto_atual = agora.minute
data_atual = agora.date()
ano_atual = agora.year

# Carregar planilha
planilha_agenda = 'C:/Users/Vitor/PycharmProjects/PythonProject1/agenda.xlsx'
agenda = pd.read_excel(planilha_agenda)


# Função para converter diferentes formatos de data
def converter_data(valor):
    try:
        # Se já é datetime, retorna a data
        if isinstance(valor, datetime.datetime):
            return valor.date()

        # Se é string no formato "27-nov" (sem ano), adiciona o ano atual
        if isinstance(valor, str) and '-' in valor:
            # Adiciona o ano atual à string
            valor_com_ano = f"{valor}-{ano_atual}"
            return datetime.datetime.strptime(valor_com_ano, '%d-%b-%Y').date()

        # Tenta converter com pandas
        return pd.to_datetime(valor).date()
    except:
        return None


# Converter a coluna 'data'
agenda['data_convertida'] = agenda['data'].apply(converter_data)

descricao, responsavel, hora_agenda = [], [], []

for index, row in agenda.iterrows():
    # Pular linhas com data inválida
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