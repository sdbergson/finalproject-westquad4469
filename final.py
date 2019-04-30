import Spotify_info
import spotipy
import secrets
import spotipy.util as util
import json
from bs4 import BeautifulSoup
import requests
import sqlite3 as sqlite
import billboard
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import csv
plotly.tools.set_credentials_file(username='sdbergson', api_key='GokEqMNANQQKDSJide4v')


spotify_token = util.oauth2.SpotifyClientCredentials(client_id=Spotify_info.client_id, client_secret=Spotify_info.client_secret)
cache1_token = spotify_token.get_access_token()
spotify = spotipy.Spotify(cache1_token)


#Get Spotify Data
artist_names = ['Post Malone', 'Ariana Grande', 'Cardi B', 'J. Cole', 'Travis Scott', 'Khalid', 'Meek Mill', 'Marshmello', 'Billie Eilish']
spotify_list = []
for s in artist_names:
	results = spotify.search(q='artist:' + s , type='artist')
	items = results['artists']['items']
	if len(items) > 0:
		artist = items[0]
		y = str((artist['uri']))
		x = str(artist['followers']['total'])
		p = str(artist['popularity'])

	lz_uri = y
	



	results = spotify.artist_top_tracks(lz_uri)

	for track in results['tracks'][:10]:
		top10tracks = ( track['name'])
		_artist = s
		_followers = x
		_popularity = p
		_song = track['name']
		_popularity_s = track['popularity']
		sp_tuple = (_artist, _followers, _song, _popularity, _popularity_s)
		spotify_list.append(sp_tuple)





#Get Billboard Data
chart = billboard.ChartData('hot-100')

billboard_list = []
for x in chart:
	_title = x.title
	_artist = x.artist
	_peak = x.peakPos
	_last = x.lastPos
	_weeks = x.weeks
	_rank = x.rank

	my_tuple =  (_title, _artist, _peak, _last, _weeks, _rank,)
	billboard_list.append(my_tuple)





#Creating the Database

conn = sqlite.connect('Billboard.sqlite')
cur = conn.cursor()



cur.execute('CREATE TABLE IF NOT EXISTS Billboard(title TEXT, artist TEXT, peak INTEGER, last INTEGER, weeks INTEGER, rank INTEGER, UNIQUE(rank))')

cur.execute('SELECT * FROM Billboard')

fetch = cur.fetchall()
leng = len(fetch)


if leng < 20:
	for t in billboard_list[:20]:
	
		cur.execute('''INSERT OR IGNORE INTO Billboard (title, artist, peak, last, weeks, rank) VALUES (?, ?, ?, ?, ?, ?)''', t)
elif leng >= 20 and leng < 40: 
	for t in billboard_list[20:40]:
	
		cur.execute('''INSERT OR IGNORE INTO Billboard (title, artist, peak, last, weeks, rank) VALUES (?, ?, ?, ?, ?, ?)''', t)
elif leng >= 40 and leng < 60:
	for t in billboard_list[40:60]:
	
		cur.execute('''INSERT OR IGNORE INTO Billboard (title, artist, peak, last, weeks, rank) VALUES (?, ?, ?, ?, ?, ?)''', t)
elif leng >= 60 and leng < 80:
	for t in billboard_list[60:80]:
	
		cur.execute('''INSERT OR IGNORE INTO Billboard (title, artist, peak, last, weeks, rank) VALUES (?, ?, ?, ?, ?, ?)''', t)
elif leng >= 80 and leng < 100:
	for t in billboard_list[80:100]:
	
		cur.execute('''INSERT OR IGNORE INTO Billboard (title, artist, peak, last, weeks, rank) VALUES (?, ?, ?, ?, ?, ?)''', t)


conn.commit()







conn = sqlite.connect('Billboard.sqlite')
cur = conn.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS Spotify(artist TEXT, followers TEXT, song INTEGER, popularity INTEGER, popularitys INTEGER, UNIQUE (song))')

cur.execute('SELECT * FROM Spotify')

fetch1 = cur.fetchall()
leng1 = len(fetch1)


if leng1 < 20: 
	for q in spotify_list[:20]:
	
		cur.execute('''INSERT OR IGNORE INTO Spotify (artist, followers, song, popularity, popularitys) VALUES (?, ?, ?, ?, ?)''', q)

elif leng1 >= 20 and leng1 < 40: 
	for q in spotify_list[20:40]:
	
		cur.execute('''INSERT OR IGNORE INTO Spotify (artist, followers, song, popularity, popularitys) VALUES (?, ?, ?, ?, ?)''', q)


elif leng1 >= 40 and leng1 < 60: 
	for q in spotify_list[40:60]:
	
		cur.execute('''INSERT OR IGNORE INTO Spotify (artist, followers, song, popularity, popularitys) VALUES (?, ?, ?, ?, ?)''', q)


elif leng1 >= 60 and leng1 < 80: 
	for q in spotify_list[60:80]:
	
		cur.execute('''INSERT OR IGNORE INTO Spotify (artist, followers, song, popularity, popularitys) VALUES (?, ?, ?, ?, ?)''', q)


elif leng1 >= 80 and leng1 < 100: 
	for q in spotify_list[80:100]:
	
		cur.execute('''INSERT OR IGNORE INTO Spotify (artist, followers, song, popularity, popularitys) VALUES (?, ?, ?, ?, ?)''', q)

conn.commit()


conn = sqlite.connect('Billboard.sqlite')
cur = conn.cursor()
cur.execute('SELECT artist , popularity FROM Spotify')



	
popularity_dict = {}
for row in cur:
	art = row[0]
	pop = row[1]
	popularity_dict[art] = pop


#Get Plot One

conn = sqlite.connect('Billboard.sqlite')
cur = conn.cursor()
cur.execute('SELECT artist ,popularitys, song FROM Spotify')

art_dict = {}
art_song_dict = {}
pop_s_list = []
art_list = []
song_list = []
for row in cur:
	art = row[0].lower()
	pop_s = row[1]
	pop_s_list.append(pop_s) 
	song = row[2].lower()
	
	art_list.append(art)
	song_list.append(song)


art_dict[art_list[10]] = sum(pop_s_list[10:20]) / 10
art_dict[art_list[20]] = sum(pop_s_list[20:30]) /10
art_dict[art_list[30]] = sum(pop_s_list[30:40]) /10
art_dict[art_list[40]] = sum(pop_s_list[40:50]) /10
art_dict[art_list[50]] = sum(pop_s_list[50:60]) /10
art_dict[art_list[60]] = sum(pop_s_list[60:70]) /10
art_dict[art_list[70]] = sum(pop_s_list[70:80]) /10

art_song_dict[art_list[0]] = song_list[:10]
art_song_dict[art_list[10]] = song_list[10:20]
art_song_dict[art_list[20]] = song_list[20:30]
art_song_dict[art_list[30]] = song_list[30:40]
art_song_dict[art_list[40]] = song_list[40:50]
art_song_dict[art_list[50]] = song_list[50:60]
art_song_dict[art_list[60]] = song_list[60:70]
art_song_dict[art_list[70]] = song_list[70:80]





data = [go.Bar(x = [art_list[0],art_list[10],art_list[20],art_list[30],art_list[40],art_list[50],art_list[60]], y = [art_dict[art_list[10]],art_dict[art_list[20]] ,art_dict[art_list[30]],art_dict[art_list[40]],art_dict[art_list[50]],art_dict[art_list[60]],art_dict[art_list[70]]])]
#uncomment the line below to get the bar chart visualization
#py.iplot(data, filename = 'Billboard.sqlite')


#Get Plot Two

conn = sqlite.connect('Billboard.sqlite')
cur = conn.cursor()
cur.execute('SELECT title , artist FROM Billboard')

title_list = []
for row in cur:
	title = row[0].lower()
	artist = row[1]
	title_list.append(title)


songs_in_top100_list = []
songs_100 = {}
art_song_items = art_song_dict.items()


for s in song_list:
	if s in title_list:
		songs_in_top100_list.append(s)

for j in art_song_items:
	for song in j[1]:
		if song in songs_in_top100_list and j[0] in songs_100:
			
			songs_100[j[0]] += [song]
		elif song in songs_in_top100_list and j[0] not in songs_100.keys():
			songs_100[j[0]] = [song]
	

freq_list = []
for x in songs_100.keys():
	freq_list.append(len(songs_100[x]))

freq_dict = {}

freq_dict[art_list[0]] = freq_list[0] #/ 100
freq_dict[art_list[10]] = freq_list[1] #/100
freq_dict[art_list[20]] = freq_list[2] #/100
freq_dict[art_list[30]] = freq_list[3] #/ 100
freq_dict[art_list[40]] = freq_list[4] #/100
freq_dict[art_list[50]] = freq_list[5] #/100
freq_dict[art_list[70]] = freq_list[6] #/100

labels = [art_list[0],art_list[10],art_list[20],art_list[30],art_list[40],art_list[50],art_list[60]]
values = [freq_dict[art_list[0]], freq_dict[art_list[10]], freq_dict[art_list[20]],freq_dict[art_list[30]],freq_dict[art_list[40]],freq_dict[art_list[50]],freq_dict[art_list[70]]]

trace = go.Pie(labels=labels, values=values)
#uncomment the line below to get the pie chart visualization
#py.iplot([trace], filename='Billboard.sqlite')









	


	


