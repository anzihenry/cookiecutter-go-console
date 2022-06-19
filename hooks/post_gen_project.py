"""
Does the following:
1. checks the project is an open source project, and choose license.
2. checks golang, and setup go.mod with default dependency.
3. checks CI, choose travis for open source project, and drone for private project.
4. checks docker, and make docker stuffs done.
5. checks git, make sure athor name and email are set. setup .gitignore, do initial commit.
"""
from datetime import datetime
import os
from subprocess import Popen
import requests

app_version = '{{cookiecutter.version}}'
is_open_source = '{{cookiecutter.open_source}}'
license = '{{cookiecutter.license}}'
author = '{{cookiecutter.author}}'
author_email = '{{cookiecutter.author_email}}'
enable_ci = '{{cookiecutter.enable_ci}}'
enable_docker = '{{cookiecutter.enable_docker}}'
enable_git = '{{cookiecutter.enable_git}}'
enable_sphinx_for_docs = '{{cookiecutter.enable_sphinx_for_docs}}'
year = datetime.now().year

def create_file(fileName, content):
    with open(fileName, 'w') as f:
        f.write(content)

def get_makefile():
    return """
    all:
        go build -o {{cookiecutter.project_name}}
    """  

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
    return """
    language: go
    os: 
    - linux
    - osx
    go:
    - 1.18.x
    notifications:
        email:true
    """

def get_drone():
    return """
    language: go
    """

def get_docker_file():
    return """
    ##
    ## Build
    ##
    FROM golang:1.18-alpine as builder
    RUN apk add --no-cache git make gcc g++
    WORKDIR /go/src/{{cookiecutter.project_name}}
    COPY . .
    RUN make build

    ##
    ## Deploy
    ##
    FROM scratch
    COPY --from=builder /go/src/{{cookiecutter.project_name}}/bin/{{cookiecutter.project_name}} /usr/local/bin/{{cookiecutter.project_name}}
    ENTRYPOINT ["/usr/local/bin/{{cookiecutter.project_name}}"]
    """

def setup_app_version():
    with open('VERSION', 'w') as f:
        f.write(app_version)

def setup_makefile():
    create_file("Makefile", get_makefile())

def setup_open_source():
    create_file("LICENSE", get_license(license))

def setup_docs():
    pass

# setup go stuffs
def setup_go():
    global author, author_email
    # make sure author and email are set
    if author == '' or author_email == '':
        print('WARNING: author name and email are required!')
        author = input('Please input author name: ')
        author_email = input('Please input author email: ')
        
    # download cobra-cli, cobra-cli makes command line biz easy.
    go_bin_path = os.path.join(os.environ['GOPATH'], 'bin')
    cobra_path = os.path.join(go_bin_path, 'cobra-cli')
    if not os.path.exists(cobra_path):
        go_cobra_cli = Popen(['go', 'install', 'github.com/spf13/cobra-cli@latest'])
        go_cobra_cli.wait()
    # init go module
    go_mod = Popen(['go', 'mod', 'init', '{{cookiecutter.project_name}}'])
    go_mod.wait()
    # create .cobra.yaml
    dot_cobra_yaml = """
    author: {} <{}>
    year: {}
    useViper: true
    """
    cobra_yaml_path = os.path.join(os.environ['HOME'], '.cobra.yaml')
    create_file(cobra_yaml_path, dot_cobra_yaml.format(author, author_email, year))
    # create cobra-base barebone files
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
        ['git', 'branch', '-m', 'main'],
        ['git', 'add', '.'],
        ['git', 'commit', '-m', 'initial commit']
    ]
    for command in GIT_COMMAND:
        git = Popen(command)
        git.wait()
        

def setup_project():
    setup_app_version()
    setup_makefile()
    if is_open_source == 'yes':
        setup_open_source()
    setup_go()
    if enable_docker == 'yes':
        setup_docker()
    if enable_ci == 'yes':
        setup_ci()
    if enable_sphinx_for_docs == 'yes':
        setup_docs()
    if enable_git == 'yes':
        setup_git()


# main
setup_project()


