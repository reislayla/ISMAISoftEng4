import csv
from veiculo import *
from datetime import datetime
import pandas as pd
from function import *


class Ocupa:

    def __init__(self, veiculo, entrada = datetime.now(), saida= None, duracao = 0, valor = 0):
        validate = True
        with open('ocupacao.csv') as csv_file:
            reader = csv.reader(csv_file, delimiter = ';')
            for row in reader:
                if str(row[3]) == "None" and str(row[0]) == veiculo.getMatricula():
                    print("Veiculo já se encontra dentro do estacionamento.")
                    validate = False
                    break
        if (validate == False):
            pass
        else:
            if veiculo.getMatricula() == None:
                pass
            elif vehicleValidation(veiculo) == False:
                print("Veiculo não registado.")
                nif = input("Adicionar NIF : ")
                with open('ep1.csv', 'a+', newline='') as csv_file:
                    ep1_writer = csv.writer(csv_file, delimiter=';')
                    ep1_writer.writerow([veiculo.getMatricula(), veiculo.getMarca(), nif])
                self.setVeiculo(veiculo)
                self.setEntrada(entrada)
                self.setSaida(saida)
                with open('ocupacao.csv', 'a+', newline='') as csv_file:
                    ocupa_writer = csv.writer(csv_file, delimiter=';')
                    ocupa_writer.writerow([veiculo.getMatricula(), veiculo.getMarca(), str(entrada), str(saida), "DurationNull1", "ValueNull"])
            elif (isinstance(saida, datetime) == False):
                self.setVeiculo(veiculo)
                self.setEntrada(entrada)
                self.setSaida(saida)
                with open('ocupacao.csv', 'a+', newline='') as csv_file:
                    ocupa_writer = csv.writer(csv_file, delimiter=';')
                    ocupa_writer.writerow([veiculo.getMatricula(), veiculo.getMarca(), str(entrada), str(saida), "DurationNull", "ValueNull"])
            else:
                self.setVeiculo(veiculo)
                self.setEntrada(entrada)
                self.setSaida(saida)
                self.setDuracao(duracao)
                self.setValor(valor)


    def getVeiculo(self):
        return self.__veiculo

    def getEntrada(self):
        return self.__entrada

    def getSaida(self):
        return self.__saida

    def getDuracao(self):
        return self.__duracao

    def getValor(self):
        return self.__valor

    def setVeiculo(self,l_veiculo):
        if  isinstance(l_veiculo, Veiculo) == False or vehicleValidation(l_veiculo) == False:
            pass
        else:
            self.__veiculo = l_veiculo

    def setEntrada(self,l_entrada):
        if  isinstance(l_entrada, datetime) == False or l_entrada > datetime.now():
            pass
        else:
            datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
            self.__entrada=datetime.strptime(str(l_entrada), datetimeFormat)

    def setSaida(self,l_saida):
        if  isinstance(l_saida, datetime) == False or l_saida > datetime.now():
            self.__saida= None
        else:
            datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
            self.__saida=datetime.strptime(str(l_saida), datetimeFormat)

    def setValor(self,l_valor):
        self.__valor=l_valor

    def setDuracao(self,l_duracao):
        self.__duracao=l_duracao

    def addValorDuracao(self):
        dateNow =  datetime.now()
        duracao = int(calcDurationMinutes(self.getEntrada(), dateNow))
        valor = duracao * 0.01
        registerSaida(self.getVeiculo().getMatricula())
        self.setDuracao(int(duracao))
        self.setValor(round(valor, 2))

    def __repr__(self):
        return {'Veiculo':self.getVeiculo(), 'Entrada': self.getEntrada().strftime("%m/%d/%Y, %H:%M:%S")}

    def __str__(self):
        return str(self.getVeiculo())+' Entrada = '+self.getEntrada().strftime("%m/%d/%Y, %H:%M:%S")

    def __eq__(self, other):
        if isinstance(other, Ocupa):
            if(self.getEntrada() == other.getEntrada() and self.getVeiculo() == other.getVeiculo()):
                return True
        return False
