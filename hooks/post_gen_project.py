"""
Does the following:
1. checks the project is an open source project, and choose license.
2. checks golang, and setup go.mod with default dependency.
3. checks CI, choose travis for open source project, and drone for private project.
4. checks docker, and make docker stuffs done.
5. checks git, make sure athor name and email are set. setup .gitignore, do initial commit.
"""
from datetime import datetime
from email import header
import os
from subprocess import Popen
import requests

is_open_source = '{{cookiecutter.open_source}}'
license = '{{cookiecutter.license}}'
author = '{{cookiecutter.author}}'
author_email = '{{cookiecutter.author_email}}'
enable_ci = '{{cookiecutter.enable_ci}}'
enable_docker = '{{cookiecutter.enable_docker}}'
enable_git = '{{cookiecutter.enable_git}}'
year = datetime.now().year

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
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def get_travis():
    return ""

def get_drone():
    return ""

def get_docker_file():
    return ""

def setup_open_source():
    create_file("LICENSE", get_license(license))

# setup go stuffs
def setup_go():
    global author, author_email

    if author == '' or author_email == '':
        print('WARNING: author name and email are required!')
        author = input('Please input author name: ')
        author_email = input('Please input author email: ')
        
    # cobra-cli makes command line biz easy.
    go_cobra_cli = Popen(['go', 'install', 'github.com/spf13/cobra-cli@latest'])
    go_cobra_cli.wait()
    # init go module
    go_mod = Popen(['go', 'mod', 'init', '{{cookiecutter.project_name}}'])
    go_mod.wait()
    # create .cobra.yaml
    dot_cobra_yaml = """
    author: %s %s
    year: %s
    useViper: true
    """
    create_file(".cobra.yaml", dot_cobra_yaml % {'author': author, 'author_email': author_email, 'year': year})
    # create cobra-base barebone
    go_cobra_init = Popen(['cobra-cli', 'init'])
    go_cobra_init.wait()

# setup ci
def setup_ci():
    global is_open_source

    if is_open_source == 'yes':
        create_file(".travis.yml", get_travis())
    else:
        create_file(".drone.yml", get_drone())
        

# setup docker
def setup_docker():
    create_file("DockerFile", get_docker_file())

# setup git
def setup_git():
    global author, author_email
    
    if author == '' or author_email == '':
        print('WARNING: author name and email are required!')
        author = input('Please input author name: ')
        author_email = input('Please input author email: ')
        
        create_file(".gitignore", get_dot_gitignore('go'))

        GIT_COMMAND = [
            ['git', 'init'],
            ['git', 'config', 'user.name', author],
            ['git', 'config', 'user.email', author_email],
            ['git', 'add', '.'],
            ['git', 'commit', '-m', 'initial commit']
        ]
        for command in GIT_COMMAND:
            git = Popen(command)
            git.wait()
        
    
# main
if is_open_source == 'yes':
    setup_open_source()
setup_go()
if enable_docker == 'yes':
    setup_docker()
if enable_ci == 'yes':
    setup_ci()
if enable_git == 'yes':
    setup_git()

