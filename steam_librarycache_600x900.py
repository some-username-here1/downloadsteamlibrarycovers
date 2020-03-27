import urllib.request
import urllib.response
import re
import os

website = urllib.request.urlopen("https://steamcommunity.com/profiles/76561198205903185/games/?tab=all").read().decode(
    'utf-8'
)
gameIDs = re.findall(r"(?:appid\":)\d+", website)
gameIDs[:] = [s.replace('appid\":', '') for s in gameIDs]
folder = os.path.abspath(os.getcwd())

for i in gameIDs:
    try:
        URLOpen = urllib.request.urlopen("https://steamcdn-a.akamaihd.net/steam/apps/"
                                         + i + "/library_600x900.jpg").read()
        open(folder + '/' + i + '_library_600x900.jpg', 'wb+').write(URLOpen)
    except Exception as e:
        ResponseData = e.read().decode("utf8", 'replace')
