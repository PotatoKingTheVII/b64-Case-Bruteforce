from tkinter import scrolledtext
from tkinter import *
import itertools as it
import base64
import math


####Define functions####
#Return true if the b64 decoded only contains ascii from range 32 to 126
def isValidb64(b64):
    decoded = base64.b64decode(b64)
    for i in range(0,len(decoded)):
        if(decoded[i]<32 or decoded[i] > 126):
            return False    #Current letter is outside range, fail
    return True #All letters have passed and are valid

def base64CaseCombos(b64input):
    ##Make sure b64 is padded to a multiple of 4 and split up into a list of 4 chunks
    chunkList = []
    b64length = len(b64input)

    #Pad to multiple of 4 with =
    b64input = b64input.ljust( (math.ceil(b64length/4))*4 ,"=")

    #Create list of all 4 chunks
    for i in range(0,b64length,4):
        chunkList.append(b64input[i:i+4])

    #Loop through each chunks combinations checking for all valid cases
    possibleB64 = []
    for chunk in chunkList:
        chunkPossibilities = []
        comboList = list(map(''.join, it.product(*zip(chunk.upper(), chunk.lower())))) #Make list of all case combos
        comboList = list(dict.fromkeys(comboList))  #Remove repeats due to non alphabetic characters
        comboList.reverse() #Reverse to check lower values first, more likely to be the proper result

        for combo in comboList: #Check all case combos for the current chunk till a valid one then add it to the result
            if(isValidb64(combo)):
                chunkPossibilities.append(base64.b64decode(combo).decode("utf-8"))
        possibleB64.append(chunkPossibilities)
    return possibleB64


#Actually split up the base64 into all possible chunks and make list boxes for each        
def BcalcB64():
    inputText = (ciphertextTXT.get("1.0",'end-1c'))
    combos = base64CaseCombos(inputText)
    global buttonList
    buttonList = []
    for i in range(0,len(combos)):
        #Calculate grid pos
        x = (i%11)+0
        y = (i//11)+0
        currentCombo = combos[i]
        buttonList.append(Listbox(BottomIO,width=8, height=2,exportselection=False))
        buttonList[i].bind("<Button-1>", lambda x:combineResults())
        buttonList[i].bind("<MouseWheel>", on_mousewheel)
        for specificPerm in currentCombo:
            buttonList[i].insert(END, specificPerm)                           
            buttonList[i].grid(column=x, row=y,sticky=W)
            buttonList[i].select_set(0)
            buttonList[i]['highlightbackground']='#212121'
            buttonList[i]['selectbackground']='#212121'
            
    combineResults()    #Call so we actully display the inital state text
    return


#Combine current selection of all listboxes and write to plaintext
#Anytime one is changed or if bruteforce first clicked
def combineResults():
    CurrentSrollPos = plaintextTXT.yview()
    finalResult = ""
    for listChoice in buttonList:
        try:
            choiceValueINDEX = (listChoice.curselection())
            choiceValue = listChoice.get(choiceValueINDEX)
            if(choiceValue):
                finalResult += choiceValue
        except:
            pass


    plaintextTXT.delete(1.0, 'end-1c')
    plaintextTXT.insert('end-1c', finalResult)

    #To stop the scroll pos being reset after writing to it
    plaintextTXT.yview_moveto(CurrentSrollPos[0])

    return

#For scrolling bottom window if not on scrollbar itself
def on_mousewheel(event):
    BottomIOCanvas.yview_scroll(int(-1*(event.delta/100)),"units")
    BottomIOCanvas.focus_set()



####GUI Code####
####Initalise window####
window = Tk()
window.title("B64 Bruteforce")
window.geometry('650x700')


####Create sections and layout format####
TopIO = Frame(window)
TopIO.grid(row=0, column=0, sticky='nsew')
BottomIOCanvas = Canvas(window,width=567, height=200)
BottomIOCanvas.grid(row=1,column=0,sticky="W", padx=20, pady=20)
BottomIO = Frame(BottomIOCanvas)


#Create scrollbar for bottom part
vbar = Scrollbar(window, orient=VERTICAL)
vbar.config(command=BottomIOCanvas.yview)
vbar.grid(row=1,column=1,sticky="NSW")
BottomIOCanvas.config(yscrollcommand=vbar.set)
BottomIOCanvas.create_window((0, 0), window=BottomIO, anchor="nw")  #Put frame in as window

#Setup the visible window for scrolling
BottomIO.bind(
    "<Configure>",
    lambda e: BottomIOCanvas.configure(
        scrollregion=BottomIOCanvas.bbox("all")
    )
)

#Setup general scroll lookout if not actually on the scrollbar
BottomIOCanvas.bind("<MouseWheel>", on_mousewheel)
BottomIO.bind("<MouseWheel>", on_mousewheel)


####Section Styling####
window['highlightcolor']='#212121'
window['background']='#212121'
TopIO['background']='#212121'
BottomIO['background']='#212121'
BottomIOCanvas['background']='#212121'


####Labels####
plaintextLBL = Label(TopIO, text="Plaintext")
plaintextLBL.grid(column=0, row=3)
plaintextLBL['background']='#212121'
plaintextLBL['foreground']='#FFFFFF'

ciphertextLBL = Label(TopIO, text="Ciphertext")
ciphertextLBL.grid(column=0, row=0)
ciphertextLBL['background']='#212121'
ciphertextLBL['foreground']='#FFFFFF'


####Textboxes####
ciphertextTXT = scrolledtext.ScrolledText(TopIO,width=70,height=10)
ciphertextTXT.grid(column=0,row=1, padx=20, pady=5)
ciphertextTXT['background']='#2e2e2e'
ciphertextTXT['foreground']='#bfbfbf'

plaintextTXT = scrolledtext.ScrolledText(TopIO,width=70,height=10)
plaintextTXT.grid(column=0,row=4, padx=20, pady=5)
plaintextTXT['background']='#2e2e2e'
plaintextTXT['foreground']='#afafaf'

####Buttons####
calcB64input = Button(TopIO,height=1, pady=5, text="Bruteforce", command=lambda:BcalcB64())
calcB64input.grid(column=0,row=2, padx=20)
calcB64input['background']='#545454'
calcB64input['foreground']='#efefef'


window.mainloop()
