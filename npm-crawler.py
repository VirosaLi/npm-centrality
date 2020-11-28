from math import ceil

from bs4 import BeautifulSoup
import requests


def npm_top_dep_format(offset: int):
    return f"https://www.npmjs.com/browse/depended?offset={offset}"


def npm_package_format(package: str):
    return f"https://www.npmjs.com/package/{package}"


def npm_depended_format(module: str, offset: int):
    return f"https://www.npmjs.com/browse/depended/{module}?offset={offset}"


def npm_get_most_depended_upon_packages(limit: int):
    package_per_page = 36
    num_pages = ceil(limit / package_per_page)
    packages = []
    for i in range(num_pages):
        url = npm_top_dep_format(i * package_per_page)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        deps = soup.find_all(
            "h3",
            class_="db7ee1ac fw6 f4 black-90 dib lh-solid ma0 no-underline hover-black",
        )
        for dep in deps:
            packages.append(dep.text)
    return packages[:limit]


def npm_get_num_dependents(package: str):
    url = npm_package_format(package)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    tags = soup.find_all("span", class_="c3fc8940")
    num_dependents = tags[1].text
    num_dependents = "".join(c for c in num_dependents if c.isdigit())
    return int(num_dependents)


def npm_get_dependents(package: str, num_dependents: int):
    package_per_page = 36
    num_pages = ceil(num_dependents / package_per_page)
    packages = []
    for i in range(num_pages):
        url = npm_depended_format(package, i * package_per_page)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        deps = soup.find_all(
            "h3",
            class_="db7ee1ac fw6 f4 black-90 dib lh-solid ma0 no-underline hover-black",
        )
        for dep in deps:
            packages.append(dep.text)
        print(f"page {i} finished, result length {len(packages)}")
    return packages


# num_package = 100
# package_list = npm_get_most_depended_upon_packages(num_package)

tmp_package = "lodash"
num_deps = npm_get_num_dependents(tmp_package)
print(num_deps)
deps_list = npm_get_dependents(tmp_package, num_deps)
print(deps_list)
print(len(deps_list))
