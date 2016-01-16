'''
Faça um Programa que leia três números e mostre-os em ordem decrescente.

'''
a = int(input("Digite o primeiro numero: "))
b = int(input("Digite o segundo numero: "))
c = int(input("Digite o terceiro numero: "))


if a >= b >= c:
    print(a, b, c)
elif a >= c >= b:
    print(a, c, b)
elif b >= a >= c:
    print(b, a, c)
elif b >= c >= a:
    print(b, c, a)
elif c >= a >= b:
    print(c, a, b)
else:
    print(c, b, a)

