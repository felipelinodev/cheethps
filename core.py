from win32com.client import Dispatch
import os
import json
from functions_app import NomeDosJson


def StartarAcao(texto):
    nome_card = texto
    
    with open('dados.json', 'r') as meu_json:
        banco_de_dados = json.load(meu_json)

    operacao = None

    for dados in banco_de_dados:
        print(dados)
        if nome_card in dados:
            operacao = dados

    nome_operacao = nome_card
    numero_card = operacao[nome_operacao]["Numero card"]
    arquivo_psd = operacao[nome_operacao]["Arquivo psd"]
    pasta_exportacao = operacao[nome_operacao]["Pasta Export"]
    meu_cards = operacao[nome_operacao]["Meus Cards"]

    ps = Dispatch("Photoshop.Application")
    doc = ps.Open(arquivo_psd)

    class MudarConteudosPsd:
        def __init__(self):
            pass

        def MudarNomesConteudo(self, nome_camada, novo_conteudo):
            camada = doc.ArtLayers[nome_camada] #doc.ArLayers[] SERVE PARA PEGAR UMA CAMADA DENTRO DO DOCOMENTO POR NOME
            camada_conteudo = camada.TextItem
            camada_conteudo.Contents = novo_conteudo
                
        def ExportarConteudo(self, caminho, nomepng):
            options = Dispatch('Photoshop.PNGSaveOptions')
            options.compression = 4
            pngfile = f"{caminho}\\{nomepng}"
            doc.SaveAs(pngfile, options, True)

    mudar_conteudo = MudarConteudosPsd()

    for nome, conteudo in meu_cards.items():
        nome_card = nome

        for chave, valor in conteudo.items():
            if chave == "Camada_e_substitucao":
                for cam, subs in valor.items():
                    mudar_conteudo.MudarNomesConteudo(nome_camada=cam, novo_conteudo=subs)

        mudar_conteudo.ExportarConteudo(caminho=pasta_exportacao, nomepng=nome_card)


