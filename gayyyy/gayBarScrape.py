from bs4 import BeautifulSoup, Comment
import html5lib
import datetime
import unicodedata
import re
from Event import EventO

EAGLE_BOLT_URL = "http://eagleboltbar.com/daily_specials.html"
EAGLE_BOLT_SPECIAL_URL = "http://eagleboltbar.com/special_events.html"
SALOON_URL = "http://saloonmn.com/calendar-of-events"
DAY_MAPPING = {0: 'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
DEBUG_MODE = True

#taken from scrapeTutorial exercise, returns beautifulsoup
def get_soup(url):
	html = request.urlopen(url).read()
	soup = BeautifulSoup(html, "html5")
	return soup

#want saloon from day to day, eventually as json
def get_saloon_daily_special(currentDay=None):
	soup = get_soup(SALOON_URL)
	allEvents = soup.findAll("div","cover-container") #types in python!
	eventOList = []

	for cover in allEvents:
		eventTitle = cover.find("h4","day")
		eventDescription = cover.find("div","event-description")
		eventDay = print_coded_thing(eventTitle).decode('utf-8')
		eventDayNumber = get_day_number(eventDay)
		eventDescription = print_coded_thing(eventDescription).decode('utf-8')

		indexAfterAge = eventDescription.find("\n",eventDescription.find("\n",eventDescription.find("\n")+1)+1)
		eventAge = eventDescription[(indexAfterAge-3):indexAfterAge]

		indexAfterCover = eventDescription.find("\n",indexAfterAge+1)
		eventCover = eventDescription[indexAfterAge:indexAfterCover].strip();
		print("eventAge",eventAge)
		#print("index after cover",indexAfterCover,"indexAfterAge",indexAfterAge)
		print("eventCover",eventCover)
		eventHours = eventDescription[indexAfterCover:].strip();

		#should have done this earlier and better
		eventDescription = eventDescription[:eventDescription.find("\n")]
		print("eventHours",eventHours)
		print("eventDescription",eventDescription)
		eventOList.append(EventO("n/a", eventDescription, eventDay, eventHours, eventCover, eventAge))

	#for eventO in eventOList:
	#	print(eventO.printStuff(),"\n");
def print_coded_thing(coverMaybe):
	text = ''.join(coverMaybe.findAll(text=True))
	data = text.strip()
	nkfd_form = unicodedata.normalize('NFKD', data)
	only_ascii = nkfd_form.encode('ASCII', 'ignore')
	print("printing uncoded",only_ascii)
	return only_ascii
'''
def printEncodedText(text):
	data = text.strip()
	nkfd_form = unicodedata.normalize('NFKD', data)
	only_ascii = nkfd_form.encode('ASCII', 'ignore')
	print("printing uncoded",only_ascii)
	return only_ascii
'''
def get_day_number(dayAsString):
	if 'monday' in str(dayAsString).lower():
		return 0
	elif 'tuesday' in str(dayAsString).lower():
		return 1
	elif 'wednesday' in str(dayAsString).lower():
		return 2
	elif 'thursday' in str(dayAsString).lower():
		return 3
	elif 'friday'in str(dayAsString).lower():
		return 4
	elif 'saturday' in str(dayAsString).lower():
		return 5
	elif 'sunday' in str(dayAsString).lower():
		return 6

def get_current_day(currentDay=None):
	if currentDay == None:
		dayNumber = datetime.datetime.today().weekday() #from datetime, get current day as int from monday = 0
		print(dayNumber)
		currentDay = DAY_MAPPING[dayNumber]

#def convert_to_whatever_code(SALOON_MAPPINGS):
#	for key in SALOON_MAPPINGS:#== for key in dict.keys
#		text = SALOON_MAPPINGS[key]
#		SALOON_MAPPINGS[key] = print_coded_thing(text).decode('utf-8')
#python 2 or python 3 import urllib
try:
	from urllib import request
except ImportError:
	import urllib2

def get_eagle_special_events(EAGLE_SPECIAL_MAPPINGS):
	soup = get_soup(EAGLE_BOLT_SPECIAL_URL)
	allDays = soup.findAll("span","style34") #types in python!
	for day in allDays:
		if day.text is '':
			continue;
		eventDescription = day.find_next("blockquote")
		day.text
		EAGLE_SPECIAL_MAPPINGS[day.text] = eventDescription.text

def get_eagle_daily_specials(EAGLE_DAILY_MAPPINGS):
	soup = get_soup(EAGLE_BOLT_URL)
	comments = soup.findAll(text=lambda text:isinstance(text, Comment))
	[comment.extract() for comment in comments]
	r = re.compile('[a-zA-Z]+day')
	#assert r.match('sss')
	assert r.match('sunday')
	assert r.match('SUNday')
	allDays = soup.findAll(is_a_and_name_ends_with_day)
	for day in allDays:
		greatGrandparent = day.parent.parent.parent
		activities = greatGrandparent.next_sibling.next_sibling
		if activities is None:
			activities = greatGrandparent.parent.next_sibling.next_sibling
		activity = ""
		for str in activities.stripped_strings:
			activity = activity + str + "\n"
		#print(activity)
		EAGLE_DAILY_MAPPINGS[day['name']] = activity

	print("leaving specials")

def is_a_and_name_ends_with_day(tag):
	return tag.has_attr("name") and re.compile('[a-zA-Z]+day').match(tag['name'])

def consolidate_lists():
	#I don't know if this is necessary yet. unwritten
	return ""

def log_it(stuffToBeWritten):
	log = open("log.txt", "a")
	log.write(stuffToBeWritten)
	log.close()





##1. get eagle events
#EAGLE_SPECIAL_MAPPINGS = {}
#get_eagle_special_events(EAGLE_SPECIAL_MAPPINGS)
#if DEBUG_MODE:
#print(EAGLE_SPECIAL_MAPPINGS)

#2. get eagle daily_specials
EAGLE_DAILY_MAPPINGS = {}
get_eagle_daily_specials(EAGLE_DAILY_MAPPINGS)
#print(EAGLE_DAILY_MAPPINGS)
#3 Saloon stuff
SALOON_MAPPINGS = {}
get_saloon_daily_special()
#print(SALOON_MAPPINGS)