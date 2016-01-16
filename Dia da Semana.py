"""

Faça um programa qie leia um número e exiba o dia correspondente da semana.
(1- Domingo, 2- Segunda, etc), se digitar outro valor deve aparece valor inválido.
"""
dia = int(input("Digite o dia da semana:"))
verifica = False

if dia == 1:
    print("Domingo")
    verifica = True
if dia == 2:
    print("Segunda")
    verifica = True
if dia == 3:
    print("Terça")
    verifica = True
if dia == 4:
    print("Quarta")
    verifica = True
if dia == 5:
    print("Quinta")
    verifica = True
if dia == 6:
    print("Sexta")
    verifica = True
if dia == 7:
    print("Sábado")
    verifica = True

if verifica != True:
    print(" Este dia não exite!!! ")
    print(" ... Somente de 1 á 7 ")
