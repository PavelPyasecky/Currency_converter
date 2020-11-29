from bs4 import BeautifulSoup
from decimal import Decimal


def calc(f_v, f_n, s_v, s_n, amount):
    coef = f_v / f_n * s_n / s_v
    return (amount * coef).quantize(Decimal('.0001'))


def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get('http://www.cbr.ru/scripts/XML_daily.asp',
                            params={
                                'date_req':date
                                })  # Использовать переданный requests
    soup = BeautifulSoup(response.content,'html.parser')
    first_cur = soup.find('charcode', text=cur_from)
    second_cur = soup.find('charcode', text=cur_to)
    if cur_from == "RUB":
        result = calc(Decimal('1'),
         Decimal('1'),
         Decimal(second_cur.find_next_sibling('value').string.replace(',','.')),
         Decimal(second_cur.find_next_sibling('nominal').string.replace(',','.')),
         amount
         )
    elif cur_to == "RUB":
        result = calc(Decimal(first_cur.find_next_sibling('value').string.replace(',','.')),
         Decimal(first_cur.find_next_sibling('nominal').string.replace(',','.')),
         Decimal('1'),
         Decimal('1'),
         amount
         )
    else:
        result = calc(Decimal(first_cur.find_next_sibling('value').string.replace(',','.')),
         Decimal(first_cur.find_next_sibling('nominal').string.replace(',','.')),
         Decimal(second_cur.find_next_sibling('value').string.replace(',','.')),
         Decimal(second_cur.find_next_sibling('nominal').string.replace(',','.')),
         amount
         )

    return result  # не забыть про округление до 4х знаков после запятой
