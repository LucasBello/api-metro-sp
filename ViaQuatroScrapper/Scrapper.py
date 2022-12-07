import logging
import os
import requests
import time
import datetime
from bs4 import BeautifulSoup
import json

LINES_METRO = ['azul', 'verde', 'vermelha', 'amarela', 'lilás', 'prata']
LINES_CPTM = [
    'rubi',
    'diamante',
    'esmeralda',
    'turquesa',
    'coral',
    'safira',
    'jade']
ALL_LINES = LINES_METRO + LINES_CPTM

VQ_HOME_REQUEST = requests.get('http://www.viaquatro.com.br')
VQ_HOME_CONTENT = VQ_HOME_REQUEST.text

soup = BeautifulSoup(VQ_HOME_CONTENT, 'html.parser')
operation_column = soup.find(class_= "operacao")
extracted_status = {line:'' for line in ALL_LINES}
status_amarela = operation_column.find(class_="status").text
extracted_status['amarela'] = status_amarela
lines_containers = operation_column.find_all(class_ = "linhas")
for container in lines_containers:
    line_info_divs = container.find_all(class_ = "info")
    for div in line_info_divs:
        line_title  = ":"
        line_status = ","
        spans = div.find_all("span")
        line_title = spans[0].text.lower()
        line_status = spans[1].text.lower()
        extracted_status[line_title] = line_status
time_data = soup.find('time').text

def Convert(string):
    li = list(string.split(" "))
    return li
# Driver code
str1 = time_data
time=(Convert(str1))

bList = time
jsonStrb = json.dumps(bList, ensure_ascii=False, indent=2)
print(jsonStrb)


aList = extracted_status
jsonStr = json.dumps(aList, ensure_ascii=False, indent=2)
print(jsonStr)
with open("extracted_status.json", "w") as outfile:
    outfile.write('{\n''"Linhas": [\n'+jsonStr+'\n],\n'+'"Horario":'+jsonStrb+'\n}')