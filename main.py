import loguru
import requests
from deep_translator import GoogleTranslator
from loguru import logger
import os
import time
arquivo_conselhos ='conselhos.txt'
url = 'https://api.adviceslip.com/advice'

def traduzir(texto):
    print('Traduzindo a sabedoria recebida')
    try:
        traducao = GoogleTranslator(source='auto', target='portuguese').translate(texto)
        return traducao
    
    except Exception as error:
        logger.exception(f'Erro ao traduzir: {error}')

def traduzir_saved(arquivo):

    lista_traduzida = []
    #tratamento de error - checar se existe o arquivo
    if os.path.exists(arquivo):
        with open (arquivo,'r') as file:
            arquivo_existe = file.read()
            arquivo_existe = arquivo_existe.splitlines()
        for conselho in arquivo_existe:
            try:
                conselho = GoogleTranslator(source='auto', target='portuguese').translate(conselho)
                lista_traduzida.append(conselho)
            except Exception as error:
                logger.exception(f'Erro ao traduzir: {error}')
        for conselho in lista_traduzida:
            print(conselho)
    else:
        return('Ei Dr. o arquivo não existe, por favor salvar alguma mensagem no texto!')
        

def tome_um_conselho():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            
            conselho = f'ID: {response.json()['slip']['id']}, Advice: {response.json()['slip']['advice']}'
            print (conselho)
            return conselho
        
        else:
            print("Erro ao tentar gerar conselho.")
            
            return None
    except Exception as e:
        
        logger.exception(f"Erro na requisição da API: {e}")
        
        return None
 
def salva_conselhos(arquivo,conselhos_salvos):
    print('Salvando a sabedoria dos anciões')
    #tratamento de error - checar se existe o arquivo
    global conselhos
    if os.path.exists(arquivo):
        with open(arquivo, 'r') as file:
            arquivo_existe = file.read()
            arquivo_existe = arquivo_existe.splitlines()

    else:
        arquivo_existe=[]
       
    arquivo_existe.extend(conselhos_salvos)
    with open (arquivo,'w') as file:
        for conselho in arquivo_existe:
            file.write(conselho + '\n')
    print('Conselhos salvos com sucesso!')
    conselhos=[]

def lembrar_conselhos(arquivo):
    print('Estou lembrando da sabedoria dos anciões anglófonos')
    if os.path.exists(arquivo):
        with open (arquivo,'r') as file:
            arquivo_existe = file.read()
            arquivo_existe = arquivo_existe.splitlines()
        for conselho in arquivo_existe:
            print(conselho)
    else:
        return('Ei Zé o arquivo não existe, por favor salvar alguma mensagem no texto!')


def exibir_menu():
    
    print('---------------------------------------')
    print('**** MENU DA CACHAÇARIA DO SEU ZÉ *****')
    print('1 - Selecionar numero de conselhos')
    print('2 - Salvar conselhos num arquivo de texto')
    print('3 - Lembrar conselhos em inglês')
    print('4 - Traduzir os conselhos que acabei de gerar')
    print('5 - Traduzir sabedoria guardada')
    print('0 - Sair do programa')
    print('----------------------------------------')

def esperando():
    print('\nclique qualquer botão para continuar')
    input() 
    time.sleep(1)
    os.system('cls')

if __name__ == "__main__":
    conselhos = []
    status = -1


    while status != 0:
        exibir_menu()
        status = int(input(f'Digite a opção desejada: '))
        time.sleep(1)
        os.system('cls')
       
        match status:
            case 1:
                print('Recebendo conhecimento dos anciões')
                try:
                    numero_de_conselhos = int(input('Quantos conselhos você vai querer?: '))

                    for i in range(numero_de_conselhos):
                        conselhos.append(tome_um_conselho())

                except Exception as e:
                    logger.exception(f"Erro! Tente novamente um valor válido: {e}")
                esperando()

            case 3:
                lembrar_conselhos(arquivo_conselhos)
                print('\nterminando de lembrar')
                esperando()
                        
            case 4:
                if conselhos:
                    print('Traduzindo sabedoria recebida')
                    traduzidos = []
                    
                    for i in range(len(conselhos)):
                        texto = conselhos[i]
                        traduzidos.append(traduzir(texto))
                    print('Conselhos traduzidos:\n')
                    for traduzido in traduzidos:
                        print(traduzido)
                    esperando()
                else:
                    os.system('cls')    
                    print('Ei Sr. Zé! Não tem nada gerado, ou o que foi gerado foi salvo no arquivo.')
                    esperando()
            case 5:
                traduzir_saved(arquivo_conselhos)
                esperando()

            case 2:
                salva_conselhos(arquivo_conselhos, conselhos)
                esperando()        
            
            case 0:
                status = 0

            case _:
                logger.error("Opção inválida. Escolha uma opção do menu!") 
    print('Obrigado por visitar a Cachaçaria do seu Zé!')
