import base64
from tkinter import filedialog, Tk, Label, Button, Canvas, PhotoImage
from tkinter import messagebox
from PIL import Image, ImageTk
import io, os
from datetime import datetime

# Função para decodificar a string base64 e salvar como PNG
def base64_para_imagem(base64_string):
    try:
        # Decodificar base64
        imagem_decodificada = base64.b64decode(base64_string)
        # Converter para objeto de imagem
        imagem = Image.open(io.BytesIO(imagem_decodificada))
        return imagem
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao decodificar: {str(e)}")
        return None

# Função para salvar a imagem em um caminho escolhido
def salvar_imagem(imagem):
    # Define o nome do arquivo com o formato de data e hora
    timestamp = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    nome_arquivo = f"{timestamp}.png"
    
    # Define o diretório 'PNGout'
    diretorio_saida = "PNGout"
    
    # Verifica se o diretório existe, caso contrário, cria-o
    if not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)
    
    # Caminho completo para salvar a imagem
    caminho_arquivo = os.path.join(diretorio_saida, nome_arquivo)
    
    # Salva a imagem
    try:
        imagem.save(caminho_arquivo, 'PNG')
        messagebox.showinfo("Sucesso", f"Imagem salva em {caminho_arquivo}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao salvar a imagem: {str(e)}")

# Função para criar a interface GUI para mostrar e baixar a imagem
def mostrar_interface(imagem):
    root = Tk()
    root.title("Conversor Base64 para PNG")

    canvas = Canvas(root, width=500, height=500)
    canvas.pack()

    # Redimensiona a imagem para caber no canvas (opcional)
    img = imagem.resize((500, 500))
    img_tk = ImageTk.PhotoImage(img)
    canvas.create_image(250, 250, anchor='center', image=img_tk)

    # Botão para salvar a imagem
    salvar_btn = Button(root, text="Salvar Imagem", command=lambda: salvar_imagem(imagem))
    salvar_btn.pack()

    # Mantém a janela aberta
    root.mainloop()

# Função para verificar se a string é um caminho de arquivo ou base64
def obter_base64_de_entrada(entrada):
    # Verifica se a entrada é um caminho para um arquivo
    if os.path.isfile(entrada):
        try:
            with open(entrada, "r") as file:
                return file.read().strip()  # Lê o conteúdo do arquivo
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível ler o arquivo: {str(e)}")
            return None
    else:
        return entrada.strip()  # Retorna a entrada como base64, assumindo que seja válida

# Função principal para conversão e GUI
def conversor_base64_para_png(entrada):
    base64_string = obter_base64_de_entrada(entrada)
    if base64_string:
        imagem = base64_para_imagem(base64_string)
        if imagem: mostrar_interface(imagem)
    else:
        imagem = base64_para_imagem(entrada)
        if imagem: mostrar_interface(imagem)

if __name__ == "__main__":
    # Entrada de base64 pela CLI ou caminho do arquivo
    entrada = input("Insira o código base64 ou o caminho para o arquivo: ")

    # Inicia o conversor
    conversor_base64_para_png(entrada)

