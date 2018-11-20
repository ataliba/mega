#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from cookielib import CookieJar
import urllib
import urllib2
import re
import sys
import os.path


"""
megang
====

Segunda geração do scriptzinho em Python feito para conferir os jogos da megasena

Instruções
==========

1) Edite o arquivo contador.txt com o número do primeiro sorteio que você irá conferir.
   Exemplo, caso seja o concurso 1470, coloque no conteúdo do arquivo este número.

2) Crie um arquivo de nome 1470 e ali coloque os números que você apostou ( caso seja mais de um jogo,
coloque mais de uma linha ).

04-07-12-25-37-43
02-09-12-16-28-33-43-46-51-52
02-05-07-11-17-34-42-54

3) Executar o script :

$ ./mega.py


4) É possível colocar no cron

0 5 * * 1 /home/ataliba/mega.py 1450 | mail -s "Resultado Mega" ataliba@pm.me


4) Se você ganhar faça um donate pra mim! ;-)


Creditos ao Leandro de Souza que criou o script original e me deu a base para fazer este aqui :)

TODO:

* Terminar a parte de integração com o Telegram
* Modificar os comentários internos do script


Author: Leandro T. Souza <leandrotoledo [at] member [dot] fsf [dot] org>
Modified by : Ataliba Teixeira <ataliba [at] pm [dot] me> 
Update: Thu, 27 17:45 2012
"""

URL_CONCURSO = 'http://www1.caixa.gov.br/loterias/loterias/megasena/megasena_pesquisa_new.asp?submeteu=sim&opcao=concurso&txtConcurso='
ARQ_CONTADOR='contador.txt'

"""
Coloque aqui as informações do seu bot : 

TELEGRAM_BOT = True caso queira ser notificado, False caso não queira
BOT_KEY = coloque a chave do bot que você recebeu via BOTFATHER no telegram
CHAT = código do chat para o qual serão enviadas as mensagens 

"""

TELEGRAM_BOT=True
BOT_KEY=''
CHAT=''

def TelegramBot(Mensagem):
    # motando a url a ser usada para enviar mensagem no Telegram 
    
    URL_BOT='https://api.telegram.org/bot' + BOT_KEY + 'sendMessage?chat_id=' + CHAT + '&text=' + Mensagem
     
    req = urllib2.Request(URL_BOT)
    response = urllib2.urlopen(req)
    the_page = response.read()

def getApostas():
    apostas = []

    if os.path.isfile(concurso):
      with open(concurso, 'r') as f:
        for r in f:
            r = r.replace('\n', '')
            apostas.append(r)
    else:
       Mensagem = 'Você esqueceu de criar o arquivo do concurso' + ' ' + concurso
       if TELEGRAM_BOT:
          TelegramBot(Mensagem)
       else:
          print Mensagem

       exit()

    return apostas


def getResultado(concurso):
    
    url = URL_CONCURSO + str(concurso)
    cj = CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    url = opener.open(url)
    html = url.read()
    url.close()

    data = html.split('|')
    if data[-1].decode('iso-8859-1', 'utf-8') == u'Não existe resulado!': # sim, resulado...
       Mensagem='Ainda não saiu o resultado...'    
       if TELEGRAM_BOT: 
          TelegramBot(Mensagem)
       else:
          print 'Ainda não saiu o resultado...'
        exit()

    
    resultado = re.findall('\d{2}', data[20]) # resultado ordenado

    return resultado


def sorteio(apostas, resultado):
    Mensagem = '[ TOTAL DE ACERTOS ] | JOGO'
    Mensagem = Mensagem + '\n'

    for aposta in apostas:
        aposta = aposta.split('-')

        total = 0
        for i in resultado:
            for j in aposta:
                if i == j:
                    total += 1

        if total == 6:
            Mensagem = Mensagem + '[%s] | %s GANHOU!' % (total, '-'.join(aposta))
        else:
            Mensagem = Mensagem + '[%s] | %s' % (total, '-'.join(aposta))

    Mensasgem = Mensagem + '\n'
    Mensagem = Mensagem + 'JOGO:', '-'.join(resultado)

    if TELEGRAM_BOT: 
       TelegramBot(Mensagem)
    else: 
       print Mensagem


    concursomaisum = int(concurso) + 1

    file_counter = open(ARQ_CONTADOR, 'w')
    file_counter.write(str(concursomaisum))
    file_counter.close()


def main(concurso):
    apostas = getApostas()
    resultado = getResultado(concurso)

    sorteio(apostas, resultado)


if __name__ == '__main__':
    try:
        file_counter = open(ARQ_CONTADOR, 'r')
        concurso = file_counter.readline().rstrip()
        file_counter.close()
    except IOError:
        print 'Crie o arquivo contador.txt com o número do primeiro concurso que você quer consultar'
        print 'Por exemplo: 1450'
        exit()
    main(concurso)
