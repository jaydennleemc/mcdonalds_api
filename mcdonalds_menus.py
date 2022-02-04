import os
import requests
from bs4 import BeautifulSoup

# Get full menu data
r = requests.get('https://www.mcdonalds.com.hk/full-menu/')
soup = BeautifulSoup(r.text, 'lxml')

Catalogs_path = './Catalogs'
Menus_path = './Menus'


menus = soup.find('div', class_='menu_col border')

links = []
titles = []
images = []

for i in menus:
    link = i.find('a')
    if link is not -1:
        print(link.attrs['href'])
        links.append(link.attrs['href'])

    title = i.find('span')
    if title is not -1:
        print(title.text)
        titles.append(title.text)

    img = i.find('img')
    if img is not -1:
        print(img.attrs['src'])
        images.append(img.attrs['src'])

# Dwonload catalogs
print('-------- Start download catalogs --------')
if (os.path.isdir(Catalogs_path) == False):
    os.mkdir(Catalogs_path)

for i in zip(titles, images):
    name = i[0].replace(' ', '').replace('\n', '') + '.png'
    url = i[1]
    print(name, url)
    r = requests.get(url)
    img_path = f'{Catalogs_path}/{name}'
    with open(img_path, 'wb') as f:
        f.write(r.content)


# Download menus
if (os.path.isdir(Menus_path) == False):
    os.mkdir(Menus_path)
print('-------- Start download menus --------')
for i in links:
    r = requests.get(i)
    s = BeautifulSoup(r.text, 'lxml')
    title = s.find('h1', class_='page_title font_bold size_56')
    print(title.text)
    if os.path.isdir(f'{Menus_path}/{title.text}') == False:
        os.mkdir(f'{Menus_path}/{title.text}')
    divs = s.find_all('div', class_='menu_category_item flex_item_3')
    for j in divs:
        img = j.find('img')
        if img is not -1:
            url = img.attrs['src']
            name = j.find('h5').text + '.png'
            name = name.replace('/', '-')
            
            print(url, name)
            img_path = f'{Menus_path}/{title.text}/{name}'
            r = requests.get(url)
            with open(img_path, 'wb') as f:
                f.write(r.content)
