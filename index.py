import requests
from tkinter import *
from tkinter import ttk

# Função para converter a moeda
def converter():
    try:
        # Validação do valor inserido
        valor = entrada_valor.get()
        if not valor.replace('.', '', 1).isdigit() or float(valor) <= 0:
            label_resultado.config(text="Por favor, insira um valor numérico positivo.", fg="red")
            return
        
        valor = float(valor)
        moeda_origem = selector_moeda_origem.get().upper()
        moeda_destino = selector_moeda_destino.get().upper()

        # URL da API com a chave fornecida
        url = f"https://v6.exchangerate-api.com/v6/7855d54f1099347569bb08e1/latest/{moeda_origem}"
        resposta = requests.get(url)
        dados = resposta.json()

        if dados['result'] == 'success':
            if moeda_destino in dados['conversion_rates']:
                taxa = dados['conversion_rates'][moeda_destino]
                resultado = valor * taxa
                label_resultado.config(text=f"{valor} {moeda_origem} = {resultado:.2f} {moeda_destino}", fg="green")
                # Adicionar ao histórico
                adicionar_ao_historico(valor, moeda_origem, resultado, moeda_destino)
            else:
                label_resultado.config(text="Moeda destino não encontrada.", fg="red")
        else:
            label_resultado.config(text="Erro ao obter as taxas de câmbio.", fg="red")

    except Exception as e:
        label_resultado.config(text=f"Erro: {str(e)}", fg="red")

# Função para adicionar ao histórico
def adicionar_ao_historico(valor, moeda_origem, resultado, moeda_destino):
    # Adicionar a conversão ao histórico
    historico.insert(0, f"{valor} {moeda_origem} = {resultado:.2f} {moeda_destino}")
    if len(historico.get(0, END)) > 3:
        historico.delete(3)  # Limitar o histórico a 3 entradas

# Função para inverter as moedas
def inverter_moedas():
    moeda_origem = selector_moeda_origem.get()
    moeda_destino = selector_moeda_destino.get()
    selector_moeda_origem.set(moeda_destino)
    selector_moeda_destino.set(moeda_origem)

# Criação da interface com Tkinter
app = Tk()
app.title("Conversor de Moedas")
app.geometry("500x500")
app.configure(bg="#2E2E2E")  # Fundo grafite

# Função para criar um botão estilizado
def criar_botao(parent, texto, comando):
    return Button(parent, text=texto, command=comando, bg="#3B3B3B", fg="white", font=("Arial", 12), relief="solid", bd=2, padx=20, pady=10, activebackground="#555", activeforeground="white")

# Função para criar entradas estilizadas
def criar_entrada(parent, fundo="#4D4D4D"):
    return Entry(parent, font=("Arial", 12), bg=fundo, fg="black", bd=2, relief="solid", width=30)

# Função para criar um seletor de moeda
def criar_selector(parent, moedas):
    var = StringVar(parent)
    var.set(moedas[0])  # Valor inicial
    menu = OptionMenu(parent, var, *moedas)
    menu.config(bg="#4D4D4D", fg="white", font=("Arial", 12), width=20)
    return var, menu

# Título
Label(app, text="Conversor de Moedas", font=("Helvetica Neue", 18, "bold"), bg="#2E2E2E", fg="white").pack(pady=20)

# Campo para valor
Label(app, text="Valor a converter:", font=("Arial", 12), bg="#2E2E2E", fg="white").pack()
entrada_valor = criar_entrada(app, fundo="white")  # Fundo branco para o campo de valor
entrada_valor.pack(pady=10)

# Seletor de moedas de origem
Label(app, text="Selecione a moeda origem:", font=("Arial", 12), bg="#2E2E2E", fg="white").pack()
moedas = ["USD", "EUR", "GBP", "BRL", "JPY", "AUD", "CAD", "CHF", "INR"]
selector_moeda_origem, menu_moeda_origem = criar_selector(app, moedas)
menu_moeda_origem.pack(pady=10)

# Seletor de moedas de destino
Label(app, text="Selecione a moeda destino:", font=("Arial", 12), bg="#2E2E2E", fg="white").pack()
selector_moeda_destino, menu_moeda_destino = criar_selector(app, moedas)
menu_moeda_destino.pack(pady=10)

# Botão de conversão
botao_converter = criar_botao(app, "Converter", converter)
botao_converter.pack(pady=15)

# Botão para inverter moedas
botao_inverter = criar_botao(app, "Inverter Moedas", inverter_moedas)
botao_inverter.pack(pady=10)

# Resultado da conversão
label_resultado = Label(app, text="", font=("Arial", 14), bg="#2E2E2E", fg="white")
label_resultado.pack(pady=10)

# Histórico de conversões
Label(app, text="Histórico de conversões:", font=("Arial", 12), bg="#2E2E2E", fg="white").pack(pady=10)
historico = Listbox(app, height=3, width=40, font=("Arial", 10), bd=2, bg="#4D4D4D", fg="white", selectmode=SINGLE)
historico.pack(pady=10)

app.mainloop()

