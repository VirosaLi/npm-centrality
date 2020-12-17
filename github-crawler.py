import xml.etree.ElementTree as ET
from json import dump, load, loads
from json.decoder import JSONDecodeError
from subprocess import run

import requests
from github import Github


def format_clone_url(repo_name):
    return f"https://github.com/{repo_name}.git"


def format_package_json_url(repo_name):
    return f"https://raw.githubusercontent.com/{repo_name}/master/package.json"


def format_query_word(key):
    return f"{key}+language:JavaScript"


def github_repo_walker(query_word, star_limit):

    g = Github()
    repos = g.search_repositories(query_word, "stars", "desc")

    repo_names = []
    for repo in repos:
        if int(repo.stargazers_count) >= star_limit:
            repo_names.append(repo.full_name)
        else:
            break

    repo_dict = {}
    for name in repo_names:
        url = format_package_json_url(name)
        if name == "iotaledger/trinity-wallet":
            url = url.replace("master", "develop")
        page = requests.get(url)
        try:
            data = loads(page.content)
            deps = data.get("dependencies", {})
            print(f"{name} has {len(deps)} dependencies")
            repo_dict[name] = [dep for dep, _ in deps.items()] if len(deps) != 0 else []

        except JSONDecodeError:
            print(f"Cannot get package.json for {name}.")
    return repo_dict


def get_loc_from_xml(xml_name):
    tree = ET.parse(xml_name)
    root = tree.getroot()
    loc = 0
    for child in root.iter("file"):
        loc += int(child.get("code"))
    return loc


def github_repo_analyser(repo_name):
    url = format_clone_url(repo_name)
    repo_dir = "tmp"
    loc_report = "cloc.xml"
    run(f"git clone {url} {repo_dir}", shell=True)
    run(f"pygount --suffix=js --format=cloc-xml --out={loc_report} tmp", shell=True)
    loc = get_loc_from_xml(loc_report)
    print(loc)


def search_github():
    key_words = ["wallet", "web3"]
    stars = 100
    for key_word in key_words:
        query = format_query_word(key_word)
        result = github_repo_walker(query, stars)
        with open(f"data/{key_word}.json", "w") as file:
            dump(result, file, indent=4)


def fetch_repo():
    pass


if __name__ == "__main__":
    fetch_repo()
