# run 'scrapy runspider CDC_General_scraper.py' to scrape data

from datetime import date

import scrapy
from scrapy.crawler import CrawlerProcess
import json

count = 0
lang = 'fr'

class CovidScraper(scrapy.Spider):
    name = "CDC_Scraper"
    if lang == 'en':
        start_urls = ["https://www.cdc.gov/coronavirus/2019-ncov/faq.html"]
    elif lang == 'es':
        start_urls = ["https://espanol.cdc.gov/coronavirus/2019-ncov/faq.html"]
    elif lang == 'fr':
        start_urls = ["https://www.cdc.gov/coronavirus/2019-ncov/hcp/non-us-settings/overview/index-fr.html"]

    def parse(self, response):
        global count, lang

        today = date.today()
        current_category = ""

        all_nodes = response.xpath("//*")
        for i,node in enumerate(all_nodes):
            # in category
            if node.attrib.get("class") == "onThisPageAnchor":
                current_category = node.attrib["title"]
                continue

            # in category
            if current_category:
                # in question
                if node.attrib.get("role") == "heading":
                    current_question = node.css("::text").get()

                # in answer
                if node.attrib.get("class") == "card-body":
                    current_answer = node.css(" ::text").getall()
                    current_answer = " ".join(current_answer).strip()
                    current_answer_html = node.getall()
                    current_answer_html = " ".join(current_answer_html).strip()

                    # add question-answer-pair to data dictionary
                    doc = {}
                    doc["title"] = current_question
                    doc["text"] = current_answer
                    doc["category"] = current_category
                    doc["link"] = ["https://www.cdc.gov/coronavirus/2019-ncov/faq.html"]
                    doc["source"] = ["Center for Disease Control and Prevention (CDC)"]
                    doc["lang"] = [lang]
                    doc["last_update"] = [today.strftime("%Y/%m/%d")]

                    with open(f'{lang}/CDC_{count}.json', 'w') as fp:
                        json.dump(doc, fp, sort_keys=True, indent=4)
                        count+=1

            # end of category
            if node.attrib.get("class") == "row":
                current_category = ""

        #return columns



if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(CovidScraper)
    process.start()
