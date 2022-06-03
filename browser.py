import argparse
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore

init(autoreset=True)

parser = argparse.ArgumentParser()
parser.add_argument('file', help='directory name')
args = parser.parse_args()
path = args.file
if os.access(path, os.F_OK):
    pass
else:
    os.mkdir(path)

stack = deque()
last_website = None


def previous_website():
    if len(stack) > 1:
        for _ in range(2):
            if last_website != stack[-1]:
                read_websites(stack.pop())
            else:
                stack.pop()


def read_websites(web):
    with open(f'{path + "/" + web}', 'r') as f:
        print(f.read())


def save_website(web, text):
    with open(f'{path + "/" + web}', 'w', encoding='UTF-8') as f:
        f.write(text)


def read_html(r):
    soup = BeautifulSoup(r.content, 'html.parser')
    tags = ['p', 'a', 'ul', 'ol', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    output = ''
    for t in soup.body.descendants:
        if t.name == 'a':
            output += Fore.BLUE + t.get_text()
        elif t.name in tags:
            output += t.get_text()

    save_website(web_input, output)
    print(output)

search = True
while search:
    web_input = input().strip().lower()
    if web_input == 'exit':
        search = False
        break
    elif web_input == 'back':
        previous_website()
        continue
    websites = os.listdir(path)
    for i in websites:
        if web_input == i:
           read_websites(web_input)
           continue
    if web_input[-4] != '.':
        print('Incorrect URL')
        continue
    if web_input[:7] == 'https://':
        r = requests.get(web_input)
    else:
        r = requests.get('https://' + web_input)
    read_html(r)
    stack.append(web_input[:-4])
    last_website = web_input[:-4]
