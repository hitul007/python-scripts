import requests
import urlparse
import os

github_token = os.environ.get('GITHUB_TOKEN')
current_repo_url = os.environ.get('GITHUB_REPO_URL')

headers = {'Authorization': 'token %s' % github_token}

current_user = os.popen("git config -l | grep user.name").read()
current_branch = os.popen("git status | head -n1 | rev | cut -d ' ' -f1 | rev").read()

if current_branch:
    current_branch = current_branch.replace('\n', '')

r = requests.get(urlparse.urljoin(current_repo_url, 'pulls?head=coverfox:%s' % (current_branch)), headers=headers)
responses = [r]
r = requests.get(urlparse.urljoin(current_repo_url, 'pulls?head=%s:%s' % (current_user, current_branch)), headers=headers)
responses.append(r)
json_data = r.json()

if r.status_code != 200:
    print("Request failed")

for res in responses:
   json_data = res.json()
   for data in json_data:
        url = data['html_url']
        state = data['state']
        print("*" * 72)
        print("Open pull requests")
        print("%s | %s" % (url, state))
        print("*" * 72)

