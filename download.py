import requests as rq
import sys, json

# Define a function to acess the api at url and return parsed json.
def get(url):
    object = rq.get(url)
    return json.loads(object.text)

# Get username from cmd input, store it in username.
if len(sys.argv) != 2:
    raise ValueError('Please provide a username.')
username = sys.argv[1]

# Get the submissions of the use and store it in gallery.
gallery = get(f"http://localhost:9292/user/{username}/gallery.json")

#Initialize downloads.txt.
with open("downloads.txt", "a", encoding="latin1") as file:
    #Loop through posts in gallery.
    for post in gallery:
        #Find the download link.
        request = get(f"http://localhost:9292/submission/{post}.json")["download"]

        #Check if file is valid text and save to download.txt, skip it not.
        if request.endswith('.txt'):
            download = rq.get(request)
            file.write(download.text)
        else:
            print(f"File {request} is not a valid text file. It will be skipped.")