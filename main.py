# -*- coding: utf-8 -*-

import telebot

API_TOKEN = 'xxxxxxxxx'
bot = telebot.TeleBot(API_TOKEN)


class StopExcp(Exception):
    pass



class Node:
    def __init__(self, parent=None, question=None, yes=None, no=None):
        self.parent = parent
        self.yes = yes
        self.no = no
        self.question = question

    def get_child(self, messageReceived, default_node):
      if messageReceived=='indietro':
        if self.parent==None:
          return self, ''
        return self.parent, ''

      if self.no==None or self.yes==None:
        return default_node, 'Cominciamo una nuova conversazione!'

      if messageReceived=='si':
        return self.yes, ''

      if messageReceived=='no':
        return self.no, ''


      return self, 'Mi spiace, non ho capito quello che hai detto... Riprova!'

    def __str__(self):
      if self.no==None or self.yes==None:
        return 'None'
      return 'question: ' + self.question + '\nif yes: ' + self.yes.question + '\nif no: ' + self.no.question

root_node = Node(question="Suo figlio/a è stato allontanato da scuola?")

def search(node_list, question):
  for node in node_list:
    if node.question == question:
      return node
  return


# def read_tree():
node_list = [root_node]
str_nodes = open('tree.txt', 'r').readlines()
for n in str_nodes:
  prop = n.split(';')
  new_node = Node(question=prop[0])
  parent_node = search(node_list, prop[1])

  new_node.parent = parent_node
  if prop[2] == 'yes':
    parent_node.yes = new_node
  elif prop[2] == 'no':
    parent_node.no = new_node
  node_list.append(new_node)

parent_node = root_node

class color:
   RED = '\033[91m'
   BOLD = '\033[1m'
   END = '\033[0m'

welcome_message = "Ciao! Sono il BOT che ti aiuterà a comprendere quale modulo è necessario consegnare nel caso in cui tuo figlio/a sia stato assente o allontanato da scuola.\nTi farò una serie di domande, alle quali dovrai rispondere 'Si' oppure 'No'. Se vuoi tornare alla domanda precedente basterà digitare 'indietro'. Per altre informazioni usa '/help'. Mi potrai contattare in ogni momento.\nSe ci sono problemi tecnici, contatta l’assistenza informatica all’indirizzo email lorenzopisa00@gmail.com.\nPrima di iniziare, ti ricordo che per assenze, anche di salute, minori di 3 giorni (non vengono conteggiati i festivi) non sono richiesti moduli giustificativi per il rientro a scuola.\n\nTuo figlio è stato allontanato da scuola?"
help_message = "Il servizio BOT è composto da una struttura di domande collegate fra loro attraverso la scelta di risposte affermative (SI) o negative (NO). Ad ogni quesito è quindi possibile scegliere solamente una delle due risposte possibili. E’ possibile, in ogni momento, tornare alla domanda precedente attraverso la parola chiave indietro.\n\nsi-> risposta affermativa\nno -> risposta negativa\nindietro -> torna al quesito precedente\n"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    global parent_node
    bot.send_message(message.from_user.id, welcome_message)
    parent_node = root_node

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.from_user.id, help_message)

def send_document(parent_node, message):
    messageToDefine = parent_node.question

    if 'modulo' in messageToDefine:

        d = {'modulo_1':'1','modulo_2':'2','modulo_3':'3','modulo_4':'4'}

        doc = open('modulo_'+d[messageToDefine]+'.pdf', 'rb')
        bot.send_document(message.from_user.id, doc)
        endMessage(message)

        if d[messageToDefine] == '2' or d[messageToDefine] == '3':
            bot.send_message(message.from_user.id, 'NB: Le assenze devono essere giustificate nel registro elettronico')


def endMessage(message):
    bot.send_message(message.from_user.id, 'Questo modulo deve essere inviato il giorno prima del rientro previsto a PGEE04000b@istruzione.it oppure riconsegnato al rientro al collaboratore scolastico.')
    bot.send_message(message.from_user.id, 'Questa conversazione è terminata. Se volessi iniziarne una nuova, digita /start')

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global parent_node

    parent_node, nextMessage = parent_node.get_child((message.text).lower(), root_node)

    if 'modulo' in parent_node.question:
      send_document(parent_node, message)
    else:
      nextMessage += '\n' + parent_node.question
      bot.send_message(message.from_user.id, nextMessage)

    if 'nuovamente ammesso' in nextMessage:
        doc = open('modulo_1.pdf', 'rb')
        bot.send_document(message.from_user.id, doc)
        endMessage(message)
    elif 'POSITIVO' in nextMessage:
        doc = open('circolare_n_108.pdf', 'rb')
        bot.send_document(message.from_user.id, doc)
        endMessage(message)

bot.polling()