"""
27. Uma fruteira está vendendo frutas com a seguinte tabela de preços:
o                         Até 5 Kg           Acima de 5 Kg
o   Morango         R$ 2,50 por Kg          R$ 2,20 por Kg
o   Maçã            R$ 1,80 por Kg          R$ 1,50 por Kg
 
Se o cliente comprar mais de 8 Kg em frutas ou o valor total da compra
ultrapassar R$ 25,00, receberá ainda um desconto de 10% sobre este total.
 
Escreva um algoritmo para ler a quantidade (em Kg) de morangos e a quantidade
(em Kg) de maças adquiridas e escreva o valor a ser pago pelo cliente.
 
"""
 
morango = float(input("Digite a quantidade de morango(kg): "))
maçã = float(input("Digite a quantidade de maçã(kg): "))
 
total = 0
 
if morango > 5:
    total += morango*2.2
else:
    total += morango*2.5
 
if maçã > 5:
    total += maçã*1.5
else:
    total += maçã*1.8
 
if total > 25:
    total *= 0.9
 
print("Total a ser pago: R$ %g"%total)

