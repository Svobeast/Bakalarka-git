import random, sys

pocet = int(sys.argv[1])

soucty = [0]*19


for i in range(0, pocet):

    soucet = random.randint(1,6)+random.randint(1,6)+random.randint(1,6)

    soucty[soucet]+=1

for i in range(0, len(soucty)):
    print (f"Číslo {i} padlo {soucty[i]}", flush=True)