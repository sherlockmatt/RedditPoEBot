import redis


redis = redis.StrictRedis(host="localhost")

# Pull ini file values from redis.
app_key = redis.get("app_key")
app_secret = redis.get("app_secret")
token = redis.get("token")
refresh_token = redis.get("refresh_token")
valid_until = redis.get("valid_until")

if app_key is None or app_secret is None or token is None or refresh_token is None or valid_until is None:
    print "Unable to fetch oauth values from redis. Exiting."
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
""" % (app_key, app_secret, token, refresh_token, valid_until)

with open("oauth.ini", "w+") as file:
    file.write(contents)