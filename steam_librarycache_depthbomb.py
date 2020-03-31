import re
import os
import sys
import urllib.request
import urllib.response


# Enter the image name for the first nested list item and its base URL (with trailing slash)
# Different types of images:
# --------------------------
# Images NOT used by the Steam Library, but the Steam Store (and going under a different URL):
#   capsule_231x87.jpg
#   capsule_467x181.jpg
#   capsule_616x353.jpg
#   page_bg_raw.jpg
# Images used by the Steam Library:
#   header.jpg
#   library_600x900.jpg
#   library_600x900_2x.jpg
#   library_hero.jpg
#   library_hero_blur.jpg
#   logo.png
#   icon.jpg
image_types = [
#	["icon.jpg", 'https://steamcdn-a.akamaihd.net/steamcommunity/public/images/apps/'],
	["logo.png", 'https://steamcdn-a.akamaihd.net/steam/apps/'],
	["header.jpg", 'https://steamcdn-a.akamaihd.net/steam/apps/'],
	["library_hero.jpg", 'https://steamcdn-a.akamaihd.net/steam/apps/'],
	["library_hero_blur.jpg", 'https://steamcdn-a.akamaihd.net/steam/apps/'],
	["library_600x900.jpg", 'https://steamcdn-a.akamaihd.net/steam/apps/'],
	["library_600x900_2x.jpg", 'https://steamcdn-a.akamaihd.net/steam/apps/'],
]

download_all = False
is_id = False
steam_id  = str(input("Enter a Steam profile URL, SteamID64 or SteamID3: ")).rstrip("/")
file_type = str(input(f"Enter a number between 0 and {len(image_types)}, enter A to download all types: ")).lower()
force_download = True if input("Force redownloading of existing files? (yes/[NO]): ").lower() in ("yes", "true", "y", "1") else False

# Process user input and check for errors
errors = [] # Create an empty list, we will push error messages onto this list
if not re.match(r"(?:https?:\/\/)?steamcommunity\.com\/(?:profiles|id)\/[a-zA-Z0-9]+", steam_id):
	# not a Steam profile URL, let's see if it is a raw ID input...
	if not re.match(r"7656119[0-9]{10}|\[U:[0-1]{1}:[0-9]{1,10}\]", steam_id):
		# Fun fact, you can use SteamID3s in profile URLs, like this: steamcommunity.com/profiles/[U:1:66133073]
		errors.append("You did not enter a valid Steam profile URL or SteamID64/SteamID3")
	else:
		is_id = True

if file_type == "a":
	download_all = True
else:
	if int(file_type) > len(image_types):
		errors.append("The file type number you provided is out of range")

print()

# Check if we have any errors in our error list
if len(errors) > 0:
	print("Please fix these errors and try again:")
	print()
	for e in errors:
		print(f"	> {e}")
	print()
	exit()


# Set steam_profile accordingly depending on what the user entered for the first argument:
# if ID entered -> manually construct the profile URL
# else -> assume steam_id is the profile URL
steam_profile = f"https://steamcommunity.com/profiles/{steam_id}" if is_id else steam_id
website = urllib.request.urlopen(steam_profile + "/games/?tab=all").read().decode('utf-8')

game_ids = re.findall(r"(?:appid\":)\d+", website)
if len(game_ids) < 1:
	print("Could not get game IDs from profile, is the profile private?")
	exit()
game_ids[:] = [s.replace('appid\":', '') for s in game_ids]
folder = os.path.abspath(os.getcwd())


def gamecover(image, base_url):

	print()
	print(f"Downloading {image} assets...")
	print()

	def download(url, dest):
		request = urllib.request.urlopen(url)
		print(f"Downloaded {url} to {dest}")
		open(dest, 'wb+').write(request.read())

	for i in game_ids:
		image_name = str(i) + "_" + image
		image_folder = os.path.join(folder, i)
		image_path = os.path.join(image_folder, image_name)
		image_url  = base_url + f"{i}/{image}"

		try:
			if not os.path.exists(image_folder):
				os.mkdir(image_folder)

			if os.path.exists(image_path):
				if force_download:
					download(image_url, image_path)
				else:
					print(f"{image_name} has already been downloaded, skipping...")
			else:
				download(image_url, image_path)
		except Exception as e:
			print(f"Failed to download {image_url} - HTTP {e.getcode()}")


if download_all:
	for i, t in enumerate(image_types):
		image_type = image_types[i][0]
		base_url   = image_types[i][1]
		gamecover(image_type, base_url)
else:
	image_type = image_types[file_type][0]
	base_url   = image_types[file_type][1]
	gamecover(image_type, base_url)


exit()
