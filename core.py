from win32com.client import Dispatch
import os
import json
from funcoes_app import NomeDosJson


def StartarAcao(nome_opercao):
    
    with open('dados.json', 'r', encoding='utf-8') as meu_json:
        banco_de_dados = json.load(meu_json)

    #ESSA PARTE SERVE PARA FAZER O RECORTE DO OBJETO JSON DESEJADO
    operacao = None
    for dados in banco_de_dados:
        if nome_opercao in dados:
            operacao = dados


    # numero_card = operacao[nome_operacao]["Numero card"]
    arquivo_psd = operacao[nome_opercao]["Arquivo psd"]
    pasta_exportacao = operacao[nome_opercao]["Pasta Export"]
    meu_cards = operacao[nome_opercao]["Meus Cards"]

    #GARENTE QUE O PROGAM FUNCIONE COM DIVERSAS VERSÕES.
    def GerenciadorDeVersoes():
        versoes_photohop = ["Photoshop.Application", 
                            "Photoshop.Application.16", 
                            "Photoshop.Application.17",  
                            "Photoshop.Application.18", 
                            "Photoshop.Application.19", 
                            "Photoshop.Application.20",  
                            "Photoshop.Application.21",
                            "Photoshop.Application.22",
                            "Photoshop.Application.23",
                            "Photoshop.Application.24"]
        for versao in versoes_photohop:
            try:
                global ps
                ps = Dispatch(versao)
                break
            except Exception:
                continue
    GerenciadorDeVersoes()

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

    MudarConteudos = MudarConteudosPsd()
    for nome_card, conteudo in meu_cards.items():
        doc = ps.Open(arquivo_psd)

        for chave, valor in conteudo.items():
            if chave == "Camada_e_substitucao":
                for cam, subs in valor.items():
                    MudarConteudos.MudarNomesConteudo(nome_camada=cam, novo_conteudo=subs)

        MudarConteudos.ExportarConteudo(caminho=pasta_exportacao, nomepng=nome_card)
        doc.Close(2)

