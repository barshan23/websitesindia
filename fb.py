import requests,sqlite3,json

# this is the page access token that is needed for accessing data of a facebook page. And for a unreviewed fb apps,
# we can only access the pages of the users from whose account the access token is generated
page_access_token = "EAAKpTuo29L0BABb3SL1HMVeuC4vIZB3ZCjPzZBpijNUOFzjP52iqWXkXYTzvb092asJAUOUDZBcqZAOnBc9F0KqZAA4kyi2daYZBYTz6F3QDEhZB5gHovNuiKhJRZCRjZAZApGVL6P2wZAEHAmZBUxawu1xcyVnqJCr0ZAuy2QTy2BcG0E3kzILXnPwIDqCxvnriA5jTm6DCns8h5pygZDZD"


base_url = "https://graph.facebook.com/v3.1/"

# connection object for the sqlite database
conn = sqlite3.connect("fb_page_data.db")

# get the cursor object from the connection object
cur = conn.cursor()

def migrateDb(cur):
	# call this to create the table with cursor object as the argument
	cur.execute('''
		CREATE TABLE posts (id text, created_time text, message text)
		''')
	# photos table
	cur.execute('''
		CREATE TABLE photos (id text, created_time text, link text)
		''')

#uncomment this line when running the code first time
# migrateDb(cur)


# page_id = raw_input("Enter the page id to fetch posts, pictures(only links), videos(only links)")
page_id = "transactbooks"

posts = json.loads(requests.get(base_url+page_id+'/posts?access_token='+page_access_token).text)['data']

for post in posts:
	print post
	if not 'message' in post:
		continue

	if 'created_time' in post:
		created_time = post['created_time']
	if 'id' in post:
		id = post['id']
	cur.execute("INSERT INTO posts VALUES (?,?,?)", (id, created_time, post['message']))

# commit the changes to the database
conn.commit()

for row in cur.execute("SELECT * FROM posts"):
	print row

# now let's fetch the photos of the page
pictures = json.loads(requests.get(base_url+page_id+'/photos?fields=link,created_time&access_token='+page_access_token).text)['data']

for picture in pictures:
	if 'link' in picture:
		# insert the links to the database
		cur.execute("INSERT INTO photos VALUES (?,?,?)",(picture['id'], picture['created_time'], picture['link']))
conn.commit()

for row in cur.execute("SELECT * FROM photos"):
	print row