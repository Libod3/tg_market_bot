import requests as rqt
import bs4


session = rqt.Session()
session.headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    "Accept-Language": "ru"
}


def load_page():
    url = "https://market.yandex.ru/product--kruzhka-khameleon-dlia-chaia-shrek-mem-zelenyi-ogr/1910133384?sponsored=1&sku=102209585030&do-waremd5=Zxh2Ed-gh8j1cTDX6_wCWQ&uniqueId=6188840"
    res = session.get(url)
    res.raise_for_status()
    return res.text


def parse_page(text):
    soup = bs4.BeautifulSoup(text, 'lxml')
    all_headers = soup.select('h3')
    for header_i in all_headers:
        header_i_text = header_i.text
        if "Цена с картой Яндекс Пэй:" in header_i_text:
            return parse_info(header_text=header_i_text)


def parse_info(header_text):
    result_info = header_text[header_text.rfind(':') + 1:]
    return result_info


def run():
    text = load_page()
    return parse_page(text)


print(run())


