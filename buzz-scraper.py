import requests
from bs4 import BeautifulSoup
import mysql.connector

id_shop = 2

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="sportShop"
)

cursor = mydb.cursor()

base_url = 'https://www.buzzsneakers.ba/patike/za-muskarce+unisex/za-odrasle/'
current_page = 0

total_items_req = base_url + str(current_page)
buzz_req = requests.get(total_items_req)

buzz_req_soup = BeautifulSoup(buzz_req.text, 'html.parser')
buzz_req_soup.prettify()
page = buzz_req_soup.findAll('li', {'class': 'number'})
number_pages = int(page[-1].text)

while current_page < number_pages:
    print('--------------------------------------------')
    print("Upisano: " + str(current_page * 24))

    url = base_url + str(current_page)
    buzz_r = requests.get(url)
    buzz_soup = BeautifulSoup(buzz_r.text, 'html.parser')
    buzz_soup.prettify()

    all_content = buzz_soup.findAll('div', {'data-productcategoryid': '1'})
    try:
        for link in all_content:
            name = link.findAll('div', {'class': 'title'})
            price = link.findAll('div', {'class': 'current-price'})
            image = 'https://www.buzz.ba' + link.find('img')['src']
            
            if price:
                print(name[0].text.strip(), image, price[0].text.replace(" ", ""))
                cursor.execute("INSERT INTO articles(article,price,photo,shops_id,review) VALUES (%s,%s,%s,%s,%s)",
                                   [name[0].text.strip(), price[0].text.replace(" ", ""), image, id_shop, 0.0])
                mydb.commit()
        current_page += 1
    except Exception as e:
        print(e)