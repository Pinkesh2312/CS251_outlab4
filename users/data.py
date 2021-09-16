import requests
from requests.exceptions import Timeout

def profile_info(username):
    try:
        response =requests.get('https://api.github.com/users/'+username, timeout=10)
    except Timeout:
        print('The request timed out')
    response.encoding = 'utf-8'
    dictionary = response.json()
    useful_info = dict()
    useful_info["followers"] = dictionary["followers"]
    useful_info["last_updated"] = dictionary["updated_at"]
    
    try:
        response = requests.get('https://api.github.com/users/'+username+'/repos', timeout=10)
    except Timeout:
        print('The request timed out')
    response.encoding = 'utf-8'
    listOfRepos = response.json()
    useful_info["repos"] = dict()
    for repo in listOfRepos:
        useful_info["repos"][repo["name"]] = repo["stargazers_count"]

    return useful_info
