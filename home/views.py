from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Hod_kostkou
from .models import Numbers
import random
# Create your views here.

def home_view(response):
    
    if response.method == 'POST' :
        print(response.POST)
        form = Hod_kostkou(response.POST)

        if form.is_valid():
            pocet = form.cleaned_data["pocet"]
            
            soucty = [0]*19 

            for i in range(0, pocet):

                soucet = random.randint(1,6)+random.randint(1,6)+random.randint(1,6)

                soucty[soucet]+=1
            
            for i in range(0, len(soucty)):
                new = Numbers(name = i, value = soucty[i])
                new.save()
        return HttpResponseRedirect('vysledek')

    else:
        form = Hod_kostkou()
        try:
            for i in range (0,18):
                Numbers.objects.all().delete()
        except: 
            pass
    return render(response,'home/kostka.html', {"form":form})

def vysledek(response):
    data = Numbers.objects.all()
    return render(response, 'home/vysledek.html', {"data": data})

def znovu(response):
    return HttpResponseRedirect()