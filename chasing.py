#Simple game where one dot is chased ba another
import pygame
import random
import numpy as np
from scipy import stats
import Agent1
import Agent2

useag2 = True

#Calculates possible state-changes
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
x1 = random.randint(0+(width/2), xlength-(width/2))
y1 = random.randint(0+(height/2), ylength-(height/2))
x2 = random.randint(0+(width/2), xlength-(width/2))
y2 = random.randint(0+(height/2), ylength-(height/2))


#Velocity
vel = 5

#Main Loop
run = True
while run:
    #(Millisekunden!)
    pygame.time.delay(0)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
            
    #calculationg distance
    distance_before = np.sqrt(sum([(x1-x2)**2, (y1-y2)**2]))
    
    #Predicting move for Agent1
    state_data1 = get_state_data([x1, y1, x2, y2], [0,1], 5, False)
    input_data1 = get_input_data(
            [0, 0]+[([x1, y1, x2, y2][i]-250)/250 for i in range(0,len(state_data1))], 
            [0,1], 5, False)
    
    if useag2:
        state_data2 = get_state_data([x2, y2, x1, y1], [0,1], 5, False)
        input_data2 = get_input_data(
            [0, 0]+[([x2, y2, x1, y1][i]-250)/250 for i in range(0,len(state_data2))], 
            [0,1], 5, False)    
        model_predictions2=np.squeeze(Agent2.model.predict(input_data2))
        prediction_agent2 = get_choice(model_predictions2, 0.3)
        new_state2 = state_data2[prediction_agent2]
        training_data2 = np.expand_dims(input_data2[prediction_agent2], axis=0)
    
    
    model_predictions1=np.squeeze(Agent1.model.predict(input_data1))
    #Using Exploration and Exploitation!!!
    #prediction_agent1 = np.random.choice([i for i in range(0,len(model_predictions1))], #!!!
    #                                     p=model_predictions1/np.sum(model_predictions1))
    prediction_agent1 = get_choice(model_predictions1, 0.3)

    training_data1 = np.expand_dims(input_data1[prediction_agent1], axis=0)
    new_state1 = state_data1[prediction_agent1]
    
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
    reward = (distance_before-distance_after)/5+(500-distance_after)/20
    
        #Game Over
    if(x1 > x2-20 and x1 < x2+20 and y1 > y2-20 and y1 < y2+20):
        #run=False
        #Die Position des Spielers wird zufällig gewählt:
        x1 = random.randint(0+(width/2), xlength-(width/2))
        y1 = random.randint(0+(height/2), ylength-(height/2))
        x2 = random.randint(0+(width/2), xlength-(width/2))
        y2 = random.randint(0+(height/2), ylength-(height/2))
        reward +=20
    
    #Using Q-Learning for Optimisation:
    Agent1.model.fit(training_data1,
                     np.asarray([reward]), epochs=1)
    
    Agent2.model.fit(training_data2,
                     np.asarray([-reward]), epochs=1)
    #Den gesamten Bildschirm Schwarz ausmahlen
    win.fill([0,0,0])
    
    #Window, colour, center, position
    rect1 = pygame.draw.rect(win, (255,0,0), (x1,y1,height,width))
    rect2 = pygame.draw.rect(win, (0,0,255), (x2,y2,height,width))
    pygame.display.update()
    


pygame.quit()


        
