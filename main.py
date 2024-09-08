import requests, b64topng
from datetime import datetime
import time, os
import threading

if os.name == 'nt': 
    CL = "cls"
else: 
    CL = "clear"

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
    if neg: 
        p = input("N: ")
    else: 
        p = input("P: ")
    return p

def txt2img(url: str, headers: dict, result: dict, body: dict):
    request = requests.post(url, headers=headers, json=body)
    result['image'] = request.json()['images'][0]

def monitor_progress(progress_url):
    while True:
        try:
            # Obter progresso do servidor
            progress = requests.get(progress_url).json().get('progress')
            
            # Verificar se o progresso é None (se a resposta não tiver o campo 'progress')
            if progress is None:
                print("Erro: Não foi possível obter o progresso.")
                break

            progress = round(float(progress), 2)

            if progress == 100:
                print("Processo concluído!")
                break

            # Limpar a tela e mostrar o progresso
            os.system(CL)
            print(f"Gerando imagem... ({progress}%)")

            # Espera antes de verificar o progresso novamente
            time.sleep(3)

        except Exception as e:
            print(f"Erro ao verificar o progresso: {e}")
            break

def main():
    url, headers = get_url()
    txt2img_url = url + "/sdapi/v1/txt2img"
    progress_url = url + "/sdapi/v1/progress"

    result = {}  # Dicionário para armazenar o resultado da thread
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

    
    # Criar e iniciar a thread para gerar a imagem
    thread = threading.Thread(target=txt2img, args=(txt2img_url, headers, result, body))
    thread.start()

    # Monitorar o progresso
    monitor_progress(progress_url)

    # Aguardar a thread terminar se já não terminou
    thread.join()

    # Processar a imagem gerada
    img_b64 = result.get('image')

    if img_b64:
        # Salvar o Base64 em arquivo
        path = "B64out/" + datetime.today().strftime('B64.%Y-%m-%d_%H_%M_%S')
        os.makedirs("B64out", exist_ok=True)
        with open(path, "w") as f: 
            f.write(img_b64)
        print(f"Base64 salvo em: {path}")

        # Perguntar ao usuário o próximo passo
        _ = int(input("Mostrar imagem ou outro prompt? (1; 2) "))
        if _ == 1: 
            b64topng.conversor_base64_para_png(img_b64)
        else: 
            main()
    else:
        print("Erro: A imagem não foi gerada corretamente.")

if __name__ == "__main__":
    main()
