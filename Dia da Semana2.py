"""
Observação este Programa é muito simples
Faça um programa qie leia um número e exiba o dia correspondente da semana.
(1- Domingo, 2- Segunda, etc), se digitar outro valor deve aparece valor inválido.
"""
dia = int(input("Digite o dia da semana: ..."))


if dia == 1:
    print("Domingo ")
    verifica = True
elif dia == 2:
    print("Segunda ")
 
elif dia == 3:
    print("Terça ")
   
elif dia == 4:
    print("Quarta ")
    
elif dia == 5:
    print("Quinta ")
    
elif dia == 6:
    print("Sexta " )
   
elif dia == 7:
    print("Sábado ")
 
else:


    print(" Este dia não exite!!! ")
    print(" ... Somente de 1 á 7 ")
