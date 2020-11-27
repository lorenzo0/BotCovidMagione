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

    def get_child(self, messageReceived, default_node):
      if messageReceived=='indietro':
        if self.parent==None:
          return self, 'sono alla root'
        return self.parent, ''

      if self.no==None or self.yes==None:
        return default_node, 'todo_restart'
      
      if messageReceived=='si':
        return self.yes, ''
      
      if messageReceived=='no':
        return self.no, ''
      
        
      return self, 'Mi spiace, non ho capito quello che hai detto... Riprova!'

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
  elif prop[2] == 'no':
    parent_node.no = new_node
  node_list.append(new_node)

chat_id = 774306756
parent_node = root_node

welcome_message = "Ciao! Sono il bot che ti aiuterà a comprendere, al meglio, quale dei moduli bisogna consegnare in ogni possibile casistica. \nTi farò una serie di domande e ti chiedo gentilmente di rispondermi in modo molto preciso 'Si' oppure 'No'. \nMi potrai contattare ad ogni momento. \nSe ci sono problemi tecnici con il bot, ti prego di contattare il mio creatore, attraverso la mail lorenzopisa00@gmail.com. \n\nIniziamo quindi con una domanda semplice, tuo figlio è stato allontanato da scuola?"

# todo help
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id, welcome_message)

def send_document(messageToDefine):
    d = {'modulo_1':'1','modulo_2':'2','modulo_3':'3','modulo_4':'4'}
    
    doc = open('modulo_'+d[messageToDefine]+'.pdf', 'rb')
    bot.send_document(chat_id, doc)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    global parent_node

    #toreview
    parent_node, nextMessage = parent_node.get_child((message.text).lower(), root_node)
    
    if 'modulo' in parent_node.question:
      send_document(parent_node.question)
    else:
      nextMessage += '\n' + parent_node.question
      bot.send_message(chat_id, nextMessage)

bot.polling()
