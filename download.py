import requests as rq
import requests_cache
import bbcode
from docx import Document
from pdfminer.high_level import extract_text
import json, os, configparser

# Create BBCode parser
parser = bbcode.Parser()

# Create requests cache
requests_cache.install_cache()

# Config Stuff
config = configparser.ConfigParser()
with open('config.ini') as configfile:
    config.read('config.ini')
    username = config['Main']['username']
    link = config['Main']['scraper']


# Define a function to access the api at url and return parsed json
def get(url):
    object = rq.get(url)
    return json.loads(object.text)


# Get submissions of user and store it in gallery
gallery = get(f"http://{link}/user/{username}/gallery.json")
print(str(len(gallery)) + " submissions found.")

# Remove old downloads.txt
if os.path.exists("downloads.txt"):
    os.remove("downloads.txt")

# Open downloads.txt.
with open("downloads.txt", "a", encoding="utf8") as file:
    # Loop through posts in gallery
    for post in gallery:
        # Find the download link of post
        request = get(f"http://{link}/submission/{post}.json")
        title = request["title"]
        print("Downloading " + title)

        # Check file type and process it accordingly
        if request["download"].endswith('.txt'):
            # Remove BBCode from .txt file and add it to downloads.txt
            download = rq.get(request["download"])
            text = bytes(parser.strip(download.text), 'latin-1').decode('utf-8')
            file.write(text)

        elif request["download"].endswith('.doc') or request["download"].endswith('.docx'):
            with open('tempdownload.docx', 'wb') as tempfile:
                # Download and write file to a temporary file
                download = rq.get(request["download"])
                tempfile.write(download.content)
                # Load temporary file and convert to raw text
                document = Document('tempdownload.docx')
                docText = '\n\n'.join(
                    paragraph.text for paragraph in document.paragraphs
                )
            # Write text to downloads.txt and remove temporary file
            file.write(docText)
            os.remove("tempdownload.docx")

        elif request["download"].endswith('.pdf'):
            with open('tempdownload.pdf', 'wb') as tempfile:
                # Download and write file to a temporary file
                download = rq.get(request["download"])
                tempfile.write(download.content)
            # Convert pdf to raw text
            text = extract_text('tempdownload.pdf')
            # Write text to downloads.txt and remove temporary file
            file.write(text)
            os.remove('tempdownload.pdf')

        else:
            print(f"Submission {title} is not a valid file. It will be skipped.")
