import psycopg2
import os
import urlparse

urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.environ['DATABASE_URL'])

conn = psycopg2.connect("dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname))
cur = conn.cursor()
cur.execute("DROP TABLE commutes;")
query = "CREATE TABLE commutes (REQ_TIME TIMESTAMPTZ NOT NULL, TO_WORK_TIME_MIN NUMERIC NOT NULL, TO_WORK_DIST_MILES NUMERIC NOT NULL, FROM_WORK_TIME_MIN NUMERIC NOT NULL, FROM_WORK_DIST_MILES NUMERIC NOT NULL);"
cur.execute(query)
conn.commit()
conn.close()