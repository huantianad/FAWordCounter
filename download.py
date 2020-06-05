import requests as rq
import bbcode
from docx import Document
from pdfminer.high_level import extract_text
import json, os, configparser

# Create BBCode parser
parser = bbcode.Parser()

# Config Stuff
config = configparser.ConfigParser()
config.read('config.ini')
username = config['Main']['username']
link = config['Main']['scraper']

# Define a function to access the api at url and return parsed json.
def get(url):
    object = rq.get(url)
    return json.loads(object.text)

# Get submissions of user and store it in gallery.
gallery = get(f"http://{link}/user/{username}/gallery.json")
print(str(len(gallery)) + " submissions found.")

# Remove old downloads.txt
try:
    os.remove("downloads.txt")
except:
    pass

# Initialize downloads.txt.
with open("downloads.txt", "a", encoding="utf8") as file:
    # Loop through posts in gallery.
    for post in gallery:
        # Find the download link.
        request = get(f"http://{link}/submission/{post}.json")
        title = request["title"]
        print("Downloading " + title)

        # Check if file is valid text and strip bbcode and save to download.txt, skip it not.
        if request["download"].endswith('.txt'):
            download = rq.get(request["download"])
            text = bytes(parser.strip(download.text), 'latin-1').decode('utf-8')
            file.write(text)
        elif request["download"].endswith('.doc') or request["download"].endswith('.docx'):
            with open('tempdownload.docx', 'wb') as tempfile:
                download = rq.get(request["download"])
                tempfile.write(download.content)
                document = Document('tempdownload.docx')
                docText = '\n\n'.join(
                    paragraph.text for paragraph in document.paragraphs
                )
            file.write(docText)
            os.remove("tempdownload.docx")
        elif request["download"].endswith('.pdf'):
            with open('tempdownload.pdf', 'wb') as tempfile:
                download = rq.get(request["download"])
                tempfile.write(download.content)
            text = extract_text('tempdownload.pdf')
            file.write(text)
            os.remove('tempdownload.pdf')
        else:
            print(f"Submission {title} is not a valid file. It will be skipped.")
