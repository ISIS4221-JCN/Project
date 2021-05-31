# run 'scrapy runspider WHO_scraper.py' to scrape data

from datetime import date
import scrapy
import json

pg_count = 0

class CovidScraper(scrapy.Spider):
    # Language
    lang = 'fr'
    name = "WHO_scraper"

    # WHO FAQ URLs
    if lang == 'en':
        start_urls = ["https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-adolescents-and-youth",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-masks",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/q-a-children-and-masks-related-to-covid-19",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-breastfeeding",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-cleaning-and-disinfecting-surfaces-in-non-health-care-settings",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-climate-change",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-contact-tracing",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-contraception-and-family-planning",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-dexamethasone",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/environmental-surveillance",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-food-businesses",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-food-safety-and-nutrition",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-health-and-safety-in-the-workplace",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-how-is-it-transmitted",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-mass-gatherings",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-pregnancy-and-childbirth",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-risks-and-safety-for-older-people",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-schools",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-staying-active",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-staying-at-hotels-and-accommodation-establishments",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-tobacco",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-(covid-19)-vaccines",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-(covid-19)-vaccines-safety",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-ventilation-and-air-conditioning",
                      "https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-travel-advice-for-the-general-public"]
    elif (lang == 'es') or (lang == 'fr'):
            start_urls = [f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-adolescents-and-youth",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-masks",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/q-a-children-and-masks-related-to-covid-19",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-breastfeeding",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-cleaning-and-disinfecting-surfaces-in-non-health-care-settings",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-climate-change",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-contact-tracing",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-contraception-and-family-planning",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-dexamethasone",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/environmental-surveillance",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-food-businesses",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-food-safety-and-nutrition",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-health-and-safety-in-the-workplace",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-how-is-it-transmitted",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-mass-gatherings",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-pregnancy-and-childbirth",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-risks-and-safety-for-older-people",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-schools",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-staying-active",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-staying-at-hotels-and-accommodation-establishments",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-tobacco",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-ventilation-and-air-conditioning",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-(covid-19)-vaccines",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-(covid-19)-vaccines-safety",
                          f"https://www.who.int/{lang}/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19-travel-advice-for-the-general-public"]
    def parse(self, response):
        global pg_count
        lang = 'fr'
        docs = {
            "title": [],
            "text": [],
            "link": [],
            "name": [],
            "source": [],
            "lang": [],
            "last_update": [],
        }

        QUESTION_ANSWER_SELECTOR = ".sf-accordion__panel"
        QUESTION_SELECTOR = ".sf-accordion__link::text"
        ANSWER_SELECTOR = ".sf-accordion__content ::text"
        ANSWER_HTML_SELECTOR = ".sf-accordion__content"

        questions_answers = response.css(QUESTION_ANSWER_SELECTOR)
        for question_answer in questions_answers:
            question = question_answer.css(QUESTION_SELECTOR).getall()
            question = " ".join(question).strip()
            answer = question_answer.css(ANSWER_SELECTOR).getall()
            answer = " ".join(answer).strip()
            answer_html = question_answer.css(ANSWER_HTML_SELECTOR).getall()
            answer_html = " ".join(answer_html).strip()

            # add question-answer pair to data dictionary
            docs["title"].append(question)
            docs["text"].append(answer)

        today = date.today()

        docs["link"] = [response.url] * len(docs["title"])
        docs["name"] = ["Q&A on coronaviruses (COVID-19)"] * len(docs["title"])
        docs["source"] = ["World Health Organization (WHO)"] * len(docs["title"])
        docs["lang"] = [lang] * len(docs["title"])
        docs["last_update"] = [today.strftime("%Y/%m/%d")] * len(docs["title"])

        print(f'Number of docs: {len(docs["text"])}')
        print(f'Doc titles: {docs["title"]}')
        with open(f'{lang}/WHO_{pg_count}.json', 'w') as fp:
            json.dump(docs, fp, sort_keys=True, indent=4)
            pg_count+=1

        #return columns
