import json
import os.path
import re

import time

from splinter import Browser

DL_DIR = "svg"


def parse_url(url):
    m = re.search("icons/(.+)\?", url)
    name = m.group(1)

    m = re.search("style=(.+)", url)
    style = m.group(1)

    return name, style


def dl_icon(b, url):
    b.visit(url)

    svg = b.find_by_css("svg.fa-7x")[0]

    name, style = parse_url(url)
    filename = "{name}-{style}.svg".format(name=name, style=style)

    with open(os.path.join(DL_DIR, filename), "w") as f:
        f.write(svg.outer_html)



def get_icon_names(b):
    b.visit("https://fontawesome.com/icons?d=gallery")

    button_css = "div.mt3-ns > button"

    while len(b.find_by_css(button_css)) > 0:
        next_button = b.find_by_css(button_css)[0]
        next_button.click()

    items = b.find_by_css("#results-icons li a")

    urls = [x["href"] for x in items]

    return list(filter(lambda x: x!="https://fontawesome.com/pro", urls))


def dl_icons(b, urls):
    for i,url in enumerate(urls):
        dl_icon(b, url)
        time.sleep(1)

        # hacky way to avoid memory leak
        if i > 0 and i%100 == 0:
            b.quit()
            b = Browser()


def load_urls(filename="urls.json"):
    with open("urls.json") as f:
        return json.load(f)


def run():
    with Browser() as b:
        urls = get_icon_names(b)

        # Save urls in json file just in case you need it later
        with open("urls.json", "w") as f:
            json.dump(urls, f)

        dl_icons(b, urls)


if __name__ == "__main__":
    run()
