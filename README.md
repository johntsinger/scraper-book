# scraper-book
scraper of books.toscrape.com with scrapy

### Install Python :

If you don't have Python 3, please visit : https://www.python.org/downloads/ to download it !

### Virtual Environment :

#### Create a virtual environment in the project root :

    python -m venv env

#### Activate a virtual environment :

##### windows :

    env/Scripts/activate
    
##### linux/mac :

    source env/bin/activate
    
#### Install dependencies :

    pip install -r requirements.txt

## Run the program :

On the root folder 

    cd book

to csv :

    scrapy crawl book -O books.csv

to json :

    scrapy crawl book -O books.json
