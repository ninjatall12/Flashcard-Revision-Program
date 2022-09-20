#Importing the required libraries for the project
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import textwrap
import re
import os
import csv
import random
#This is the class that holds the first program for my application.
class Flashcardwindow():
#This is the initialisation for the widgets on the mainwindow
    def __init__(self):
        #This is a boolean that is used for determining if the subjectfolder is created
        self.subjectsfoldercreated=False
        #This variable holds the path in which the program is in
        self.path=os.getcwd()
        #This is a list that holds of the names of files in the directory where this program is stored
        self.directories=os.listdir(self.path)
        #This branch checks if the Subjects folder exists and sets boolean value to True if it does.
        for filename in self.directories:
            if filename == "Subjects":
                self.subjectsfoldercreated=True             
        #This is a function that initialises the tkinter window
        self.flashcardwindow=Tk()
        #This code modifies the height and width of the program
        self.flashcardwindow.geometry("1024x512")
        #This checks that if checks if subject folder is created
        if self.subjectsfoldercreated==False:
         os.mkdir("Subjects")
        #Checks if there are any current subjects
        if len(os.listdir(self.path+"\\"+"Subjects"))==0:
         choice=messagebox.askyesno("New user","It seems like you do not have any subjects,would you like to create a subject?")
         if choice==1:
            self.addsubject()
        #This variable holds the string variable of the selected subject in the subjectbox
        self.selected_subject=StringVar()
        #The variable holds the string variable of the selected topic in the subjectbox.
        self.selected_topic=StringVar()
        #This dictionary holds the keys(Questions) and Values(Answers) of the flashcards.
        self.flashcardstorage={}
        #This dictionary holds the keys(Questions) and Values(Answers of the failed flashcards.
        self.failedflashcardstorage={}
        #Sets the study failed cards to default 0
        self.studyfailedflashcards=0
        #This integer is used to count the amount of total questions the person has done and will be used for a future iteration
        self.totalquestions=0
        #This integer is used to count the amount of answers the user has got correct(is used for a display label) and will be used for a future iteration.
        self.correctanswers=0
        #This integer is used to count the amount of answers the user has got wrong(is used for a display label) and will be used for a future iteration.
        self.wronganswers=0
        #The integer value of percentage 
        self.percentagecorrect=0
        #This variable is used for when asking if a user wants to add to an empty csv
        self.addflashcardtoemptycsv=0
        #This variable holds flashcard storage length in this case its 0 because nothing has been loaded
        self.flashcardstoragelength=0
        #This is to record whether the last flashcard has been deleted
        self.lastflashcarddeleted=False
        #This boolean is set to true because the front of the card will always be displayed unless the flashcard is flipped
        self.frontofcard=True
        #This boolean is set to false is used in modify and delete function the purpose of it is to be set to true when modify function is true so that delete flash card method will be ran then addflashcard method
        self.flashcardmodified=False
        #This boolean variable is for checking if flashcards have been loaded.
        self.flashcardsloaded=False
        #This lets tkinter know that a menubar will be created
        self.menubar=Menu(self.flashcardwindow)
        self.flashcardwindow.config(menu=self.menubar)
        #This creates a variable that holds a list of menu buttons that will be used in the menu dropdown
        self.addmenu=Menu(self.menubar)
        self.modifymenu=Menu(self.menubar)
        self.deletemenu=Menu(self.menubar)
        #Adds a cascade under the menu 
        self.menubar.add_cascade(label="Add menu",menu=self.addmenu)
        #Adds a cascade under the menu
        self.menubar.add_cascade(label="Modify menu",menu=self.modifymenu)
        #Adds a cascade under the menu
        self.menubar.add_cascade(label="Delete menu",menu=self.deletemenu)
        #Add subject method underneath Add menu
        self.addmenu.add_command(label="Add subject",command=self.addsubject)
        #Add topic method underneath Add menu
        self.addmenu.add_command(label="Add topic",command=self.addtopic)
        #Add flashcard method underneath Add menu
        self.addmenu.add_command(label="Add flashcard",command=self.addflashcard)
        #Modify flashcard method underneath Modify menu
        self.modifymenu.add_command(label="Modify flashcard",command=self.modifyflashcard)
        #Delete flashcard method underneath Delete menu
        self.deletemenu.add_command(label="Delete flashcard",command=self.deleteflashcard)
        #a list variable that holds all the directories in Subjects folder
        self.subjectboxcontents=os.listdir(self.path+"\\"+"Subjects")
        # a Combo box that holds all of the subjects in the subjects directory
        self.subjectbox=ttk.Combobox(self.flashcardwindow,textvariable=self.selected_subject)
        #appends all of subject contents into the subjectbox
        self.subjectbox['values']=self.subjectboxcontents
        #Disables the user's ability to enter customwords in the combobox
        self.subjectbox['state'] = 'readonly'
        #Local function to call initialisetopicbox.
        def initialise_topic(n):
            self.initialisetopicbox()
        #Sets a function that if something within combobox is selected intialise topic function is called.
        self.subjectbox.bind('<<ComboboxSelected>>',initialise_topic)
        #Sets the currentflashcard to a string telling user instructions
        self.currentflashcard="Please choose a subject and topic then load flashcards"
        #a list variable that holds all of csvs in the subject that is chosen.    
        self.topicboxcontents=os.listdir(self.path+"\\"+"Subjects"+"\\"+self.selected_subject.get()+"\\")
        #A topic box for all of the topics csv
        self.topicbox=ttk.Combobox(self.flashcardwindow,textvariable=self.selected_topic)
        #Disables the user's ability to enter customwords in the combobox
        self.topicbox['state'] = 'readonly'
        #Creates an entrybox for adding the answer for a flashcard
        self.flashcardanswerentry=Entry(self.flashcardwindow)
        #Creates a displayboxbutton for flipping the flashcard.
        self.displayboxbutton=Button(self.flashcardwindow,text=self.currentflashcard,command=self.showbackofcard,wraplength=150)
        #Creates a button to load flashcards.
        self.loadflashcardbutton=Button(self.flashcardwindow,text="Load Flashcards",command=self.loadflashcards)
        #Creates a submit answer button.
        self.submitanswer=Button(self.flashcardwindow,text="Submit your answer",command=self.continueflashcards)
        #Creates a total questions label
        self.totalquestionslabel=Label(self.flashcardwindow,text=f"Total Questions: {self.totalquestions}")
        #Creates a percentage correct label
        self.percentagecorrectlabel=Label(self.flashcardwindow,text=f"Percentage correct: {self.percentagecorrect}%")
        #Creates a score label to display the score of the user
        self.correctanswerslabel=Label(self.flashcardwindow,text=f"Answers correct: {self.correctanswers}")
        #Creates a wrongscore label to display the score of the user.
        self.wronganswerslabel=Label(self.flashcardwindow,text=f"Wrong answers: {self.wronganswers}")
        #Creates a subject label to show where subject box is.
        self.subjectlabel=Label(self.flashcardwindow,text="Subject box")
        #Creates a subject label to show where topic box is.
        self.topiclabel=Label(self.flashcardwindow,text="Topic box")
        #Creates a subject label to show where flip box is.
        self.flipcardlabel=Label(self.flashcardwindow,text="Flip card")
        #Placing of widgets
        self.subjectlabel.place(x=650,y=25)
        self.topiclabel.place(x=870,y=25)
        self.correctanswerslabel.place(x=530,y=0)
        self.wronganswerslabel.place(x=650,y=0)
        self.totalquestionslabel.place(x=760,y=0)
        self.percentagecorrectlabel.place(x=870,y=0)
        self.flipcardlabel.place(x=280,y=10)
        self.submitanswer.place(x=620,y=450,height=40,width=115)
        self.flashcardanswerentry.place(x=10,y=450,height=40,width=600)
        self.displayboxbutton.place(x=10,y=30,height=400,width=600)
        self.loadflashcardbutton.place(x=915,y=450,height=40,width=100)
        self.subjectbox.place(x=620,y=50,height=25,width=200)
        self.topicbox.place(x=820,y=50,height=25,width=200)
        self.flashcardwindow.mainloop()

        
    #Shows all of the topics of the subject when called    
    def initialisetopicbox(self):
        #Sets all of the topicbox contents to the current selected subject
        self.topicboxcontents=os.listdir(self.path+"\\"+"Subjects"+"\\"+self.selected_subject.get()+"\\")
        #Appends the values in topicboxcontents to the topicbox.
        self.topicbox['values']=self.topicboxcontents
    
    #A method to refresh my subject box    
    def refreshsubjectbox(self):
        self.subjectboxcontents=os.listdir(self.path+"\\"+"Subjects")
        self.subjectbox['values']=self.subjectboxcontents

    #A method that refreshes display box      
    def refreshdisplaybox(self):
        #Check if there is an item in the dictionary set a new flashcard
        if len(self.flashcardstorage)>0:
           self.setnewcurrentflashcard() 
        else:
        #Since there is no item in the dictionary it checks if the last flashcard was deleted by user and checks if the user has been asked to previously restudy failed flashcards.
            if self.lastflashcarddeleted==False and self.studyfailedflashcards==0:
                #In order to study failed cards there must be wronganswers that is the first thing being checked
                if self.wronganswers>0 :
                    self.studyfailedflashcards=messagebox.askyesno("Question"," Would you like to study failed flashcards?")
                #Since the user wanted to study failed flashcards the program would reset variables and replaces the contents in flashcardstorage with failedcardstorage 
                if self.studyfailedflashcards == 1:
                    self.congratspopup()
                    self.flashcardstorage=self.failedflashcardstorage
                    self.failedflashcardstorage={}
                    self.resettostarterflashcard()
                    self.flashcardsloaded=True
                    self.setnewcurrentflashcard()
                    self.resettotalquestions()
                    self.disableuiforfailedflashcardtest()
                    self.studyfailedflashcards=0
                #The user did not want to study failed flashcards the program congratulates the user and displays the percentage they got on their topic
                else:
                    self.congratspopup()
                    #The user is asked if they want to load the flashcards again.
                    continueset=messagebox.askyesno("Completed Flashcard set!","Do you wish to load the flashcards again?")
                    #The user agrees to load the flashcards
                    if continueset==1:
                        self.loadflashcards()
                        self.enableuifornormalflashcardtest()
                        self.disablesubjectandtopicboxes()
                    #The user disagrees to load the flashcards and the currentflashcard is reset and the ui elements are enabled.
                    else:
                        self.resettostarterflashcard()
                        self.enableuifornormalflashcardtest()
            #This code will be ran when the lastflashcard has been deleted by the user.It resets the ui back to its starter state
            else:
                self.resettostarterflashcard()
                self.resettotalquestions()
                self.enablesubjectandtopicboxes()

    #Refreshes the totalquestionslabel and is called when the topic is loaded or failed flashcard test
    def refreshtotalquestions(self):
        self.totalquestionslabel.configure(text=f"Total Questions: {self.flashcardstoragelength}")
        
    #Refreshes the percentagecorrectlabel and is called after an answer submition
    def refreshpercentagecorrect(self):
        self.percentagecorrectlabel.configure(text=f"Percentage correct: {self.percentagecorrect}%")
        
    #Resets the totalquestions  
    def resettotalquestions(self):
        self.flashcardstoragelength=len(self.flashcardstorage)
        self.refreshtotalquestions()
        
    #Resets the percentage correct label
    def resetpercentagecorrect(self):
        self.percentagecorrect=0
        self.refreshpercentagecorrect()
        
    #A method that resets to starter flashcard
    def resettostarterflashcard(self):
        self.currentflashcard="Please choose a subject and topic then load flashcards" 
        self.flashcardstoragelength=0
        self.flashcardsloaded=False
        self.displayboxbutton.configure(text=self.currentflashcard)
        self.refreshscores()

    #Shows the congratulations pop up and the percentage they got on the topic/failedcard test.
    def congratspopup(self):
        messagebox.showinfo("Congratulations!",f"You have got {self.percentagecorrect}% correct on {self.selected_topic.get()}")
        self.studytime()
        self.correctanswers=0
        self.wronganswers=0
        self.totalquestions=0
        self.flashcardstoragelength=0
        self.refreshscores()
        self.resetpercentagecorrect()
        self.resettotalquestions()

    #Shows the time the student has to wait till they have to restudy their cards
    #You can change the range of values by changing the integers
    #You can change the time by changing the string on the right 5 minutes to 10 minutes
    def studytime(self):
        if self.percentagecorrect<=25:
            messagebox.showinfo("New study time",f"You should study {self.selected_topic.get()} atleast 5 minutes after your current time")
        elif self.percentagecorrect<=50:
            messagebox.showinfo("New study time",f"You should study {self.selected_topic.get()} atleast 10 minutes after your current time")
        elif self.percentagecorrect<=75:
            messagebox.showinfo("New study time",f"You should study {self.selected_topic.get()} atleast 30 minutes after your current time")
        elif self.percentagecorrect<=90:
            messagebox.showinfo("New study time",f"You should study {self.selected_topic.get()} atleast 1 hour after your current time")
        elif self.percentagecorrect<100:
            messagebox.showinfo("New study time",f"You should study {self.selected_topic.get()} atleast 3 hours after your current time")
        elif self.percentagecorrect==100:
            messagebox.showinfo("New study time",f"You should study {self.selected_topic.get()} atleast 4 days after your current time")

    #Disable the ui widgets for the failed flashcard test
    def disableuiforfailedflashcardtest(self):
        self.addmenu.entryconfig("Add flashcard",state="disabled")
        self.addmenu.entryconfig("Add topic",state="disabled")
        self.modifymenu.entryconfig("Modify flashcard",state="disabled")
        self.deletemenu.entryconfig("Delete flashcard",state="disabled")
        self.loadflashcardbutton['state']="disabled"
        self.disablesubjectandtopicboxes()

    #Enables the ui widgets for the normal flashcard test
    def enableuifornormalflashcardtest(self):
        self.addmenu.entryconfig("Add flashcard",state="normal")
        self.addmenu.entryconfig("Add topic",state="normal")
        self.modifymenu.entryconfig("Modify flashcard",state="normal")
        self.deletemenu.entryconfig("Delete flashcard",state="normal")
        self.loadflashcardbutton['state']="normal"
        self.enablesubjectandtopicboxes()

    #Disables the subject and topic boxes
    def disablesubjectandtopicboxes(self):
        self.subjectbox['state']='disabled'
        self.topicbox['state']='disabled'
    
    #Enables the subject and topic boxes    
    def enablesubjectandtopicboxes(self):
        self.subjectbox['state']='readonly'
        self.topicbox['state']='readonly'

    #Sets a new current flashcard from the first index of the flashcard dictionary
    def setnewcurrentflashcard(self):
        #Takes the first flashcard in the flashcardstorage.
        self.currentflashcard=list(self.flashcardstorage.keys())[0]
        #Changes the text on the displaybox button to the value of currentflashcard.
        self.displayboxbutton.configure(text=self.currentflashcard)

    #A method that inverts the side of the flashcard by showing the dictionary value instead of key or vice versa
    def showbackofcard(self):
        #Checks if the flashcard being flipped is not the default flashcard
        if self.currentflashcard!="Please choose a subject and topic then load flashcards":
            #Reverses the front of card boolean
            self.frontofcard= not self.frontofcard
            #If its not the front of the card change the text on the displaybutton to the flashcard answer
            if self.frontofcard == False:
                self.displayboxbutton.configure(text=self.flashcardstorage[self.currentflashcard])
            #since its the front of the card the text is the flashcard question
            else:
                self.displayboxbutton.configure(text=self.currentflashcard)
        else:
            messagebox.showerror("Error","Make sure you have loaded flashcards before trying to flip the flashcard")

    #A method that changes the score labels after an answer is submitted
    def refreshscores(self):
        self.correctanswerslabel.configure(text=f"Answers correct: {self.correctanswers}")
        self.wronganswerslabel.configure(text=f"Wrong answers: {self.wronganswers}")
 
    #A method that loads all the flashcards from the topic folder to the csv and refreshes displaybox.
    def loadflashcards(self):
        if len(self.selected_subject.get())>0 and len(self.selected_topic.get())>0:
            #Resets flashcardstorage incase another one has already been loaded
            self.flashcardstorage={}
            #Opens the csv file for the selected topic
            with open(self.path+"\\"+"Subjects"+"\\"+self.selected_subject.get()+"\\"+self.selected_topic.get())as csv:
                for lines in csv.readlines():
                    Line=lines.strip().split(",")
                    self.flashcardstorage[Line[0]]=Line[1]
            #Gets the length of flashcardstorage
            self.flashcardstoragelength=len(self.flashcardstorage)
            flashcardstoragekeys=list(self.flashcardstorage.keys())
            random.shuffle(flashcardstoragekeys)
            shuffledflashcardstorage={}
            for flashcardstoragekey in flashcardstoragekeys:
                      shuffledflashcardstorage[flashcardstoragekey]=self.flashcardstorage[flashcardstoragekey]
            self.flashcardstorage=shuffledflashcardstorage
            #Checks if there is anything in the csv before proceeding
            if self.flashcardstoragelength> 0:
                self.flashcardsloaded=True
                self.refreshdisplaybox()
                self.refreshtotalquestions()
                self.disablesubjectandtopicboxes()
            else:
                #Error message asking to add flashcard because there's nothing in the csv
                self.addflashcardtoemptycsv=messagebox.askyesno("Error","Empty CSV Loaded,Do you want to add a flashcard")
                #The user decided to add a flashcard to the empty csv
                if self.addflashcardtoemptycsv==1:
                    self.addflashcard()
                    #Checks if the user has actually added a flashcard instead of exiting the window
                    if self.currentflashcard!="Please choose a subject and topic then load flashcards":    
                        self.refreshdisplaybox()
                        self.flashcardstoragelength+=1
                        self.refreshtotalquestions()
                #The user did not decide to add flashcard to the empty csv so the current flashcard resets.
                else:
                    self.resettostarterflashcard()
        else:
            messagebox.showerror("Error","Make sure you have selected a subject and topic from their combo boxes")

    #A method that writes flashcardstorage to csv    
    def flashcardcsvwriter(self):
        with open(self.path+"\\"+"Subjects"+"\\"+self.selected_subject.get()+"\\"+self.selected_topic.get(),'w',newline='')as file:
         writer=csv.writer(file)
         for key,value in self.flashcardstorage.items():
          writer.writerow([key,value])
          
    #A method that checks if flashcardstorage is empty before writing to csv.
    def saveflashcardstocsv(self):
        #Checks if there is anything in the csv before saving.
        if len(self.flashcardstorage)==0:
            #Asks user if they want to clear all flashcards in the topic
            userresponse=messagebox.askyesno("Caution!", f"Are you sure you want to clear {self.selected_topic.get()} ?")
            #The user decided to clear the csv
            if userresponse==1:
                self.flashcardcsvwriter()
                self.lastflashcarddeleted=True
                self.refreshdisplaybox()
                self.lastflashcarddeleted=False
        else:
            #Writes the changes to csv then refreshes the display box
            self.flashcardcsvwriter()
            self.refreshdisplaybox()

    #A function that is called when user presses the x button on the window
    def userdestroyedaddflashcardwindow(self):
        #Since the flashcard has not been added the csv is still empty
        self.flashcardsloaded=False
        self.addflashcardwindow.destroy()
        
    #Addflashcard window
    def addflashcard(self):
        #Creates a pop up window.
        self.addflashcardwindow=Toplevel(self.flashcardwindow)
        #Makes it so that this window is set as primary focus,so that you can not interact with other buttons on different interfaces
        self.addflashcardwindow.grab_set()
        #Creates an entrybox for adding the flashcardquestion.
        self.addflashcardquestionentry=Entry(self.addflashcardwindow)
        #Creates an entrybox for adding the flashcardanswer.
        self.addflashcardanswerentry=Entry(self.addflashcardwindow)
        #A label that shows where the add question.
        self.addflashcardquestionlabel=Label(self.addflashcardwindow,text="Add your question below")
        #A label that shows where the add answer question.
        self.addflashcardanswerlabel=Label(self.addflashcardwindow,text="Add your answer below")
        #A button that is for adding the flashcard to the csv.
        self.addflashcardbutton=Button(self.addflashcardwindow,command=self.addflashcardmethod,text="Add flashcard")
        #If the user is adding a flashcard to empty csv.
        if self.addflashcardtoemptycsv==1:
            #Changes the exit button function on the window so that if a user exited it would inform program that user exited the window rather than program naturally closing it.
            self.addflashcardwindow.protocol("WM_DELETE_WINDOW",self.userdestroyedaddflashcardwindow)
        self.addflashcardquestionlabel.place(x=0,y=10,height=15,width=200)
        self.addflashcardanswerlabel.place(x=0,y=50,height=15,width=200)
        self.addflashcardquestionentry.place(x=0,y=25,height=25,width=200)
        self.addflashcardanswerentry.place(x=0,y=70,height=50,width=200)
        self.addflashcardbutton.place(x=40,y=140,height=30,width=100)

    #Add flashcard method for the button    
    def addflashcardmethod(self):
        #Checks if the user has selected a subject and topic
        if len(self.selected_subject.get())>0 and len(self.selected_topic.get())>0:
            #Checks if there is anything in the flashcardstorage or checks if the user is adding a flashcard to empty csv
            if len(self.flashcardstorage)>0 or self.addflashcardtoemptycsv == 1:
                checkifquestion=False
                stringinanswerbox=False
                #Checks if there is anything in the entrybox before trying to get the qyestion mark
                if len(self.addflashcardquestionentry.get())>0:
                    questionmark=self.addflashcardquestionentry.get().strip()[-1]
                else:
                    messagebox.showerror("Error","Make sure you enter a question in the questionbox!")

                #Checks if the last character in entrybox is equal to question mark
                if questionmark=="?":
                    #Sets checkifquestion to true as it is a question
                    checkifquestion=True
                else:
                    #Sets checkifquestion to False as its not a question
                    checkifquestion=False

                if len(self.addflashcardanswerentry.get())==0:
                    stringinanswerbox=False
                else:
                    stringinanswerbox=True

                #Checks if its a question before proceeding
                if checkifquestion==True:
                    #Checks if there is a string in answerbox
                    if stringinanswerbox==True:
                        #Removes commas and speechmarks from the answer and question as this affects how its stored in csv.
                        self.addflashcardquestion=re.sub(r',',' ',self.addflashcardquestionentry.get())
                        self.addflashcardquestion=re.sub(r'"','',self.addflashcardquestion.lstrip().rstrip())
                        self.addflashcardquestion=re.sub(r'\n',' ',self.addflashcardquestion)
                        self.addflashcardanswer=re.sub(r',',' ',self.addflashcardanswerentry.get())
                        self.addflashcardanswer=re.sub(r'"','',self.addflashcardanswer.lstrip().rstrip())
                        self.addflashcardanswer=re.sub(r'\n',' ',self.addflashcardanswer)
                        #Appends the question to flashcardstorage
                        self.flashcardstorage[self.addflashcardquestion]=self.addflashcardanswer
                        self.flashcardstoragelength+=1
                        self.refreshtotalquestions()
                        #Saves flashcard to topic csv.
                        self.saveflashcardstocsv()
                        #When the method is ran if its adding a flashcard to an empty csv
                        if self.addflashcardtoemptycsv==1:
                            self.flashcardsloaded=True
                            self.disablesubjectandtopicboxes()
                        self.addflashcardwindow.destroy()
                    else:
                        messagebox.showerror("Error","Make sure you enter in an answer in the answerbox!")
                else:
                 messagebox.showerror("Error", "Make sure you put a question mark next to your question!")
            else:
                messagebox.showerror("Error", "Make sure you have loaded flashcards before proceeding to add flashcards")
        else:
            messagebox.showerror("Error", "Make sure you have selected a subject and topic from their combo boxes")

    #Modifies the selected flashcard by deleting and adding it.   
    def modifyflashcard(self):
        #Lets program know that the card is being modified
        self.flashcardmodified=True
        #Calls the deleteflashcard method
        self.deleteflashcard()

    #Delete flashcard window
    def deleteflashcard(self):
        #Creates a list of flashcard keys.
        self.flashcardkeylist=[]
        #Appends all of dictionary into a list.
        for keys in self.flashcardstorage:
            self.flashcardkeylist.append(keys)
        #Creates a toplevel window for deleting flashcard.
        self.deleteflashcardwindow=Toplevel(self.flashcardwindow)
        #Makes it so that this window is set as primary focus,so that you can not interact with other buttons on different interfaces
        self.deleteflashcardwindow.grab_set()
        #Creates a combobox in the flashcard window
        self.deleteflashcardcombobox=ttk.Combobox(self.deleteflashcardwindow)
        #Appends all of the keys into the deleteflashcardcombobox.
        self.deleteflashcardcombobox['values']=self.flashcardkeylist
        #Sets the combobox to readonly so that you can only select flashcards rather than type them in
        self.deleteflashcardcombobox['state']='readonly'
        #Creates a button to confirm the deletion of the flashcard selected.
        self.deleteflashcardbutton=Button(self.deleteflashcardwindow,command=self.deleteflashcardmethod,text="Delete Flashcard")
        self.deleteflashcardcombobox.place(x=0,y=25,height=25,width=200)
        self.deleteflashcardbutton.place(x=40,y=140,height=30,width=100)

    #Deletes the selected flashcard.
    def deleteflashcardmethod(self):
        #Checks if there's a subject and topic selected and if there's anything in the flashcard storage
        if len(self.selected_subject.get())>0 and len(self.selected_topic.get())>0 and self.flashcardstoragelength>0:
            #Deletes the value selected in the value
            if len(self.deleteflashcardcombobox.get())>0:
                del self.flashcardstorage[self.deleteflashcardcombobox.get()]
                self.flashcardstoragelength-=1
                self.refreshtotalquestions()
            else:
                messagebox.showerror("Error","Make sure you select a flashcard from the combobox")
            #Saves the flashcardstorage to csv
            self.saveflashcardstocsv()
            if self.flashcardmodified==False:
                #Ends method because flashcard is not being modified
                self.deleteflashcardwindow.destroy()
            else:
                #Calls add flashcard because flashcard is being modified
                self.addflashcard()
                #Resets the boolean to its original state
                self.flashcardmodified=False
                #Destroys the window
                self.refreshtotalquestions()
                self.deleteflashcardwindow.destroy()
        else:
            messagebox.showerror("Error", "Make sure you have selected a subject and topic from their combo boxes and have loaded the flashcards")

    #Add subject window
    def addsubject(self):
        #Creating popup window for adding subject pop up window.
        self.addsubjectwindow=Toplevel(self.flashcardwindow)
        #Makes it so that this window is set as primary focus,so that you can not interact with other buttons on different interfaces
        self.addsubjectwindow.grab_set()
        #Creating an entrybox for user to enter subject name.
        self.addsubjectentry=Entry(self.addsubjectwindow)
        #Creating addsubject button to confirm string in the entrybox.
        self.addsubjectbutton=Button(self.addsubjectwindow,command=self.addsubjectmethod,text="Add Subject")
        self.addsubjectentry.place(x=0,y=25,height=25,width=200)
        self.addsubjectbutton.place(x=40,y=140,height=30,width=100)

    #Makes a subject directory
    def addsubjectmethod(self):
        #Checks if there is anything in the subject entrybox
        if len(self.addsubjectentry.get())>0:
            #Subjectbox contents but lowered
            subjectcontentslower=[i.lower() for i in self.subjectboxcontents]
            #Creates a new path string
            self.newpath=os.path.join(self.path+"\\"+"Subjects"+"\\"+self.addsubjectentry.get())
            if self.addsubjectentry.get().lower() not in subjectcontentslower:
                #Makes the string into an actual directory.
                os.mkdir(self.newpath)
                #Refreshes the subjectbox
                self.refreshsubjectbox()
                #Destroys the window
                self.addsubjectwindow.destroy()
            else:
                messagebox.showerror("Error","That subject already exists")
        else:
            messagebox.showerror("Error", "Make sure you put the name of the Subject in the entrybox")  

    #Add topic window
    def addtopic(self):
        #Creating popup window for addtopic window.
        self.addtopicwindow=Toplevel(self.flashcardwindow)
        #Makes it so that this window is set as primary focus,so that you can not interact with other buttons on different interfaces
        self.addtopicwindow.grab_set()
        #Creating an entrybox for user to enter name of topic.
        self.addtopicentry=Entry(self.addtopicwindow)
        #Creating a button to confirmstring in entrybox.
        self.addtopicbutton=Button(self.addtopicwindow,command=self.addtopicmethod,text="Add Topic")
        self.addtopicbutton.place(x=40,y=140,height=30,width=100)
        self.addtopicentry.place(x=0,y=25,height=25,width=200)

    #Method for creating the topic
    def addtopicmethod(self):
        #Checks if there's anything in the topic entrybox and whether the user has selected a subject.
        if len(self.addtopicentry.get())>0 and len(self.selected_subject.get())>0:
            #Creates a path where the new topic will be saves
            self.newpath=os.path.join(self.path+"\\"+"Subjects"+"\\"+self.selected_subject.get()+"\\"+self.addtopicentry.get())
            #Opens an empty file which creates the csv
            with open (f"{self.newpath}.csv","w")as empty:
                pass
            #Refreshes the topicbox checkbox
            self.initialisetopicbox()
            #Destroys the add topic window
            self.addtopicwindow.destroy()
        else:
            messagebox.showerror("Error", "Make sure you put the name of the topic in the entrybox and make sure a subject is selected in the combobox") 

    #Checks answer against the the value of the currentflashcard
    def continueflashcards(self):
        #If the flashcards are loaded record the answer
        if self.flashcardsloaded==True:
            self.recordanswer()
        #Display an error message informing the user to do what is required
        else:
          messagebox.showerror("Error", "Make sure you have selected a subject and topic from their combo boxes and have loaded the flashcards")  

    #Checks if the answer the user inputted and the one in flashcardstorage is the same
    def recordanswer(self):
     #Increases total questions by 1 this is used to calculate percentage
     self.totalquestions+=1
     #Removes all of symbols and spaces and makes answer lowercase
     self.answersub=re.sub(r'[^\w]','',self.flashcardstorage[self.currentflashcard].lower())
     #Removes all of symbols and spaces and makes input lowercase
     self.inputsub=re.sub(r'[^\w]','',self.flashcardanswerentry.get().lower())
     #Checks if answer==input and adds one to correct answers otherwise add 1 to wrong answers
     if self.answersub==self.inputsub:
      #Adds 1 to correctanswers as the answer is equal to the user's input
      self.correctanswers+=1
     else:
      #Adds 1 to wronganswers as the answer is not equal to the user's input
      self.wronganswers+=1
      self.failedflashcardstorage[self.currentflashcard]=self.flashcardstorage[self.currentflashcard]
     #Removes the current flashcard as its been tested
     del self.flashcardstorage[self.currentflashcard]
     #Calculates the percentage
     self.percentagecorrect=self.correctanswers/self.totalquestions*100
     self.refreshpercentagecorrect()
     self.refreshscores()
     self.refreshdisplaybox()
     self.frontofcard=True
     self.flashcardanswerentry.delete(0,END)
    
      
             

start=Flashcardwindow
start()
        
