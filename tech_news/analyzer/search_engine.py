from tech_news.database import db
from datetime import datetime


# Requisito 7
def search_by_title(title):
    itens = []
    search = db.news.find({'title': {"$regex": title, "$options": "i"}})

    for item in search:
        itens.append((item['title'], item['url']))

    return itens


# Requisito 8
def search_by_date(date):
    itens = []
    try:
        date = "{:%d/%m/%Y}".format(datetime.strptime(date, '%Y-%m-%d'))
    except ValueError:
        raise ValueError('Data inválida')

    search = db.news.find({'timestamp': date})
    for item in search:
        itens.append((item['title'], item['url']))

    return itens


# Requisito 9
def search_by_category(category):
    itens = []
    search = db.news.find({'category': {"$regex": category, "$options": "i"}})
    for item in search:
        itens.append((item['title'], item['url']))

    return itens
