import psycopg2
import os
import urlparse

urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.environ['DATABASE_URL'])

conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
cur = conn.cursor()
query = "CREATE TABLE commutes (REQ_TIME TIMESTAMPTZ NOT NULL, TRIP_TIME_MIN NUMERIC NOT NULL, TRIP_DIST_MILES NUMERIC NOT NULL);"
cur.execute(query)
cur.execute("INSERT INTO commutes VALUES ('2015-01-24 22:30:06 EST', 54.7833333333, 47.781565787);")
cur.execute("SELECT * FROM commutes;")
rows = cur.fetchall()

for row in rows:
    print row[0]
    
conn.commit()

cur.execute("DELETE FROM commutes;")
conn.commit()
