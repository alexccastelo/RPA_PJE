import pandas as pd


def csv_to_excel(csv_file_path, excel_file_path):
    # Ler o arquivo CSV usando pandas
    df = pd.read_csv(csv_file_path)

    # Salvar os dados em um arquivo Excel
    df.to_excel(excel_file_path, index=False)


# Exemplo de uso
csv_file = "processsos.csv"  # Substitua pelo caminho do seu arquivo CSV
excel_file = "processsos1.xlsx"  # Substitua pelo caminho desejado para o arquivo Excel

csv_to_excel(csv_file, excel_file)