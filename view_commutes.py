import psycopg2, os, urlparse
urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.environ['DATABASE_URL'])

conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
cur = conn.cursor()

cur.execute("SELECT * FROM commutes;")
colnames = [desc[0] for desc in cur.description]
rows = cur.fetchall()
print colnames[0] + ", " + colnames[1] + ", " + colnames[2] + ", " + colnames[3] + ", " + colnames[4]
for row in rows:
    print str(row[0]) + ", " + str(row[1]) + ", " + str(row[2]) + ", " + str(row[3]) + ", " + str(row[4])

conn.close()