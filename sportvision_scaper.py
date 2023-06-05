import requests
from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_mysqldb import MySQL
from bs4 import BeautifulSoup

id_shop=2

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mysql'

mysql = MySQL(app)
cursor = mysql.cursor()

base_url='https://www.sportvision.ba/obuca/za-muskarce+za-zene+unisex/page-'
current_page=0

total_items_req=base_url+str(current_page)
sportvision_req=requests.get(total_items_req)

sportvision_req_soup=BeautifulSoup(sportvision_req.text, 'html.parser')
sportvision_req_soup.prettify()
page=sportvision_req_soup.findAll('li', {'class':'number'})
number_pages=int(page[-1].text)

while current_page < number_pages:
    print('--------------------------------------------')
    print("Upisano: " + str(current_page * 24))

    url = base_url + str(current_page)
    sportvision_r = requests.get(url)
    sportvision_soup=BeautifulSoup(sportvision_r.text, 'html.parser')
    sportvision_soup.prettify()

    all_content = sportvision_soup.findAll('div', {'data-productcategoryid': '1'})
    try:
        for link in all_content:
            name=link.findAll('div', {'class':'title'})
            price=link.findAll('div', {'class':'current-price price-with-discount'})
            image='https://www.sportvision.ba'+link.find('img')['src']
            ocjene=link.findAll('div', {'class':'item-rate-wrapper-stars'})
            if price:
                print(name[0].text.strip(),price[0].text.strip())
                print(image)
                if ocjene[0].find_all('div') != []:
                   sirina=ocjene[0].find_all('div')[0].find_all('div')[2].get('style')
                   ocjena=float(sirina[7:-1])*0.05
                   print(ocjena)
                cursor.execute("INSERT INTO articles(article,price,photo,review,shops_id) VALUES (%s,%s,%s,%s,%s)",
                            [name[0].text, price[0].text, image, ocjena, id_shop])
                mysql.connection.commit()
                cursor.close()
        current_page += 1
    except Exception as e:
        print(e)