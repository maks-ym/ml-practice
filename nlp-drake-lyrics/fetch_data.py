import requests
import configparser
# import datetime
from bs4 import BeautifulSoup


def readConfig() -> str:
    config = configparser.ConfigParser()
    config.read('auth.cfg')
    auth_token = config.get('Auth', 'Token')
    return auth_token


def lyrics_from_song_api_path(song_api_path, prefix):
    prefix = str(prefix)
    song_url = "/".join([base_url, song_api_path])
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    print("song path: {}".format(path))

    #gotta go regular html scraping... come on Genius
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    # with open(prefix + "_scrapped_page", "w") as outpage:
    #     outpage.write(page.text)
    html = BeautifulSoup(page.text, "html.parser")
    # print(html)
    # with open(prefix + "_parsed_html", "w") as outhtml:
    #     outhtml.write(str(html))
    #remove script tags that they put in the middle of the lyrics
    [h.extract() for h in html('script')]
    # with open(prefix + "_removed_scripts", "w") as outscrremoved:
    #     outscrremoved.write(str(html))
    # at least Genius is nice and has a tag called 'lyrics'!
    # updated css where the lyrics are based in HTML
    lyrics = html.find("div", class_="lyrics").get_text() 
    lyrics_file = "data/drake/" + prefix + "_lyrics"
    with open(lyrics_file, "w") as lyr_out:
        lyr_out.write(lyrics)
    return lyrics

#search for song
# import requests

client_access_token = str(readConfig())
print("client_access_token: {}".format(client_access_token))
base_url = 'https://api.genius.com'

user_input = input('artist and song: ').replace(" ", "-")

path = 'search/'
request_uri = '/'.join([base_url, path])
print(request_uri + user_input)

params = {'q': user_input}

token = 'Bearer {}'.format(client_access_token)
headers = {'Authorization': token}

r = requests.get(request_uri, params=params, headers=headers)
res = r.json()

if res["meta"]["status"] != 200:
    print("request failed. Terminate")
    exit()

artists = {}
songs = []

for hit in res["response"]["hits"]:
    if hit["type"] == "song":
        artist_name = hit["result"]["primary_artist"]["name"]
        artist_id = hit["result"]["primary_artist"]["id"]
        song_name =  hit["result"]["full_title"]
        song_id = hit["result"]["id"]
        lyrics_state = hit["result"]["lyrics_state"]
        artists[artist_name] = artist_id
        songs.append({
            "song": song_name, 
            "id": song_id,
            "lyrics_state": lyrics_state})


print("artists:")
for a_name, a_id in artists.items():
    print(a_name, a_id)

print("songs")
for i, s in enumerate(songs):
    print(s)
    if str(s["lyrics_state"]) != "complete":
        print("not complete lyrics - skip")
    else:
        song_api_path = "/".join(["songs", str(s["id"])])
        prefix = str(s["id"]) + "_" + str(s["song"])
        lyrics_from_song_api_path(song_api_path, prefix)

print("done!")




    # for hit in json["response"]["hits"]:
    #     if hit["result"]["primary_artist"]["name"] == artist_name:
    #         song_info = hit
    #         break
    #     if song_info:
    #     pass


# def getData(auth_token, id):
#     s = random.randint(100000, 1000000)
#     id_str = str(s)
#     conn = http_client.HTTPSConnection("api.genius.com")
#     request_uri = "/songs/" + id_str
#     headersMap = {
#             "User-Agent": "CompuServe Classic/1.22",
#             "Accept": "application/json",
#             "Authorization": "Bearer " + auth_token
#     }
#     conn.request("GET", request_uri, headers=headersMap)
#     response = conn.getresponse()
#     ### Output the HTTP status code and reason text...
#     #print response.status, response.reason
#     data = response.read()
#     result = json.loads(data)

#     output = "[" + id_str + "] "
#     if response.status == 200:
#         title = result["response"]["song"]["full_title"];
#         song_uri = result["response"]["song"]["path"];
#         print "[" + id_str + "] " + title + "\nLink: https://genius.com" + song_uri + "\n"
#     else:
#         if response.status == 404:
#            #Just in case the song was not found, try again recursively and then continue with the for-loop
#            getData()
#         else:
#            print "unknown error: " + str(response.status) +  " "  + str(response.reason)






