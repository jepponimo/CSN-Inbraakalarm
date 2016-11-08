import time
def isInt(integer):
    try:
        integer = int(integer)
        return True
    except:
        return False

def timer(tijd_interval):
    import time
    if isInt(tijd_interval) == True:
        start = time.time()
        time.sleep(tijd_interval)

        done = time.time()
        elapsed = done - start
        print('Knipper')
    else:
        print('De opgegeven waarde is geen getal/integer')

def lampAan(tijd_interval):
    import time
    if isInt(tijd_interval) == True:
        time.sleep(tijd_interval)
        print('Lamp Aan')
        return True
    else:
        return False

def lampUit(tijd_interval):
    import time
    if isInt(tijd_interval) == True:
        time.sleep(tijd_interval)
        print('Lamp Uit')
        return True
    else:
        return False

def lampKnipper(tijd_interval):
    lampAan(tijd_interval)
    lampUit(tijd_interval)

while True: # Geeft een reactie per 1 seconde
    lampKnipper(1)
