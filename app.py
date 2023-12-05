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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

numero_cpf = "017.062.273-88"

# Opções para o navegador Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Executa o Chrome em modo headless
driver = webdriver.Chrome()
driver.get("https://pje2g.trf1.jus.br/consultapublica/ConsultaPublica/listView.seam")
sleep(3)
driver.set_window_size(1920, 1080)
numerocpf = driver.find_element(By.XPATH, '//input[@id="fPP:dpDec:documentoParte"]')
numerocpf.send_keys(numero_cpf)
botao_pesquisar = driver.find_element(By.XPATH, "//input[@id='fPP:searchProcessos']")
botao_pesquisar.click()
sleep(5)
links_processos = driver.find_elements(By.XPATH, "//b[@class='btn-block']")
for processo in links_processos:
    processo.click()
    janelas = driver.window_handles
    # driver.switch_to.window(janelas[-1])
    driver.set_window_size(1920, 1080)
    wait = WebDriverWait(driver, 10)
    numero_processo = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-sm-12 ']"))
    )
    numero_processo = driver.find_elements(By.XPATH, "//div[@class='col-sm-12 ']")
    numero_processo = numero_processo[0].text 
    data_distribuicao = driver.find_elements(
        By.XPATH, "//div[@class='value col-sm-12 ']"
    )
    data_distribuicao = data_distribuicao[1]
    data_distribuicao = data_distribuicao.text
sleep(1)

workbook = openpyxl.load_workbook("processos_test.xlsx")

try:
    pagina_processo = workbook[numero_cpf]
except KeyError:
    # Se a planilha não existir, cria uma nova
    pagina_processo = workbook.create_sheet(numero_cpf)
    pagina_processo["A1"].value = "Número Processo"
    pagina_processo["B1"].value = "Data Distribuição"

    pagina_processo["A2"].value = numero_processo
    pagina_processo["B2"].value = data_distribuicao
    workbook.save("processos_test.xlsx")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
driver.quit()  # Este comando irá fechar todas as janelas do navegador e encerrar a sessão do WebDriver
