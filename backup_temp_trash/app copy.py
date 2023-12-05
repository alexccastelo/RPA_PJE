# sequence:
# 1. entrar na URL
# 2. digitar o número do cpf
# 3. clicar em pesquisar
# 4. entrar em cada um dos processos
# 5. após abrir nova janela
# 6. extrair numero do processo e data da distribuição
# 7. guardar no excel
# 8. criar nova sheet com o numero do processo
# 9. incluir:
#    1. célula B2 em diante: data da distribuição
#    2. célula C2 em diante: numero do cpf
#    3. célula D2 em diante: nome da parte
# CÓDIGO FUNCIONANDO PERFEITAMENTE EM 29/11/2023 ÀS 12:05 - UP TO GITHUB
# -----------------------------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from time import sleep
import openpyxl
import sys


# Função para formatar o CPF no estilo "000.000.000-00"
def formatar_cpf(cpf):
    cpf = "".join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return None
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


# Verifique se pelo menos um argumento foi fornecido (o primeiro argumento é o nome do script)
if len(sys.argv) >= 2:
    # O segundo argumento (índice 1) é o CPF passado da aplicação PHP
    numero_cpf = sys.argv[1]
    # Formate o CPF no estilo "000.000.000-00"
    numero_cpf_formatado = formatar_cpf(numero_cpf)
else:
    numero_cpf = ""
    numero_cpf_formatado = ""  # Agora você pode usar 'numero_cpf' e 'numero_cpf_formatado' na aplicação Python conforme necessário

# Opções para o navegador Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Executa o Chrome em modo headless
driver = webdriver.Chrome()
driver.get("https://pje2g.trf1.jus.br/consultapublica/ConsultaPublica/listView.seam")
sleep(3)
numerocpf = driver.find_element(By.XPATH, '//input[@id="fPP:dpDec:documentoParte"]')
numerocpf.send_keys("017.062.273-88")
botao_pesquisar = driver.find_element(By.XPATH, "//input[@id='fPP:searchProcessos']")
botao_pesquisar.click()
sleep(10)
links_processos = driver.find_elements(By.XPATH, "//b[@class='btn-block']")
for processo in links_processos:
    processo.click()
    sleep(3)
    janelas = driver.window_handles
    driver.switch_to.window(janelas[-1])
    driver.set_window_size(1920, 1080)
    numero_processo = driver.find_elements(By.XPATH, "//div[@class='col-sm-12 ']")
    numero_processo = numero_processo[0]
    numero_processo = numero_processo.text
    data_distribuicao = driver.find_elements(
        By.XPATH, "//div[@class='value col-sm-12 ']"
    )
    data_distribuicao = data_distribuicao[1]
    data_distribuicao = data_distribuicao.text
    workbook = openpyxl.load_workbook("processos_test.xlsx")
    try:
        pagina_processo = workbook[numero_processo]
        pagina_processo["A1"].value = "Numero Processo"
        pagina_processo["B1"].value = "Data Distribuição"
        pagina_processo["A2"].value = numero_processo
        pagina_processo["B2"].value = data_distribuicao
        workbook.save("processos.xlsx")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    except Exception as error:
        workbook.create_sheet(numero_processo)
        pagina_processo = workbook[numero_processo]
        pagina_processo["A1"].value = "Numero Processo"
        pagina_processo["B1"].value = "Data Distribuição"
        pagina_processo["A2"].value = numero_processo
        pagina_processo["B2"].value = data_distribuicao
        workbook.save("processos_test.xlsx")
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
driver.quit()  # Este comando irá fechar todas as janelas do navegador e encerrar a sessão do WebDriver
