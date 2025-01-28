import json
from tkinter import filedialog

def AdicionarDadosJson(nome_operacao, num_cards, meus_cards, camin_psd, camim_export):
    with open('dados.json', 'r', encoding='utf-8') as meu_json:
        dados = json.load(meu_json)
    dados_gravar = {
        f"{nome_operacao}": {
        "Numero card": int(num_cards),
        "Meus Cards": meus_cards,
        "Arquivo psd" : rf"{camin_psd}",
        "Pasta Export" : rf"{camim_export}"
    }}
    dados.append(dados_gravar)
    with open('dados.json', 'w', encoding='utf-8') as meu_json:
        json.dump(dados, meu_json, indent=4)

def AbirPasta():
    pasta = filedialog.askdirectory()
    return pasta

def AbirFile():
    caminho_arquivo_psd = filedialog.askopenfilename(
        title="Selecione um arquivo",
        filetypes=[("Arquivos PSD", "*.psd"), ("Todos os arquivos", "*.*")])
    return caminho_arquivo_psd

def TamanhoJson():
    with open('dados.json', 'r', encoding='utf-8') as meu_json:
        dados = json.load(meu_json)
    ndados = len(dados)
    return ndados

def NomeDosJson(idx):
    if (TamanhoJson() != 0) and (idx <= TamanhoJson()):
        with open('dados.json', 'r', encoding='utf-8') as meu_json:
            infos = json.load(meu_json)
        idx = idx - 1
        item = list(infos[idx].keys())[0]
        return item
    
def RemoverOperacoesJson(nome):
    with open('dados.json', 'r', encoding='utf-8') as arquivo:
        meus_dados = json.load(arquivo)
    new_date = meus_dados
    for i, card in enumerate(meus_dados):
        # Esse cara aqui list(card.keys())[0] ele me retorna o nome do meu podcast, sem um list() ele retorna um nome sujo, como assim?
        # Uma parada assim: dict_keys(['CARD FLOW PODCAST']) eu preciso do nome limpo, para fazer a comparação abaixo... Quando eu a converto em lista, automaticamente
        # O python o tranforma me lista, ai tira a porra do  dict_keys() e deixa apenas, ['CARD FLOW PODCAST'] com isso, eu só uso [0] para obter o nome de uma lista normal
       
        if list(card.keys())[0] == nome:
            new_date.remove(card)
    with open('dados.json', 'w', encoding='utf-8') as arquivo:
        json.dump(new_date, arquivo, indent=4)

def LimitarPalavra(palavra):
    if len(palavra) >= 30: 
        palavra2 = ""
        for i, c in enumerate(palavra):
            if i+1 <= 27:
                palavra2 += c
        return f"{palavra2}..."
    return palavra