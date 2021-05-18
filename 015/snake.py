import random
import cv2 as cv
import numpy as np
import pygame
import time

def centroid(thresh):
    centers = cv.moments(thresh)

    cX = int(centers["m10"] / centers["m00"])
    cY = int(centers["m01"] / centers["m00"])

    return cX, cY

    
 
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
dis_width = 600
dis_height = 400
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Edureka')
 
clock = pygame.time.Clock()
 
snake_block = 10
snake_speed = 15
 
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
 
def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])
 
 
 
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])
 
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
 


def gameLoop():
    cam = cv.VideoCapture(0)
    snake_move = [False, False, False, False]
    cima = 0
    baixo = 0
    dir = 0
    esq = 0

    game_over = False
    game_close = False
    measure = True
 
    x1 = dis_width / 2
    y1 = dis_height / 2
 
    x1_change = 0
    y1_change = 0
 
    snake_List = []
    Length_of_snake = 1
    
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    
    count_tries = 40

    while not game_over:
            
        check, frame = cam.read()

        frame = cv.flip(frame, 1)
        #print(frame)

        # Constants for the crop size
        camxMin = 0
        camyMin = 0
        camxMax = 380
        camyMax = 260

        img = frame[camyMin:camyMax,camxMin:camxMax] # this is all there is to cropping

        #positining user hand
        if measure == True:
            cv.rectangle(img, (125, 115), (145, 135), (0,255,0), 1)
            cv.rectangle(img, (175, 115), (195, 135), (0,255,0), 1)
            cv.rectangle(img, (225, 115), (245, 135), (0,255,0), 1)
            cv.rectangle(img, (125, 145), (145, 165), (0,255,0), 1)
            cv.rectangle(img, (175, 145), (195, 165), (0,255,0), 1)
            cv.rectangle(img, (225, 145), (245, 165), (0,255,0), 1)
            cv.rectangle(img, (125, 175), (145, 195), (0,255,0), 1)
            cv.rectangle(img, (175, 175), (195, 195), (0,255,0), 1)
            cv.rectangle(img, (225, 175), (245, 195), (0,255,0), 1)
            
        
        #cv.imshow('video', cv.flip(frame, 1))

        key = cv.waitKey(1)
        if key == 27:
            break

        
        hsvim = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        lower = np.array([0, 40, 10], dtype = "uint8")
        upper = np.array([80, 255, 255], dtype = "uint8")
        skinRegionHSV = cv.inRange(hsvim, lower, upper)
        blurred = cv.blur(skinRegionHSV, (9,9))
        ret,thresh = cv.threshold(blurred,0,255,cv.THRESH_BINARY)
        #cv.imshow("thresh", thresh)
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        try:
            contours = max(contours, key=lambda x: cv.contourArea(x)) if max(contours, key=lambda x: cv.contourArea(x)) is not None else None
        except:
            print("Coloque sua mao em frente a camera, caso contrario, o jogo se encerrara' em ", count_tries/10)
            count_tries -= 1
            if count_tries > 0:
                continue
            else:
                break

        cv.drawContours(img, [contours], -1, (0, 255, 255), 2)
        
        #print(type(contours))
        

        cx, cy = centroid(thresh)
        cv.circle(img, (cx,cy), 5, [255, 0, 255], -1)
        cv.putText(img, "centroid", (cx - 25, cy - 25),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        result = np.where(contours[:,:,0] == np.amax(contours[:,:,0]))

        minx = contours[result[0]][0][0]

        euclid_dir = np.sqrt((minx[0]-cx)**2 + (minx[1]-cy)**2)
        print("EUCLID DIR", euclid_dir)

        cv.circle(img, tuple(minx), 5, [255, 0, 255], -1)
        cv.putText(img, "maxDir", (minx[0] - 25, minx[1] - 25),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        result = np.where(contours[:,:,0] == np.amin(contours[:,:,0]))

        maxx = contours[result[0]][0][0]

        euclid_esq =  np.sqrt((maxx[0]-cx)**2 + (maxx[1]-cy)**2)
        print("EUCLID ESQ", euclid_esq)

        cv.circle(img, tuple(maxx), 5, [255, 0, 0], -1)
        cv.putText(img, "maxEsq", (maxx[0] - 25, maxx[1] - 25),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


        result = np.where(contours[:,:,1] == np.amin(contours[:,:,1]))

        maxy = contours[result[0]][0][0]

        euclid_cima = np.sqrt((maxy[0]-cx)**2 + (maxy[1]-cy)**2)
        print("EUCLID CIMA", euclid_cima)

        cv.circle(img, tuple(maxy), 5, [0, 0, 255], -1)
        cv.putText(img, "maxCima", (maxy[0] - 25, maxy[1] - 25),cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


        if euclid_cima > euclid_dir and euclid_cima > euclid_esq and euclid_cima > 100 and abs(euclid_esq - euclid_cima) > 15 and euclid_esq < 120:
            cima += 1

        elif abs(euclid_esq - euclid_cima) < 15 and euclid_esq > 100 and abs(euclid_dir < euclid_esq):
            esq += 1

        elif euclid_dir > 115 and euclid_dir > euclid_cima and euclid_dir > euclid_esq and euclid_cima < 100:
            dir += 1

        elif euclid_esq > 100 and euclid_cima > 100 and euclid_dir > 100:
            baixo += 1

        if cima == 3:
            snake_move = [False, True, False, False]
            print("CIMA")
            cima = 0
        elif esq == 3:
            snake_move = [False, False, True, False]
            print("ESQUERDA")
            esq = 0
        elif dir == 3:
            snake_move = [False, False, False, True]
            print("DIREITA")
            dir = 0
        elif baixo == 3:
            snake_move = [True, False, False, False]
            print("BAIXO")
            baixo = 0

        cv.imshow("trace", img)

 
        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()
 
            for event in pygame.event.get():
                measure = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
 
        
        else:
            if snake_move[2] == True:
                x1_change = -snake_block
                y1_change = 0
            elif snake_move[3] == True:
                x1_change = snake_block
                y1_change = 0
            elif snake_move[1] == True:
                y1_change = -snake_block
                x1_change = 0
            elif snake_move[0] == True:
                y1_change = snake_block
                x1_change = 0
 
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
 
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
 
        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)
 
        pygame.display.update()

        #print("------------------------") 
        #print("X: ", abs(x1 - foodx))
        #print("Y: ", abs(y1 - foody))
        #print("------------------------")
        
        if (abs(x1 - foodx) < 30 and abs(y1 - foody) < 30):
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
 
        clock.tick(snake_speed)
 
    cam.release()
    cv.destroyAllWindows()
    pygame.quit()
    quit()


gameLoop()


