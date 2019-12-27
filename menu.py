#Designing a simple menu for chasing
import tkinter as tk
#from tkinter import *

class menu():
    
    new_game=False
    
    def __init__(self):
        self.root = tk.Tk()
        self.enable_training = tk.IntVar()
        self.enable_training.set(1)
        self.training_intervall = tk.StringVar()
        self.training_intervall.set("1")

    def new_game_init(self):
        if(self.new_game == False):
            self.new_game=True
        print(self.new_game)
        self.root.destroy()
        
            
    def get_new_game(self):
        return(self.new_game)
        
    def get_training_enabled(self):
        return(self.enable_training.get())
        
    def apply(self):
        self.root.destroy()
    
    #Start Menu
    def start_menu(self): 
        self.root.title("Menu")
        
        #New Game Button
        button_ng = tk.Button(self.root, text='New Game', width=25, command=self.new_game_init)
        button_ng.pack()
        
        #Model Training Checkbox
        training = tk.Checkbutton(self.root, text="Enable Training", variable=self.enable_training)
        if(self.enable_training.get() == 1):
            training.select()
            self.enable_training.set(1)
        training.pack()
        
        #Entry for Training Intervall:
        intervall_label = tk.Label(self.root, text="Training Interavall") 
        intervall_label.pack()
        intervall_entry = tk.Entry(self.root, textvariable=self.training_intervall)
        intervall_entry.pack()
        
        #Apply Button
        button_apply = tk.Button(self.root, text='Apply', width=25, command=self.apply)
        button_apply.pack()
        
        self.root.mainloop()
        
        
#x = menu()
#x.start_menu()





