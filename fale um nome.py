"""
Observação este Programa é muito simples
Faça um programa qie leia um número e exiba o dia correspondente da semana.
(1- Domingo, 2- Segunda, etc), se digitar outro valor deve aparece valor inválido.
"""

adivinhar = int(input("Digite um número de  1 á 100  e ganhe um premio: "))


if  adivinhar == 1:
    print("tessoura ")
elif adivinhar == 2:
    print("alicate ") 
elif adivinhar == 3:
    print("Esmalte ")
elif adivinhar == 4:
    print("erro ")
elif adivinhar == 5:
    print("passou perto ")
elif adivinhar == 6:   
    print("fala outro número ")
elif adivinhar == 7:
    print("tenta novamente")
    
elif adivinhar == 8:
    print("quase ")
elif adivinhar == 9:
    print("perdi ")
elif adivinhar == 10:
    print("mais um ")
elif adivinhar == 11:
    print("não erro ")
elif adivinhar == 12:
    print("ganhou R$1000,00 reais")

else:   
    print(" Este objeto não exite!!! ")
    
