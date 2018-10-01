import time,sqlite3
from bs4 import BeautifulSoup
from selenium import webdriver

conn = sqlite3.connect('wordpress.db')
def migrate(conn):
	conn.execute('''CREATE TABLE POSTS
			 (ID INTEGER PRIMARY KEY AUTOINCREMENT ,
			 POST TEXT NOT NULL,
			 URL TEXT,
			 IMG TEXT);''')


#uncomment this line when running the code first time
# migrateDb(conn)

# options for the starting chrome
option = webdriver.ChromeOptions()
option.add_argument('-incognito')

#url for scraping
url  = "https://www.thisisyourkingdom.co.uk"


driver=webdriver.Chrome(executable_path='./chromedriver', chrome_options=option)

# open the page in chrome
driver.get(url)

soup = BeautifulSoup(driver.page_source, 'lxml')

# find the posts from the page
posts = soup.find_all('div', class_='boxedFeature')

for post in posts:
	# get the full post's url
	url = post.find('a')['href']
	# get the truncated post 
	p = post.find('p').text
	# get the image url
	img = post.find('img')['src']
	print (p, img, url)
	conn.execute("INSERT INTO POSTS (POST,IMG, URL) VALUES (?, ?, ?)", (p, img, url))
	conn.commit()

driver.quit()