import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import lxml
from dateutil import parser


from modules import insert, find_period


HEADERS = {
    'Cookies': 'yandexuid=7872100861644332491; yuidss=7872100861644332491; my=YwA=; ymex=1972109901.yrts.1656749901;'
               ' yandex_gid=117428; gdpr=0; _ym_uid=1645464466702207110; amcuid=4972560311656757599;'
               ' is_gdpr=1; is_gdpr_b=CNzDcxCdfBgBKAI=; _ym_d=1657306071;',
    'Acceept-Language': 'ru-RU,ru;q=0.9',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/103.0.0.0 Safari/537.36',
    'sec-ch-ua-mobile': '?0'}


def find_rate(date):
    url = f'https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To={date}'
    response = requests.get(url, headers=HEADERS)
    text = response.text

    try:
        bool(parser.parse(date))
    except ValueError:
        return 'Дата должна быть строго в формате DD.MM.YYYY'

    soup = BeautifulSoup(text, 'html.parser')

    USD = str(soup.find_all(class_='data'))
    USD = [i for i in USD.split('</td>\n<td>')]

    for i in USD:
        if '</td>\n</tr>\n<tr>\n<td>' in i:
            ind = USD.index(i)
            lis = i.split('</td>\n</tr>\n<tr>\n<td>')
            USD.pop(ind)
            USD.insert(ind, lis[0])
            USD.insert(ind, lis[1])
    if '978' in USD:
        result = f'На {date} курс доллара: {USD[USD.index("978") + 1]}'
    else:
        result = f'На заданную дату нет установленного курса.'
    return result


def create_graph(date_start, date_end):

    try:
        bool(parser.parse(date_start))
    except ValueError:
        return 'Дата должна быть строго в формате DD.MM.YYYY'

    try:
        bool(parser.parse(date_end))
    except ValueError:
        return 'Дата должна быть строго в формате DD.MM.YYYY'

    datepd = pd.to_datetime(date_start)
    datepd_2 = pd.to_datetime(date_end)
    div = pd.date_range(start=datepd, end=datepd_2, periods=10)
    lis = {str(i).split(' ')[0] for i in div}
    lis = {f'{i[8:]}.{i[5:7]}.{i[:4]}' for i in lis}

    for i in lis:
        url = f'https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To={i}'
        response = requests.get(url, headers=HEADERS)
        text = response.text

        soup = BeautifulSoup(text, 'html.parser')

        USD = str(soup.find_all(class_='data'))
        USD = [i for i in USD.split('</td>\n<td>')]

        for item in USD:
            if '</td>\n</tr>\n<tr>\n<td>' in item:
                ind = USD.index(item)
                lis_temp = item.split('</td>\n</tr>\n<tr>\n<td>')
                USD.pop(ind)
                USD.insert(ind, lis_temp[0])
                USD.insert(ind, lis_temp[1])
        insert(i, USD[USD.index("978") + 1])

    result = find_period(lis)
    charts = chart(result)
    return charts


def chart(dict_dates):
    dict_temp = {}

    for i in dict_dates:
        for k, v in i.items():
            k = f'{k[6:]}-{k[3:5]}-{k[:2]}'
            dict_temp.setdefault(k, v)
    new_list = {}
    for key, value in dict_temp.items():
        key = pd.to_datetime(key)
        value = float(value.replace(',', '.'))
        new_list.setdefault(key, value)

    dates = [i for i in new_list.keys()]
    ts = pd.Series(data=new_list, index=sorted(dates))
    plt.figure(figsize=(10, 6))
    ax = ts.plot()
    fig = ax.get_figure()
    plt.xticks(sorted(dates))
    #plt.show()
    fig.savefig('graph.png')
    result = 'graph.png'
    return result


def find_other_rate(currency, date):
    url = f'https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To={date}'

    try:
        bool(parser.parse(date))
    except ValueError:
        return 'Дата должна быть строго в формате DD.MM.YYYY'

    info = pd.read_html(url)
    index = info[0]['Букв. код'] == currency
    rate = int(info[0][index]['Курс']) / 10000
    rate = f'{rate:.4f}'.replace('.', ',')
    name = str(info[0][index]["Валюта"]).split(' ')[4] + ' ' + str(info[0][index]["Валюта"]).split(' ')[5].split()[0]
    result = f'На {date} ЦБ РФ установил для валюты - {name} - следующий курс к рублю: {rate}'
    return result
