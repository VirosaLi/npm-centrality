from math import ceil

from bs4 import BeautifulSoup
import requests


def npm_dep_format(offset: int):
    return f'https://www.npmjs.com/browse/depended?offset={offset}'


def npm_get_most_depended_upon_packages(limit: int):
    package_per_page = 36
    num_pages = ceil(limit / 36)
    packages = []
    for i in range(num_pages):
        url = npm_dep_format(i*package_per_page)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        deps = soup.find_all("h3", class_="db7ee1ac fw6 f4 black-90 dib lh-solid ma0 no-underline hover-black")
        for dep in deps:
            packages.append(dep.text)
    return packages[:limit]


num_package = 100
package_list = npm_get_most_depended_upon_packages(num_package)
