"""
Does the following:
1. checks the project is an open source project, and choose license.
2. checks golang, and setup go.mod with default dependency.
3. checks CI, choose travis for open source project, and drone for private project.
4. checks docker, and make docker stuffs done.
5. checks git, make sure athor name and email are set. setup .gitignore, do initial commit.
"""
from email import header
import os
from subprocess import Popen
import requests

is_open_source = '{{cookiecutter.open_source}}'
license = '{{cookiecutter.license}}'
if is_open_source == 'yes':
    create_file("LICENSE", get_license(license))

# setup go.mod
Popen(['go', 'mod', 'init', '{{cookiecutter.project_name}}'])

# setup ci
enable_ci = '{{cookiecutter.enable_ci}}'
if enable_ci = 'yes':
    if is_open_source == 'yes':
    create_file(".travis.yml", get_travis())
    else:
    create_file(".drone.yml", get_drone())


# setup docker
enable_docker = '{{cookiecutter.enable_docker}}'
if enable_docker == 'yes':
    create_file("DockerFile", get_docker_file())

# setup git
enable_git = '{{cookiecutter.enable_git}}'
author = '{{cookiecutter.author}}'
author_email = '{{cookiecutter.author_email}}'
if enable_git == 'yes':
    if author == '' or author_email == '':
        print('WARNING: author name and email are required!')
        author = input('Please input author name: ')
        author_email = input('Please input author email: ')
    
    create_file(".gitignore", get_dot_gitignore('go'))
    Popen(['git', 'init'])
    Popen(['git', 'config', 'user.name', author])
    Popen(['git', 'config', 'user.email', author_email])
    Popen(['git', 'add', '.'])
    Popen(['git', 'commit', '-m', 'initial commit'])
    

def create_file(fileName, content):
    with open(fileName, 'w') as f:
        f.write(content)  

def get_license(license_type):
    url = 'https://api.github.com/licenses/%s' % license_type.lower()
    gh_headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=gh_headers)
    if response.status_code == 200:
        return response.json()["body"]
    else:
        return None

def get_dot_gitignore(language_or_ide):
    url = "https://www.toptal.com/developers/gitignore/api/%s" % language_or_ide
    response = request.get(url)
    if response.status_code == 200:
        return response.body
    else:
        return None

def get_travis():
    return ""

def get_drone():
    return ""

def get_docker_file():
    return ""

