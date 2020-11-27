# -*- coding: utf-8 -*-

import telebot

API_TOKEN = 'xxxxxx'

bot = telebot.TeleBot(API_TOKEN)


class StopExcp(Exception):
    pass


class Node:
    def __init__(self, parent=None, question=None, yes=None, no=None):
        self.parent = parent
        self.yes = yes
        self.no = no
        self.question = question

    def __str__(self):
      if self.no==None or self.yes==None:
        return 'None'
      return 'question: ' + self.question + '\nif yes: ' + self.yes.question + '\nif no: ' + self.no.question


root_node = Node(question="Tuo figlio è stato allontanato da scuola?")

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
  #print(prop)
  new_node = Node(question=prop[0])
  parent_node = search(node_list, prop[1])

  new_node.parent = parent_node
  if prop[2] == 'yes':
    parent_node.yes = new_node
  else:
    parent_node.no = new_node

  node_list.append(new_node)

chat_id = 774306756
parent_node = root_node

welcome_message = "Ciao! Sono il bot che ti aiuterà a comprendere, al meglio, quale dei moduli bisogna consegnare in ogni possibile casistica. \nTi farò una serie di domande e ti chiedo gentilmente di rispondermi in modo molto preciso 'Si' oppure 'No'. \nMi potrai contattare ad ogni momento. \nSe ci sono problemi tecnici con il bot, ti prego di contattare il mio creatore, attraverso la mail lorenzopisa00@gmail.com. \n\nIniziamo quindi con una domanda semplice, tuo figlio è stato allontanato da scuola?"

# todo help
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id, welcome_message)
    parent_node = root_node

def send_document(messageToDefine):
    a=0

    if(messageToDefine == 'modulo_1'):
        a = 1
    elif(messageToDefine == 'modulo_2'):
        a = 2
    elif(messageToDefine == 'modulo_3'):
        a = 3
    elif(messageToDefine == 'modulo_4'):
        a = 4

    doc = open('modulo_'+str(a)+'.pdf', 'rb')
    bot.send_document(chat_id, doc)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global parent_node

    if (message.text).lower() == 'si':
        parent_node = parent_node.yes
        nextMessage = parent_node.question
        if 'modulo' in nextMessage:
            send_document(nextMessage)
        else:
            bot.send_message(chat_id, nextMessage)
    elif (message.text).lower() == 'no':
        parent_node = parent_node.no
        nextMessage = parent_node.question
        if 'modulo' in nextMessage:
            send_document(nextMessage)
        else:
            bot.send_message(chat_id, nextMessage)

    else:
        nextMessage = "Mi spiace, non ho capito quello che hai detto... Riprova!"

bot.polling()
