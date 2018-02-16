import csv
import json
import helpers

tmdb = open('tmdb_5000_movies.csv', encoding='utf8')
reader = csv.DictReader(tmdb)
tmdb_movies = list(reader)
tmdb.close()

tmdbCredit = open('tmdb_5000_credits.csv', encoding='utf8')
reader = csv.DictReader(tmdbCredit)
tmdb_credits = list(reader)
tmdbCredit.close()

dc = open('filmdeathcounts.csv', encoding='utf8')
reader = csv.DictReader(dc)
death_counts = list(reader)
dc.close()

aa = open('academy_awards.csv', encoding='utf8')
reader = csv.DictReader(aa)
awards = list(reader)
aa.close()


### Create the basic data structures to gather information

actor_names = set()
unicode_problems = set()
movie_names = set()

for movie in tmdb_movies:
	movie_names.add(movie['title'].strip())

for movie in death_counts:
	movie_names.add(movie['Film'].strip())

for award in awards:
	award['Year'] = award['Year'].split()[0]
	if("Act" in award['Category']):
		award['Info'] = award['Info'].split(' {')[0]

for award in awards:
	if('Act' in award['Category']):
		movie_names.add(award['Info'].strip())
		actor_names.add(award['Nominee'].strip())
	else:
		movie_names.add(award['Nominee'].strip())

for credit in tmdb_credits:
	cast = json.loads(credit['cast'])
	for p in cast:
		name = p['name'].strip()
		actor_names.add(name)


### Gather our data into dictionaries

movieDict = {}

for movie in tmdb_movies:
	name = movie['title'].strip()
	budget = int(movie['budget'])
	revenue = int(movie['revenue'])
	try:
		runtime = int(float(movie['runtime']))
	except:
		runtime = 0
	vote_avg = float(movie['vote_average'])
	vote_count = int(movie['vote_count'])
	try:
		release = int(movie['release_date'].split('-')[0])
	except:
		release = 0

	movieDict[name] = {'actors': set(), 'budget': 0, 'revenue': 0, 'runtime': 0, 'release': 0, 'vote_avg': 0.0, 'vote_count': 0, 'kills': 0, 'rating': "", 'genre': set()}
	movieDict[name]['budget'] = budget
	movieDict[name]['revenue'] = revenue
	movieDict[name]['runtime'] = runtime
	movieDict[name]['release'] = release
	movieDict[name]['vote_avg'] = vote_avg
	movieDict[name]['vote_count'] = vote_count
	genres = []
	genreJson = json.loads(movie['genres'])
	for x in genreJson:
		genres.append(x['name'])
	movieDict[name]['genre'] = genres

for credit in tmdb_credits:
	movie = credit['title'].strip()
	cast = json.loads(credit['cast'])
	for p in cast:
		name = p['name'].strip()
		movieDict[movie]['actors'].add(name)

for movie in death_counts:
	name = movie['Film'].strip()

	if name not in movieDict.keys():
		movieDict[name] = {'actors': set(), 'budget': 0, 'revenue': 0, 'runtime': 0, 'release': 0, 'vote_avg': 0.0, 'vote_count': 0, 'kills': 0, 'rating': "", 'genre': set()}
		movieDict[name]['runtime'] = int(movie['Length_Minutes'])
		movieDict[name]['vote_avg'] = float(movie['IMDB_Rating'])
		genres = movie['Genre'].split('|')
		movieDict[name]['genre'] = genres
		movieDict[name]['release'] = int(movie['Year'])

	movieDict[name]['kills'] = int(movie['Body_Count'])
	movieDict[name]['rating'] = movie['MPAA_Rating']

for award in awards:
	name = ""
	if('Act' in award['Category']):
		name = award['Info'].strip()
	else:
		name = award['Nominee'].strip()
	if name not in movieDict.keys():
		movieDict[name] = {'actors': set(), 'budget': 0, 'revenue': 0, 'runtime': 0, 'release': 0, 'vote_avg': 0.0, 'vote_count': 0, 'kills': 0, 'rating': "", 'genre': set()}


### Connect to our database

cursor, conn = helpers.connect_to_database('localhost', 'movies', 'Armann', 'postgres')


### Insert the actors

insertstring = "INSERT INTO actors (name) VALUES "
numberofrowstoinsert = 2000
counter = 0
values = []

for name in actor_names:
    values.append( (name,) )
    counter += 1

    if counter == numberofrowstoinsert:
        args_str = b','.join(cursor.mogrify("(%s)", x) for x in values)
        cursor.execute(insertstring + args_str.decode('utf-8'))
        values = []
        counter = 0

if len(values) > 0:
    args_str = b','.join(cursor.mogrify("(%s)", x) for x in values)
    cursor.execute(insertstring + args_str.decode('utf-8'))
    values = []
    counter = 0


### Insert into movies

for name, values in movieDict.items():
	tables = ['name']
	ins_values = [name,]

	if values['budget'] > 0:
		tables.append('budget')
		ins_values.append(values['budget'])
	if values['revenue'] > 0:
		tables.append('revenue')
		ins_values.append(values['revenue'])
	if values['runtime'] > 0:
		tables.append('runtime')
		ins_values.append(values['runtime'])
	if values['release'] > 0:
		tables.append('release')
		ins_values.append(values['release'])
	if values['vote_avg'] > 0:
		tables.append('vote_avg')
		ins_values.append(values['vote_avg'])
	if values['vote_count'] > 0:
		tables.append('vote_count')
		ins_values.append(values['vote_count'])
	if values['kills'] > 0:
		tables.append('kills')
		ins_values.append(values['kills'])
	if values['rating'] != "":
		tables.append('rating')
		ins_values.append(values['rating'])

	insertstring = "INSERT INTO movies ({}) VALUES ".format(','.join(tables))

	if len(tables) == 9:
		cursor.execute(insertstring + "(%s,%s,%s,%s,%s,%s,%s,%s,%s)", ins_values)	
	elif len(tables) == 8:
		cursor.execute(insertstring + "(%s,%s,%s,%s,%s,%s,%s,%s)", ins_values)
	elif len(tables) == 7:
		cursor.execute(insertstring + "(%s,%s,%s,%s,%s,%s,%s)", ins_values)
	elif len(tables) == 6:
		cursor.execute(insertstring + "(%s,%s,%s,%s,%s,%s)", ins_values)
	elif len(tables) == 5:
		cursor.execute(insertstring + "(%s,%s,%s,%s,%s)", ins_values)
	elif len(tables) == 4:
		cursor.execute(insertstring + "(%s,%s,%s,%s)", ins_values)
	elif len(tables) == 3:
		cursor.execute(insertstring + "(%s,%s,%s)", ins_values)
	elif len(tables) == 2:
		cursor.execute(insertstring + "(%s,%s)", ins_values)
	elif len(tables) == 1:
		cursor.execute(insertstring + "(%s)", ins_values)


### Insert into Genres

insertstring = "INSERT INTO genres (movie, genre) VALUES "
numberofrowstoinsert = 2000
counter = 0
values = []

for name, movie_values in movieDict.items():
	if len(movie_values['genre']) > 0:
		for genre in movie_values['genre']:
			values.append( (name, genre) )
			counter += 1

			if counter == numberofrowstoinsert:
				args_str = b','.join(cursor.mogrify("(%s,%s)", x) for x in values)
				cursor.execute(insertstring + args_str.decode('utf-8'))
				values = []
				counter = 0

if len(values) > 0:
    args_str = b','.join(cursor.mogrify("(%s,%s)", x) for x in values)
    cursor.execute(insertstring + args_str.decode('utf-8'))
    values = []
    counter = 0


### Insert into castmembers

insertstring = "INSERT INTO castmembers (movie, actor) VALUES "
numberofrowstoinsert = 2000
counter = 0
values = []

for name, movie_values in movieDict.items():
	if len(movie_values['actors']) > 0:
		for actor in movie_values['actors']:
			values.append( (name, actor) )
			counter += 1

			if counter == numberofrowstoinsert:
				args_str = b','.join(cursor.mogrify("(%s,%s)", x) for x in values)
				cursor.execute(insertstring + args_str.decode('utf-8'))
				values = []
				counter = 0

if len(values) > 0:
    args_str = b','.join(cursor.mogrify("(%s,%s)", x) for x in values)
    cursor.execute(insertstring + args_str.decode('utf-8'))
    values = []
    counter = 0


### Insert into awards

insertstring = "INSERT INTO awards (year, category, movie, actor, won) VALUES "
numberofrowstoinsert = 2000
counter = 0
values = []

for award in awards:
	if('Act' in award['Category']):
		year = int(award['Year'])
		category = award['Category']
		movie = award['Info'].strip()
		actor = award['Nominee'].strip()
		won = True if award['Won'] == "YES" else False

		values.append( (year, category, movie, actor, won) )
		counter += 1

		if counter == numberofrowstoinsert:
			args_str = b','.join(cursor.mogrify("(%s,%s,%s,%s,%s)", x) for x in values)
			cursor.execute(insertstring + args_str.decode('utf-8'))
			values = []
			counter = 0

if len(values) > 0:
    args_str = b','.join(cursor.mogrify("(%s,%s,%s,%s,%s)", x) for x in values)
    cursor.execute(insertstring + args_str.decode('utf-8'))
    values = []
    counter = 0

insertstring = "INSERT INTO awards (year, category, movie, won) VALUES "
numberofrowstoinsert = 2000
counter = 0
values = []

for award in awards:
	if('Act' not in award['Category']):
		year = int(award['Year'])
		category = award['Category']
		movie = award['Nominee'].strip()
		won = True if award['Won'] == "YES" else False

		values.append( (year, category, movie, won) )
		counter += 1

		if counter == numberofrowstoinsert:
			args_str = b','.join(cursor.mogrify("(%s,%s,%s,%s)", x) for x in values)
			cursor.execute(insertstring + args_str.decode('utf-8'))
			values = []
			counter = 0

if len(values) > 0:
    args_str = b','.join(cursor.mogrify("(%s,%s,%s,%s)", x) for x in values)
    cursor.execute(insertstring + args_str.decode('utf-8'))
    values = []
    counter = 0

conn.commit()
cursor.close()
conn.close()