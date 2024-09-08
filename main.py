import requests, b64topng
from datetime import datetime
import time, os
import threading

if os.name == 'nt': CL = "cls"
else: CL = "clear"

def get_url():
    _ = input("O url é do AWS SageMaker? (s/n) ")
    if _.lower() == 's':
        id = input("ID ngrok: ")
        url = f"http://{id}-3-135-152-169.ngrok-free.app"
        headers = {"ngrok-skip-browser-warning": "true"}
    else:
        url = "http://brasa.onthewifi.com:7860"
        headers = {}
    return url, headers


def prompt(neg=False):
    if neg: p: str = input("N: ")
    else: p: str = input("P: ")
    return p

def txt2img(url: str, headers: dict, result: dict):
    body = {
                "prompt": prompt(),
                "negative_prompt": prompt(neg=True),
                "seed": -1,
                "sampler_name": "DPM++ 2M",
                "scheduler": "Karras",
                "batch_size": 1,
                "n_iter": 1,
                "steps": 35,
                "cfg_scale": 7,
                "width": 512,
                "height": 768
    }

    request = requests.post(url, headers=headers, json=body)
    result['image'] = request.json()['images'][0]

def main():
    url, headers = get_url()
    txt2img_url = url + "/sdapi/v1/txt2img"
    progress_url = url + "/sdapi/v1/progress"

    result = {}  # Dicionário para armazenar o resultado da thread

    # Criar e iniciar a thread para gerar a imagem
    thread = threading.Thread(target=txt2img, args=(txt2img_url, headers, result))
    thread.start()

    # Monitorar o progresso

    time.sleep(10)
    while thread.is_alive():
        os.system(CL)
        progress = round(requests.get(progress_url).json()['progress'], 2)
        print(f"Gerando imagem... ({progress * 100}%)")
        time.sleep(3)

    # Aguardar a thread terminar se já não terminou
    thread.join()

    # Processar a imagem gerada
    img_b64 = result['image']

    path = "B64out/" + datetime.today().strftime('B64.%Y-%m-%d_%H_%M_%S')
    with open(path, "w") as f: 
        f.write(img_b64)
    print(f"Base64 salvo em: {path}")
    _ = int(input("Mostrar imagem ou outro prompt? (1; 2) "))
    if _ == 1: b64topng.conversor_base64_para_png(img_b64)
    else: main()

if __name__ == "__main__":
    main()
