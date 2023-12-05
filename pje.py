import csv
import time

from flask import Flask, render_template, render_template_string, request, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# Carregar o HTML do formulário como uma string
with open("form.html", "r") as file:
    form_html = file.read()


@app.route("/")
def index():
    return render_template_string(form_html)


@app.route("/consulta_processos", methods=["POST"])
def consulta_processos():
    if request.method == "POST":
        cpf = request.form["cpf"]
        start_time = time.time()

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(
            "https://pje2g.trf1.jus.br/consultapublica/ConsultaPublica/listView.seam"
        )
        driver.set_window_size(1920, 1080)
        time.sleep(2)

        numerocpf = driver.find_element(
            By.XPATH, '//input[@id="fPP:dpDec:documentoParte"]'
        )
        numerocpf.send_keys(cpf)
        botao_pesquisar = driver.find_element(
            By.XPATH, "//input[@id='fPP:searchProcessos']"
        )
        botao_pesquisar.click()
        time.sleep(3)
        links_processos = driver.find_elements(By.XPATH, "//b[@class='btn-block']")

        quantidade_processos = len(links_processos)  # Contagem dos processos

        with open("processos.csv", "a", newline="") as file:
            writer = csv.writer(file)

            for i, link in enumerate(links_processos):
                main_window = driver.current_window_handle
                link.click()
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(2)

                numero_processo = driver.find_element(
                    By.XPATH, "//div[@class='col-sm-12 ']"
                )
                data_distribuicao = driver.find_element(
                    By.XPATH,
                    '//*[@id="j_id135:processoTrfViewView:j_id153"]/div/div[2]',
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

        # Preparando os dados para o template
        dados = []
        with open("processos.csv", "r") as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                dados.append(row)

        return render_template(
            "resultados.html",
            cpf=cpf,
            quantidade_processos=quantidade_processos,
            total_time=total_time,
            dados=dados,
        )
    else:
        return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)
