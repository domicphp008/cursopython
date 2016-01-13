"""
Faça um programa que pergunte o preço de três produtos e informe qual produto
você deve comprar, sabendo que a decisão é sempre pelo mais barato.
"""
 
a = int(input("Digite o primeiro produto: "))
b = int(input("Digite o segundo produto: "))
c = int(input("Digite o terceiro produto: "))
 
print("O produto que deve ser comprado é aquele cujo preço é:")
############################################
#Algoritmo para a aula 009
if a < b:
    if a < c:
        print("R$", a)
    else:
        print("R$", c)
else:
    if b < c:
        print("R$", b)
    else:
        print("R$", c)
#############################################
#Algoritmo para a aula 010
if a < b < c:
    print("R$", a)
elif a < c < b:
    print("R$", a)
elif b < a < c:
    print("R$", b)
elif b < c < a:
    print("R$", b)
elif c < a < b:
    print("R$", c)
else:
    print("R$", c)
