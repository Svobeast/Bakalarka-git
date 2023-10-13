from django import forms



class Vyber(forms.Form):
    moznosti = [("Aknbl", "NBL - aktuální tabulka"),
                ("HisNbl", "NBL - Historická tabulka"),
                ("pocasiP", "Počasí - Písek"),
                ("AkPocasi", "Aktuální počasí")                
             ]
    data = forms.ChoiceField(choices=moznosti, label="Jaká data chceš?")