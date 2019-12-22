#Simple game where one dot is chased ba another
import pygame
import random
import numpy as np
from scipy import stats
import Agent1

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

x1p = x1
y1p = y1
x2p = x2
y2p = y2

#Velocity
vel = 5

#Main Loop
run = True
while run:
    #(Millisekunden!)
    pygame.time.delay(50)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
            
    #calculationg distance
    distance_before = np.sqrt(sum([(x1-x2)**2, (y1-y2)**2]))
    
    #Predicting move for Agent1
    input_data = np.expand_dims(stats.zscore(np.asarray([x1, y1, x2, y2])), axis=0)
    prediction_agent1 = Agent1.model.predict(input_data)[0]
    move_agent1 = np.random.choice(["L","R","U","D"], 
                                   p=prediction_agent1/np.sum(prediction_agent1))
    
    if(x1>xlength or x1<10 or y1>ylength or y1<10):
        None
    elif move_agent1 == "L":
        x1p = x1
        x1 -= vel
    elif move_agent1 == "R":
        x1p = x1
        x1 += vel
    elif move_agent1 == "U":
        y1p = y1
        y1 += vel
    elif move_agent1 == "D":
        y1p = y1
        y1 -= vel
    
    distance_after = np.sqrt(sum([(x1-x2)**2, (y1-y2)**2]))
    print(distance_after)
    
    fake_y = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
    fake_y_agent1 = fake_y[np.random.choice([0,1,2,3], 
                                   p=prediction_agent1/np.sum(prediction_agent1))]

    if(distance_before>distance_after):
        reward=1
    else:
        reward=-1
    
    Agent1.model.fit(input_data,
                     np.expand_dims(np.multiply(reward,fake_y_agent1),
                                    axis=0))
    
    #Den gesamten Bildschirm Schwarz ausmahlen
    win.fill([0,0,0])
    
    #Window, colour, center, position
    rect1 = pygame.draw.rect(win, (255,0,0), (x1,y1,height,width))
    rect2 = pygame.draw.rect(win, (0,0,255), (x2,y2,height,width))
    pygame.display.update()

pygame.quit()


