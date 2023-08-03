from urllib.parse import urljoin
import re
import scrapy
from book.items import BookItem


class BookSpider(scrapy.Spider):
    name = 'book'
    start_urls = ["http://books.toscrape.com/"]

    def parse(self, response):
        """Follows the link of each book that the site
        contains for each page of the site
        """
        book_page_links = response.css('h3 a')
        yield from response.follow_all(book_page_links, self.parse_book)

        pagination_links = response.css('li.next a')
        yield from response.follow_all(pagination_links, self.parse)

    def parse_book(self, response):
        """Parse the book's detail page"""

        def extract_with_css(query):
            return response.css(query).get(default='').strip()

        def parse_relative_url(url, query):
            """Create full url with the relative url"""
            # get the base url http://books.toscrape.com
            base_url = urljoin(url, '/')
            relative_url = extract_with_css(query)

            return urljoin(base_url, relative_url)

        def parse_rating(query):
            """Change the rating number in word form to it's integer form"""
            text_to_int = {
                'one': 1,
                'two': 2,
                'three': 3,
                'four': 4,
                'five': 5,
            }
            # get the class of <p class=star-rating Five>,
            # split it to get only the second class and lower it
            rating = extract_with_css(query).split()[1].lower()

            return text_to_int[rating] if rating else 'not-rated'

        def parse_product_information():
            """Parse the table that contains product informations"""
            # list of all <th> values
            labels = response.css('tr th::text').getall()
            # list of all <td> values
            values = response.css('tr td::text').getall()
            product_information = {}
            for i, label in enumerate(labels):
                if label.lower() == 'availability':
                    # get only the number of available books
                    values[i] = re.search(r'\d+', values[i]).group()
                # remove parenthesis and dot in the label if they are any
                # change the value of the string to an integer 
                # if it is a number
                product_information[re.sub(r'[().]', '', label.lower())] = \
                    int(values[i]) if values[i].isdigit() else values[i]

            return product_information

        # create book item
        book = BookItem()
        # get url
        book['url'] = response.url
        # get <a> in the second last <li> in <ul> that has breadcrumb class
        book['category'] = extract_with_css(
            '.breadcrumb li:nth-last-child(2) a::text'
        )
        # get <h1>
        book['title'] = extract_with_css('h1::text')
        # get <img> src attribute in <div> that has product_gallery id
        book['image'] = parse_relative_url(
            book['url'],
            '#product_gallery img::attr(src)'
        )
        # get <p class=star-rating Five> class attribute
        # that is not in product_pod
        book['rating'] = parse_rating(
            ':not(.product_pod) > .star-rating::attr(class)'
        )
        # get first <p> just after <div> that has product_description class
        book['description'] = extract_with_css(
            '#product_description + p::text'
        )
        # get product information in <table>
        product_information = parse_product_information()
        book['upc'] = product_information['upc']
        book['product_type'] = product_information['product type']
        book['price_excluding_tax'] = product_information['price excl tax']
        book['price_including_tax'] = product_information['price incl tax']
        book['tax'] = product_information['tax']
        book['availability'] = product_information['availability']
        book['number_of_reviews'] = product_information['number of reviews']

        yield book
