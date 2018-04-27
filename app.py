from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/<string:turing_account>/<string:repo>')
def scraper_with_user(turing_account, repo):
    return get_user_pr(turing_account, repo, None)

@app.route('/<string:turing_account>/<string:repo>/<string:github_user>')
def scraper_nometadata(turing_account, repo, github_user):
    return get_user_pr(turing_account, repo, github_user)


def get_user_pr(account, repo, username):
    url = 'https://github.com/{account}/{repo}/pulls'.format(
        account=account,
        repo=repo,
    )
    list_items = None
    pr_list = []

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    list_items = soup.select("li")
    for list_item in list_items:
        links = list_item.select("a")
        if len(links) >= 2:
            pr = 'https://github.com/{}'.format(links[0]['href'])
            user = links[1].text
            if '/pull/' in pr and (not username or (username and username.lower() == user.lower())):
                pr_list.append(pr)
    counter_position = None
    if len(pr_list) == 1:
        return pr_list[0]
    elif len(pr_list) > 1:
        return jsonify({'pr_list': pr_list})
    return "None"

if __name__ == '__main__':
    app.run(debug=True)
