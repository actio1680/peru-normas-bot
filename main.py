# El presente script se encuentra desplegado en la plataforma Heroku, por lo que, algunas de sus variables requieren una configuración en la plataforma en mención. A efectos de no causar perjuicio, también puede ser ejecutada de manera local realizando las ediciones respectivas. 

#Importar las dependencias necesarias
import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Crear opciones para inicializar el navegador en modo headless y deshabilitar el sandbox y el uso de la shell de desarrollador
op = webdriver.ChromeOptions()
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.add_argument("--headless")
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-sh-usage")

# Crear instancia del navegador y abrir la página web
driver = webdriver.Chrome(executable_path = os.environ.get("CHROMEDRIVER_PATH"), chrome_options = op)
driver.get("https://diariooficial.elperuano.pe/Normas")

# Esperar a que el elemento "article" esté disponible
wait = WebDriverWait(driver, 10)
parent_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article[@class='edicionesoficiales_articulos']")))

# Iterar sobre los elementos "article" y extraer los elementos "div" con los criterios de búsqueda especificados
with open('resultados.txt', 'w') as f:
    for parent_element in parent_elements:
        elements_1 = parent_element.find_elements(By.XPATH, ".//div[@class='ediciones_texto']")
        link = parent_element.find_element(By.XPATH, ".//div[@class='ediciones_botones']/ul/li/a[1]")
        url = link.get_attribute("href")
        elements = elements_1 
        content = " ".join([element.text for element in elements])
        # Escribir el contenido y la URL en el archivo de texto
        f.write(content + " " + url + "\n")

# Cerrar el navegador
driver.close()

# Token de acceso del bot de Telegram
TOKEN = "TOKEN_SECRETO"

# ID del chat al que quieres enviar el mensaje
CHAT_ID = CHAT_SECRETO

# Abrir el archivo de texto y leer su contenido
with open('resultados.txt', 'r') as f:
    text = f.read()

# Dividir el texto en varias partes para enviarlo en varios mensajes
MAX_MESSAGE_LENGTH = 4096
parts = [text[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(text), MAX_MESSAGE_LENGTH)]

# Enviar cada parte del texto como un mensaje individual
for part in parts:
    response = requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": part,
        }
    )

    # Comprobar si la solicitud se ha realizado con éxito
    if response.status_code == 200:
        print("Mensaje enviado con éxito")
    else:
        print(f"Error al enviar el mensaje: {response.text}")
