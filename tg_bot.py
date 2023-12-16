import telebot as tb

bot = tb.TeleBot('6719997416:AAGlbZmDTN_d41andMhDQSQ1QKb5rRQRHWc')


@bot.message_handler(commands=['start', 'hello', 'main'])
def main(message):
    bot.send_message(message.chat.id, f'Привет')


@bot.message_handler(commands=['help'])
def what_can_u_do(message):
    bot.send_message(message.chat.id, 'Моей задачей является запись цены товара и её изменения спустя время.'
                                      'Запись новой цены происходит по запросу пользователя.')


@bot.message_handler()
def any_message(message):
    bot.send_message(message.chat.id, f'{message.chat.username}, пожалуйста, выберите команду /help')


bot.polling(none_stop=True)