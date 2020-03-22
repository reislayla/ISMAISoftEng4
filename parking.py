﻿import re

def menu(text):
    print()
    print('Opcoes disponiveis:')
    if text:
        print('0 - Terminar')
        print('1 - Ler ficheiro de clientes')
        print('2 - Imprimir clientes ordenados')
        print('3 - Mostrar matriculas por Cliente')
        print('4 - Adicionar acesso ao parque')
        print('5 - Gravar acessos ao parque')
        print('6 - Gerar fatura para um cliente')
    else:
        print('[Impressao das varias opcoes]')
        
    o = int(input('Opcao? '))
    return o


def loadClients ():   
    import csv
    file_name = 'ep1.csv'
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        data = list(reader)      
    print("Nome do ficheiro: "+file_name)
    print("Foram importados "+str(len(data))+" registos")
    return data 


def printClients(v):
    if not v :
        print("Não existem clientes!")
    else :
        s = sorted(v, key = lambda x: (x[2], x[1]))
        for client in s:
            print(client[2]+" : ('"+client[0]+"','"+client[1]+"')")

        
def saveEntries(l):
    import csv
    if not l :
        print("Não existem entradas no Parque!")
    else :
        from collections import OrderedDict
        # l = [{'matricula' : '34-DF-54','tempo' : 54}, 
        # {'matricula' : '34-DF-54','tempo' : 50}, 
        # {'matricula' : '34-DF-54','tempo' : 52}]
        #order list
        items = sorted(l, key=lambda d: d['tempo'], reverse=True)   
        #get header names     
        keys = items[0].keys()
        with open('parque.csv', 'w') as output_file:
            dict_writer = csv.DictWriter(output_file, keys, delimiter=';')
            dict_writer.writeheader()
            dict_writer.writerows(items)      
        print("Ficheiro gravado com sucesso!")

def pedirtempo():
    tempo= int(input('Qual o tempo que esteve estacionado no parque de estacionamento(Minutos)? '))    
    while tempo<0:
        print ('Tem de ser um valor positivo')
        tempo= int(input('Qual o tempo que esteve estacionado no parque de estacionamento(Minutos)? '))
    return tempo
        
def addParkEntry():    
    while True:
        matricula= str(input('Qual a sua Matrícula? Ex:00-XX-00: ' ))
        if validPlate(matricula):
            tempo = pedirtempo()
            dicionariomatriculas = {
                'matricula' : matricula, 'tempo' : tempo
            }
            print ('Inserido com sucesso: ')
            return dicionariomatriculas
        else:
            print('Tem de introduzir uma matricula válida')
        
    
# d.	Escreva uma função que valide se uma string, passada como argumento, representa uma matrícula válida em Portugal. Considere apenas matrículas 
# posteriores a 2005 compostas por letras no meio como no seguinte exemplo: 00-AA-00. A função deverá devolver um valor lógico Verdadeiro se a matrícula for válida e Falso, caso contrário.
def validPlate(matricula):
    return re.findall("^(\d{2}-[A-Z]{2}-\d{2})$", matricula)
   

def matches(s, pattern):
    ...
    
    
def printClientPlates(c):
    if not c :
        print("Não existem clientes!")
    else :
        clients = []
        for record in c:
            if record[2] not in clients:
                clients.append(record[2])
                
        for client in clients:
            plates = []
            for record in c :
                if client == record[2] :
                    plates.append(record[0])
        
            # imprimir matrículas por cliente - nif
            print(client, ": ", plates)   



def invoice(c, o):
    ...

###############################################################################
vehicles = []
operations = []
op = menu(True)

while True:
    #op = menu(False)
    if op == 0:
        print('Obrigado por usar o nosso software!')
        break
        
    elif op == 1:
        vehicles += loadClients()

    elif op == 2:
        printClients(vehicles)

    elif op == 3:
        printClientPlates(vehicles)
        
    elif op == 4:
        operations.append(addParkEntry())      
    
    elif op == 5:
        saveEntries(operations)
        
    elif op == 6:
        invoice(vehicles, operations) 
    if op != 0:
        op = menu(True)
