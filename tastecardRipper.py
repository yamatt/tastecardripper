import BeautifulSoup
import time
import couchdb
import urllib2
from optparse import OptionParser
from uuid import uuid4
import re
try:
	import json    #python2.6
except ImportError:
	import simplejson as json #python2.5

def load_config (path):
	if path:
		file = open(path, 'r')
		config_data = file.read()
		return json.loads(config_data)
	else:
		print "config file not specified or found"

def connect (server, database, username, password):
	couch = couchdb.Server(server)
	db = couch[database]
	if username and password:
		try:
			db.resource.credentials = username, password
		except:
			print "You need the latest version of python-couchdb"
			raise
	return db

def get_restaurants (url):
	page = urllib2.urlopen(url)
	soup = BeautifulSoup.BeautifulSoup(page)
	return soup.find('select', id="restaurant").findChildren('option')[config['start']:]

def update_restaurants (db, restaurants, restaurant_url):
	this_version = str(uuid4())
	print "This Version: " + this_version
	print "Restaurant Count: " + str(len(restaurants))

	for restaurant in restaurants:
		restaurant_id = restaurant['value']
		print str(restaurants.index(restaurant)) + "\t" + time.asctime(time.gmtime()) + "\t" + restaurant_id

		# get restaruant data
		restaurant_full_url = restaurant_url % restaurant_id
		restaurant_page = urllib2.urlopen(restaurant_full_url)
		restaurant_xml = BeautifulSoup.BeautifulStoneSoup(restaurant_page)
		restaurant_data = restaurant_xml.markers.marker

		doc = db.get(restaurant_id)
		if not doc:
			doc = {}

		# make document
		doc['name'] = restaurant.contents[0]
		if (float(restaurant_data['lng'] or False) and float(restaurant_data['lat'] or False)):
			doc['loc'] = [round(float(restaurant_data['lng']),5), round(float(restaurant_data['lat']),5)]
		doc['telephone'] = restaurant_data['bookingtel']
		doc['url'] = restaurant_data['restaurantwebsite']
		doc['cuisine'] = restaurant_data['cuisine']
		doc['availability'] = availability (
						restaurant_data['availablefri'],
						restaurant_data['availablefriday'],
						restaurant_data['availablesat'],
						restaurant_data['availablesatday'],
						restaurant_data['availabledec']
					)
		doc['limitations'] = limitations (
						restaurant_data['restaurantphonebookings'],
						restaurant_data['restaurantcarduse'],
						restaurant_data['restaurantcardusetype'],
						restaurant_data['restaurantmaxpeople'],
					)
		doc['version'] = this_version

		db[restaurant_id] = doc		# create/update
		
		# attach image to completed document
		image = urllib2.urlopen(config['imageurl'] % restaurant_data['image'])
		file = str(image.read())
		db.put_attachment(db[restaurant_id], file, restaurant_data['image'])

		time.sleep(config['delay'])		# prevent server swamping

	if config['delete']:
		delete_old (db, this_version)

def availability (friday, friday_day, saturday, saturday_day, december):
	returnDoc = {}
	if bool(int(friday)):
		if bool(int(friday_day)):
			returnDoc['friday'] = "all"
		else:
			returnDoc['friday'] = "night"

	if bool(int(saturday)):
		if bool(int(saturday_day)):
			returnDoc['saturday'] = "all"
		else:
			returnDoc['saturday'] = "night"

	returnDoc['december'] = bool(int(december))
	return returnDoc

def limitations (phone_booking, card_use, deal, max_people):
	return {
		'phone_booking': re.search(config['regex']['phone_before'], phone_booking).group(0),
		'card_use': re.search(config['regex']['card_use'], card_use).group(0),
		'deal': re.search(config['regex']['deal'], deal).group(0),
		'max_people': int(re.search(config['regex']['max_people'], max_people).group(0)),
	}

def delete_old (db, current_version):
	query = '''function(doc) { if (doc.version != "%s") { emit (doc.id, doc.id) } }''' % current_version
	results = db.query(query)
	print 'Deleting %d rows' % len(results.rows)
	for row in results.rows:
		print 'Deleting: ' + row['id']
		doc = db[row['id']]
		db.delete(doc)

if __name__ == "__main__":
        parser = OptionParser()
        parser.add_option("-c", "--config", dest="config_path", help="File to read configuration settings from")
        (options, args) = parser.parse_args()
        config = load_config(options.config_path);
	print 'Started: ' + time.asctime(time.gmtime())
	restaurant_list = get_restaurants(config['restaurants'])
	if len(restaurant_list) < 4000:
		print "There were less than 4000 restaurants. Sees odd."
		raise
	update_restaurants(
		connect(
			config['server'],
			config['database'],
			config['username'],
			config['password']), 
		restaurant_list,
		config['restaurant'])
	print 'Finished: ' + time.asctime(time.gmtime())
