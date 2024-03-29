#!/usr/bin/python3
# coding: utf-8

__author__ = '@zNairy'
__contact__ = 'Github: https://github.com/znairy || Discord: __Nairy__#7181'
__version__ = '2.0'

from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from termcolor import colored
from json import loads, dumps
from sqlite3 import connect
from os import uname, system
from time import sleep
import emoji.unicode_codes.en

class Client(object):
    def __init__(self, host='0.0.0.0', port=5000):
        self.address = (host, port)
        self.__client = None
        self.codeName = None
        self.serverIsOn = True
        self.nameColor = 'white'

    def configureSocketConnection(self):
        self.__client = socket(AF_INET, SOCK_STREAM)
        self.__client.connect(self.address)

    def getCodeName(self):
        codename = ''.join(char for char in input(colored(' Máximo de 20 caractéres | Nickname: ', 'yellow')).split())
        return self.clearCodeName(codename)
    
    def createProfileData(self, codename, identifier=""):
        return {"codename": codename, "identifier": identifier}

    def saveUserProfile(self, profile):
        with connect('client.db') as database:
            cursor = database.cursor()
            cursor.execute('insert into profiles values (?,?)',(profile['codename'],profile['identifier'],))
            database.commit()

    def openUserProfile(self, codename):
        with connect('client.db') as database:
            cursor = database.cursor()

            cursor.execute('select * from profiles where codename = ?', (codename,))
            data = cursor.fetchall()[0]
            return self.createProfileData(data[0], data[1])

    def userProfileExists(self, codename):
        with connect('client.db') as database:
            cursor = database.cursor()

            cursor.execute('select * from profiles where codename = ?',(codename,))
            if cursor.fetchone():
                return True

    # this function shows all usable emojis
    def showAllEmojis(self, params=None):
        for allemojis in emoji.EMOJI_UNICODE_ENGLISH:
            print(allemojis + '->' + emoji.emojize(allemojis))

    # this function only the most common emojis based on the website - > https://www.go2web.com.br/pt-BR/blog/os-100-emojis-mais-usados.html
    def showEmojis(self, params=None):
        lista = [
            ':red_heart:',
            ':face_with_tears_of_joy:',
            ':cat_with_tears_of_joy:',
            ':unamused_face:',
            ':fire:',
            ':smirking_face:',
            ':two_hearts:',
            ':thumbs_up:',
            ':thumbs_down:',
            ':eyes:',
            ':flushed_face:',
            ':disappointed_face:',
            ':sunglasses:',
            ':hot_beverage:',
            ':skull:'
        ]
        for iten in lista:
            print(iten +' -> '+emoji.emojize(iten))

    def changeNameColor(self, params):
        availableColors = ['grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

        if params['functionArgs']:
            if params['functionArgs'][0] in availableColors:
                self.nameColor = params['functionArgs'][0]
            else:
                print(colored('    Cor inválida ou indisponível, execute /namecolor para ver todas as cores disponíveis...', 'red'))
        else:
            print(colored(f'[Servidor]:', 'green'), params['description'])

    def splitReceivedCommand(self, command):
        if self.internalCommands().get(command[0]):
            return self.internalCommands()[command[0]], command[1:]
        
        return False, command[1:]

    def internalCommands(self):
        commands = {
            "/namecolor": {"description": "Troca a cor do seu nome de usuário. Ex: /namecolor red | Cores disponíveis:\n   Grey, Red, Green, Yellow, Blue, Magenta, Cyan, White.", "function": self.changeNameColor},
            "/exit": {"description": "Não vai ficar para a demonstração?", "function": self.exitSession},
            "/allemojis": {"description": "Mostra os emojis disponíves", "function": self.showAllEmojis},#calls the function of line 53
            "/emojis": {"description": "Mostra os emojis mais comuns", "function": self.showEmojis},#calls the function of line 58
            "/clear": {"description": "Limpou a tela antes de eu querer mostrar amigão ;( ", "function": self.clearScreen}
        }
        
        return commands

    def receiveMessages(self):
        sleep(0.5)
        while True:
            message = self.__client.recv(2048)
            if message:
                data = loads(message)                                        #this piece of code (emoji.emojize()) is used to show the emoji
                print(colored(f'\n[{data["codename"]}]:', data["nameColor"]), emoji.emojize(data["message"]) , end='')
                print(colored(f'\n[{self.codeName}]: ', self.nameColor), end='')
            else:
                print(colored('\n     Conexao encerrada pelo servidor...','red'))
                self.exitSession()
                break

    def sendMessages(self):
        try:
            while True:
                if self.serverIsOn:
                    message = input(colored(f'[{self.codeName}]: ', self.nameColor)).strip()
                    if message and len(message) <= 1024:
                        internalCommand, args = self.splitReceivedCommand(message.split())
                        if not internalCommand:
                            data = {'codename': self.codeName, 'nameColor': self.nameColor, 'message': message}
                            self.__client.send(dumps(data).encode())
                        else:
                            params = {"description": internalCommand['description'], "functionArgs": args}
                            internalCommand['function'](params)
                else:
                    break

        except KeyboardInterrupt:
            exit(0)
        except EOFError:
            exit(0)

    def clearCodeName(self, codename):
        invalidChars = ['/', '\\', '"', '[', ']', ',', ';', '?', '`', '´', '{', '}', '~',
        ':', '<', '>', '=', '-', '#', '&', '%', '@', '!', "'", '$', '¨', '*', '(', ')', '+']
        for char in invalidChars:
            codename = codename.replace(char, '')

        return codename

    def checkCodeNameSize(self, codename):
        if codename.strip() and len(codename.strip()) <= 20:
            return True

    def loginUser(self, codename):
        self.codeName = codename
        self.startProcess(self.receiveMessages, ())
        self.sendMessages()

    def startNewSession(self):
        try:
            codename = self.getCodeName()
        except KeyboardInterrupt:
            exit(0)
        except EOFError:
            exit(0)
        finally:
            if self.userProfileExists(codename):
                userProfile = self.openUserProfile(codename)
                userProfile.update({'codename': codename})
                self.__client.send(dumps(userProfile).encode())
                response = self.__client.recv(128)
                if response:
                    self.loginUser(codename)
                else:
                    self.clearScreen()
                    print(colored(' Identificador inválido ou usuário já cadastrado.', 'red'))
                    self.__client.close()
                    self.run()
            else:
                if self.checkCodeNameSize(codename):
                    data = self.createProfileData(codename)
                    self.__client.send(dumps(data).encode())

                    response = self.__client.recv(128)
                    if response:
                        profile = loads(response)
                        self.saveUserProfile(profile)
                        self.loginUser(profile['codename'])
                    else:
                        self.clearScreen()
                        print(colored(' Esse nickname já está em uso, por favor tente novamente e informe outro...', 'red'))
                        self.__client.close()
                        self.run()
                else:
                    self.clearScreen()
                    print(colored(' Nickname muito longo, por favor informe outro...', 'red'))
                    self.startNewSession()

    def startProcess(self, function, args):
        thread = Thread(target=function, args=args)
        thread.daemon = True
        thread.start()

    def clearScreen(self, params=None):
        system('clear' if uname().sysname.lower() == 'linux' else 'cls')

    def showServerInfo(self, status='Inativo', color='red'):
        print(colored(f"   Endereço: {self.address[0]}:{self.address[1]} | Status: {status}", color))
    
    def exitSession(self, params=None):
        self.serverIsOn = False & exit(0)

    def run(self):
        try:
            self.configureSocketConnection()
        except ConnectionRefusedError:
            self.showServerInfo() & exit(1)
        
        self.showServerInfo('Ativo', 'green')
        self.startNewSession()

def main():
    client = Client()
    client.run()



if __name__ == '__main__':
    main()
