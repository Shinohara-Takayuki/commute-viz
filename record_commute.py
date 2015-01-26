import simplejson, urllib, psycopg2, os, urlparse
from time import strftime

with open("msoft_key.data") as f:
    msoft_key = f.read()

with open("home_address.data") as f:
    home = f.read()

work = '340%20Main%20Street%20Venice,CA%2090291'

url1 = "http://dev.virtualearth.net/REST/v1/Routes?wayPoint.1=%s&wayPoint.2=%s&optimize=timeWithTraffic&routeAttributes=routeSummariesOnly&maxSolutions=1&distanceUnit=mi&key=%s" % (home, work, msoft_key)
url2 = "http://dev.virtualearth.net/REST/v1/Routes?wayPoint.1=%s&wayPoint.2=%s&optimize=timeWithTraffic&routeAttributes=routeSummariesOnly&maxSolutions=1&distanceUnit=mi&key=%s" % (work, home, msoft_key)

req_time = strftime("%Y-%m-%d %H:%M:%S %Z")
result1 = simplejson.load(urllib.urlopen(url1))
extract1 = result1['resourceSets'][0]['resources'][0]
result2 = simplejson.load(urllib.urlopen(url2))
extract2 = result2['resourceSets'][0]['resources'][0]


urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.environ['DATABASE_URL'])

conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
cur = conn.cursor()

cur.execute("INSERT INTO commutes VALUES ('%s', %f, %f, %f, %f);" % (req_time, extract1['travelDurationTraffic'] / 60.0, extract1['travelDistance'], extract2['travelDurationTraffic'] / 60.0, extract2['travelDistance']))
conn.commit()
conn.close()