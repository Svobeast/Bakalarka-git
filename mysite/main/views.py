from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Vyber
import pandas as pd
import os
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pytz


# Create your views here.


def home(response):
    
    if response.method == "POST":
        form = Vyber(response.POST)
        if form.is_valid():
            vyber = form.cleaned_data["data"]
            return HttpResponseRedirect(vyber)
    else:
        form = Vyber()
    return render(response, 'main/home.html', {"form":form})

def pocasiP(response):
    current_directory = os.getcwd()
    print(current_directory)
    if os.path.isfile("main/scraping/pocasi.xlsx"):
        try:
            df = pd.read_excel("main/scraping/pocasi.xlsx")
            print("1")
        except Exception as e:
            # Handle any other exceptions that may occur while reading the Excel file
            df = None
            print(e)
    else:
        # Handle the case where the file doesn't exist
        df = None
        print("3")
    return render(response, "main/pocasiP.html", {"df":df})

def AkPocasi(response):
    stranky = ["https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/blatna-15/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/branisov-1625/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/ceske-budejovice-54/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/ceske-velenice-55/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/cesky-krumlov-58/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/dacice-60/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/jindrichuv-hradec-157/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/majdalena-2636/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/orlik-nad-vltavou-4330/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/pisek-307/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/prachatice-325/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/putim-4342/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/rozmberk-nad-vltavou-1759/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/strakonice-386/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/spicak-7015/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/vrcovice-4357/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/zahori-2682/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/zlata-koruna-1769/",
               "https://www.in-pocasi.cz/predpoved-pocasi/cz/jihocesky/zabovresky-1724/"]
    #vytvoreni noveho filu
    existuje = os.path.exists("main/scraping/AkPocasi.csv")
    print(existuje)
    print(os.getcwd())
    if existuje == False:
        with open("main/scraping/AkPocasi.csv", "w", encoding="utf-8") as nove:
            nove.write("Den, Čas, Město, Teplota, Pocitová teplota, Vlhkost\n")
    else:
        with open("main/scraping/AkPocasi.csv", "w", encoding="utf-8") as smaz:
            smaz.write("Den, Čas, Město, Teplota, Pocitová teplota, Vlhkost\n")
    #for projeti kazde stranky
    for i in range(0, len(stranky)):
        dotaz = requests.get(stranky[i])
        web = dotaz.text
        soup = BeautifulSoup(web, "html.parser")
        #scrapovani stranek
        
        #pridavani do daneho filu
        with open("main/scraping/AkPocasi.csv", "a", encoding="utf-8") as file:
            tz = pytz.timezone("Europe/Prague")
            cas_temp = datetime.now(tz)
            cas = cas_temp.strftime("%H:%M")
            den = cas_temp.strftime("%d.%m.%Y")
            mesto = soup.find(name="h1", class_="mb-0").text.strip()
            mesto = mesto.replace("Předpověď počasí", "").strip()
            teplota = soup.find(name="div", class_="alfa mb-1").string.strip()
            zbytek = soup.findAll("span", class_="strong text-black")
            pocit = zbytek[0].string.strip()
            vlhkost = zbytek[1].string.strip()
            #zapis
            data = f"{den}, {cas}, {mesto}, {teplota}, {pocit}, {vlhkost}" + "\n"
            file.write(data)
    #vytvoreni Excel souboru
    DoE = pd.read_csv("main/scraping/AkPocasi.csv")
    DoE.to_excel("main/scraping/AkPocasi.xlsx", "Aktuální počasí", index=False)

    slozka = os.getcwd()
    print(slozka)
    if os.path.isfile("main/scraping/AkPocasi.xlsx"):
        try:
            df = pd.read_excel("main/scraping/AkPocasi.xlsx")
            print("1")
        except Exception as e:
            # Handle any other exceptions that may occur while reading the Excel file
            df = None
            print(e)
    else:
        # Handle the case where the file doesn't exist
        df = None
        print("3")

    return render(response, "main/AkPocasi.html", {"df":df})

"""def nbl(response):
    zadost = requests.get("https://nbl.basketball/statistiky?y=2022&p2=0&zak=1#tab-pane-three")
    web = zadost.text

    soup = BeautifulSoup(web, "html.parser")

    with open("nbl.txt", "w", encoding="utf-8") as new_file:            WIP
        new_file.write(str(soup))

    with open("tabulka.txt", "w", encoding="utf-8") as new_file:
        chci = soup.findAll("table")[1] #druha tabulka na strance
        new_file.write(str(chci))
    """