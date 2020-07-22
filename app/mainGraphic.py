import tkinter as tk
from tkinter import font as font
from tkinter import ttk
from tkinter import messagebox as tkmsg
import workerHour as wh
import mailHour as mh
import cityMG as cm
import sys
import time
import genLib as gl
import subprocess
import os
import workerName as wn
import user

class mainGraphic :

    def __init__(self):
        self.width=1900
        self.height=950
        self.fileWorkerHourPath = "./dataBase/workerHour.csv" #includes name, first name, date and number of hours work
        self.fileMGPath = "./dataBase/mg.csv" #includes name of city and this MG (kilometer allowance)
        self.fileSendHourPath = "./html/sendHour.html" #includes the file to send with worker name and forstname, date, number of hours work and MG (in html)
        self.fileUserPath = "./user/user.csv" #includes user password and email of client
        self.scriptPath = "./app/scriptSendMail.py" #the programme that send the file in html by email
        self.fileCssPath = "./html/style.css" #the cs of html file to send
        self.fileWorkerNamePath = "./dataBase/workerName.csv" #includes name and firstname of all workers
        if sys.platform != 'linux' : #if os is window, paths are different
            self.height=600
            self.fileWorkerHourPath = "." + self.fileWorkerHourPath
            self.fileMGPath = "." + self.fileMGPath
            self.fileSendHourPath = "." + self.fileSendHourPath
            self.fileUserPath = "." + self.fileUserPath
            self.scriptPath = "." + self.scriptPath
            self.fileCssPath = "." + self.fileCssPath
            self.fileWorkerNamePath = "." + self.fileWorkerNamePath
        self.window = tk.Tk(className="Horaires")
        self.window.geometry(str(self.width) + "x" + str(self.height+15))
        self.listbox = tk.Listbox(self.window)
        #label and input
        #worker name
        self.labelWorkerName = tk.Label(self.window, text="Nom de l'ouvrier : ")
        self.valueWorkerName = tk.StringVar()
        self.inputWorkerName = tk.Entry(self.window, textvariable=self.valueWorkerName)
        #worker first name
        self.labelWorkerFirstName = tk.Label(self.window, text="Prénom de l'ouvrier : ")
        self.valueWorkerFirstName = tk.StringVar()
        self.inputWorkerFirstName = tk.Entry(self.window, textvariable=self.valueWorkerFirstName)
        #arriving time
        self.labelArrivingTime = tk.Label(self.window, text="Heure d'arrivée (en heure) : ")
        self.valueArrivingTime = tk.StringVar()
        self.inputArrivingTime = tk.Entry(self.window, textvariable=self.valueArrivingTime)
        #meal
        self.labelMeal = tk.Label(self.window, text="Repas (en minute) : ")
        self.valueMeal = tk.StringVar()
        self.inputMeal= tk.Entry(self.window, textvariable=self.valueMeal)
        #departure time
        self.labelDepartureTime = tk.Label(self.window, text="Heure de départ (en heure) : ")
        self.valueDepartureTime = tk.StringVar()
        self.inputDepartureTime = tk.Entry(self.window, textvariable=self.valueDepartureTime)
        #city
        self.labelCity = tk.Label(self.window, text="Lieu du chantier : ")
        self.valueCity = tk.StringVar()
        self.inputCity = tk.Entry(self.window, textvariable=self.valueCity)
        #MG
        self.labelMG = tk.Label(self.window, text="MG : ")
        self.valueMG = tk.StringVar()
        self.inputMG = tk.Entry(self.window, textvariable=self.valueMG)
        #date
        self.labelDate = tk.Label(self.window, text="Date (sous le format aaaa-mm-jj) : ")
        self.valueDate = tk.StringVar()
        self.inputDate = tk.Entry(self.window, textvariable=self.valueDate)
        #combobox to facilitate the choice
        self.comboWorkerName = ttk.Combobox(self.window)
        self.comboWorkerFistName = ttk.Combobox(self.window)
        self.comboCity = ttk.Combobox(self.window)
        #button
        self.buttonAddHour = tk.Button(self.window, text="Ajouter les heures", command=self.addHour)
        self.buttonAddMG = tk.Button(self.window, text="Ajouter la ville et ses MG", command=self.addCity)
        self.buttonEditHour = tk.Button(self.window, text="Editer les horaires", command=self.editHour)
        self.closeButton = tk.Button(self.window, text="Fermer", command=self.close)
        self.buttonAddWorker = tk.Button(self.window, text="Ajouter l'ouvrier", command=self.addWorker)
        self.buttonRemoveWorker = tk.Button(self.window, text="Supprimer l'ouvrier", command=self.removeWorker)
        #password button (all actions need password)
        self.buttonEditPassWord = tk.Button(self.window, text="Changer le mot de passe", command=self.editPassWord)
        self.buttonCheckPassWordEditPassWord = tk.Button(self.window, text="Valider", command=self.checkPassWordEditPassWord)
        self.buttonCheckPassWordEditHour = tk.Button(self.window, text="Valider", command=self.checkPassWordEditHour)
        self.buttonCheckPassWordAddMG = tk.Button(self.window, text="Valider", command=self.checkPassWordAddMG)
        self.buttonCheckPassWordEditEmail = tk.Button(self.window, text="Valider", command=self.checkPassWordEditEMail)
        self.buttonEditEmail = tk.Button(self.window, text="Changer le mail", command=self.editEmail)
        self.buttonCheckPassWordAddWorker = tk.Button(self.window, text="Valider", command=self.checkPassWordAddWorker)
        self.buttonCheckPassWordRemoveWorker = tk.Button(self.window, text="Valider", command=self.checkPassWordRemoveWorker)
        #password
        self.password = gl.getLinesOfFile(self.fileUserPath)[0][0:-1]
        self.labelPassWord = tk.Label(self.window, text="Mot de passe : ")
        self.valuePassWord = tk.StringVar()
        self.inputPassWord = tk.Entry(self.window, textvariable=self.valuePassWord, exportselection=0, show="*")
        self.inputPassWordWhitoutStars = tk.Entry(self.window, textvariable=self.valuePassWord, exportselection=0)
        #email
        self.email = gl.getLinesOfFile(self.fileUserPath)[1]
        self.labelEmail= tk.Label(self.window, text="Email : ")
        self.valueEMail = tk.StringVar()
        self.inputEmail = tk.Entry(self.window, textvariable=self.valueEMail, exportselection=0)

    def main(self) :
        """
        the main function, thaht lunch all of features.
        add, show, edit work hours.
        add city and this MG. (kilometer allowance)
        edit password, email.
        add, remove worker.
        """
        subprocess.Popen(["python3", self.scriptPath, "&"]) #to send the mail (call from another program which takes care of everything)
        self.listbox.config( width = '27', height = str(self.listbox.size()))
        self.listbox['font'] = font.Font(size=20)
        self.listbox.pack()
        self.listbox.insert(tk.END, "Ajouter un horaire ")
        self.listbox.insert(tk.END, "Voir les horaires")
        self.listbox.insert(tk.END, "Modifier les horaires d'un ouvrier")
        self.listbox.insert(tk.END, "Ajouter une ville et ses MG")
        self.listbox.insert(tk.END, "Changer le mot de passe")
        self.listbox.insert(tk.END, "Mot de passe oublié")
        self.listbox.insert(tk.END, "Changer l'email")
        self.listbox.insert(tk.END, "Ajouter un ouvrier" )
        self.listbox.insert(tk.END, "Supprimer un ouvrier")
        self.listbox.bind("<<ListboxSelect>>", self.choose)
        self.window.mainloop()

    def choose(self, event):
        """
        choose the good feature with the good click.
        """
        if self.listbox.curselection() != () :
            choice = self.listbox.curselection()[0]
            if choice == 0 :
                self.showAddHour()
            elif choice == 1 :
                self.showHours()
            elif choice == 2 :
                self.showPassWordEditHour()
            elif choice == 3 :
                self.showPassWordAddMG()
            elif choice == 4 :
                self.showPassWordEditPassWord()
            elif choice == 5 :
                self.showForgetPassWord()
            elif choice == 6 :
                self.showPassWordEditMail()
            elif choice == 7 :
                self.showPassWordAddWorker()
            elif choice == 8 :
                self.showPassWordRemoveWorker()
            
    def upSize(self) :
        """
        up the size of the element in the window.
        """
        listOfSize = ["Button", "Label", "Entry", "ttk"]
        children = self.window.winfo_children()
        for e in children :
            t = str(type(e)).split(".")[1].split("'")[0]
            if t in listOfSize :
                e['font'] = font.Font(size=15)

    def close(self) :
        """
        do 'pack_forget' to hide all elements in the window. 
        """
        children = self.window.winfo_children()
        for e in children :
            e.pack_forget()
        self.listbox.pack()

    def packForgetListBoxAndUpSize(self) :
        """
        do self.upSize() and hide the listbox.
        """
        self.listbox.pack_forget()
        self.upSize()

    def lineBreak(self) :
        """
        pack a line break to space out.
        """
        tk.Label(self.window, text="").pack()

    def checkStateError(self, state) :
        """
        check the state to show error and correct them.
        """
        #errors :
        if state == "name" : #empty name
            tkmsg.showerror("Erreur ", "Nom vide") 
        elif state == "firstname" : #empty firstname.
            tkmsg.showerror("Erreur ", "Prénom vide")
        elif state == "arriving" : #empty arriving time.
            tkmsg.showerror("Erreur ", "Heure d'arrivée vide")
        elif state == "departure" : #empty departure time.
            tkmsg.showerror("Erreur ", "Heure de départ vide")
        elif state == "meal" : #empty meal time.
            tkmsg.showerror("Erreur ", "Heure de repas vide")
        elif state == "city" : #empty city.
            tkmsg.showerror("Erreur ", "Ville vide")
        elif state == "add" or state == "remove": #worker not found to add work hours or remove him.
            tkmsg.showerror("Erreur ", "Ouvrier non trouvé")
        elif state == "errorHourBegin" : #invalid arriving time.
            tkmsg.showerror("Erreur ", "Heure d'arrivée invalide")
        elif state == "errorHourEnd" : #invalid departure time.
            tkmsg.showerror("Erreur ", "Heure de départ invalide")
        elif state == "errorMinute" : #invalid meal time.
            tkmsg.showerror("Erreur ", "Temps de repas invalide")
        elif state == "errorSameDate" : #work hours already save for this date.
            tkmsg.showerror("Erreur ", "Horaires déjà enregistrés aujourd'hui")
        elif state == "edit" : ##worker not found to edit work hours or date not found.
            tkmsg.showerror("Erreur ", "Ouvrier ou date non trouvé")
        elif state == "date" : #empty date.
            tkmsg.showerror("Erreur ", "Date vide")
        elif state == "mg" : #empty MG. 
            tkmsg.showerror("Erreur ", "MG vide")
        elif state == "mg," : #MG with comma.
            tkmsg.showerror("Erreur ", "Mettre un point pour les MG, pas de virgule (ex : 4.5)")
        elif state == "errorMG" : #invalid MG.
            tkmsg.showerror("Erreur ", "MG invalide")
        elif state == "double" : #already save tuple name and firstname.
            tkmsg.showerror("Erreur ", "Ouvrier déjà ajouté")
        #ok :
        elif state == "okAddHour" : #work hours added.
            tkmsg.showinfo("OK", "Horaires ajoutés")
        elif state == "okEditWorker" : #work hours edited.
            tkmsg.showinfo("OK", "Horaires edités")
        elif state == "okAddCity" : #city added.
            tkmsg.showinfo("OK ", "Ville ajoutée")
        elif state == "okAddWorker" : #worker added.
            tkmsg.showinfo("Ok ", "Ouvrier ajouté")
        elif state == "okRemoveWorker" : #worker removed.
            tkmsg.showinfo("Ok ", "Ouvrier supprimé")

#add work hours :
    def showAddHour(self) :
        """
        show elements to add work hours.
        (name, firstname, arriving time, meal time, departure time, city, button to add and to close).
        """
        self.packForgetListBoxAndUpSize()
        self.labelWorkerName.pack()
        self.comboWorkerName['values'] = gl.notDoubleInListAndSort(wn.takeValuesCombobox(0, self.fileWorkerNamePath))
        self.comboWorkerName.pack()
        self.lineBreak()
        self.labelWorkerFirstName.pack()
        self.comboWorkerFistName['values'] = gl.notDoubleInListAndSort(wn.takeValuesCombobox(1, self.fileWorkerNamePath))
        self.comboWorkerFistName.pack()
        self.lineBreak()
        self.labelArrivingTime.pack()
        self.inputArrivingTime.pack()
        self.lineBreak()
        self.labelDepartureTime.pack()
        self.inputDepartureTime.pack()
        self.lineBreak()
        self.labelMeal.pack()
        self.inputMeal.pack()
        self.lineBreak()
        self.labelCity.pack()
        self.comboCity['values'] = wn.takeValuesCombobox(0, self.fileMGPath)
        self.comboCity.pack()
        self.lineBreak()
        self.buttonAddHour.pack()
        self.lineBreak()
        self.closeButton.pack()

    def addHour(self) :
        """
        add work hours in the database.
        take the name, firstname, arriving time, meal time, departure time, city, get the day and write them on the databse.
        """
        workerName = self.comboWorkerName.get().strip()
        workerFirstName = self.comboWorkerFistName.get().strip()
        workerArrivingTime = self.valueArrivingTime.get().strip()
        workerDepartureTime = self.valueDepartureTime.get().strip()
        workerMeal = self.valueMeal.get().strip()
        workerCity = self.comboCity.get().strip()
        state = wh.addWorkerDataBase(workerName.upper(), workerFirstName.capitalize(), workerArrivingTime, workerDepartureTime, workerMeal, workerCity.upper(), self.fileWorkerHourPath, self.fileMGPath)
        self.checkStateError(state)

#show work Hours :
    def showHours(self) :
        """
        call the function that show work hours. (open webbrowser and the file to send by email).
        """
        mh.hoursDataBase(self.fileWorkerHourPath, self.fileSendHourPath, self.fileCssPath)
    
##feature that need password :
    def showPassWord(self) :
        """
        show elements to take password and check it.
        (password input).
        """
        self.packForgetListBoxAndUpSize()
        self.labelPassWord.pack()
        self.inputPassWord.pack()
        self.lineBreak()

    def checkPassWord(self) :
        """
        check the password. if is good, return true. false for otherwise.
        """
        pw = self.valuePassWord.get().strip()
        self.valuePassWord.set("") #to hide password
        if pw == self.password :
            self.close()
            return True
        else :
            return False

#edit work hours :
    def showPassWordEditHour(self) :
        """
        show elements to take password and check it to edit work hours.
        (button to ckeck and to close).
        """
        self.showPassWord()
        self.buttonCheckPassWordEditHour.pack()
        self.lineBreak()
        self.closeButton.pack()
    
    def checkPassWordEditHour(self) :
        """
        check the password. if is good, show elements to edit work hours.
        """
        if self.checkPassWord() :
            self.showEditWorkHours()
        else :
            tkmsg.showerror("Erreur ", "Mot de passe incorrect")

    def showEditWorkHours(self) :
        """
        show elements to edit work hours.
        (name, firstname, date, arriving time, meal time, departure time, button to edit and to close).
        """
        self.packForgetListBoxAndUpSize()
        self.labelWorkerName.pack()
        self.comboWorkerName['values'] = gl.notDoubleInListAndSort(wn.takeValuesCombobox(0, self.fileWorkerNamePath))
        self.comboWorkerName.pack()
        self.lineBreak()
        self.labelWorkerFirstName.pack()
        self.comboWorkerFistName['values'] = gl.notDoubleInListAndSort(wn.takeValuesCombobox(1, self.fileWorkerNamePath))
        self.comboWorkerFistName.pack()
        self.lineBreak()
        self.labelDate.pack()
        self.inputDate.pack()
        self.lineBreak()
        self.labelArrivingTime.pack()
        self.inputArrivingTime.pack()
        self.lineBreak()
        self.labelDepartureTime.pack()
        self.inputDepartureTime.pack()
        self.lineBreak()
        self.labelMeal.pack()
        self.inputMeal.pack()
        self.lineBreak()
        self.buttonEditHour.pack()
        self.lineBreak()
        self.closeButton.pack()

    def editHour(self) : 
        """
        edit work hour in the database.
        take name, firstname, arriving time, meal time departure time and write them on the database.
        """
        workerName = self.comboWorkerName.get().strip()
        workerFirstName = self.comboWorkerFistName.get().strip()
        workerArrivingTime = self.valueArrivingTime.get().strip()
        workerDepartureTime = self.valueDepartureTime.get().strip()
        workerMeal = self.valueMeal.get().strip()
        editDate = self.valueDate.get().strip()
        state = wh.editWorkerDataBase(workerName.upper(), workerFirstName.capitlize(), workerArrivingTime, workerDepartureTime, workerMeal, editDate, self.fileWorkerHourPath)
        self.checkStateError(state)

#add city and this MG :
    def showPassWordAddMG(self) :
        """
        show elements to take password and check it to add city and this MG.
        (button to ckeck and to close).
        """
        self.showPassWord()
        self.buttonCheckPassWordAddMG.pack()
        self.lineBreak()
        self.closeButton.pack()

    def checkPassWordAddMG(self) :
        """
        check the password. if is good, show elements to add city and this MG.
        """
        if self.checkPassWord() :
            self.showAddCity()
        else :
            tkmsg.showerror("Erreur ", "Mot de passe incorrect")

    def showAddCity(self) :
        """
        show elements to add city and this MG.
        (city, MG, button to add and to close).
        """
        self.packForgetListBoxAndUpSize()
        self.labelCity.pack()
        self.inputCity.pack()
        self.lineBreak()
        self.labelMG.pack()
        self.inputMG.pack()
        self.lineBreak()
        self.buttonAddMG.pack()
        self.lineBreak()
        self.closeButton.pack()

    def addCity(self) :
        """
        dd work hour in the database.
        take the city and this MG and write them on the database.
        """
        city = self.valueCity.get().strip()
        mg = self.valueMG.get().strip()
        state = cm.addCityDataBase(city.upper(), mg, self.fileMGPath)
        self.checkStateError(state)

#edit password :
    def showPassWordEditPassWord(self) :
        """
        show elements to take password and check it to edit password.
        (button to ckeck and to close).
        """
        self.showPassWord()
        self.buttonCheckPassWordEditPassWord.pack()
        self.lineBreak()
        self.closeButton.pack()

    def checkPassWordEditPassWord(self) :
        """
        check the password. if is good, show elements to edit password.
        """
        if self.checkPassWord() :
            self.showEditPassWord()
        else :
            tkmsg.showerror("Erreur ", "Mot de passe incorrect")

    def showEditPassWord(self) :
        """
        show elements to edit password.
        (old password, new password, button to add and to close).
        """
        tk.Label(self.window, text="Ancien mot de passe : " + self.password).pack()
        self.lineBreak()
        self.packForgetListBoxAndUpSize()
        self.labelPassWord.pack()
        self.inputPassWordWhitoutStars.pack()
        self.lineBreak()   
        self.buttonEditPassWord.pack()
        self.lineBreak()
        self.closeButton.pack()

    def editPassWord(self) :
        """
        edit the password. (write on the database the new password).
        """
        pw = self.valuePassWord.get().strip()
        self.valuePassWord.set("") #to hide password
        if pw == "" :
            tkmsg.showerror("Erreur ", "Mot de passe vide")
        else :
            self.password = pw
            gl.writeInFile(self.fileUserPath, self.password + "\n" + self.email)
            tkmsg.showinfo("Ok ", "Mot de passe changé en : " + pw)
    
#forget password :
    def showForgetPassWord(self) :
        """
        call the function that send email with the old password.
        """
        tkmsg.showinfo("Ok ", "Votre mot de passe a été envoyé à l'adresse mail enregistré")
        user.sendMailForgetPassWord(self.email, self.password)

#edit email
    def showPassWordEditMail(self) :
        """
        show elements to take password and check it to edit email.
        (button to ckeck and to close).
        """
        self.showPassWord()
        self.buttonCheckPassWordEditEmail.pack()
        self.lineBreak()
        self.closeButton.pack()

    def checkPassWordEditEMail(self) :
        """
        check the password. if is good, show elements to edit email.
        """
        if self.checkPassWord() :
            self.showEditEmail()
        else :
            tkmsg.showerror("Erreur ", "Mot de passe incorrect")

    def showEditEmail(self) :
        """
        show elements to edit email.
        (old email, new email, button to add and to close).
        """
        if self.email.strip() == "" :
            tk.Label(self.window, text="Aucun mail enregistré").pack()
        else :
            tk.Label(self.window, text="Mail enregistré : " + self.email).pack()
        self.packForgetListBoxAndUpSize()
        self.lineBreak()
        self.labelEmail.pack()
        self.inputEmail.pack()
        self.lineBreak()
        self.buttonEditEmail.pack()
        self.lineBreak()
        self.closeButton.pack()

    def editEmail(self) :
        """
        edit the email. (write on the database the new email).
        """
        email = self.valueEMail.get().strip()
        if email == "" :
            tkmsg.showerror("Erreur ", "Mail vide")
        else :
            self.email = email
            gl.writeInFile(self.fileUserPath, self.password + "\n" + self.email)
            tkmsg.showinfo("Ok ", "Mail changé en : " + email)
    
#add worker
    def showPassWordAddWorker(self) :
        """
        show elements to take password and check it to add worker.
        (button to ckeck and to close).
        """
        self.showPassWord()
        self.buttonCheckPassWordAddWorker.pack()
        self.lineBreak()
        self.closeButton.pack()

    def checkPassWordAddWorker(self) :
        """
        check the password. if is good, show elements to add worker.
        """
        if self.checkPassWord() :
            self.showAddWorker()
        else :
            tkmsg.showerror("Erreur ", "Mot de passe incorrect")
        
    def showAddWorker(self) :
        """
        show elements to add worker.
        (name, firstname, button to add and to close).
        """
        self.packForgetListBoxAndUpSize()
        self.labelWorkerName.pack()
        self.inputWorkerName.pack()
        self.lineBreak()
        self.labelWorkerFirstName.pack()
        self.inputWorkerFirstName.pack()
        self.lineBreak()
        self.buttonAddWorker.pack()
        self.lineBreak()
        self.closeButton.pack()

    def addWorker(self) :  
        """
        add worker in the database.
        take the name, firstname, and write them on the databse.
        """
        workerName = self.valueWorkerName.get().strip()
        workerFirstName = self.valueWorkerFirstName.get().strip()
        state = wn.addWorkerNameDataBase(workerName.upper(), workerFirstName.capitalize(), self.fileWorkerNamePath, self.fileWorkerHourPath)
        self.checkStateError(state)

#remove worker :
    def showPassWordRemoveWorker(self) :
        """
        show elements to take password and check it to remove worker.
        (button to ckeck and to close).
        """
        self.showPassWord()
        self.buttonCheckPassWordRemoveWorker.pack()
        self.lineBreak()
        self.closeButton.pack()

    def checkPassWordRemoveWorker(self) :
        """
        check the password. if is good, show elements to remove worker.
        """
        if self.checkPassWord() :
            self.showRemoveWorker()
        else :
            tkmsg.showerror("Erreur ", "Mot de passe incorrect") 

    def showRemoveWorker(self) :
        """
        show elements to remove worker.
        (name, firstname, button to add and to close).
        """
        self.packForgetListBoxAndUpSize()
        self.labelWorkerName.pack()
        self.comboWorkerName['values'] = gl.notDoubleInListAndSort(wn.takeValuesCombobox(0, self.fileWorkerNamePath))
        self.comboWorkerName.pack()
        self.lineBreak()
        self.labelWorkerFirstName.pack()
        self.comboWorkerFistName['values'] = gl.notDoubleInListAndSort(wn.takeValuesCombobox(1, self.fileWorkerNamePath))
        self.comboWorkerFistName.pack()
        self.lineBreak()
        self.buttonRemoveWorker.pack()
        self.lineBreak()
        self.closeButton.pack()

    def removeWorker(self) :  
        """
        remove worker in the database.
        take the name, firstname, and remove them of the databse.
        """
        workerName = self.comboWorkerName.get().strip()
        workerFirstName = self.comboWorkerFistName.get().strip()
        state = wn.removeWorkerNameDataBase(workerName.upper(), workerFirstName.capitalize(), self.fileWorkerNamePath)
        self.checkStateError(state)

#lunch main
mainGraphic().main()