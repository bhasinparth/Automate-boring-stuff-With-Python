from tkinter import *
import re
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
import pandas
import html5lib

#class for AutocompleteEntry
class AutocompleteEntry(Entry):
    def __init__(self, autocompleteList, *args, **kwargs):

        # Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        # Custom matches function
        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def matches(fieldValue, acListEntry):
                pattern = re.compile('.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
                return re.match(pattern, acListEntry)

            self.matchesFunction = matches


        Entry.__init__(self, *args, **kwargs)
        self.focus()

        self.autocompleteList = autocompleteList

        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)

        self.listboxUp = False

    def changed(self, name, index, mode):
        if self.var.get() == '':
            if self.listboxUp:
                self.listbox.destroy()
                self.listboxUp = False
        else:
            words = self.comparison()
            if words:
                if not self.listboxUp:
                    self.listbox = Listbox(width=self["width"], height=self.listboxLength)
                    self.listbox.bind("<Button-1>", self.selection)
                    self.listbox.bind("<Right>", self.selection)
                    self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.listboxUp = True

                self.listbox.delete(0, END)
                for w in words:
                    self.listbox.insert(END,w)
            else:
                if self.listboxUp:
                    self.listbox.destroy()
                    self.listboxUp = False

    def selection(self, event):
        if self.listboxUp:
            self.var.set(self.listbox.get(ACTIVE))
            self.listbox.destroy()
            self.listboxUp = False
            self.icursor(END)

    def moveUp(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            if index != '0':
                self.listbox.selection_clear(first=index)
                index = str(int(index) - 1)

                self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def moveDown(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]

            if index != END:
                self.listbox.selection_clear(first=index)
                index = str(int(index) + 1)

                self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def comparison(self):
        return [ w for w in self.autocompleteList if self.matchesFunction(self.var.get(), w) ]

if __name__ == '__main__':

    #for getting list of airports
    url="https://en.wikipedia.org/wiki/List_of_international_airports_by_country"
    table=pandas.read_html(url)
    maindf=pandas.DataFrame()
    for x in range(62):
        newdf=pandas.DataFrame()
        newdf["Place"]=table[x][0]
        newdf["Airport"]=table[x][1]
        newdf["Code"]=table[x][2]
        maindf=maindf.append(newdf)

    maindf=maindf.dropna(how='any')
    to_drop=['Location']
    maindf=maindf[~maindf['Place'].isin(to_drop)]
    maindf=maindf.reset_index(drop=True)

#flight code options
    autocompleteList = (maindf['Place']+" ("+maindf['Airport']+")"+"-"+maindf['Code']).tolist()
    eco=["ECONOMY","BUSINESS"]

    def matches(fieldValue, acListEntry):
        pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
        return re.match(pattern, acListEntry)

    window=Tk()
    stdate=" "
    eddate=" "
    adult=0
    kid=0
    infant=0
    flightcode=" "
    def inputs():
        stdate=(e1_val.get())
        eddate=(e2_val.get())
        adult=(adu_val.get())
        kid=(chi_val.get())
        infant=(inf_val.get())
        starting=(entry.get())
        ending=(entryss.get())
        ecobu=(ecobus.get())
        binary = FirefoxBinary('C:\Program Files\Mozilla Firefox\Firefox.exe')
        browser = webdriver.Firefox(firefox_binary=binary)
        url='https://in.via.com/flight/search?numAdults='+adult+'&numChildren='+kid+'&numInfants='+infant+'&flightClass='+ecobu+'&routingType=ALL&source='+starting[-3:]+'&destination='+ending[-3:]+'&month='+stdate[3:5]+'&day='+stdate[0:2]+'&year='+stdate[-4:]+'&month2='+eddate[3:5]+'&day2='+eddate[0:2]+'&year2='+eddate[-4:]+'&returnType=return&utm_campaign='+starting[-3:]+'-'+ending[-3:]+'&currency=INR'
# mmt domestic       'https://flights.makemytrip.com/makemytrip/search/R/R/'+ecobu[0]+'/'+str(adult)+'/'+str(kid)+'/'+str(infant)+'/S/V0/'+starting[-3:]+'_'+ending[-3:]+'_'+stdate+','+ending[-3:]+'_'+starting[-3:]+'_'+eddate
# mmt international  https://www.makemytrip.com/air/search?tripType=R&itinerary=JFK-LHR-D-27Aug2017_LHR-JFK-D-05Sep2017&paxType=A-4&cabinClass=E
        browser.get(url)
        time.sleep(2)
        browser.find_element_by_link_text('Book').click()

    Label(window, text="(DD-MM-YYYY)").grid(row=0,column=1)
    Label(window, text="Start Date").grid(row=1)
    Label(window, text="End Date").grid(row=2)
    Label(window, text="Adult 12+").grid(row=3)
    Label(window, text="Child 2-12").grid(row=4)
    Label(window, text="Infant 0-2").grid(row=5)
    Label(window, text="Starting Station").grid(row=6)
    Label(window, text="Ending Station").grid(row=7)

#startdate
    e1_val=StringVar()
    e1=Entry(window,textvariable=e1_val)
    e1.grid(row=1,column=1)

#enddate
    e2_val=StringVar()
    e2=Entry(window,textvariable=e2_val)
    e2.grid(row=2,column=1)

#number of adults
    adu_val=StringVar()
    adu_val.set(1)
    adu=Entry(window,textvariable=adu_val)
    adu.grid(row=3,column=1)

#number of children
    chi_val=StringVar()
    chi_val.set(0)
    chi=Entry(window,textvariable=chi_val)
    chi.grid(row=4,column=1)

#number of infant
    inf_val=StringVar()
    inf_val.set(0)
    inf=Entry(window,textvariable=inf_val)
    inf.grid(row=5,column=1)

#flight code
#variable.set(OPTIONS[0]) # default value
#w = OptionMenu(window ,variable ,*OPTIONS)
#w.grid(row=6,column=1)
    entry = AutocompleteEntry(autocompleteList, window, listboxLength=6, width=64, matchesFunction=matches)
    entry.grid(row=6, column=1)

    entryss = AutocompleteEntry(autocompleteList, window, listboxLength=6, width=64, matchesFunction=matches)
    entryss.grid(row=7, column=1)

#business or economy
    ecobus = StringVar()
    ecobus.set(eco[0]) # default value
    ee = OptionMenu(window ,ecobus ,*eco)
    ee.grid(row=8,column=1)


#submit button
    b1=Button(window,text="Submit",command=inputs)
    b1.grid(row=9,column=0)

    window.mainloop()
