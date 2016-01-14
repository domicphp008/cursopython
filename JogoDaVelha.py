from tkinter import *
import tkinter.messagebox as messagebox
 
 
JOGADOR = 0
 
VALORES = ['X', 'O']
 
BOTOES = {}
 
TAB = []
 
JOGANDO = True
 
def callback(pos):
    """
    Lida com o evento do pressionamento de um botão
    Recebe a posição de pressionamento do botão
    """
    # Declara as variáveis globais
    global JOGADOR, BOTOES, TAB, VALORES, JOGANDO
     
    # Se o botão já foi pressionado anteriormente não devemos mudar seu texto
    if BOTOES[pos]["text"] != "" or not JOGANDO:
        return
     
    # Colocamos um valor apropriado no botão
    BOTOES[pos].config(text= VALORES[JOGADOR])
 
    # E adicionamos ao Tabuleiro
    TAB[pos[0]*3 + pos[1]] = JOGADOR
 
    # Verificamos se há vitória ou derrota
    if ganhou():
        # Se há nós colocamos uma mensagem na tela
        messagebox.showinfo("Fim de Jogo", "O jogador %i (%s) ganhou"%(int(JOGADOR) + 1, VALORES[JOGADOR]))
        JOGANDO = False
 
    # Verificamos se há empate
    if sum(TAB) == 4:
        messagebox.showinfo("Fim de Jogo", "Empate!")
        JOGANDO = False
 
    # E trocamos o jogador
    JOGADOR = not JOGADOR
 
 
def criaBotoes():
    """
    Cria os botões usados no jogo
    """
    # Declara as variáveis globais
    global BOTOES, TAB, frame
 
    # Cria a lista de posições possíveis
    posições = [ (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2) ]
     
    # Para cada posição
    for pos in posições:
        # Cria-se um botão
        b = Button(frame, width = 10,  height = 5, command = lambda p=pos: callback(p))
        # Armazena-se esse botão no dicionário de botões
        BOTOES[pos] = b
        # Seleciona-se uma posição específica para esse botão
        b.grid( row = pos[0], column = pos[1] )
        # E adicona-se um elemento vazio ao tabuleiro
        TAB.append(-1)
 
def ganhou():
    """
    Verifica se o jogador atual ganhou
    """
    global JOGADOR
    return ((TAB[6] == JOGADOR and TAB[7] == JOGADOR and TAB[8] == JOGADOR) or # Linha horizontal baixa
    (TAB[3] == JOGADOR and TAB[4] == JOGADOR and TAB[5] == JOGADOR) or # Linha horizontal meio
    (TAB[0] == JOGADOR and TAB[1] == JOGADOR and TAB[2] == JOGADOR) or # Linha horizontal alta
    (TAB[6] == JOGADOR and TAB[3] == JOGADOR and TAB[0] == JOGADOR) or # Linha vertical Esquerda
    (TAB[7] == JOGADOR and TAB[4] == JOGADOR and TAB[1] == JOGADOR) or # Linha vertical central
    (TAB[8] == JOGADOR and TAB[5] == JOGADOR and TAB[2] == JOGADOR) or # Linha vertical direita
    (TAB[6] == JOGADOR and TAB[4] == JOGADOR and TAB[2] == JOGADOR) or # diagonal
    (TAB[8] == JOGADOR and TAB[4] == JOGADOR and TAB[0] == JOGADOR)) # diagonal
 
if __name__ == "__main__":
    # Criamos a instância de Tk
    root = Tk()
    # Definimos um título
    root.title("Jogo da Velha")
    # Construimos uma frame para armazenar os botões
    frame = Frame(root)
    # Criamos os botões
    criaBotoes()
    # Empacotamos a frame
    frame.pack()
    # Rodamos o aplicativo
    root.mainloop()
