import http.client as http_client
import urllib, json,  random, sys, configparser


def readConfig() -> str:
    config = configparser.ConfigParser()
    config.read('auth.cfg')
    auth_token = config.get('Auth', 'Token')
    return auth_token


def getData(auth_token, id):
    s = random.randint(100000, 1000000)
    id_str = str(s)
    conn = http_client.HTTPSConnection("api.genius.com")
    request_uri = "/songs/" + id_str
    headersMap = {
            "User-Agent": "CompuServe Classic/1.22",
            "Accept": "application/json",
            "Authorization": "Bearer " + auth_token
    }
    conn.request("GET", request_uri, headers=headersMap)
    response = conn.getresponse()
    ### Output the HTTP status code and reason text...
    #print response.status, response.reason
    data = response.read()
    result = json.loads(data)

    output = "[" + id_str + "] "
    if response.status == 200:
        title = result["response"]["song"]["full_title"];
        song_uri = result["response"]["song"]["path"];
        print "[" + id_str + "] " + title + "\nLink: https://genius.com" + song_uri + "\n"
    else:
        if response.status == 404:
           #Just in case the song was not found, try again recursively and then continue with the for-loop
           getData()
        else:
           print "unknown error: " + str(response.status) +  " "  + str(response.reason)






