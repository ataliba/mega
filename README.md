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
