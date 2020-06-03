import requests as rq
import bbcode
import sys, json, os

# Create BBCode parser
parser = bbcode.Parser()


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
print(str(len(gallery)) + " submissions found.")

try:
    os.remove("downloads.txt")
except:
    pass

# Initialize downloads.txt.
with open("downloads.txt", "a", encoding="latin1") as file:
    # Loop through posts in gallery.
    for post in gallery:
        # Find the download link.
        request = get(f"http://localhost:9292/submission/{post}.json")
        title = request["title"]
        print("Downloading " + title)
        # Check if file is valid text and strip bbcode and save to download.txt, skip it not.
        if request["download"].endswith('.txt'):
            download = rq.get(request["download"])
            file.write(parser.strip(download.text))
        else:
            print(f"Submission {title} is not a valid .txt file. It will be skipped.")
