import time,sqlite3
from bs4 import BeautifulSoup
import re
from selenium import webdriver


# create a connection with the sqlite database
conn = sqlite3.connect('indiamart.db')
def migrate(conn):
	conn.execute('''CREATE TABLE PRODUCTS
			 (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
			 PRODUCT           TEXT    NOT NULL,
			 SELLER        TEXT,
			 URL TEXT);''')

#uncomment this line when running the code first time
# migrateDb(conn)

# options for the starting chrome
option = webdriver.ChromeOptions()
option.add_argument('-incognito')

#url for scraping
url  = "https://www.indiamart.com/jyotipaperudyog/"

driver=webdriver.Chrome(executable_path='./chromedriver', chrome_options=option)

# open the page in chrome
driver.get(url)

# print(driver.title)

# find the product range button to click for getting the list of products being sold by the seller
product_range=driver.find_element_by_id("drpDwnMenu")
# click on the button
product_range.click()

# get the page source and parse it for dom traversing
bs=BeautifulSoup(driver.page_source, 'lxml')

# find all the product ranges in the page
products = bs.find_all('div', class_='prodrange')



links = []
for product in products:
	if product:
		# get the product range's url 
		links.append(url+product.find('a')['href'])

for link in links:
	# open each product range's page url
	driver.get(link)
	soup = BeautifulSoup(driver.page_source, 'lxml')
	# get all the products of that category
	ps = soup.find_all('div', id=re.compile("productnum"))
	for p in ps:
		# get the title of the product
		a = p.find('h2', class_="comp-titl").find('a')
		if a:
			# if title is found write the details into the db
			print (a.string)
			conn.execute("INSERT INTO PRODUCTS (PRODUCT, SELLER, URL) VALUES (?, ?, ?)", (a.string, url, a['href']))
			conn.commit()

conn.close()

driver.quit()