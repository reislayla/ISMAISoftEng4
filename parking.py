import csv
import re
import pandas as pd

#Importação dos ficheiros de classes
from cliente import Cliente
from veiculo import Veiculo
from duracao import Duracao
from function import *
from ocupa import Ocupa
from fatura import Fatura

#Variavel para guardar entradas
contadorEntradas = 0
combine = 0

def menu(text):
    print()
    print('Opcoes disponiveis:')
    if text:
        print('0 - Terminar')
        print('1 - Registar entrada de Veiculo')
        print('2 - Registar saida de Veiculo')
        print('3 - Imprimir clientes ordenados')
        print('4 - Adicionar acesso ao parque')
        print('5 - Gravar acessos ao parque')
        print('6 - Gerar fatura para um cliente')
        print('7 - Remover Veiculo')

    else:
        print('[Impressao das varias opcoes]')

    o = int(input('Opcao? '))
    return o

def loadClients (): #metodo para buscar cliente ao arquivo ep1.csv
    global contadorEntradas
    contadorEntradas = 0
    listaClienteVeiculo = []
    with open('ep1.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter = ';')
        for row in reader:
            if len(str(row[2])) < 9 or str(row[2]).isnumeric() == False:
                pass
            else:
                l_cliente = Cliente(row[2])
                l_cliente.removerTodosVeiculo()
                if not listaClienteVeiculo:
                    l_cliente.adicionarVeiculo(row[0], row[1])
                    listaClienteVeiculo.append(l_cliente)
                    contadorEntradas += 1
                else:
                    if l_cliente in listaClienteVeiculo:
                        l_veiculo = Veiculo(row[0], row[1])
                        for i in range(len(listaClienteVeiculo)):
                            if listaClienteVeiculo[i] == l_cliente and listaClienteVeiculo[i].verificarVeiculo(l_veiculo) == False:
                                listaClienteVeiculo[i].adicionarVeiculo(row[0], row[1])
                                listaClienteVeiculo[i].ordenarVeiculos()
                                contadorEntradas += 1
                    else:
                        l_cliente.adicionarVeiculo(row[0], row[1])
                        listaClienteVeiculo.append(l_cliente)
                        contadorEntradas += 1
        return listaClienteVeiculo

def removeVehicle(matricula): #metodo para remover do arquivo ep1.csv um determinado veiculo
    indexRemove = -1
    matricula = correctMatricula(str(matricula))
    vehicleExist = False
    with open('ep1.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter = ';')
        for row in reader:
            if (str(row[0]) == matricula):
                print(indexRemove)
                vehicleExist = True
                break
            indexRemove += 1
    if (vehicleExist == False):
        print("Veiculo não encontrado.")
    else:
        with open('ep1.csv') as csv_file:
            pandaReader = pd.read_csv(csv_file, sep = ";")
            pandaReader.drop([indexRemove], inplace = True)
            pandaReader.to_csv("ep1.csv", index=False, sep = ';')

def printClients(l_listaVeiculosCliente): #metodo para imprimir cliente e matriculas de forma ordenada
    l_listaVeiculosCliente = sorted(l_listaVeiculosCliente, key=lambda cliente: cliente.getNif()).copy()
    for i in range(len(l_listaVeiculosCliente)):
        print('\n'+str(l_listaVeiculosCliente[i])+'\n')
        print('     Matrícula  Marca')
        for index in range(l_listaVeiculosCliente[i].numeroVeiculos()):
            print('     '+str(l_listaVeiculosCliente[i].getVeiculoIndex(index)))

def saveEntries(combine):


    #Gravar informações da lista combine no ficheiro parque.csv
    with open ('parque.csv', mode='a', newline='') as parque_file:
        parque_writer = csv.writer(parque_file, delimiter=';')
        for x in range(0, len(combine)-1,2):
            parque_writer.writerow([combine[x]]+[str(combine[x+1])])
    #Informar que a gravação foi realizada com sucesso
    print(("Ficheiro gravado com sucesso"))
    #Ordenar o dados de forma descrescente em relação a duração do estacionamento
    df = pd.read_csv('parque.csv', sep=';')
    df.sort_values(by=['duracao'], ascending=False, inplace=True)
    df.to_csv('parque.csv', sep=';', index=False)
    combine = []

def addParkEntry():

    #Variável global combine. Irá conter os dados de matricula e duração.
    global combine
    combine = []

    #Validação da matricula e duracao
    while True:
        #Função para validação da matricula (validPlate())
        m1, plateFlag = validPlate()
        if (m1!='0' and m1 !=''):
            while True:
                if plateFlag == True:
                    while True:
                        #Função para validação da duracao (validDuration())
                        d1, durationFlag, exitFlag = Duracao.validDuration()
                        if durationFlag == True:
                            if exitFlag == 0:
                                #Inserir dados na variável combine
                                combine.append(m1)
                                combine.append(d1)
                                #Chamar função da matricula novamente para continuar a inserir.
                                m1, plateFlag = validPlate()
                        else:
                            plateFlag = False
                        break
                #Ao inserir 0 ou Enter o sistema para e impede a gravação.
                elif (m1=='0' or m1 ==''):
                    print("Obrigada por usar nosso software.")
                    break
                #Ao inserir valores inválidos o sistema avisa e impede gravação.
                else:
                    print("Valor inválido")
                    m1, plateFlag = validPlate()
        break


def validPlate():

    #Modelo para validação da placa. Ex.: 11-XX-22
    model8 = re.compile('^\d{2}[-][A-Z]{2}[-]\d{2}$')
    #Modelo para validação da placa e posterior correção. Ex.: 11XX22
    model6 = re.compile('^\d{2}[A-Z]{2}\d{2}$')
    m = input("Digite a matricula (0 ou Enter para sair): ")
    m = m.upper();

    #Matricula no modelo válido final ("11-XX-22")
    if len(m) == 8 and model8.match(m):
        print("Matricula: ", m)
        return m, True

    #Matricula no modelo válido para correção ("11XX22")
    elif len(m) == 6 and model6.match(m):
        print("Valor necessita correção")
        correcao = list(m)
        m = (correcao[0]+correcao[1]+"-"+correcao[2]+correcao[3]+"-"+correcao[4]+correcao[5]);
        print("Correção: ", m)
        return m, True

    #Matricula inválida.
    else:
        return m, False

def matches(s, pattern):
    ...


def printClientPlates(l_listaVeiculosCliente): #metodo para imprimir somente as matriculas de forma ordenada, NÃO IMPLEMENTADO ja que o metodo de impressao dos clientes ja responde a esta necessidade
    l_listaVeiculosCliente = sorted(l_listaVeiculosCliente, key=lambda cliente: cliente.getNif()).copy()
    for i in range(len(l_listaVeiculosCliente)):
        print('\n'+str(l_listaVeiculosCliente[i])+'\n')
        print('     Matrículas:')
        for index in range(l_listaVeiculosCliente[i].numeroVeiculos()):
            print('     '+str(l_listaVeiculosCliente[i].getVeiculoIndex(index).getMatricula()))


def invoice(nif): #metodo para impressão de faturas do mes de um determinado cliente
    fatura = Fatura(Cliente(nif))
    fatura.calcularValor()
    print("NIF: "+nif)
    print("")
    print("Matricula  Marca               Duracao     Custo")
    for ocupa in fatura.getOcupa():
        print(str(ocupa.getVeiculo().getMatricula())+"   "+str(ocupa.getVeiculo().getMarca())+"                 "+str(ocupa.getDuracao())+"          "+str(ocupa.getValor()))
    print("Total:                                      "+str(fatura.getValorTotal()))


def vehicleEntry(): # metodo para registar entrada de um determinado veiculo ao parque
    matricula = input("Introduza Matricula: ")
    marca = input("Introduza Marca: ")
    ocupa = Ocupa(Veiculo(matricula, marca))
    print("Veiculo de matricula "+ ocupa.getVeiculo().getMatricula()+" deu entrada ao parque.")
    ocupacoes
###############################################################################
vehicles = []
operations = []
ocupacoes= []
op = menu(True)

vehicles += loadClients()

while True:
    op = menu(False)
    if op == 0:
        print('Obrigado por usar o nosso software!')
        break;

    elif op == 1:
        vehicleEntry()
        vehicles += loadClients()

    elif op == 2:
        matricula = input('Insira Matricula: ')
        registerSaida(matricula)

    elif op == 3:
        printClients(vehicles)

    elif op == 4:
        operations.append(addParkEntry())

    elif op == 5:
        saveEntries(operations)

    elif op == 6:
        nif = input("Introduza o seu NIF: ")
        invoice(nif)

    elif op == 7:
        matricula = input('Insira Matricula; ')
        removeVehicle(matricula)
        vehicles += loadClients()
