TasteCard Ripper
===================

This program screen scrapes the tastecard.co.uk website for the restaurant data and saves it in to a couchdb with geocordinates. If you're using GeoCouch you can then use the data to create some useful maps.

Setup
--------------------
You will need a CouchDB to add your data too. I recommend using GeoCouch specifically or a couchone.com database. If you use couchone.com it will be slower since the data is going over the internet, so I recommend you get a local CouchDB then sync it to the couchone.com database.

You will also need to create a database in your CouchDB instance called 'tastecard'.

Usage
--------------------
Modify the config.json file so that the script can communicate with your CouchDB and then run tcrun.sh.

config.json
-------------------
*   *server*: is the url to your couchdb server
*   *database*: is the database to add to your restaurant entries in to
*   *username*: the username used to access the database -- leave blank if you have Admin Party
*   *password*: the password used to access the database -- leave blank if you have Admin Party
*   *delay*: the number of seconds between requests to the tastecard.co.uk website (so as to not overload it)
*   *start*: the start position in the list (only really used for debugging)
*   *delete*: whether to delete old entries from the database
*   *restaurants*: url to get the list restaurants from (incase they change something)
*   *restaurant*: url to get each restaurant data from (incase they change something)
*   *imageurl*: url to find the image for the restaurant (incase they change something)
*   *regex*: types of values to detect (incase they change something)

License
------------------

   Copyright Matthew Copperwaite 2011

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.

   See the README.md file for contact information.
