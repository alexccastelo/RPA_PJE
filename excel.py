import pandas as pd


def csv_to_excel(csv_file_path, excel_file_path):
    # Ler o arquivo CSV usando pandas sem cabeçalho, se ele já existir no CSV
    df = pd.read_csv(csv_file_path, header=None)

    # Definindo o cabeçalho personalizado
    headers = ["CPF", "Num. Processo", "Data Distrib.", "Data Consulta"]

    # Verifica se o DataFrame está vazio (sem cabeçalho)
    if df.empty:
        # Se estiver vazio, adicione apenas o cabeçalho
        df = pd.DataFrame(columns=headers)
    else:
        # Se não estiver vazio, adicione o cabeçalho aos dados
        df.columns = headers

    # Salvar os dados em um arquivo Excel começando da linha 1
    df.to_excel(excel_file_path, index=False, startrow=0)


# Exemplo de uso
csv_file = "processos.csv"  # Substitua pelo caminho do seu arquivo CSV
excel_file = "processos1.xlsx"  # Substitua pelo caminho desejado para o arquivo Excel

csv_to_excel(csv_file, excel_file)
