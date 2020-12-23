from os import environ
from subprocess import run, CalledProcessError
from json import loads, load, dump

from tqdm import tqdm


environ["GITHUB_AUTH_TOKEN"] = "token"

with open("../data/wallet_url_improved.json", "r") as file:
    urls = load(file)


def format_criticality_command(target_url):
    return f"criticality_score --repo {target_url} --format json"


def fetch_criticality(repo_name):
    url = urls[repo_name].replace("/issues", "")
    command = format_criticality_command(url)
    try:
        result = run(command, capture_output=True, shell=True, check=True)
        try:
            json_result = loads(result.stdout)
            return json_result["criticality_score"]
        except ValueError:
            print(f"load result from {url} failed, invalid json")
            print(result.stdout)

    except CalledProcessError:
        print(f"fetch score from {url} failed")


# result_list = []
# for url in tqdm(urls.values()):
#     url = url.replace("/issues", "")
#     command = format_criticality_command(url)
#     try:
#         result = run(command, capture_output=True, shell=True, check=True)
#         try:
#             json_result = loads(result.stdout)
#             result_list.append(json_result)
#         except ValueError:
#             print(f"load result from {url} failed, invalid json")
#             print(result.stdout)
#
#     except CalledProcessError:
#         print(f"fetch score from {url} failed")
#
# with open('../data/wallet_criticality.json', 'w') as file:
#     dump(result_list, file)
