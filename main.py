import re
import requests
from bs4 import BeautifulSoup
from time import sleep
from table import writer

def get_href(name):
    link_element = name.find("a")
    if link_element:
        href = link_element.attrs.get("href")
        card_url = "https://www.yelp.ca" + href if href else ''
        return card_url
    return None



def scrape_data():
    data = []
    category_first_salon = {}
    a = 0

    for p in range(24):
        url = f"https://www.yelp.ca/search?find_desc=Beauty+%26+Spas&find_loc=Vancouver%2C+BC&start={a}"
        request = requests.get(url)
        sleep(3)
        soup = BeautifulSoup(request.text, 'html.parser')

        names = soup.find_all("h3", class_="css-1agk4wl")
        categories = soup.find_all("span", class_="css-11bijt4")
        district = soup.find_all("span", class_="css-chan6m")

        district_new = []
        for el in district:
            try:
                if el.text[0] != '(' and ord('a') <= ord(el.text[0].lower()) <= ord("z"):
                    district_new.append(el)
            except IndexError as e:
                district_new.append(None)
                continue


        for name, category, district in zip(names, categories, district_new[:10]):
            name_text = name.text.strip()
            category_text = category.text.strip()
            district_text = district.text.strip() if district else ''

            card_url = get_href(name)
            if card_url:
                card_request = requests.get(card_url)
                sleep(5)
                card_soup = BeautifulSoup(card_request.text, 'html.parser')

                number = card_soup.find_all("p", class_="css-1p9ibgf")
                numbers = [
                    el
                    for el in number
                    if re.match(r'\(\d+\)', el.text.strip())
                ]
                district_fulls = card_soup.find_all("div", class_="arrange__09f24__LDfbs gutter-2__09f24__CCmUo vertical-align-middle__09f24__zU9sE border-color--default__09f24__NPAKY")

                if numbers and district_fulls:
                    numbers_text = numbers[0].text.strip()
                    site_full_text = district_fulls[2].text.strip() if len(district_fulls) >= 3 else ''
                    address_full_text = district_fulls[4].text.strip() if len(district_fulls) >= 5 else ''


                    if name_text not in category_first_salon:
                        category_first_salon[name_text] = True

                    if category_first_salon[name_text]:
                        data.append({
                            'name': name_text,
                            'category': category_text,
                            'district': district_text,
                            'number': numbers_text,
                            'address_full': address_full_text,
                            'site': site_full_text
                        })
                        category_first_salon[name_text] = False
                        print(name_text, category_text, district_text, numbers_text, address_full_text, site_full_text)
        a += 10
    print("Дані успішно збережено в ексель.")
    writer(data)

if __name__ == '__main__':
    scrape_data()