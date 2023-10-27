from django import forms



class Vyber(forms.Form):
    moznosti = [("Aknbl", "NBL - Aktuální tabulka"),
                ("HisNbl", "NBL - Historická tabulka"),
                ("AkPocasi", "Aktuální počasí"),
                ("zlato", "Vývoj ceny Zlata")       
             ]
    data = forms.ChoiceField(choices=moznosti, label="Jaká data chceš?")