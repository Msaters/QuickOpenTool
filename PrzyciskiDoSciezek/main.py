import tkinter as tk
from tkinter import filedialog, Text, messagebox
import os

root = tk.Tk()
apps = []

buttons = []
buttonValues = []
buttonOpenList = []
buttonLocalizationsList = []
buttonCount = 0

#wyciaganie buttonow z txt
if os.path.isfile('buttonLocalizations.txt'):
    with open('buttonLocalizations.txt', 'r') as f:
        tempLocalizations = f.read()
        tempLocalizations = tempLocalizations.split('*')
        Lozalizations = [x for x in tempLocalizations if x.strip()]
        for i in Lozalizations:
            i = i.split(',')
            if (i != ""):
                buttonLocalizationsList.append(i[0])
                buttonLocalizationsList.append(i[1])
                buttonCount += 1

if os.path.isfile('buttonOpenLists.txt'):
    with open('buttonOpenLists.txt', 'r') as f:
        tempOpenLists = f.read()
        tempOpenLists = tempOpenLists.split('*')
        OpenLists = [x for x in tempOpenLists if x.strip()]
        for i in OpenLists:
            print(i)
            if(i != ""):
                buttonOpenList.append(i)

if os.path.isfile('buttonValues.txt'):
    with open('buttonValues.txt', 'r') as f:
        tempValues = f.read()
        tempValues = tempValues.split('*')
        Values = [x for x in tempValues if x.strip()]
        for i in Values :
            i = i.split(',')
            if(i != ""):
                buttonValues.append(i[0])
                buttonValues.append(i[1])

def addApp():

    for widget in frame.winfo_children():
        widget.destroy()

    filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                          filetypes=(("executables", "*exe"), ("siusiak", ".")))
    apps.append(filename)
    for app in apps:
        label = tk.Label(frame, text=app, bg="gray")
        label.pack()

def clearApp():
    global apps
    apps = []
    for widget in frame.winfo_children():
        widget.destroy()

    with open('save.txt', 'w') as f:
        for app in apps:
            f.write(app + ',')

def runApps():
    for app in apps:
        os.startfile(app)

def runAppsWithOpenList(widget):
    list = ""
    for i in range(len(buttons)):
        if (buttons[i] == widget):
            list = buttonOpenList[i]
            break
    print(list)
    if(list =='1'):
        list = ""
    list = list.split(",")
    lapps = [x for x in list if x.strip()]
    for app in lapps:
        print(app)
        os.startfile(app)

def drag_start(event):
    widget = event.widget
    widget.startX = event.x
    widget.startY = event.y

def drag_motion(event):
    widget = event.widget
    zmianaX = True
    zmianaY = True
    x = widget.winfo_x() - widget.startX + event.x
    y = widget.winfo_y() - widget.startY + event.y
    if(x >= 0 and x <= 295):
        zmianaX = True
    else:
        zmianaX = False

    if (y >= 0 and y <= 565):
        zmianaY = True
    else:
        zmianaY = False
    if(zmianaX and zmianaY):
        widget.place(x=x,y=y)
    else :
        if(zmianaX and zmianaY == False):
            widget.place(x = x, y=widget.winfo_y())
        else:
            if (zmianaX == False and zmianaY):
                widget.place(x=widget.winfo_x(), y=y)
            else:
                widget.place(x=widget.winfo_x(), y=widget.winfo_y())

def buttonDestroy(widget):
    global  buttonCount
    j = 0
    for i in range(len(buttons)):
        if(buttons[i] == widget.widget):
            buttons.pop(i)
            break
        j += 1
    buttonOpenList.pop(j)
    buttonValues.pop(j*2)
    buttonValues.pop(j*2)
    buttonCount -= 1
    widget.widget.destroy()

def makeShort():
    frameShort = tk.Frame(root)
    frameShort.place(relwidth=0.6, relheight=0.95, relx=0.02, rely=0.02)
    tk.Label(frameShort, text="QuickPick Button Name").grid(row=0)
    tk.Label(frameShort, text="Color of Button").grid(row=1)
    e1 = tk.Entry(frameShort)
    e2 = tk.Entry(frameShort)
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    def ConfirmButtonChoose():
        global buttonCount
        global apps
        nazwa = e1.get()
        kolor = e2.get()
        openList = ""
        for app in apps:
            openList = openList + app + ","
        try:
            ButtonMade = tk.Button(buttonFrame,text=nazwa, bg=kolor, padx=10, pady=5, fg="white")
        except:
            messagebox.showerror(title = "siusiak", message = "nie poprawnie wpisany kolor")
        ButtonMade.place(relx = 0,rely = 0)
        buttonCount += 1
        buttonValues.append(nazwa)
        buttonValues.append(kolor)
        ButtonMade["command"] = lambda widg=ButtonMade: runAppsWithOpenList(widg)
        ButtonMade.bind("<Button-3>", drag_start)
        ButtonMade.bind("<B3-Motion>", drag_motion)
        ButtonMade.bind("<Button-2>", lambda widg = ButtonMade: buttonDestroy(widg))
        buttons.append(ButtonMade)
        openList = ""
        for app in apps:
            openList = openList + app + ","
        buttonOpenList.append(openList)
        clearApp()
        for widget in frameShort.winfo_children():
            widget.destroy()
        frameShort.destroy()


    Confirm = tk.Button(frameShort, text="Confirm Button", padx=10, pady=5, fg="white", bg="#893E42", command=ConfirmButtonChoose)
    Confirm.place(relx=0.20, rely=0.10)

def OnQuit():
    #localizations
    with open("buttonLocalizations.txt", "w") as f:
        for button in buttons:
            f.write(str(button.winfo_x()) + ",")
            f.write(str(button.winfo_y()) + "*")

    with open("buttonValues.txt", "w") as f:
        i = 1
        for buttonValue in buttonValues:
            f.write(str(buttonValue))
            if(i%2==0):
                f.write("*")
            else:
                f.write(",")
            i += 1

    with open("buttonOpenLists.txt", "w") as f:
        for buttonOpenLis in buttonOpenList:
            if(buttonOpenLis == ""):
                f.write("1")
            f.write(str(buttonOpenLis) + "*")
    root.destroy()

canvas = tk.Canvas(root, height = 700, width= 1200, bg="#263D42")
canvas.pack()

frameShort = tk.Frame(root)

frame = tk.Frame(root)
frame.place(relwidth=0.6, relheight=0.95, relx = 0.02, rely = 0.02)

buttonFrame = tk.Frame(root, bg="#263D42")
buttonFrame.place(relx = 0.65, rely = 0.15, relwidth=0.3, relheight=0.85)

print("tworzenie")
#tworzenie przyciskow z txt
for i in range(buttonCount):
    nazwa = buttonValues[i*2]
    kolor = buttonValues[i*2+1]
    x = int(buttonLocalizationsList[i*2])
    y = int(buttonLocalizationsList[i*2+1])
    ButtonMade = tk.Button(buttonFrame, text=nazwa, bg=kolor, padx=10, pady=5, fg="white")
    ButtonMade["command"] = lambda widg = ButtonMade: runAppsWithOpenList(widg)
    ButtonMade.place(x=x, y=y)
    ButtonMade.bind("<Button-3>", drag_start)
    ButtonMade.bind("<B3-Motion>", drag_motion)
    ButtonMade.bind("<Button-2>", lambda widg=ButtonMade: buttonDestroy(widg))
    buttons.append(ButtonMade)


openFile = tk.Button(root, text="Open File", padx=10, pady=5, fg="white", bg="#453E42", command = addApp)
openFile.place(relx = 0.65,rely = 0.02)

runApps = tk.Button(root, text="Run Apps", padx=10, pady=5, fg="white", bg="#453E42", command=runApps)
runApps.place(relx = 0.75,rely = 0.02)

clearApps = tk.Button(root, text="Clear App List", padx=10, pady=5, fg="white", bg="#453E42", command=clearApp)
clearApps.place(relx = 0.75,rely = 0.1)

makeShort = tk.Button(root, text="Make Own QuickPick Button", padx=10, pady=5, fg="white", bg="#453E42", command=makeShort)
makeShort.place(relx = 0.84,rely = 0.02)

for app in apps:
     Label = tk.Label(frame, text=app)

root.protocol("WM_DELETE_WINDOW", OnQuit)
root.mainloop()
