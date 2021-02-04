#!/usr/bin/python3

import json
import requests
import csv
import os
import random
import tweepy

auth = tweepy.OAuthHandler('AoyJJwRG637eX4vS13d9hERFA', 'hQ4wPF9k6GaK5meE0i6fDcQsNjcNDDLwhlSR9loR7gB1mzlNM6')
auth.set_access_token('1357032687031181314-VwawQNiLR4SdHbyvuYzxfQRsFfcWzW', 'rkzYH4o8NcgpJ5WkW5GY9GDbhnKuiTvu5LYcIezV9zEeU')
api = tweepy.API(auth)

# aktuellen pegelstand abrufen
url = 'https://www.pegelonline.wsv.de/webservices/rest-api/v2/stations/SANKT%20ARNUAL/W/currentmeasurement.json'
db = '/home/pi/python/hochwassaar/hochwassaar.csv'
response = requests.get(url)
data = response.json()
pegel = int(data['value'])
zeitpunkt = data['timestamp']
rows = [zeitpunkt, pegel]

# pegelvergleiche
stubbis = float(round(pegel/17.5,1))
stubbi = str(stubbis) + ' Stubbis'
maggi = float(round(pegel/15,1))
baguette = float(round(pegel/65,1))
anstieg = ['Ouh. De Saarpegel steiht.', 'Es gebbt meh.', 'Do misse ma e Au druff han.', ' ']
abfall = ['Joo, gebbt wenischer.', 'Fließt ab.', ' ']
hashtags = '#Saar #Saarland #Saarpegel #Saarbrücken'

# vergleich mit letztem pegelstand
try:
	with open(db, 'r') as csvfile:
		pegel_hist = []
		csvreader = csv.reader(csvfile)
		for row in csvreader:
			pegel_hist.append(row[1])
		pegel_alt = int(pegel_hist[-1])
except:
	pass
finally:
	with open(db, 'a+', newline='') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(rows)	
try:
	change = pegel - pegel_alt
except:
	pass

# bei änderung von pegelstand:
try:
	pegel_alt
except:
	pass
else:
	if int(pegel_alt) != int(pegel):
		if change > 0:
			aenderung = random.choice(anstieg)
		elif change < 0:
			aenderung = random.choice(abfall)
		if stubbis == 20:
			stubbi = 'e ganzer Kaschde gestapelde Stubbis'
		elif stubbis > 20:
			random_stubbi = ['mehr als ähner Kaschde Stubbi-Flasche üwernana', str(stubbis) + ' Stubbis']
			stubbi = random.choice(random_stubbi)
		else:
			pass
		hoehe = [
			f'De Pegel an de Saar steht in Saarbrigge grad bei {pegel} cm. Das is so hoch wie {stubbi}. {hashtags}',
			f'Grad hann ma e Pegel von {pegel} cm in Saarbrigge. In Maggiflasche umgerechnet sinn das {maggi} Stick. {hashtags}',
			f'{pegel} cm an de Saar in Saarbrigge! Das is so hoch wie {baguette} Baguette lang sinn. {hashtags}']
		if pegel < 320:
			hoehe.append(f'Kä Angschd. Bei {pegel} cm in Saarbrigge brauche ma uns noch ke Gedanke se mache. {hashtags}')
		if (change > 0) and (pegel > 370) and (pegel < 385):
			hoehe.append(f'Newefluss der Saar mit 13 Buchstawe? STADTAUTOBAHN. {pegel} cm! Langsam wirds eng. {hashtags}')
		tweet_text = f'{aenderung} {random.choice(hoehe)}'
		api.update_status(tweet_text)
	else:
		pass
