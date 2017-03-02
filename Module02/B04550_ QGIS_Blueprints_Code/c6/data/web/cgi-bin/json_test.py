#!/usr/bin/python

import cgi, cgitb, json, sys
from pyspatialite import dbapi2 as sqlite3

# Enables some debuggin functionality
cgitb.enable()

# Creating row factory function so that we can get field names
# in dict returned from query
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Connect to DB and setup row_factory
conn = sqlite3.connect('C:\\packt\\c6\\data\\prep\\c6b.sqlite')
conn.row_factory = dict_factory

# Print json headers, so response type is recognized and correctl decoded
print 'Content-Type: application/json\n\n'

# Use CGI FieldStorage object to retrieve data passed by HTTP GET
# Using numeric datatype casts to eliminate special characters
# longitude = float(fs.getfirst('longitude'))
# latitude = float(fs.getfirst('latitude'))
# day = int(fs.getfirst('day'))
longitude = 39.47785
latitude = -75.28075
day = 15

# Use user selected location and days to find nearest location (minimum distance) 
# and correct date column
query = 'SELECT pk, calc{2} as index_value, min(Distance(PointFromText(\'POINT ({0} {1})\'),geom)) as min_dist FROM vulnerability'.format(longitude, latitude, day)

# Use conection as context manager, output first/only result row as json
with conn:
    c = conn.cursor()
    c.execute(query)
    data = c.fetchone()
    print json.dumps(data) 

