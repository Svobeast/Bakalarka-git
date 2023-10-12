from django import forms



class Vyber(forms.Form):
    moznosti = [("nbl", "NBL - aktuální tabulka"),
                ("pocasiP", "Počasí - Písek"),
                ("AkPocasi", "Aktuální počasí")
             ]
    data = forms.ChoiceField(choices=moznosti, label="Jaká data chceš?")