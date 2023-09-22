from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Vyber
import pandas as pd
import os



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


"""  try:
        df = pd.read_excel("mysite/main/scraping/pocasi.xlsx")
    except FileNotFoundError:
        df = None"""

    