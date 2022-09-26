import datetime
import re
import uuid
from dataclasses import dataclass

import chromedriver_autoinstaller
import common.utils as utils
import requests
from bs4 import BeautifulSoup
from common.database import Database
from models.games.rawg import Rawg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--headless")

chromedriver_autoinstaller.install()
driver = webdriver.Chrome(options=chrome_options)


@dataclass
class Scrape:

    def find_description(self):
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        description = soup.find(
            "div", {"class": "su-spoiler-content su-u-clearfix su-u-trim"})

        try:
            description = description.text
        except:
            description = None

        return description

    @classmethod
    def init_database(cls):
        while cls.URL:
            driver.get(cls.URL)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "entry-title")))
            content = driver.page_source

            large_soup = BeautifulSoup(content, "html.parser")
            soups = large_soup.find_all("article")

            for soup in soups:
                # get category
                category_elems = soup.findAll("span", {"class": "cat-links"})
                cat_list = [element.text for element in category_elems]
                if cat_list[0] == "Lossless Repack":

                    title_elems = soup.findAll("h3")
                    title_list = [element for element in title_elems]

                    # fix no title
                    if len(title_list) == 0:
                        continue

                    dirty_title = re.findall(r"<strong>.+?<",
                                             str(title_list[0]))
                    clean_title = dirty_title[0][8:-1].strip()
                    title = clean_title.replace("&amp;", "&")

                    link_elem = soup.findAll("h1", {"class": "entry-title"})
                    link_list = [element.a['href'] for element in link_elem]
                    url = link_list[0]

                    date_elem = soup.findAll("time", {"class": "entry-date"})
                    date_list = [element['datetime'] for element in date_elem]
                    entry_date = datetime.datetime.strptime(
                        date_list[0], "%Y-%m-%dT%H:%M:%S%z")

                    magnet = None
                    try:
                        magnet_elem = soup.find(
                            'a', attrs={'href': re.compile("magnet")})
                        magnet = magnet_elem.get('href')
                    except:
                        continue

                    # get img
                    img_elems = soup.findAll("img", {"class": "alignleft"})
                    img_list = [element['src'] for element in img_elems]
                    image = img_list[0]

                    # get every entry list
                    gen_elems = soup.findAll(
                        "p", {"style": "height: 200px; display: block;"})
                    gen_list = [element.text for element in gen_elems]
                    genre_pattern = re.compile(r"(Genres/Tags: .+)")
                    original_size_pattern = re.compile(
                        r"(Original Size:\s?.+)")
                    repack_size_pattern = re.compile(r"(Repack Size:\s?.+)")

                    for item in gen_list:

                        tags = None
                        try:
                            match_genre = genre_pattern.search(item)
                            found_genre = match_genre.group(1)
                            tags = found_genre.replace("Genres/Tags: ",
                                                       "").split(", ")
                        except:
                            pass

                        match_original_size = original_size_pattern.search(
                            item)
                        found_original_size = match_original_size.group(1)
                        match_org_size_int = re.findall(
                            r"(\d+\.?,?\d?\s?\w{2})", found_original_size)

                        if len(match_org_size_int) == 0:
                            match_org_size_int = found_original_size[15:-3]
                            match_org_size_int = utils.roman_to_int(
                                match_org_size_int)
                            match_org_size_int = [
                                str(match_org_size_int) + " GB"
                            ]

                        original_size = float(
                            match_org_size_int[0][:-2].replace(
                                ",", ".").replace(" ", "")
                        ) if match_org_size_int[0][-2:] == "GB" else float(
                            match_org_size_int[0][:-3]) * 0.001

                        match_repack_size = repack_size_pattern.search(item)
                        found_repack_size = match_repack_size.group(1)

                        match_repack_size_int = re.findall(
                            r"(\d+\.?\d?\s?\w{2})", found_repack_size)

                        if len(match_repack_size_int) == 0:
                            match_repack_size_int = found_repack_size[18:-24]
                            match_repack_size_int = utils.roman_to_int(
                                match_repack_size_int)
                            match_repack_size_int = [
                                str(match_repack_size_int) + " GB"
                            ]

                        if len(match_repack_size_int) == 2:
                            match_repack_size_int[0] = match_repack_size_int[1]

                        repack_size = float(
                            match_repack_size_int[0][:-3].replace(",", ".")
                        ) if match_repack_size_int[0][-2:] == "GB" else float(
                            match_repack_size_int[0][:-3]) * 0.001

                        description = soup.find("div", {
                            "class":
                            "su-spoiler-content su-u-clearfix su-u-trim"
                        })
                        try:
                            description = description.text
                        except:
                            description = None

                        game = Database.find_one(cls.collection,
                                                 {"title": title})

                        stop_scrape = False
                        if game == None:
                            _id = uuid.uuid4().hex
                            print(f'pushing {title} to mongo')
                            cls.push_to_mongo(
                                _id, {
                                    "_id": _id,
                                    "title": title,
                                    "tags": tags,
                                    "original_size": original_size,
                                    "repack_size": repack_size,
                                    "magnet": magnet,
                                    "image": image,
                                    "entry_date": entry_date,
                                    "url": url,
                                    "description": description
                                })
                            Rawg(_id=_id, title=title).api().save_to_mongo()
                        else:
                            stop_scrape = True
            next_url = large_soup.findAll('a', {'class': 'next page-numbers'})
            if next_url and not stop_scrape:
                cls.URL = next_url[0].get('href')
            else:
                break
