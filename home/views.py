from django.shortcuts import render

import subprocess
# Create your views here.

def home_view(request):
    out = None
    if request.method == 'POST' :
            
        pocet = request.POST.get('pocet')

        result = subprocess.run(['python', 'home/test-kostka.py', pocet], capture_output=True, text=True)
        out = result.stdout.strip()

        if result.returncode == 0:
            out = result.stdout.strip()
            print('Output:', out)  # Debug statement
        else:
            print('Error:', result.stderr)  # Debug statement
        
    return render(request,'base.html', {'data':out})
    