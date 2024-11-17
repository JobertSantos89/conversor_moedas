import requests
from tkinter import *

# Função para converter a moeda
def converter():
    try:
        # Pegue o valor inserido pelo usuário
        valor = float(entrada_valor.get())
        moeda_origem = entrada_moeda_origem.get().upper()
        moeda_destino = entrada_moeda_destino.get().upper()

        # URL da API com a chave fornecida
        url = f"https://v6.exchangerate-api.com/v6/7855d54f1099347569bb08e1/latest/{moeda_origem}"
        resposta = requests.get(url)
        dados = resposta.json()

        if dados['result'] == 'success':
            if moeda_destino in dados['conversion_rates']:
                taxa = dados['conversion_rates'][moeda_destino]
                resultado = valor * taxa
                label_resultado.config(text=f"{valor} {moeda_origem} = {resultado:.2f} {moeda_destino}")
            else:
                label_resultado.config(text="Moeda destino não encontrada.")
        else:
            label_resultado.config(text="Erro ao obter as taxas de câmbio.")

    except Exception as e:
        label_resultado.config(text=f"Erro: {str(e)}")

# Criação da interface com Tkinter
app = Tk()
app.title("Conversor de Moedas")
app.geometry("400x300")

Label(app, text="Valor a converter:").pack()
entrada_valor = Entry(app)
entrada_valor.pack()

Label(app, text="Moeda origem (ex: USD):").pack()
entrada_moeda_origem = Entry(app)
entrada_moeda_origem.pack()

Label(app, text="Moeda destino (ex: EUR):").pack()
entrada_moeda_destino = Entry(app)
entrada_moeda_destino.pack()

botao_converter = Button(app, text="Converter", command=converter)
botao_converter.pack()

label_resultado = Label(app, text="", font=("Helvetica", 14))
label_resultado.pack()

app.mainloop()
