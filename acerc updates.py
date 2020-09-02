
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from datetime import date
import os

def getLinks(soup):
    links = []
    for tag in soup.findAll("li", class_="active-trail"):
        for href in tag.findAll("a", href=True):
            if href['href'] not in links:
                links.append(href['href'])

    return links

def getText(soup):
    for i in soup.findAll("p"):
        if("Last Updated" in i.getText()):
            text = i.getText()

    sep = "\n"       
    update = text.split(sep,1)[0]
    return update


def getSoup(request):
    return BeautifulSoup(request.content, 'html.parser')

def getRequest(link):
    return requests.get(link)


result = requests.get("https://energy.siu.edu/green-roof-team/")

soup = BeautifulSoup(result.content, 'html.parser')

links = getLinks(soup)
updates = []
for i in links:
    link = "https://energy.siu.edu/green-roof-team/{}".format(i)
    request = getRequest(link)
    soup = getSoup(request)
    update = [i.split("/index.php")[0], getText(soup)]
    if update not in updates:
        updates.append(update)
    newlinks = getLinks(soup)
    for new in newlinks:
        if new in links:
            pass
        else:
            newlink = link.split("index.php", 1)[0]  + new
            request = getRequest(newlink)
            soup = getSoup(request)
            update = getText(soup)
            if update not in updates:
                updates.append([new.split(".php")[0], update])

updatedata = pd.DataFrame(updates, columns=["Name", "Time"])
updatedata = updatedata.set_index("Name")

print("Current Update Data:")
print(updatedata)
path = "updatedata.csv"
if os.path.exists(path):
    olddata = pd.read_csv("updatedata.csv").set_index("Name")
    olddata = olddata.merge(updatedata, on=["Name", "Time"])
    olddata.to_csv("updatedata.csv")
else:
    updatedata.to_csv("updatedata.csv")


