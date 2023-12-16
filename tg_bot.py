import telebot as tb
import requests as rqt
import bs4
import csv

session = rqt.Session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    "Accept-Language": "ru"
}

headers_for_csv = (
    'Сслыка',
    'Имя товара',
    'Цена товара'
)

bot = tb.TeleBot('6719997416:AAGlbZmDTN_d41andMhDQSQ1QKb5rRQRHWc')


@bot.message_handler(commands=['start', 'hello', 'main'])
def main(message):
    bot.send_message(message.chat.id, f'Привет, для подробной ифнормации напишите /help')


@bot.message_handler(commands=['help'])
def what_can_u_do(message):
    bot.send_message(
        message.chat.id,
        'Моей задачей является запись цены товара и её изменения спустя время.'
        'Запись новой цены происходит по запросу пользователя'
        'Запись работает только на сайт https://market.yandex.ru и только на странице '
        'конкретного товара.\n'
        'Для внесения товара в базу данных напишите /check_the_price'
    )


@bot.message_handler(commands=['check_the_price'])
def check_price(message):
    bot.send_message(
        message.chat.id,
        'Введите ссылку на страницу товара. \n'
        'Важно: прочитайте правило пользования с помощью команды /help')


@bot.message_handler()
def any_message(message):
    if 'https://market.yandex.ru/' in message.text:
        save_results(message.text)
        bot.send_message(message.chat.id, 'Ваши данные записаны!')
    else:
        bot.send_message(message.chat.id, f'{message.chat.username}, пожалуйста, напишите команду /help')


def load_page(url):
    res = session.get(url)
    res.raise_for_status()
    return res.text


def parse_page(text):
    soup = bs4.BeautifulSoup(text, 'lxml')

    all_headers_h3 = soup.select('h3')
    price = find_price(all_headers=all_headers_h3)

    all_headers_h1 = soup.select('h1')
    name = find_name(all_headers=all_headers_h1)

    return [name, price]


def find_price(all_headers):
    for header_info_h3 in all_headers:
        header_i_text = header_info_h3.text
        if "Цена с картой Яндекс Пэй:" in header_i_text:
            price = parse_info(header_text=header_i_text)
            return price


def find_name(all_headers):
    for headers_info_h1 in all_headers:
        headers_j_text = headers_info_h1.text
        if headers_j_text is not None:
            return headers_j_text


def parse_info(header_text):
    result_info = header_text[header_text.rfind(':') + 1:]
    return result_info


def save_results(url):
    path = '/Users/libod/PycharmProjects/tg_market_bot/database.csv'
    with open(path, 'a') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        inf_about_product = parse_page(load_page(url))
        headers_for_next_line = (
            '0',
            str(inf_about_product[0]),
            str(inf_about_product[1])
        )

        writer.writerow(headers_for_next_line)


bot.polling(none_stop=True)
