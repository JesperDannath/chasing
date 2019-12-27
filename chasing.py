#Simple game where one dot is chased ba another
import pygame
import random
import numpy as np
from scipy import stats
import Agent
from menu import menu


#Calculates the Inut Data to the Networks
def get_input_data(state, change_ind ,change, standardize=False):
    result=[]
    for i in range(0, len(change_ind)):
        change_ind
        increment = state.copy()
        #increment[change_ind[i]] = increment[change_ind[i]]+change
        increment[change_ind[i-2]] = increment[change_ind[i]]+change
        decrement = state.copy()
        #decrement[change_ind[i]] = decrement[change_ind[i]]-change
        decrement[change_ind[i-2]] = decrement[change_ind[i]]-change
        result.append(increment)
        result.append(decrement)
    result = np.asarray(result)
    if(standardize==True):
        result = stats.zscore(result)
    return(result)
   
#Calculates possible state-changes
def get_state_data(state, change_ind ,change, standardize=False):
    result=[]
    for i in range(0, len(change_ind)):
        change_ind
        increment = state.copy()
        increment[change_ind[i]] = increment[change_ind[i]]+change
        decrement = state.copy()
        decrement[change_ind[i]] = decrement[change_ind[i]]-change
        result.append(increment)
        result.append(decrement)
    result = np.asarray(result)
    if(standardize==True):
        result = stats.zscore(result)
    return(result)
    
#Implements an exploration Rate for randomness Factor od Aget Decisions
def get_choice(predictions, exploration_rate):
    choice = np.random.choice(a=["explore", "exploit"], p=[exploration_rate, 1-exploration_rate])
    if choice == "explore":
        return(random.randint(0,len(predictions)-1))
    else:
        return(np.argmax(predictions))
        

pygame.init()

xlength=500
ylength=500
win = pygame.display.set_mode((xlength, ylength))

pygame.display.set_caption("Chasing")


height = 20
width = 20

#Die Position des Spielers wird zufällig gewählt:
def initialize_random_dots(number, xlength, ylength, width=20, heigth=20):
    koords = []
    for i in range(0, number):
        koords.append(random.randint(0+(width/2), xlength-(width/2)))
        koords.append(random.randint(0+(height/2), ylength-(height/2)))
    return(koords)
        
x1, y1, x2, y2 = initialize_random_dots(2, xlength, ylength)

#Build Models
model1 = Agent.build_model()
model2 = Agent.build_model()

#Velocity
vel = 5

#Main Loop
def main_loop(x1, y1, x2, y2):
    new_game=False
    run = True
    training_enabled = 1
    time_step = 1
    training_intervall = 4
    
    #Dataholders to fill
    training_data1 = np.asarray([])
    training_data2 = np.asarray([[]])
    reward1 = np.asarray([])
    reward2 = np.asarray([])
    
    while run:
        #(Millisekunden!)
        pygame.time.delay(0)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu1 = menu()
                    menu1.enable_training.set(training_enabled)
                    menu1.start_menu()
                    new_game = menu1.get_new_game()
                    training_enabled = menu1.get_training_enabled()
                    training_intervall = int(menu1.training_intervall.get())
                
        #Agent1
        #calculationg distance
        distance_before = np.sqrt(sum([(x1-x2)**2, (y1-y2)**2]))
        #Predicting move for Agent1
        state_data1 = get_state_data([x1, y1, x2, y2], [0,1], 5, False)
        input_data1 = get_input_data(
                [0, 0]+[([x1, y1, x2, y2][i]-250)/250 for i in range(0,len(state_data1))], 
                [0,1], 5, False)
        model_predictions1=np.squeeze(model1.predict(input_data1))
        #Using Exploration and Exploitation!!!
        prediction_agent1 = get_choice(model_predictions1, 0.3)
        if(training_data1.size > 0):
            training_data1 = np.concatenate(
                    (np.expand_dims(input_data1[prediction_agent1], axis=0),
                     training_data1), axis=0)
        else:
            training_data1 = np.expand_dims(input_data1[prediction_agent1], axis=0)
            
        new_state1 = state_data1[prediction_agent1]
                
        #Agent2
        state_data2 = get_state_data([x2, y2, x1, y1], [0,1], 5, False)
        input_data2 = get_input_data(
            [0, 0]+[([x2, y2, x1, y1][i]-250)/250 for i in range(0,len(state_data2))], 
            [0,1], 5, False)    
        model_predictions2=np.squeeze(model2.predict(input_data2))
        prediction_agent2 = get_choice(model_predictions2, 0.3)
        new_state2 = state_data2[prediction_agent2]
        training_data2 = np.expand_dims(input_data2[prediction_agent2], axis=0)
        
        #Verfolger
        if(x1>xlength):
            x1 -= vel
        elif(x1<20):
            x1 += vel
        elif(y1>ylength):
            y1 -= vel
        elif(y1 < 20):
            y1 += vel
        else:
            x1=new_state1[0]
            y1=new_state1[1]
            
        #Verfolgter
        if(x2>xlength):
            x2 -= vel
        elif(x2<20):
            x2 += vel
        elif(y2>ylength):
            y2 -= vel
        elif(y2 < 20):
            y2 += vel
        else:
            x2=new_state2[0]
            y2=new_state2[1]    
    
        
        distance_after = np.sqrt(sum([(x1-x2)**2, (y1-y2)**2]))
        print(distance_after)
        
        #defining the reward:
        reward_value = (distance_before-distance_after)/5+(500-distance_after)/20
        
            #Game Over
        if(x1 > x2-20 and x1 < x2+20 and y1 > y2-20 and y1 < y2+20):
            #run=False
            #Die Position des Spielers wird zufällig gewählt:
            x1, y1, x2, y2 = initialize_random_dots(2, xlength, ylength)
            reward_value +=20
            
        if(new_game == True):
            x1, y2, x2, y2 = initialize_random_dots(2, xlength, ylength)
            new_game=False
            
        if(reward1.size > 0):
            reward1 = np.append(reward_value, reward1)
        else:
            reward1 = np.expand_dims(np.asarray(reward_value), axis=0)
            
        
        if(training_enabled and (time_step % training_intervall)==0):
            #Using Q-Learning for Optimisation:
            model1.fit(training_data1,
                             reward1, epochs=1)
            
            model2.fit(training_data2,
                             np.asarray([-reward_value]), epochs=1)
            
            #Dataholders to fill
            training_data1 = np.asarray([])
            training_data2 = np.asarray([[]])
            reward1 = np.asarray([])
            reward2 = np.asarray([])
        
        #Den gesamten Bildschirm Schwarz ausmahlen
        win.fill([0,0,0])
        
        #Window, colour, center, position
        rect1 = pygame.draw.rect(win, (255,0,0), (x1,y1,height,width))
        rect2 = pygame.draw.rect(win, (0,0,255), (x2,y2,height,width))
        pygame.display.update()
        time_step += 1
    
    
main_loop(x1, y1, x2, y2)

pygame.quit()


        
