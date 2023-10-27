from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Vyber
import pandas as pd
import os
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pytz
from django.templatetags.static import static
import re
from string import printable

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
    existuje = os.path.exists("/svoboda/mysite/main/static/main/AkPocasi.csv")
    print(existuje)
    print(os.getcwd())
    if existuje == False:
        with open("/svoboda/mysite/main/static/main/AkPocasi.csv", "w", encoding="utf-8") as nove:
            nove.write("Den, Čas, Město, Teplota, Pocitová teplota, Vlhkost\n")
    else:
        with open("/svoboda/mysite/main/static/main/AkPocasi.csv", "w", encoding="utf-8") as smaz:
            smaz.write("Den, Čas, Město, Teplota, Pocitová teplota, Vlhkost\n")
    #for projeti kazde stranky
    for i in range(0, len(stranky)):
        dotaz = requests.get(stranky[i])
        web = dotaz.text
        soup = BeautifulSoup(web, "html.parser")
        #scrapovani stranek
        
        #pridavani do daneho filu
        with open("/svoboda/mysite/main/static/main/AkPocasi.csv", "a", encoding="utf-8") as file:
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
    DoE = pd.read_csv("/svoboda/mysite/main/static/main/AkPocasi.csv")
    DoE.to_excel("/svoboda/mysite/main/static/main/AkPocasi.xlsx", "Aktuální počasí", index=False)

    slozka = os.getcwd()
    print(slozka)
    if os.path.isfile("/svoboda/mysite/main/static/main/AkPocasi.xlsx"):
        try:
            df = pd.read_excel("/svoboda/mysite/main/static/main/AkPocasi.xlsx")
            print("1")
        except Exception as e:
            # Ostatni chyby
            df = None
            print(e)
    else:
        # Chyba, když neexistuje soubor
        df = None
        print("3")

    odkazy = [
            ("CSV",'main/AkPocasi.csv'),
            ("EXCEL",'main/AkPocasi.xlsx')
            ]

    return render(response, "main/AkPocasi.html", {"df":df, "odkazy":odkazy})

def Aknbl(response):
    zadost = requests.get("https://nbl.basketball/tabulka")
    web = zadost.text

    soup = BeautifulSoup(web, "html.parser")



    with open("/svoboda/mysite/main/static/main/Aknbl.csv", "w", encoding="utf-8") as new_file:
        hlavicka = soup.find_all("table")[0].find("tr").get_text(",", strip=True) #získání hlavičky - prvni tabulka na strance a jeji prvni tr
        hlavicka = hlavicka.replace(",posledních 5 zápasů,Odkaz na graf","")
        new_file.write(str(hlavicka))

        
        for i in range(1, len(soup.find_all("table")[0].find_all("tr"))):   #ziskani obsahu - prvni tabulka na strance a jeji zbyvajici tr

            obsah = soup.find_all("table")[0].find_all("tr")[i].get_text(",", strip=True)
            obsah = obsah.replace("Posun v tabulce,", "")
            obsah = obsah.replace(",Popis ikonky\"", "")
            new_file.write("\n")
            new_file.write(str(obsah))

    DoE = pd.read_csv("/svoboda/mysite/main/static/main/Aknbl.csv")
    DoE.to_excel("/svoboda/mysite/main/static/main/Aknbl.xlsx", "Aktuální tabulka NBL", index=False)

    if os.path.isfile("/svoboda/mysite/main/static/main/Aknbl.xlsx"):
        try:
            df = pd.read_excel("/svoboda/mysite/main/static/main/Aknbl.xlsx")
        except Exception as e:
            # Ostatni chyby
            df = None
            print(e)
    else:
        # Chyba, když neexistuje soubor
        df = None
        print("Soubor neni")

    odkazy = [
            ("CSV",'main/Aknbl.csv'),
            ("EXCEL",'main/Aknbl.xlsx')
            ]
    

    return render(response, "main/Aknbl.html", {"df":df, "odkazy":odkazy})

def HisNbl(response):
    zadost = requests.get("https://nbl.basketball/tabulka")
    web = zadost.text

    soup = BeautifulSoup(web, "html.parser")

    with open("/svoboda/mysite/main/static/main/HisNbl.csv", "w", encoding="utf-8") as new_file:
        hlavicka = soup.find_all("table")[1].find("tr").get_text(",", strip=True) #získání hlavičky - druha tabulka na strance a jeji prvni tr
        hlavicka = hlavicka.replace(",Odkaz na graf","")
        new_file.write(str(hlavicka))

        
        for i in range(1, len(soup.find_all("table")[1].find_all("tr"))):   #ziskani obsahu - druha tabulka na strance a jeji zbyvajici tr

            obsah = soup.find_all("table")[1].find_all("tr")[i].get_text(",", strip=True)
            new_file.write("\n")
            new_file.write(str(obsah))

    DoE = pd.read_csv("/svoboda/mysite/main/static/main/HisNbl.csv")
    DoE.to_excel("/svoboda/mysite/main/static/main/HisNbl.xlsx", "Historická tabulka NBL", index=False)

    if os.path.isfile("/svoboda/mysite/main/static/main/HisNbl.xlsx"):
        try:
            df = pd.read_excel("/svoboda/mysite/main/static/main/HisNbl.xlsx")
        except Exception as e:
            # Ostatni chyby
            df = None
            print(e)
    else:
        # Chyba, když neexistuje soubor
        df = None
        print("Soubor neni")

    odkazy = [
            ("CSV",'main/HisNbl.csv'),
            ("EXCEL",'main/HisNbl.xlsx')
            ]

    return render(response, "main/HisNbl.html", {"df":df, "odkazy":odkazy})

def zlato(response):
    #zakladni setup
    base_url = "https://www.kurzy.cz/komodity/zlato-graf-vyvoje-ceny/" #202309-czk-1g format: rok|mesic-mena-jednotka
    tz = pytz.timezone("Europe/Prague")
    cas_temp = datetime.now(tz)
    mesic = cas_temp.strftime("%m")
    rok = cas_temp.strftime("%Y")
    print(mesic, rok)
    konec = 12

    existuje = os.path.exists("/svoboda/mysite/main/static/main/zlato.csv")
    
    if existuje == False:
        with open("/svoboda/mysite/main/static/main/zlato.csv", "w", encoding="utf-8") as new_file:
            new_file.write(f"Rok, Měsíc, Průměr, Maximum, Minimum, Měsíční změna\n")
        for i in range(2006, int(rok)+1):
            if i == int(rok):
                konec = int(mesic) - 1 
            for j in range(1, int(konec)+1):
                if int(j) < 10:
                    j = "0" + str(j)
                url = base_url + str(i) + str(j) + "-czk-1g"
                
                with open("/svoboda/mysite/main/static/main/zlato.csv", "a", encoding="utf-8") as file:
                    zadost = requests.get(url)
                    web = zadost.text
                    soup = BeautifulSoup(web, "html.parser")
                    datum = soup.find("h1").string.split()
                    rok = datum[2]
                    mesic = datum[1]

                    tabulka = soup.find("table")
                    maximum = tabulka.find_all("tr")[1].find_all("td")[1].get_text(strip=True)
                    minimum = tabulka.find_all("tr")[2].find_all("td")[1].get_text(strip=True)
                    prumer = tabulka.find_all("tr")[3].find_all("td")[1].get_text(strip=True)
                    
                    zacatek = tabulka.find_all("tr")[4].find_all("td")[1].get_text(strip=True)
                    zaver = tabulka.find_all("tr")[5].find_all("td")[1].get_text(strip=True)

                    zacatek = re.sub("[^{}]+".format(printable), "", zacatek) #v promenych jsou neviditelne mezery, ktere vadili pri meneni typu promenne - tohle je odstrani
                    zaver = re.sub("[^{}]+".format(printable), "", zaver) 

                    zmena = ((float(zaver)-float(zacatek))/float(zacatek))*100
                    zmena = round(zmena, 2)
                    zmena = str(zmena) + "%"

                    file.write(f"{rok},{mesic},{prumer},{maximum},{minimum},{zmena}\n")
    else:
        pass

    DoE = pd.read_csv("/svoboda/mysite/main/static/main/zlato.csv")
    DoE.to_excel("/svoboda/mysite/main/static/main/zlato.xlsx", "Vývoj ceny zlata", index=False)

    if os.path.isfile("/svoboda/mysite/main/static/main/zlato.xlsx"):
        try:
            df = pd.read_excel("/svoboda/mysite/main/static/main/zlato.xlsx")
        except Exception as e:
            # Ostatni chyby
            df = None
            print(e)
    else:
        # Chyba, když neexistuje soubor
        df = None
        print("Soubor neni")

    odkazy = [
            ("CSV",'main/zlato.csv'),
            ("EXCEL",'main/zlato.xlsx')
            ]

    return render(response, "main/zlato.html", {"df":df, "odkazy":odkazy})