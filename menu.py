#Designing a simple menu for chasing
import tkinter as tk
#from tkinter import *

class menu():
    
    new_game=False
    
    #Constructor
    def __init__(self, training_intervall, game_len, explore, lrate):
        self.root = tk.Tk()
        self.enable_training = tk.IntVar()
        self.enable_training.set(1)
        self.training_intervall = tk.StringVar()
        self.training_intervall.set(str(training_intervall))
        self.game_len = tk.StringVar()
        self.game_len.set(str(game_len))
        self.exploration = tk.StringVar()
        self.exploration.set(str(explore))
        self.lrate = tk.StringVar()
        self.lrate.set(str(lrate))

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
    
    #Start Menu and build widgets
    def start_menu(self): 
        self.root.title("Menu")
        
        #New Game Button
        button_ng = tk.Button(self.root, text='New Game', width=25, command=self.new_game_init)
        button_ng.pack()
        
        #Model Training Checkbox
        training = tk.Checkbutton(self.root, text="Enable training", variable=self.enable_training)
        if(self.enable_training.get() == 1):
            training.select()
            self.enable_training.set(1)
        training.pack()
        
        #Entry for Training Intervall:
        intervall_label = tk.Label(self.root, text="Training interavall") 
        intervall_label.pack()
        intervall_entry = tk.Entry(self.root, textvariable=self.training_intervall)
        intervall_entry.pack()
        
        #Entry for max Game Length
        game_len_label = tk.Label(self.root, text="Maximum game length") 
        game_len_label.pack()
        game_len_entry = tk.Entry(self.root, textvariable=self.game_len)
        game_len_entry.pack()
        
        #Exploration Rate
        exploration_label = tk.Label(self.root, text="Exploration rate") 
        exploration_label.pack()
        exploration_entry = tk.Entry(self.root, textvariable=self.exploration)
        exploration_entry.pack()
        
        #Learning Rate
        lrate_label = tk.Label(self.root, text="Learning rate") 
        lrate_label.pack()
        lrate_entry = tk.Entry(self.root, textvariable=self.lrate)
        lrate_entry.pack()
        
        #Apply Button
        button_apply = tk.Button(self.root, text='Apply', width=25, command=self.apply)
        button_apply.pack()
        
        self.root.mainloop()
        
        
#x = menu()
#x.start_menu()





