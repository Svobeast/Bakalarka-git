from bs4 import BeautifulSoup
import requests
from datetime import datetime
import os.path
import pandas as pd

response = requests.get("https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/pisek-307/")
web = response.text

soup = BeautifulSoup(web, "html.parser")

"""with open("pocasi.txt", "w", encoding="utf-8") as new_file:
    new_file.write(str(soup))""" #pouze na uvodni nalezeni dat

existuje = os.path.exists("mysite/main/scraping/pocasi.csv")
print(existuje)
if existuje == False:
    with open("mysite/main/scraping/pocasi.csv", "w", encoding="utf-8") as new_file:
        new_file.write("Den, Čas, Teplota, Pocitová teplota, Vlhkost\n")

with open("mysite/main/scraping/pocasi.csv", "a", encoding="utf-8") as file:
    cas_temp = datetime.now()
    cas = cas_temp.strftime("%H:%M")
    den = cas_temp.strftime("%d.%m.%Y")
    teplota = soup.find(name="div", class_="alfa mb-1").string.strip()
    zbytek = soup.findAll("span", class_="strong text-black")
    pocit = zbytek[0].string.strip()
    vlhkost = zbytek[1].string.strip()


    #       Den,Čas,Tepolota,pocitovaT,Vlhkost
    data = f"{den}, {cas}, {teplota}, {pocit}, {vlhkost}" + "\n"
    file.write(data)

nf = pd.read_csv("mysite/main/scraping/pocasi.csv")
nf.to_excel("mysite/main/scraping/pocasi.xlsx", "Počasí Písek", index=False)