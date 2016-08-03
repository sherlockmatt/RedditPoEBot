import psycopg2
import os

connection_string = os.environ["DATABASE_URL"]
db_connection = psycopg2.connect(connection_string)
db_connection.autocommit = True # So we don't have to write db_connection.commit() after every request.
db = db_connection.cursor()

db.execute("""create table if not exists parsed_comments 
(
    id text primary key,
    parse_date timestamp with time zone
)""")
db.execute("""create table if not exists oauth
(
    app_key text,
    app_secret text,
    token text,
    refresh_token text,
    valid_until text
)""")

# Pull ini file values from database.
db.execute("select app_key, app_secret, token, refresh_token, valid_until from oauth")
values = db.fetchone()

if values is None:
    print "Unable to fetch oauth values from database. Exiting."
    quit()

# Make the ini file using the values.
contents = """[app]
scope = identity,read,vote,submit,privatemessages,edit
refreshable = True
app_key = %s
app_secret = %s

[server]
server_mode = True

[token]
token = %s
refresh_token = %s
valid_until = %s
""" % values

with open("oauth.ini", "w+") as file:
    file.write(contents)
    
# Are comments, submissions and messages really unique among each other?
# Can a comment and a private message have the same ID?
def is_parsed(id):
    db.execute("select exists(select 1 from parsed_comments where id=%s)", (id,))
    return db.fetchone()

def add_parsed(id):
    return db.execute("insert into parsed_comments values (%s)", (id,))