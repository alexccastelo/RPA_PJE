import csv
import time

from flask import Flask, render_template_string, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# Carregar o HTML do formulário como uma string
with open("form.html", "r") as file:
    form_html = file.read()


@app.route("/")
def index():
    # Renderiza o formulário HTML
    return render_template_string(open("form.html").read())


@app.route("/consulta_processos", methods=["POST"])
def consulta_processos():
    mensagem = ""
    if request.method == "POST":
        cpf = request.form["cpf"]
        start_time = time.time()
        # Exemplo de mensagem
        mensagem = f"Processamento concluído para o CPF: {cpf}"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

    driver.get(
        "https://pje2g.trf1.jus.br/consultapublica/ConsultaPublica/listView.seam"
    )
    driver.set_window_size(1920, 1080)
    time.sleep(2)

    numerocpf = driver.find_element(By.XPATH, '//input[@id="fPP:dpDec:documentoParte"]')
    numerocpf.send_keys(cpf)
    botao_pesquisar = driver.find_element(
        By.XPATH, "//input[@id='fPP:searchProcessos']"
    )
    botao_pesquisar.click()
    time.sleep(3)
    links_processos = driver.find_elements(By.XPATH, "//b[@class='btn-block']")

    with open("processos.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(
                [
                    "CPF",
                    "Numero do Processo",
                    "Data de Distribuicao",
                    "Data da Pesquisa",
                ]
            )

        for i, link in enumerate(links_processos):
            main_window = driver.current_window_handle
            link.click()
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(2)

            numero_processo = driver.find_element(
                By.XPATH, "//div[@class='col-sm-12 ']"
            )
            data_distribuicao = driver.find_element(
                By.XPATH, '//*[@id="j_id135:processoTrfViewView:j_id153"]/div/div[2]'
            )
            data_pesquisa = time.strftime("%d/%m/%Y - %H:%M:%S")

            writer.writerow(
                [cpf, numero_processo.text, data_distribuicao.text, data_pesquisa]
            )

            driver.close()
            driver.switch_to.window(main_window)
            time.sleep(1)

    end_time = time.time()
    total_time = end_time - start_time

    # Renderiza a mesma página com a mensagem
    return render_template_string(form_html, mensagem=mensagem)


if __name__ == "__main__":
    app.run(debug=True)
