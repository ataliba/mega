#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from cookielib import CookieJar
import urllib
import urllib2
import re
import sys
import os.path


"""
Readme.md

Author: Leandro T. Souza <leandrotoledo [at] member [dot] fsf [dot] org>
Modified by : Ataliba Teixeira <ataliba [at] pm [dot] me> 
Update: Thu, 27 17:45 2012
"""

URL_CONCURSO = 'http://www1.caixa.gov.br/loterias/loterias/megasena/megasena_pesquisa_new.asp?submeteu=sim&opcao=concurso&txtConcurso='
ARQ_CONTADOR='contador.txt'

"""
Coloque aqui as informações do seu bot : 

TELEGRAM_BOT = 1 caso queira ser notificado, 0 caso não queira
BOT_KEY = coloque a chave do bot que você recebeu via BOTFATHER no telegram

"""

def getApostas():
    apostas = []

    if os.path.isfile(concurso):
      with open(concurso, 'r') as f:
        for r in f:
            r = r.replace('\n', '')
            apostas.append(r)
    else:
       print 'Você esqueceu de criar o arquivo do concurso' + ' ' + concurso
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
        print 'Ainda não saiu o resultado...'
        exit()

    
    resultado = re.findall('\d{2}', data[20]) # resultado ordenado

    return resultado


def sorteio(apostas, resultado):
    print '[ TOTAL DE ACERTOS ] | JOGO'
    print

    for aposta in apostas:
        aposta = aposta.split('-')

        total = 0
        for i in resultado:
            for j in aposta:
                if i == j:
                    total += 1

        if total == 6:
            print '[%s] | %s GANHOU!' % (total, '-'.join(aposta))
        else:
            print '[%s] | %s' % (total, '-'.join(aposta))

    print
    print 'JOGO:', '-'.join(resultado)

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
        print 'Crie o arquivo counter.txt com o número do primeiro concurso que você quer consultar'
        print 'Por exemplo: 1450'
        exit()
    main(concurso)
