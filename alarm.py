import time
from tkinter import *
import sqlite3
import RPi.GPIO as GPIO

global GPIOLamp
GPIOLamp = 7

global GPIOKnopStart
GPIOKnopStart = 9

global GPIOKnopStop
GPIOKnopStop = 8

# SQL
databasename = 'alarm.db'
def isDatabaseConnection(databasename):
    try:
        connect = sqlite3.connect(databasename)
        return True
    except:
        return False

def startDatabase(databasename): # Maak tabellen aan als deze nog niet bestaan
    if isDatabaseConnection(databasename) == True:
        connect = sqlite3.connect(databasename)
        c = connect.cursor()
        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS accounts
                         (gebruikersnaam text UNIQUE, email text, wachtwoord text, laatste_login_datum text)''')

        gegevens = ['NickW','nickwindt@hotmail.nl','kaas12321','09-11-2016']
        try:
            c.execute('''INSERT INTO accounts VALUES(?,?,?,?)''',gegevens)
        except:
            print('Account bestaat al')
        finally:
            connect.commit()

def isLoginCorrect(gebruikersnaam,wachtwoord):
    import sqlite3
    database = databasename
    if isDatabaseConnection(database) == True:
        connect = sqlite3.connect(database)
        c = connect.cursor()
        gegevens = [gebruikersnaam, wachtwoord]
        c.execute('''SELECT * FROM accounts WHERE gebruikersnaam = ? AND wachtwoord = ?''',gegevens)
        resultaten = c.fetchall()
        # controleer of gebruikersnaam EN wachtwoord overeenkomen met de opgegeven data
        for resultaat in resultaten:
            if resultaat[0] == gebruikersnaam and resultaat[2] == wachtwoord:
                connect.close()
                return True
        return False

def getCurrentDate():
    import datetime
    nu = datetime.datetime.now()
    datum = nu.strftime('%d-%m-%Y')
    return datum

# Timer
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
        GPIO.output(GPIOLamp,GPIO.HIGH)
        return True
    else:
        return False

def lampUit(tijd_interval):
    import time
    if isInt(tijd_interval) == True:
        time.sleep(tijd_interval)
        GPIO.output(GPIOLamp,GPIO.LOW)
        return True
    else:
        return False

def lampKnipper(tijd_interval_lampAan, tijd_interval_lampUit):

    lampAan(tijd_interval_lampAan)
    lampUit(tijd_interval_lampUit)

# GUI
root = Tk()

def showLoginMenu(): # in dit menu moet de bezoeker inloggen met zijn naam en code. De aanbieder kan hier inloggen met zijn wachtwoord en gebruikersnaam. (Via SQLite3)
    global huidigMenu
    huidigMenu = 'Inlog Menu'

    global bovenLoginFrame
    bovenLoginFrame = Frame(master=root)
    bovenLoginFrame.pack(side=TOP)

    middenLoginFrame = Frame(master=bovenLoginFrame)
    middenLoginFrame.pack(side=BOTTOM)

    gebruikersnaamLoginFrame = Frame(master=middenLoginFrame)
    gebruikersnaamLoginFrame.pack(side=TOP)

    codeLoginFrame = Frame(master=middenLoginFrame)
    codeLoginFrame.pack(side=BOTTOM)

    global onderLoginFrame
    onderLoginFrame = Frame(master=root)
    onderLoginFrame.pack(side=BOTTOM)

    informatieLoginLabel = Label(master=bovenLoginFrame,text='Vul uw gebruikersnaam en code in. Zodat U de inbraak settings kunt wijzigen',background='darkgrey',foreground='black',font=('Helvetica',10,'bold italic'),width=60,height=5)
    informatieLoginLabel.pack(side=TOP)

    global gebruikersnaamLoginEntry
    gebruikersnaamLoginEntry = Entry(master=gebruikersnaamLoginFrame, bd=5)
    gebruikersnaamLoginEntry.pack(side = RIGHT)

    gebruikersnaamLabel = Label(master=gebruikersnaamLoginFrame, text="Gebruikersnaam")
    gebruikersnaamLabel.pack(side=LEFT)

    codeLabel = Label(master=codeLoginFrame, text="Code")
    codeLabel.pack(side=LEFT)

    global wachtwoordLoginEntry
    wachtwoordLoginEntry = Entry(master=codeLoginFrame,bd=5)
    wachtwoordLoginEntry.pack(side = RIGHT)

    inlogButton = Button(master=onderLoginFrame,command=loginGebruiker,text='Login',height=3,width=20)
    inlogButton.pack(side=LEFT,pady=4,padx=25)

    terugButton = Button(master=onderLoginFrame,command=vorigMenu,text='Vorig Menu',height=3,width=20)
    terugButton.pack(side=RIGHT,pady=4,padx=25)

def hideLoginMenu(): # verberg het login menu
    bovenLoginFrame.destroy()
    onderLoginFrame.destroy()

def vorigMenu():
    pass

def loginGebruiker():
    if isLoginCorrect(gebruikersnaamLoginEntry.get(),wachtwoordLoginEntry.get()) == True:
        print('U heeft succesvol ingelogd!')
    else:
        print('Uw gegevens zijn onjuist')

# Start the program
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(GPIOLamp,GPIO.OUT)
GPIO.setup(GPIOKnopStart,GPIO.OUT)
GPIO.setup(GPIOKnopStop,GPIO.OUT)

startDatabase(databasename)
showLoginMenu()

var = 0
KnopStart = 0

while True: # Geeft een reactie per 1 seconde
    if var == 0:
        #root.mainloop()
        var = 1
    else:
        if (GPIO.input(GPIOKnopStart) == 1) or KnopStart == 1:
            lampKnipper(1,1)
            KnopStart = 1
        elif (GPIO.input(GPIOKnopStop) == 1):
            GPIO.output(GPIOLamp,GPIO.LOW)
            KnopStart = 0
