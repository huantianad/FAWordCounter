# FAWordCounter
Simple word counter for FA made in Python because I was bored.

Requres [Deer-Spangle's fork](https://github.com/Deer-Spangle/faexport) of boothale's FA Scarper to actually work because FA doesn't have an API.

Current supported file types are .txt, .doc, .docx, and .pdf. Other formats will be supported soon. Hopefully.

Downloading from users with large galleries will take a while because internet.

# Installation
1. Clone this repository using `git clone https://github.com/huantianad/FAWordCounter`.
2. Install requirements using `pipenv install`.
3. Setup [the scraper](https://github.com/Deer-Spangle/faexport) as indicated in the readme. Alternatively, you can set the url of the scraper as the official website: faexport.spangle.org.uk
4. Edit `config.ini` with the url of the scraper and user that you want to download from.

# Useage
Run `download.py`, which will download the specified user's gallery into `downloads.txt`. 
