"""
Faça um Programa para um caixa eletrônico. O programa deverá perguntar ao
usuário a valor do saque e depois informar quantas notas de cada valor
serão fornecidas. As notas disponíveis serão as de 1, 5, 10, 50 e 100 reais.
O valor mínimo é de 10 reais e o máximo de 600 reais.
O programa não deve se preocupar com a quantidade de notas existentes na
máquina.
    Exemplo 1: Para sacar a quantia de 256 reais, o programa fornece duas
    notas de 100, uma nota de 50, uma nota de 5 e uma nota de 1;
 
    Exemplo 2: Para sacar a quantia de 399 reais, o programa fornece
    três notas de 100, uma nota de 50, quatro notas de 10,
    uma nota de 5 e quatro notas de 1.
"""
saque = int(input("Digite o valor do saque: "))
 
if 10 <= saque <= 600:
    notas_cem = saque // 100
    saque = saque % 100
 
    notas_cinquenta = saque // 50
    saque = saque % 50
 
    notas_dez = saque // 10
    saque = saque % 10
 
    notas_cinco = saque // 5
    saque = saque % 5
 
    notas_um = saque // 1
 
    if notas_cem > 0:
        print(notas_cem, "notas de R$ 100")
    if notas_cinquenta > 0:
        print(notas_cinquenta, "notas de R$ 50")
    if notas_dez > 0:
        print(notas_dez, "notas de R$ 10")
    if notas_cinco > 0:
        print(notas_cinco, "notas de R$ 5")
    if notas_um > 0:
        print(notas_um, "notas de R$ 1")
               
else:
    print("Nao é possivel fazer o saque")
