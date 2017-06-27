##Телеграм-бот для НКРЯ (поэтический корпус): получить ключевые параметры запроса от пользователя, задать запрос корпусу,
##распарсить выдачу и отправить пользователю наиболее важные пункты выдачи (число слов, документов, первую страницу выдачи)

import telebot
import conf
import urllib.request
import urllib.parse
import re
bot = telebot.TeleBot(conf.TOKEN)

def find_url(word): #находит в корпусе страничку по запросу пользователя
    word = urllib.parse.quote (word,safe='')
    ll = 'http://search2.ruscorpora.ru/search.xml?env=alpha&mycorp=&mysent=&mysize=&mysentsize=&mydocsize=&dpp=&spp=&spd=&text=lexform&mode=poetic&sort=gr_tagging&ext=10&nodia=1&req=' + word
    req = urllib.request.Request(ll) 
    response = urllib.request.urlopen(req) 
    result = response.read()
    result = str(result)
    return(result)

def find_data(result): #Находит количество вхождений и количество документов
    regex = '<br></p><p.*?>([0-9]*?)<.*?>([0-9]*?)<'
    res = re.search(regex, result)
    if res:
        number_of_documents = res.group(1)
        number_of_words = res.group(2)
        number_of_documents = str(number_of_documents)
        number_of_words = str(number_of_words)
    return (number_of_documents, number_of_words)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id, "Здравствуйте! Это бот, который ищет слова в поэтическом корпусе. Начнем? Напишите слово, которое будем искать")   


@bot.message_handler(func=lambda m: True) 
def send_result(message):
    word = str(message.text) 
    result = find_url(word)
    number_of_documents, number_of_words = find_data(result)
    print('yes')
    bot.send_message(message.chat.id, 'Результат:')
    answer = 'В выдаче ' + str(number_of_words) + ' слов и ' + str(number_of_documents) + ' документов.'
    bot.send_message(message.chat.id, answer)



if __name__ == '__main__':
    bot.polling(none_stop=True)
                         
    

##if __name__ == '__main__':
##    import os
##    app.debug = True
##    port = int(os.environ.get("PORT", 5000))
##    app.run(host='0.0.0.0', port=port)
