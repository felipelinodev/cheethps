import customtkinter
from tkinter import PhotoImage
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("tema.json")
from funcoes_app import AdicionarDadosJson, AbirPasta, AbirFile, TamanhoJson, NomeDosJson, RemoverOperacoesJson, LimitarPalavra
from core import StartarAcao
from PIL import Image
from time import sleep

lista_cards = []
contador_textbox = 0

cards_salvos = []

logo = customtkinter.CTkImage(
    light_image=Image.open('logotipo.png'),
    dark_image=Image.open('logotipo.png'),
    size=(176, 36))

class Modal(customtkinter.CTk):
    def __init__(self, janela_parente, titulo, tipo, fun, resolution="300x170"):
        self.titulo = titulo
        self.janela_parent = janela_parente
        self.fun = fun
        self.tipo = tipo
        
        super().__init__()
        self.modal = customtkinter.CTkToplevel(janela_parente)
        self.modal.title(self.titulo)
        self.modal.geometry(resolution)
        self.modal.configure(fg_color="#D9DFF3")
        self.modal.resizable(False, False)
        self.modal.transient(app)
        self.modal.grab_set()

        if tipo == "Esclude":
            self.ModalEcluirItem()
        elif tipo == "Salvar":
            self.ModalSalvarItems()
        elif tipo == "Mini_Salvar":
            self.ModalMiniSalve()
        
    def ModalEcluirItem(self):            

        label = customtkinter.CTkLabel(self.modal, text="Tem certeza?", font=("Roboto", 20, "bold"), fg_color="#D9DFF3")
        label.pack(pady=9)

        label2 = customtkinter.CTkLabel(self.modal, text="A exlusão das informações é permanente!", font=("Roboto", 14), fg_color="#D9DFF3")
        label2.pack()

        label3 = customtkinter.CTkLabel(self.modal, text="Deseja excluir?", font=("Roboto", 14), fg_color="#D9DFF3")
        label3.pack()

        btn_nao_excluir = customtkinter.CTkButton(self.modal, text="NÃO", width=50, height=39, font=("Roboto", 14, "bold"), fg_color="#ACBBF1", text_color="#D9DFF3", hover_color="#899EDB", command=lambda: self.modal.destroy())
        btn_nao_excluir.pack(pady=0, side="left", padx=(45, 0))

        btn_excluir = customtkinter.CTkButton(self.modal, text="SIM PAGAR", width=150, height=39, fg_color="#FF96AD", text_color="#EBECF0",  font=("Roboto", 14, "bold"), hover_color="#E36B85", command=self.fun)
        btn_excluir.pack(pady=0, side="left", padx=5)
        btn_excluir.bind("<Button-1>", lambda event: self.modal.destroy())    

    def ModalSalvarItems(self):
        label_save = customtkinter.CTkLabel(self.modal, text="Tem certeza?", font=("Roboto", 20, "bold"), fg_color="#D9DFF3")
        label_save.pack(pady=9)

        label_save2 = customtkinter.CTkLabel(self.modal, text="Deseja salvar essa Ação?", font=("Roboto", 14), fg_color="#D9DFF3")
        label_save2.pack()

        btn_nao_excluir = customtkinter.CTkButton(self.modal, text="NÃO", width=50, height=39, font=("Roboto", 14, "bold"), fg_color="#ACBBF1", text_color="#D9DFF3", hover_color="#899EDB", command=lambda: self.modal.destroy())
        btn_nao_excluir.pack(pady=0, side="left", padx=(45, 0))

        btn_excluir = customtkinter.CTkButton(self.modal, text="SIM SALVAR", width=150, height=39, command=self.fun)
        btn_excluir.pack(pady=0, side="left", padx=5)
        btn_excluir.bind("<Button-1>", lambda event: self.modal.destroy())   

    def ModalMiniSalve(self):
        btn_nao_excluir = customtkinter.CTkButton(self.modal, text="NÃO", width=50, height=39, font=("Roboto", 14, "bold"), fg_color="#ACBBF1", text_color="#D9DFF3", hover_color="#899EDB", command=lambda: self.modal.destroy())
        btn_nao_excluir.pack(pady=0, side="left", padx=(23, 0))

        btn_excluir = customtkinter.CTkButton(self.modal, text="SALVAR", width=150, height=39, command=self.fun)
        btn_excluir.pack(pady=0, side="left", padx=5)
        btn_excluir.bind("<Button-1>", lambda event: self.modal.destroy())   


class AlertModal(customtkinter.CTk):
    def __init__(self, titulo, win, descricao):
        super().__init__()
        self.alert = customtkinter.CTkToplevel(win)
        self.alert.title(titulo)
        self.alert.geometry("300x130")
        self.alert.configure(fg_color="#FFEEF2")
        self.alert.transient(win)
        self.alert.grab_set()
        self.alert.resizable(False, False)

        self.label_save = customtkinter.CTkLabel(self.alert, text=titulo, font=("Roboto", 20, "bold"))
        self.label_save.grid(row=0, pady=9)

        self.label_save2 = customtkinter.CTkLabel(self.alert, text=descricao, font=("Roboto", 14))
        self.label_save2.grid(row=1)

        self.btn_ok = customtkinter.CTkButton(self.alert, text="OK", width=276, height=39, command=lambda: None)
        self.btn_ok.grid(row=2, pady=10, sticky="s", padx=10)
        self.btn_ok.bind("<Button-1>", lambda event: self.alert.destroy())  

class ModelTextosCards(customtkinter.CTk):
    def __init__(self, jan, valores, nome_card):
        self.nome_card = nome_card
        self.jan = jan
        self.valores = valores
        super().__init__()
        self.modal = customtkinter.CTkToplevel(jan)
        self.modal.geometry("300x180")
        self.modal.title(nome_card)
        self.modal.configure(fg_color="#D9DFF3")
        self.modal.resizable(False, False)
        self.modal.transient(jan)

        self.container_cards = customtkinter.CTkScrollableFrame(self.modal, width=280, height=120, fg_color="#EBECF0", corner_radius=6, border_width=1.2)
        self.container_cards.grid(sticky="ns")

        self.Items()
    def Items(self):
        def RevoverLinha(chave, card, delcard):
            meus_cards_obj_json[self.nome_card]["Camada_e_substitucao"].pop(chave)
            card.destroy()
            delcard.destroy()
        cont = 0
        for c, v in self.valores.items():
            cont = cont + 1

            #FUNÇÃO ESPECIFICA PARA LIMITAR O NUMERO DE PALAVRAS NO CARD
            pares = LimitarPalavra(f"{c} ⇄ {v}")

            card = customtkinter.CTkLabel(self.container_cards, text=pares, font=("Roboto",12), fg_color="#D9DFF3", corner_radius=2, text_color="#1854FF", width=250, height=20)
            card.grid(column=1, pady=5, sticky="nsew", row=cont)
       
            del_card = customtkinter.CTkButton(self.container_cards, width=20, height=20, text="-", font=("Roboto", 12),  corner_radius=3, fg_color="#FF96AD", hover_color="#E36B85")
            del_card.grid(padx=5, column=2, row=cont)
            del_card.bind("<Button-1>", lambda event, chave=c, btn_card=card, btn_del=del_card: RevoverLinha(chave, btn_card, btn_del))
            
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("CheetahPS 1.0")
        self.iconbitmap("icone.ico")
        self.geometry("1000x665")
        self.resizable(False, False)
        #A função grid_columnconfigure recebe 2 argumentos
        #O numero da coluna (0, ) e weight que se a coluna ocupa todo o espaço ou não, se for maior que 0 no caso um significa que sim, tudo que for colocado nessa coluna
        #Deve ocupar todo o espaço, por isso o weight recebe 1
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.janela_acao = customtkinter.CTkTabview(self)
        self.janela_acao.grid(row=0, column=0, padx=20, pady=20, sticky="ewns")#Esse "ewns" significa que a interface deve ocupar todo o espaço disponivel, mas só funciona com o weight
        #Do grid_columnconfigure e grid_rowconfigure = a 1.

        self.janela_acao.add(" CRIAR AÇÃO ")
        self.janela_acao.add(" EXECUTAR ")


        self.logo_label = customtkinter.CTkLabel(self.janela_acao.tab(" CRIAR AÇÃO "), text="", image=logo)
        self.logo_label.grid(row=0, column=0, sticky="w")

        # Basicamente se eu quiser centralizar algo, eu boto todo mundo para crescer menos quem vai ser centralizado
        self.janela_acao.tab(" CRIAR AÇÃO ").grid_columnconfigure(0, weight=1)
        self.janela_acao.tab(" CRIAR AÇÃO ").grid_columnconfigure(1, weight=0) #Não vai crescer
        self.janela_acao.tab(" CRIAR AÇÃO ").grid_columnconfigure(2, weight=0) #Não vai crescer
        self.janela_acao.tab(" CRIAR AÇÃO ").grid_columnconfigure(3, weight=1)

        self.janela_acao.tab(" EXECUTAR ").grid_columnconfigure(0, weight=1) 
        self.janela_acao.tab(" EXECUTAR ").grid_columnconfigure(1, weight=0)
        self.janela_acao.tab(" EXECUTAR ").grid_columnconfigure(2, weight=0)
        self.janela_acao.tab(" EXECUTAR ").grid_columnconfigure(3, weight=0)
        self.janela_acao.tab(" EXECUTAR ").grid_columnconfigure(4, weight=1)
        self.TabCricarAcao()
        self.TabExecutarAcao()


    def ValidarFormulariosNumero(self, event):
        event.widget.configure(state="normal")

        char = event.widget.get()

        if not char.isnumeric():
            event.widget.delete(0, "end")
            
    
    def TabCricarAcao(self):
        global card_completo
        card_completo = {}

        global meus_cards_obj_json
        meus_cards_obj_json = {}
    
        global valores_registro_dados
        valores_registro_dados = []


        def MostrarCamSubs(nome):
            infos_cards = meus_cards_obj_json[nome]["Camada_e_substitucao"]
            if len(infos_cards) > 0:
                ModelTextosCards(app, valores=infos_cards, nome_card=nome)
        def RemoverCardIndividual(wi1, wi2, nome):
            wi1.destroy()
            wi2.destroy()
            card_completo.pop(nome)
            cards_salvos.remove(nome)
            print(cards_salvos)


        registro_dados = customtkinter.CTkScrollableFrame(self.janela_acao.tab(" CRIAR AÇÃO "), width=150, height=150, fg_color="#EBECF0", corner_radius=6, border_width=1.2)
        registro_dados.grid(row=4, column=2, sticky="ns", pady=(50, 30)) # Com esse cara pady=(50, 0) e Sticky="n" eu falo, só bota padding em cima.

        def InsertTexBox(nome):
            global contador_textbox
            contador_textbox = contador_textbox + 1

            input_registro_dados = customtkinter.CTkButton(registro_dados, width=110, text=nome, font=("Roboto", 10, "bold"), text_color="#1854FF", height=30, fg_color="#D9DFF3", corner_radius=3, hover_color="#CAD8FF", command= lambda: MostrarCamSubs(nome))
            input_registro_dados.grid(pady=5, row=contador_textbox, column=1) 

            btn_input_registro_dados_exclude = customtkinter.CTkButton(registro_dados, width=30, height=30, text="x", font=("Roboto", 12),  corner_radius=3, fg_color="#FF96AD", hover_color="#E36B85", command=RemoverCardIndividual)
            btn_input_registro_dados_exclude.grid(padx=5, row=contador_textbox, column=2)
            btn_input_registro_dados_exclude.bind("<Button-1>", lambda event: RemoverCardIndividual(input_registro_dados, btn_input_registro_dados_exclude, nome))

        def NomeOpercao():
            lb_nome_operacao = customtkinter.CTkLabel(self.janela_acao.tab(" CRIAR AÇÃO "), text="Nome operação", font=("Roboto", 14), fg_color="#D9DFF3")
            lb_nome_operacao.grid(row=2, column=1, sticky="w", pady=5)

            global entrada_nome_operacao
            entrada_nome_operacao = customtkinter.CTkEntry(self.janela_acao.tab(" CRIAR AÇÃO "), placeholder_text="Card Operação", width=295, height=39, font=("Roboto", 14))
            entrada_nome_operacao.grid(row=3, column=1, sticky="w")

        def NumeroCards():
            lb_num_operacao = customtkinter.CTkLabel(self.janela_acao.tab(" CRIAR AÇÃO "), text="Numero Cards", font=("Roboto", 14), fg_color="#D9DFF3")
            lb_num_operacao.grid(row=2, column=2, sticky="w", pady=5, padx=20)

            global entrada_num_cards
            entrada_num_cards = customtkinter.CTkEntry(self.janela_acao.tab(" CRIAR AÇÃO "), placeholder_text="5", width=171, height=39, font=("Roboto", 14))
            entrada_num_cards.grid(row=3, column=2, padx=20)
            entrada_num_cards.bind("<KeyRelease>", self.ValidarFormulariosNumero)

        def GroupDados():
            grupo_dados = customtkinter.CTkFrame(self.janela_acao.tab(" CRIAR AÇÃO "), width=295, border_color="#D9DFF3")
            grupo_dados.grid(row=4, column=1, sticky="ns", pady=40)
            grupo_dados.columnconfigure((0, 1, 2, 3), weight=1)

            label_grupo_dados = customtkinter.CTkLabel(grupo_dados, text="Criar Cards", font=("Roboto", 14))
            label_grupo_dados.grid(row=5, column=0, columnspan=4, sticky="w", pady=5)

            global entrada_nome_card
            entrada_nome_card = customtkinter.CTkEntry(grupo_dados, placeholder_text="Nome Card", width=295, height=39, font=("Roboto", 14))
            entrada_nome_card.grid(row=6, column=0, columnspan=5, sticky="ew", padx=0, pady=5)

            global entrada_nome_camada
            entrada_nome_camada = customtkinter.CTkEntry(grupo_dados, placeholder_text="Camada", width=85, height=20, font=("Roboto", 14))
            entrada_nome_camada.grid(row=7, column=0, padx=0, sticky="ew")

            label_simbol_subs = customtkinter.CTkLabel(grupo_dados, text="⇄", font=("Roboto", 20), width=39, height=20, fg_color="#789BFF", corner_radius=6)
            label_simbol_subs.grid(row=7, column=1, padx=1)

            global entrada_novo_texto
            entrada_novo_texto = customtkinter.CTkEntry(grupo_dados, placeholder_text="Texto", width=85, height=20, font=("Roboto", 14))
            entrada_novo_texto.grid(row=7, column=2, padx=0, sticky="ew", pady=5)



            
            def Add_nome_camada_chave_valor():
                nome = entrada_nome_card.get()
                chave = entrada_nome_camada.get()
                valor = entrada_novo_texto.get()
                if not nome:
                    AlertModal(win=app, titulo="Dados Ausentes", descricao="Você precisa dá um nome ao Card.")
                elif (not chave) or (not valor) :
                    AlertModal(win=app, titulo="Dados Ausentes", descricao="O campos Camada ou Texto está vazio.")
                else:
                    def Add():
                        def AddCardsmeucards_json(nome, valores):
                            #SE O OBJETO NÃO EXISTIR ELE JÁ CRIA O OBJETO COM TODA A ESTRUTURA ADEQUADA
                            if nome not in meus_cards_obj_json:
                                meus_cards_obj_json[nome] = {
                                    "Camada_e_substitucao": {},
                                    "img": "null"
                                    }
                            #ESSE NOME JÁ EXISTINDO, ELE APENAS ADICIONA PAR DE CHAVE E VALORES A ESSA ESTRUTURA      
                            meus_cards_obj_json[nome]["Camada_e_substitucao"].update(valores)
                          

                        AddCardsmeucards_json(nome, {chave:valor})
                        
                        
                    Modal(app, "Felipe", tipo="Mini_Salvar",fun=Add, resolution="250x80")

            def SalveInTextbox():
                if (not entrada_nome_card.get()) or (not entrada_nome_camada.get()) or (not entrada_novo_texto.get()):
                    AlertModal(win=app, titulo="Dados Ausentes", descricao="Algúm campo está vazio.")
                elif(entrada_nome_card.get() in cards_salvos):
                    AlertModal(win=app, titulo="Card já Existe", descricao="Esse card já foi salvo.")
                elif(len(meus_cards_obj_json[entrada_nome_card.get()]["Camada_e_substitucao"]) == 0):
                    AlertModal(win=app, titulo="Dados Ausentes", descricao="Faltam dados de alteração camadas.")
                else:
                    def SalvarCards():
                        InsertTexBox(entrada_nome_card.get())
                        card_completo.update(meus_cards_obj_json)
                    Modal(app, "Felipe", tipo="Salvar",fun=SalvarCards)
                    
                    cards_salvos.append(entrada_nome_card.get())
                
            btn_add = customtkinter.CTkButton(grupo_dados, text="+", width=39, height=20, font=("Roboto", 17, "bold"), command=Add_nome_camada_chave_valor)
            btn_add.grid(row=7, column=3, padx=2, sticky="ew")

            btn_savecard = customtkinter.CTkButton(grupo_dados, text="SALVAR CARD", width=295, height=19, font=("Roboto", 14), corner_radius=5, command=SalveInTextbox)
            btn_savecard.grid(row=8, column=0, columnspan=4, sticky="w", pady=5)
            ###---------------------------------------

        def GrupoDiretorios():
            grupo_entrada_psd = customtkinter.CTkFrame(self.janela_acao.tab(" CRIAR AÇÃO "), width=295,  border_color="#D9DFF3")
            grupo_entrada_psd.grid(row=4, column=1, sticky="w", pady=(200, 0)) 

            label_entrada_psd = customtkinter.CTkLabel(grupo_entrada_psd, text="Arquivo PSD", font=("Roboto", 14))
            label_entrada_psd.grid(row=0, column=1, sticky="w")

            def BotoesEntradaImagens():
    
                def ObterValorPastaExportImagens():
                    global caminho_export_imagens
                    caminho_export_imagens = AbirPasta()

                    caminho_export_imagens

                    #AQUI ESTOU FAZENDO UMA ALTERAÇÃO SOBRESCREVENDO O (Entry)
                    entrada_exportacao_imagens.configure(state="normal")  #HABILITO EDIÇÃO
                    entrada_exportacao_imagens.delete(0, "end")  #LIMPO O PLEACEHOLDER ATUAL
                    entrada_exportacao_imagens.insert(0, caminho_export_imagens)  #ATUALIZO O PLEACEHOLDER
                    entrada_exportacao_imagens.configure(state="disabled")  #DESABILITO DENOVO
                
                def ObterValorPastaExportImagensPSDfile():
                    global pleaceholder_entradapsd 
                    pleaceholder_entradapsd  = AbirFile()

                    pleaceholder_entradapsd 

                    #AQUI ESTOU FAZENDO UMA ALTERAÇÃO SOBRESCREVENDO O (Entry)
                    entrada_psd.configure(state="normal")  #HABILITO EDIÇÃO
                    entrada_psd.delete(0, "end")  #LIMPO O PLEACEHOLDER ATUAL
                    entrada_psd.insert(0, pleaceholder_entradapsd)  #ATUALIZO O PLEACEHOLDER
                    entrada_psd.configure(state="disabled")  #DESABILITO DENOVO
                    
                global entrada_psd
                entrada_psd = customtkinter.CTkEntry(grupo_entrada_psd, placeholder_text=f"Pasta Arquivo Psd", width=255, height=20, font=("Roboto", 14))
                entrada_psd.grid(row=1, column=1, sticky="w", pady=5)
                entrada_psd.configure(state="disabled")

                global entrada_exportacao_imagens
                entrada_exportacao_imagens = customtkinter.CTkEntry(grupo_entrada_psd, placeholder_text="Pasta Exportação Imagens", width=255, height=20, font=("Roboto", 14))
                entrada_exportacao_imagens.grid(row=3, column=1, sticky="w", pady=5)
                entrada_exportacao_imagens.configure(state="disabled")

                btn_entrada_psd = customtkinter.CTkButton(grupo_entrada_psd, text="\uD83D\uDCC2", width=30, height=25, font=("Roboto", 15, "bold"), command=ObterValorPastaExportImagensPSDfile)
                btn_entrada_psd.grid(row=1, column=2)
                
                label_entrada_psd = customtkinter.CTkLabel(grupo_entrada_psd, text="Entrada Arquivo", font=("Roboto", 14))
                label_entrada_psd.grid(row=2, column=1, sticky="w", pady=5)
                
                btn_entrada_exportacao = customtkinter.CTkButton(grupo_entrada_psd, text="\uD83D\uDCC2", width=30, height=25, font=("Roboto", 15, "bold"), command=ObterValorPastaExportImagens)
                btn_entrada_exportacao.grid(row=3, column=2)
                

            BotoesEntradaImagens()
        def BotoesSalvarExcluir():                
        

            def saveinfojson():

                print(registro_dados.winfo_children())

                if (not entrada_nome_operacao.get()) or (not entrada_num_cards.get() or (not entrada_exportacao_imagens.get()) or (not entrada_psd.get()) or (len(registro_dados.winfo_children()) == 0)):
                    AlertModal(win=app, titulo="Dados Ausentes", descricao="Todos os campos devem ser preenchidos.")
                else:
                    def Salvar():
                        
                        nome = entrada_nome_operacao.get()
                        num =  entrada_num_cards.get()
                        cards = meus_cards_obj_json
                        psd =  entrada_psd.get()
                        export = entrada_exportacao_imagens.get()
                        AdicionarDadosJson(nome_operacao=nome, num_cards=num, meus_cards=cards, camin_psd=psd, camim_export=export)
                    Modal(app, "Felipe", tipo="Salvar",fun=Salvar)
            
            def LimparCampos():
                def Limpar():
                    entrada_exportacao_imagens.configure(state="normal")
                    entrada_exportacao_imagens.delete(0, "end")
                    entrada_exportacao_imagens.configure(state="disabled")

                    entrada_psd.configure(state="normal")
                    entrada_psd.delete(0, "end")
                    entrada_psd.configure(state="disabled")

                    entrada_nome_camada.delete(0, "end")
                    entrada_nome_card.delete(0, "end")
                    entrada_novo_texto.delete(0, "end")
                    entrada_nome_operacao.delete(0, "end")
                    entrada_num_cards.delete(0, "end")
                    
                    for w in registro_dados.winfo_children():
                        w.destroy()

                Modal(app, "Felipe", tipo="Esclude",fun=Limpar)
                #ARRUMAR ESSA FUNCIONALIDADE AQUI
                #ISSO AQUI TÁ UMA PORRA KKKKKKK

            apagar_operacao = customtkinter.CTkButton(self.janela_acao.tab(" CRIAR AÇÃO "), command=LimparCampos, text="LIMPAR", width=171, height=39, fg_color="#FF96AD", text_color="#EBECF0",  font=("Roboto", 14, "bold"), hover_color="#E36B85")
            apagar_operacao.grid(row=6, column=2, sticky="n", pady=10)

            btn_salvar_operacao = customtkinter.CTkButton(self.janela_acao.tab(" CRIAR AÇÃO "),text="SALVAR OPERAÇÃO", width=295, height=39, font=("Roboto", 14, "bold"), command=saveinfojson)
            btn_salvar_operacao.grid(row=6, column=1, sticky="w", pady=5)

        NomeOpercao()
        NumeroCards()
        GroupDados()
        GrupoDiretorios()
        BotoesSalvarExcluir()

    def TabExecutarAcao(self):
        labelExecute = customtkinter.CTkLabel(self.janela_acao.tab(" EXECUTAR "), text="Minhas Ações", font=("Roboto", 20), fg_color="#D9DFF3", text_color="#1D42AC", width=250, height=39, corner_radius=6)
        labelExecute.grid(row=0, column=1, sticky="ew")

    
        minhas_acoes = []
        #QUAL O PAPEL DESSA LISTA AQUI MANO?
        #1. SERVE PARA OBTER SEMPRE O PRÓXIMO ROW EM AddComponente(), 2. SERVE PARA QUE EU CONSIGA REMOVER ITENS DA MINHA TELA.
        def RemoverComponenteLista(w, nome_card):
            # PosModal(titulo="Remove", nome=f"Operação {nome_card} removida com sucesso!", win=app)
            def apagar():
                if w in minhas_acoes:
                    minhas_acoes.remove(w)
                    w.destroy()
                    RemoverOperacoesJson(nome_card)
            Modal(app, "Felipe", tipo="Esclude",fun=apagar)
           
        
        def AddComponente(txt):
            if len(minhas_acoes) + 1 <= TamanhoJson():
                texto_card = txt

                row_cpcard = len(minhas_acoes) + 2

                componente_acao_card = customtkinter.CTkFrame(self.janela_acao.tab(" EXECUTAR "), width=300, border_color="#D9DFF3")
                componente_acao_card.grid(row=row_cpcard, column=1, pady=5)

                acao = customtkinter.CTkLabel(componente_acao_card, text=texto_card, font=("Roboto", 14), fg_color="#1854FF", text_color="#D9DFF3", width=250, height=39, corner_radius=6)
                acao.grid(row=1, sticky="w", column=1)

                btn_delete = customtkinter.CTkButton(componente_acao_card, width=39, height=39, font=("Roboto", 14, "bold"), text="\uD83D\uDDD1", fg_color="#FF96AD", text_color="#EBECF0", hover_color="#E36B85", command= lambda : None)
                btn_delete.grid(row=1, sticky="ew", column=2, padx=3)
                btn_delete.bind("<Button-1>", lambda event, w=componente_acao_card: RemoverComponenteLista(w, texto_card))

                btn_play = customtkinter.CTkButton(componente_acao_card, width=39, height=39, font=("Roboto", 14, "bold"), text="\u25B6", command=lambda: None)
                btn_play.grid(row=1, sticky="ew", column=3)
                btn_play.bind("<Button-1>", lambda event: StartarAcao(texto_card))

                minhas_acoes.append(componente_acao_card)            

        def AddMaior():
            #ESSA FUNÇÃO VERIFICAR SE HÁ DADOS NO MEU ARQUIVO JSON, SE TIVER ALGUM DADO, ELE CHAMA OUTRA FUNÇÃO AddComponente(), QUE VAI CRIAR E EXIBIR NA TELA O
            #COMPONENTE COM O NOME ADEQUADO.
            total_dados_jason = TamanhoJson()
            
            if total_dados_jason > 0:
                for i in range(total_dados_jason):
                    AddComponente(NomeDosJson(i))

        if  TamanhoJson() > 0:
            button_add = customtkinter.CTkButton(self.janela_acao.tab(" EXECUTAR "), width=39, height=39, font=("Roboto", 14, "bold"), text="\u27F3", command=AddMaior)
            button_add.grid(row=1, column=1)

app = App()
app.mainloop()