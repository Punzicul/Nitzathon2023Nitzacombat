import pygame
import os
import socket
import threading
import math
import time

HOST = "192.168.1.226"
PORT = 5555
TYPE = "utf-8"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


pygame.init()

WIDTH, HEIGHT = 1000, 725
GRAVITY = 7


# creates screen and caption
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("All Star Battle Arena")

# time related 
FPS = 60
clock = pygame.time.Clock()

bgColor = (0, 0, 0)

# main colors which will be used in the UI
white = (222, 217, 217)
green = (0, 255, 0)
cyan = (21, 134, 220)
yellow = (219, 216, 9)
purple = (199, 9, 237)
red = (193, 29, 29)

startVoice = pygame.mixer.Sound("sounds/startingVoice.mp3")
startVoice.play()

# class of button (also handles normal texts)
class button():

    def __init__(self, text, color, secondColor, xPos, yPos, modifiable, font, size, centered, slideImg, inflateAmount, toGrow): # sets neccessary attributes to each instance of button
        self.text = text
        self.size = size
        self.fontName = font
        self.font = pygame.font.Font(font, size)
        self.startSize = size
        self.color = color
        self.xPos = xPos
        self.yPos = yPos
        self.surface = self.font.render(self.text, True, self.color)
        if centered:
            self.rect = self.surface.get_rect(center=(WIDTH // 2, yPos))
        else:
            self.rect = self.surface.get_rect(center=(self.xPos, self.yPos))
        self.secondColor = secondColor
        self.startColor = self.color
        self.backgroundColor = self.secondColor
        self.modifiable = modifiable
        if self.modifiable == False:
            self.bgRect = None
        else:
            self.bgRect = self.rect.inflate(inflateAmount, 0)
        self.hovered = False
        self.centered = centered
        self.slideImg = slideImg

        if slideImg != None:
            self.slideImg = pygame.image.load(slideImg)
            self.slideImgX = -64
            self.slideImg2 = pygame.image.load(slideImg)
            self.slideImgX2 = WIDTH + 64

        self.inflateAmount = inflateAmount
        self.toGrow = toGrow
    
    def setColor(self, color): # sets the color of the instance to the new color
        self.color = color
        self.surface = self.font.render(self.text, True, self.color)

    def setBackgroundColor(self, color): # sets background color
        self.backgroundColor = color
    
    def setText(self, text): # sets the text
        self.text = text
        self.surface = self.font.render(self.text, True, self.color)

    def isColliding(self, rect): # checks if the current object's rect is colliding with a given rect
        return self.rect.colliderect(rect)

    def animateSize(self, size): # animating the size of the text 
        currentSize = self.size
        newSize = size
    
        if currentSize > newSize:
            currentSize -= 2
        elif currentSize < newSize:
            currentSize += 2
    
        self.size = currentSize
        self.font = pygame.font.Font(self.fontName, int(currentSize))
        self.surface = self.font.render(self.text, True, self.color)
        if self.centered:
            self.rect = self.surface.get_rect(center=(WIDTH // 2, self.yPos))
        else:
            self.rect = self.surface.get_rect(center=(self.xPos, self.yPos))

        self.bgRect = self.rect.inflate(self.inflateAmount, 0)

    def animateTextColor(self, color): # animating the text color 
        currentColor = self.color
    
        currentR = currentColor[0]
        currentG = currentColor[1]
        currentB = currentColor[2]
    
        newR = color[0]
        newG = color[1]
        newB = color[2]
    
        speed = 10
    
        if currentR > newR:
            currentR = max(currentR - speed, newR)
        elif currentR < newR:
            currentR = min(currentR + speed, newR)
    
        if currentG > newG:
            currentG = max(currentG - speed, newG)
        elif currentG < newG:
            currentG = min(currentG + speed, newG)
    
        if currentB > newB:
            currentB = max(currentB - speed, newB)
        elif currentB < newB:
            currentB = min(currentB + speed, newB)
    
        self.setColor((int(currentR), int(currentG), int(currentB)))
    
    def animateBackgroundColor(self, color): # animating the background color
        currentColor = self.backgroundColor

        currentR = currentColor[0]
        currentG = currentColor[1]
        currentB = currentColor[2]

        newR = color[0]
        newG = color[1]
        newB = color[2]

        if currentR > newR and currentR - 12 >= 0:
            currentR -= 12
        elif currentR < newR and 255 - currentR > 12:
            currentR += 12
        
        if currentG > newG and currentG - 12 >= 0:
            currentG -= 12
        elif currentG < newG and 255 - currentG > 12:
            currentG += 12

        if currentB > newB and currentB - 12 >= 0:
            currentB -= 12
        elif currentB < newB and 255 - currentB > 12:
            currentB += 12
        
        self.setBackgroundColor((currentR, currentG, currentB))

    def animateSlideImg(self, direction):

        if self.slideImg != None:
            if direction == "increase":
                if self.slideImgX < self.rect.topleft[0] - 150:
                    self.slideImgX += 25
                if self.slideImgX2 > self.rect.topright[0] + 85:
                    self.slideImgX2 -= 25
            else:
                if self.slideImgX > -64 or self.slideImgX2 < WIDTH + 64:
                    self.slideImgX -= 25
                    self.slideImgX2 += 25

    def update(self, mouseRect): # update handles all the important button actions

        if self.modifiable:
            if self.isColliding(mouseRect): # handles all the animations and sounds for when a button is hovered
                if not self.hovered:
                    buttonHoverSound.play()
                    self.hovered = True

                if self.color != self.secondColor:
                    self.animateTextColor(self.secondColor)
                    self.animateBackgroundColor(self.startColor)
                    self.animateSize(self.startSize + self.toGrow)
                self.animateSlideImg("increase")

            else: # handles all the animations and sounds for when a button is not hovered
                self.hovered = False
                if self.color != self.startColor:
                    self.animateTextColor(self.startColor)
                    self.animateBackgroundColor(self.secondColor)
                    self.animateSize(self.startSize)
                self.animateSlideImg("decrease")

        
        if self.modifiable == True:
            pygame.draw.rect(screen, self.backgroundColor, self.bgRect)
            if self.slideImg != None:
                screen.blit(self.slideImg, (self.slideImgX, self.rect.topleft[1] + 10))
                screen.blit(self.slideImg, (self.slideImgX2, self.rect.topleft[1] + 10))

        screen.blit(self.surface, self.rect.topleft)
        

class sound(): # a class with an added canPlay method to handle cooldowns
    def __init__(self, path, canPlay):
        self.path = path
        self.sound = pygame.mixer.Sound(path)
        self.canPlay = canPlay
    
    def play(self):
        if self.canPlay:
            self.sound.play()

class characterCard():
    def __init__(self, type, xPos, yPos):
        self.type = type
        self.image = pygame.image.load(next(os.scandir(f"characters/{type}/idle")).path)       
        self.image = pygame.transform.scale(self.image, (192, 120))
        self.rect = self.image.get_rect()
        self.rect.center = (xPos, yPos)
        self.xPos = xPos
        self.yPos = yPos
        self.bgRect = self.rect.copy()
        padding = 40 
        self.bgRect.x += padding
        self.bgRect.width -= 2 * padding
        self.newRect = pygame.Rect(self.bgRect.bottomleft, (self.bgRect.width, self.bgRect.height // 2 - 10))
        self.font = pygame.font.Font("fonts/Gameplay.ttf", 17)
        self.name = self.font.render(type, True, (29, 75, 202))
        self.frame = pygame.image.load("images/charFrame.png")
        self.hovered = False
        self.playedSound = False
        self.displayImage = pygame.transform.scale(pygame.image.load(next(os.scandir(f"characters/{type}/idle")).path), (600, 375))
    
    def isColliding(self, other):
        if self.bgRect.colliderect(other) or self.newRect.colliderect(other):
            self.hovered = True
        else:
            self.hovered = False

    def clicked(self, mouseRect):
        return self.bgRect.colliderect(mouseRect) or self.newRect.colliderect(mouseRect)
    
    def update(self, mouseRect):
    
        self.isColliding(mouseRect)
    
        if self.hovered:
            if self.playedSound == False:
                buttonHoverSound.play()
            pygame.draw.rect(screen, red, self.bgRect)
            pygame.draw.rect(screen, (204, 153, 0), self.newRect)
            self.playedSound = True
        else:
            pygame.draw.rect(screen, white, self.bgRect)
            pygame.draw.rect(screen, (204, 153, 0), self.newRect)
            self.playedSound = False
            self.hovered = False
    
        # Calculate the position where the text should be drawn
        text_width, text_height = self.name.get_size()
        text_x = self.newRect.x + (self.newRect.width - text_width) // 2
        text_y = self.newRect.y + (self.newRect.height - text_height) // 2
    
        # Draw the text at the calculated position
        screen.blit(self.name, (text_x, text_y))
    
        # Update the image rect's center to match the bgRect's center
        self.rect.center = self.bgRect.center
    
        # Draw the character image at the updated position
        if self.type == "warrior":
            screen.blit(self.image, (self.rect.topleft[0] + 15, self.rect.topleft[1] - 5))
        elif self.type == "adventurer":
            screen.blit(self.image, (self.rect.topleft[0] + 7, self.rect.topleft[1] - 5))
    
        screen.blit(self.frame, self.bgRect.topleft)





buttonHoverSound = sound("sounds/buttonHover.mp3", True) # sound that plays when you hover over a button
buttonClickSound = pygame.mixer.Sound("sounds/buttonClick.mp3")  # sound that plays when you click a button

class SpriteSheet():
    def __init__(self, image_path, width, height, xPos, yPos):
        self.sheet = pygame.image.load(image_path).convert_alpha()
        self.frameIndex = 0
        self.width = width
        self.height = height
        self.sheetWidth = self.sheet.get_width()
        self.maxFrame = (self.sheetWidth // self.width) - 1
        self.xPos = xPos
        self.yPos = yPos

    def get_image(self, frame, width, height, scale, colour):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(colour)

        return image

    def update(self):
        screen.blit(self.get_image(int(self.frameIndex), self.width, self.height, 5, (0, 0, 0   )), (self.xPos, self.yPos))

        if self.frameIndex > self.maxFrame:
            self.frameIndex = 0
            return "end"
        else:
            self.frameIndex += 0.2
 
        
    
    
def update_animation(hovered, current, current2, start, repeat, end, start2, repeat2, end2):
    if hovered:
        res = current.update()
        current2.update()
        if res == "end" and current == start:
            current = repeat
            current2 = repeat2
    else:
        if current != start:
            current = end
            current2 = end2
            res = current.update()
            current2.update()
            if res == "end" and current == end:
                current = start
                current2 = start2
    return current, current2

def mainMenu():

    # creating neccessary bottons and titles  
    titleImage = pygame.image.load("images/titleImage.png")

    play = button("PLAY", purple, bgColor, WIDTH // 2, 200, True, "fonts/Gameplay.ttf", 50, True, "images/swords.png", 50, 20)
    settings = button("SETTINGS", green, bgColor, WIDTH // 2, 350, True, "fonts/Gameplay.ttf", 50, True, "images/setting.png", 50, 20)
    help = button("HELP", cyan, bgColor, WIDTH // 2, 500, True, "fonts/Gameplay.ttf", 50, True, "images/question.png", 50, 20)
    store = button("STORE", yellow, bgColor, WIDTH // 2, 650, True, "fonts/Gameplay.ttf", 50, True, "images/wreath.png", 50, 20)
    
    greenRepeat = SpriteSheet("images/greenLoopFlame.png", 24, 32, 850, 256)
    greenStart = SpriteSheet("images/greenStartFlame.png", 24, 32, 850, 256)
    greenEnd = SpriteSheet("images/greenEndFlame.png", 24, 32, 850, 256)

    greenRepeat2 = SpriteSheet("images/greenLoopFlame.png", 24, 32, 50, 256)
    greenStart2 = SpriteSheet("images/greenStartFlame.png", 24, 32, 50, 256)
    greenEnd2 = SpriteSheet("images/greenEndFlame.png", 24, 32, 50, 256)

    currentGreen = greenStart
    currentGreen2 = greenStart2

    purpleRepeat = SpriteSheet("images/purpleLoopFlame.png", 24, 32, 850, 106)
    purpleStart = SpriteSheet("images/purpleStartFlame.png", 24, 32, 850, 106)
    purpleEnd = SpriteSheet("images/purpleEndFlame.png", 24, 32, 850, 106)

    purpleRepeat2 = SpriteSheet("images/purpleLoopFlame.png", 24, 32, 50, 106)
    purpleStart2 = SpriteSheet("images/purpleStartFlame.png", 24, 32, 50, 106)
    purpleEnd2 = SpriteSheet("images/purpleEndFlame.png", 24, 32, 50, 106)

    currentPurple = purpleStart
    currentPurple2 = purpleStart2

    orangeRepeat = SpriteSheet("images/orangeLoopFlame.png", 24, 32, 850, 556)
    orangeStart = SpriteSheet("images/orangeStartFlame.png", 24, 32, 850, 556)
    orangeEnd = SpriteSheet("images/orangeEndFlame.png", 24, 32, 850, 556)

    orangeRepeat2 = SpriteSheet("images/orangeLoopFlame.png", 24, 32, 50, 556)
    orangeStart2 = SpriteSheet("images/orangeStartFlame.png", 24, 32, 50, 556)
    orangeEnd2 = SpriteSheet("images/orangeEndFlame.png", 24, 32, 50, 556)

    currentOrange = orangeStart
    currentOrange2 = orangeStart2

    blueRepeat = SpriteSheet("images/blueLoopFlame.png", 24, 32, 850, 406)
    blueStart = SpriteSheet("images/blueStartFlame.png", 24, 32, 850, 406)
    blueEnd = SpriteSheet("images/blueEndFlame.png", 24, 32, 850, 406)

    blueRepeat2 = SpriteSheet("images/blueLoopFlame.png", 24, 32, 50, 406)
    blueStart2 = SpriteSheet("images/blueStartFlame.png", 24, 32, 50, 406)
    blueEnd2 = SpriteSheet("images/blueEndFlame.png", 24, 32, 50, 406)

    currentBlue = blueStart
    currentBlue2 = blueStart2
    
    # storing them
    buttons = [play, settings, help, store]


    run = True
    
    # loading rotating star images
    star1 = pygame.image.load("images/star.png")
    star2 = pygame.image.load("images/star.png")

    # initial star degree
    firstDegree = 0
    secondDegree = 0

    backgroundToDisplay = None

    while run: # main loop
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                for currentButton in buttons:
                    if currentButton.modifiable == True and currentButton.hovered == True: # gets here if a clickable button was clicked
                        buttonClickSound.play()
                        return currentButton.text # returns the text withing the button to figure out what button was clicked outside of the function
                        
                    
        # creating a rect of the mouse
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseRect = pygame.Rect(mouseX, mouseY, 1, 1)

        screen.fill(bgColor)

        screen.blit(titleImage, (0, -15))

        if play.hovered:
            backgroundToDisplay = pygame.image.load("images/menuPlayBackground.png")
            screen.blit(backgroundToDisplay, (0, 126))
        
        if settings.hovered:
            backgroundToDisplay = pygame.image.load("images/settingButtonBackground.png")
            screen.blit(backgroundToDisplay, (0, 276))

        if help.hovered:
            backgroundToDisplay = pygame.image.load("images/helpButtonBackground.png")
            screen.blit(backgroundToDisplay, (0, 426))

        if store.hovered:
            backgroundToDisplay = pygame.image.load("images/storeHoveredImage.png")
            screen.blit(backgroundToDisplay, (0, 576))

        # drawing dividing lines
        pygame.draw.line(screen, white, (0, 120), (WIDTH, 120), 10)
        pygame.draw.line(screen, white, (0, 270), (WIDTH, 270), 10)
        pygame.draw.line(screen, white, (0, 420), (WIDTH, 420), 10)
        pygame.draw.line(screen, white, (0, 570), (WIDTH, 570), 10)
        pygame.draw.line(screen, white, (0, 720), (WIDTH, 720), 10)

        # getting the star rects
        star1_rect = star1.get_rect(center=(35, 50))
        star2_rect = star2.get_rect(center=(968, 50))

        # Rotate the stars
        rotated_star1 = pygame.transform.rotate(star1, firstDegree)
        rotated_star2 = pygame.transform.rotate(star2, secondDegree)

        # Set the center of the rotated stars to the center of the original rectangles
        rotated_star1_rect = rotated_star1.get_rect(center=star1_rect.center)
        rotated_star2_rect = rotated_star2.get_rect(center=star2_rect.center)

        # Blit the rotated stars onto the screen
        screen.blit(rotated_star1, rotated_star1_rect.topleft)
        screen.blit(rotated_star2, rotated_star2_rect.topleft)

        currentGreen, currentGreen2 = update_animation(settings.hovered, currentGreen, currentGreen2, greenStart, greenRepeat, greenEnd, greenStart2, greenRepeat2, greenEnd2)
        currentPurple, currentPurple2 = update_animation(play.hovered, currentPurple, currentPurple2, purpleStart, purpleRepeat, purpleEnd, purpleStart2, purpleRepeat2, purpleEnd2)
        currentBlue, currentBlue2 = update_animation(help.hovered, currentBlue, currentBlue2, blueStart, blueRepeat, blueEnd, blueStart2, blueRepeat2, blueEnd2)
        currentOrange, currentOrange2 = update_animation(store.hovered, currentOrange, currentOrange2, orangeStart, orangeRepeat, orangeEnd, orangeStart2, orangeRepeat2, orangeEnd2)

        # increment/decrement the degrees of the stars
        firstDegree -= 2
        secondDegree += 2

        for currentButton in buttons: # loop through all buttons
            currentButton.update(mouseRect) # handle all button actions (passing mouseRect to handle mouse hovers and collisions)

        pygame.display.update()

def store():
    run = True
    backgroundImage = pygame.image.load("images/storeBackground.png")
    buyButton = button("BUY", (255, 179, 0), (255, 255, 255), 180, 650, True, "fonts/Gameplay.ttf", 35, False, None, 5, 5)

    cointText = "COINS: "
    pointsFile = open("points", "r")
    cointText += pointsFile.read()
    pointsFile.close()

    coins = button(cointText, (255, 179, 0), (255, 255, 255), 180, 200, False, "fonts/Gameplay.ttf", 35, False, None, 5, 5)
    price = button("COST: 60", (255, 179, 0), (0, 0, 0), 180, 700, True, "fonts/Gameplay.ttf", 27, False, None, 2, 0)

    unlocked = button("UNLOCKED", (255, 179, 0), (0, 0, 0), 180, 650, False, "fonts/Gameplay.ttf", 27, False, None, 2, 0)

    dataFile = open("database", "r")
    data = dataFile.read().split(":")[1]
    isWizard = data == "unlocked"

    dataFile.close()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buyButton.hovered and isWizard == False:
                    data = open("database", "w")
                    data.write("wizard:unlocked")
                    isWizard = True

                    points = open("points", "r")
                    currentPoints = int(points.read()) - 60
                    points.close()
                    points = open("points", "w")
                    points.write(f"{currentPoints}")
                    points.close()
                    coins.setText(f"COINS: {currentPoints}")
                    data.close()


        mousePosition = pygame.mouse.get_pos()
        mouseRect = pygame.rect.Rect(mousePosition[0], mousePosition[1], 1, 1)

        screen.blit(backgroundImage, (0, 0))

        if isWizard == False:
            buyButton.update(mouseRect)
            price.update(mouseRect)
        else:
            unlocked.update(mouseRect)

        coins.update(mouseRect)

        pygame.display.update()
    
def help(): # handles the help window

    # all neccessary titles and buttons for the help section
    text1 = button("HOW TO PLAY:", cyan, bgColor, WIDTH // 2, 50, False, "fonts/Gameplay.ttf", 70, True, None, 0, 20)
    text3 = button("LMB - MELEE ATTACK", red, bgColor, WIDTH // 2, 200, False, "fonts/Gameplay.ttf", 50, True, None, 0, 20)
    text4 = button("C - CROUCH", red, bgColor, WIDTH // 2, 275, False, "fonts/Gameplay.ttf", 50, True, None, 0, 20)
    text5 = button("A - LEFT", red, bgColor, WIDTH // 2, 350, False, "fonts/Gameplay.ttf", 50, True, None, 0, 20)
    text6 = button("D - RIGHT", red, bgColor, WIDTH // 2, 425, False, "fonts/Gameplay.ttf", 50, True, None, 0, 20)
    text7 = button("SPACE - JUMP", red, bgColor, WIDTH // 2, 500, False, "fonts/Gameplay.ttf", 50, True, None, 0, 20)
    text8 = button("R - SPECIAL ATTACK", red, bgColor, WIDTH // 2, 575, False, "fonts/Gameplay.ttf", 50, True, None, 0, 20)
    text9 = button("BACK TO MENU", cyan, bgColor, WIDTH // 2, 680, True, "fonts/Gameplay.ttf", 50, True, None, 40, 10)

    buttons = [text1, text3, text4, text5, text6, text7, text8, text9] # storing them

    run = True

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for currentButton in buttons:
                    if currentButton.hovered == True and currentButton.modifiable == True: # only clickable buttons
                        buttonClickSound.play()
                        run = False

        # mouseRect
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseRect = pygame.Rect(mouseX, mouseY, 1, 1)

        screen.fill(bgColor)

        # drawing dividing line
        pygame.draw.line(screen, cyan, (0, 120), (WIDTH, 120), 10)

        # handling buttons/titles
        for currentButton in buttons:
            currentButton.update(mouseRect)
        
        pygame.display.update()


def settings(volumePrecentage): # handles the setting window

    # all neccessary buttons/titles
    title1 = button("SETTINGS", green, bgColor, WIDTH // 2, 50, False, "fonts/Gameplay.ttf", 70, True, None, 0, 20)
    volumeTitle = button("VOLUME:", purple, bgColor, 150, 200, False, "fonts/Gameplay.ttf", 50, False, None, 0, 20)
    decrease = button("DECREASE", purple, bgColor, 165, 275, True, "fonts/Gameplay.ttf", 30, False, None, 10, 20)
    increase = button("INCREASE", purple, bgColor, 750, 275, True, "fonts/Gameplay.ttf", 30, False, None, 10, 20)
    returnToMenu = button("RETURN TO MENU", green, bgColor, 225, 675, True, "fonts/Gameplay.ttf", 40, True, None, 40, 10)

    run = True

    buttons = [title1, volumeTitle, decrease, increase, returnToMenu]

    volumeRect = pygame.Rect(300, 180, volumePrecentage * 5, 40) # creates a rect of height 40 and width of the volumePrecentage * 5 to visualize the sound bar

    backgroundImage = pygame.image.load("images/settingsBackground.png")
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for currentButton in buttons:
                    if currentButton.hovered and currentButton.modifiable: # handles all buttons seperately
                        if currentButton.text == "DECREASE" and volumePrecentage > 0:
                            volumePrecentage -= 5
                            buttonClickSound.play()
                            volumeRect.width = volumePrecentage * 5 # sets the width to the new volume precentage * 5
                            bgMusic.set_volume(volumePrecentage / 100)
                        elif currentButton.text == "INCREASE" and volumePrecentage < 100:
                            volumePrecentage += 5
                            buttonClickSound.play()
                            volumeRect.width = volumePrecentage * 5
                            bgMusic.set_volume(volumePrecentage / 100)
                        elif currentButton.text == "RETURN TO MENU":
                            buttonClickSound.play()
                            return volumePrecentage # returns the volumePrecentage (exits the function)
                        
        # mouse rect
        mouseX, mouseY = pygame.mouse.get_pos()
        mouseRect = pygame.Rect(mouseX, mouseY, 1, 1)

        screen.fill(bgColor)

        # drawing lines and rects
        pygame.draw.line(screen, green, (0, 120), (WIDTH, 120), 10)
        pygame.draw.rect(screen, purple, volumeRect)

        for currentButton in buttons: # looping through all buttons
            currentButton.update(mouseRect)
        
        pygame.display.update()


class backgroundRect:
    def __init__(self, type, xPos, yPos, width, height, firstColor, secondColor):
        self.firstColor = firstColor
        self.secondColor = secondColor
        self.type = type
        self.xPos = xPos
        self.yPos = yPos
        self.width = width
        self.height = height
        self.color = firstColor
        self.rect = pygame.rect.Rect(self.xPos, self.yPos, self.width, self.height)

    def isColliding(self, otherRect):
        return self.rect.colliderect(otherRect)
    
    def checkCollision(self, mouseRect):
        if self.isColliding(mouseRect):
            self.color = self.secondColor
        else:
            self.color = self.firstColor
    
    def update(self, mouseRect):
        self.checkCollision(mouseRect)
        pygame.draw.rect(screen, self.color, self.rect)
        
def characterSelection():
    
    run = True
    character = None
    background = pygame.image.load("images/NinjaBackground.png")
    selectionBars = pygame.image.load("images/WizardLocked.png")

    dataFile = open("../Hackathon - Destruction/database", "r")
    isWizard = False
    for line in dataFile.readlines():
        if line.split(":")[0] == "wizard":
            if line.split(":")[1] == "unlocked":
                selectionBars = pygame.image.load("images/WizardUnlocked.png")
                isWizard = True

    dataFile.close()
                
    # text, color, secondColor, x, y, modifiable, font, size, centered, sliding image, inflation size, grow size
    returnToMenu = button("RETURN TO MENU", (29, 75, 202), (204, 153, 0), 240, 50, True, "fonts/Gameplay.ttf", 40, False, None, 10, 4)
    confirm = button("CONFIRM CHARACTER", (29, 75, 202), (204, 153, 0), WIDTH - 270, 50, True, "fonts/Gameplay.ttf", 40, False, None, 10, 4)

    startX = 85
    yPosition = 440
    gap = 34

    firstColor = (46, 9, 76)
    secondColor = (55, 55, 55)

    warriorRect = backgroundRect("warrior", startX-2, yPosition-2, 80, 105, firstColor, secondColor)
    adventurerRect = backgroundRect("adventurer", startX-2 + (gap + 75), yPosition-2, 80, 105, firstColor, secondColor)
    reaperRect = backgroundRect("reaper", startX - 2 + ((gap + 73) * 2), yPosition-2, 80, 105, firstColor, secondColor)

    warriorDisplay = pygame.image.load("images/warriorDisplay.png")
    adventurerDisplay = pygame.image.load("images/adventurerDisplay.png")
    reaperDisplay = pygame.image.load("images/reaperDisplay.png")
    wizardDisplay = pygame.image.load("images/wizardDisplay.png")

    if isWizard:
        wizardRect = backgroundRect("wizard", startX - 2 + ((gap + 73) * 3), yPosition - 2, 80, 105, firstColor, secondColor)
        allRects = [warriorRect, adventurerRect, reaperRect, wizardRect]
    else:
        allRects = [warriorRect, adventurerRect, reaperRect]

    while run:

        mousePosition = pygame.mouse.get_pos()
        mouseRect = pygame.rect.Rect(mousePosition[0], mousePosition[1], 1, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                for rect in allRects:
                    if rect.isColliding(mouseRect):
                        character = rect.type
                if returnToMenu.hovered:
                    run = False
                    return "QUIT"
                if confirm.hovered and character != None:
                    return character
                

        screen.blit(background, (0, 0))

        warriorRect.update(mouseRect)
        adventurerRect.update(mouseRect)
        reaperRect.update(mouseRect)
        if isWizard:
            wizardRect.update(mouseRect)

        screen.blit(selectionBars, (0, 0))

        if character == "warrior":
            screen.blit(warriorDisplay, (WIDTH//2 - 120, 75))
        if character == "reaper":
            screen.blit(reaperDisplay, (WIDTH//2 - 120, 120))
        if character == "adventurer":
            screen.blit(adventurerDisplay, (WIDTH//2 - 160, 120))
        if character == "wizard":
            screen.blit(wizardDisplay, (0, 0))
        returnToMenu.update(mouseRect)
        confirm.update(mouseRect)

        pygame.display.update()


bgMusic = pygame.mixer.Sound("sounds/backgroundMusic.mp3") # loading in background music
bgMusic.play(-1) # making the music play forever
bgMusic.set_volume(0.9)
volumePrecentage = 100 # setting initial precentage to 0

import threading

def waitingRoom():
    run = True
    background = "images/NinjaBackground.png"
    background = pygame.image.load(background)

    returnToMenu = button("RETURN TO MENU", (29, 75, 202), (204, 153, 0), 240, 50, True, "fonts/Gameplay.ttf", 50, True, None, 10, 4)
    waiting = button("WAITING FOR PLAYERS.", (32, 170, 205), (204, 153, 0), WIDTH//2, 300, False, "fonts/Gameplay.ttf", 60, False, None, 10, 4)

    count = 0

    def receive():
        nonlocal run
        while run:
            try:
                message = client.recv(1024).decode(TYPE)
                if message == "ready":
                    run = False
            except socket.error:
                pass

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if returnToMenu.hovered:
                    return "QUIT"

        mousePos = pygame.mouse.get_pos()
        mouseRect = pygame.rect.Rect(mousePos[0], mousePos[1], 1, 1)

        screen.blit(background, (0, 0))
        returnToMenu.update(mouseRect)
        waiting.update(mouseRect)

        # update display
        if len(waiting.text.split("S")[1]) == 3 and count == 30:
            waiting = button("WAITING FOR PLAYERS.", (32, 170, 205), (204, 153, 0), WIDTH//2, 300, False, "fonts/Gameplay.ttf", 60, False, None, 10, 4)
            count = 0
        elif len(waiting.text.split("S")[1]) == 1 and count == 30:
            waiting = button("WAITING FOR PLAYERS..", (32, 170, 205), (204, 153, 0), WIDTH//2, 300, False, "fonts/Gameplay.ttf", 60, False, None, 10, 4)
            count = 0
        elif len(waiting.text.split("S")[1]) == 2 and count == 30:
            waiting = button("WAITING FOR PLAYERS...", (32, 170, 205), (204, 153, 0), WIDTH//2, 300, False, "fonts/Gameplay.ttf", 60, False, None, 10, 4)
            count = 0
        
        count += 1

        screen.blit(background, (0, 0))
        returnToMenu.update(mouseRect)
        waiting.update(mouseRect)

        pygame.display.update()

    # return a value indicating that the game should start
    return "ready"


def manageSocket(client, action):
    if action == "connect":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        return client
    elif action == "disconnect":
        client.close()

class character():
    def __init__(self, type, xPos, yPos, groundHeight, attackDamage, specialDamage, attackCooldown, jumpCooldown, jumpHeight, attackSpeed, health, facing, attackNumber, attackRange, specialAttackRange, realType):

        self.groundHeight = groundHeight

        self.currentRect = None

        self.realType = realType
        self.attackRange = attackRange
        self.dead = False
        self.moving = False
        # default movement values
        self.xVelocity = 0
        self.yVelocity = 0
        self.xPos = xPos
        self.yPos = yPos

        # type of character
        self.type = type

        self.animationsDir = "characters/" + type.strip() # root directory of animation

        self.attackNumber = attackNumber

        self.newWidth = 200
        self.newHeight = 150

        # gets all animations
        self.idleAnimation = [pygame.transform.scale(pygame.image.load(self.animationsDir + "/idle" + "/" + file.name), (self.newWidth, self.newHeight)) for file in os.scandir(self.animationsDir + "/idle")]
        self.attackAnimation = [pygame.transform.scale(pygame.image.load(self.animationsDir + "/attack" + "/" + file.name), (self.newWidth, self.newHeight))  for file in os.scandir(self.animationsDir + "/attack")]
        self.attackAnimation2 = [pygame.transform.scale(pygame.image.load(self.animationsDir + "/secondAttack" + "/" + file.name), (self.newWidth, self.newHeight))  for file in os.scandir(self.animationsDir + "/secondAttack")]
        if self.attackNumber == 3:
            self.attackAnimation3 = [pygame.transform.scale(pygame.image.load(self.animationsDir + "/thirdAttack" + "/" + file.name), (self.newWidth, self.newHeight))  for file in os.scandir(self.animationsDir + "/thirdAttack")]
        self.crouchAnimation = [pygame.transform.scale(pygame.image.load(self.animationsDir + "/crouch" + "/" + file.name), (self.newWidth, self.newHeight))  for file in os.scandir(self.animationsDir + "/crouch")]
        self.runAnimation = [pygame.transform.scale(pygame.image.load(self.animationsDir + "/run" + "/" + file.name), (self.newWidth, self.newHeight))  for file in os.scandir(self.animationsDir + "/run")]
        self.hurtAnimation = [pygame.transform.scale(pygame.image.load(self.animationsDir + "/hurt" + "/" + file.name), (self.newWidth, self.newHeight))  for file in os.scandir(self.animationsDir + "/hurt")]
        self.jumpAnimation = [pygame.transform.scale(pygame.image.load(self.animationsDir + "/jump" + "/" + file.name), (self.newWidth, self.newHeight))  for file in os.scandir(self.animationsDir + "/jump")]
        self.deathAnimation = [pygame.transform.scale(pygame.image.load(self.animationsDir + "/death" + "/" + file.name), (self.newWidth, self.newHeight))  for file in os.scandir(self.animationsDir + "/death")]

        self.currentAnimation = self.idleAnimation
        self.currentFrame = 0   
        self.isAnimating = False
        self.animationSpeed = 0.1
        self.last_jump_time = 0
        self.last_attack_time = 0
        self.isMoving = False  # Add this flag to track if the   character is moving or not

        self.attackDamage = attackDamage
        self.specialDamage = specialDamage
        self.attackCooldown = attackCooldown
        self.jumpCooldown = jumpCooldown
        self.attackSpeed = attackSpeed
        self.jumpHeight = jumpHeight

        self.health = health
        self.healthPrecent = 100

        self.specialEnergy = 0
        self.desiredPrecent = 100


        if facing == "right":
            self.barPositionX, self.barPositionY = 159, 69
            self.energyPositionX, self.energyPositionY = 159, 93
        else:
            self.barPositionX, self.barPositionY = 552, 70
            self.energyPositionX, self.energyPositionY = 619, 94

        self.hpRect = pygame.rect.Rect(self.barPositionX, self.barPositionY, 290, 20)
        self.emptyHpRect = self.hpRect

        self.emptyEnergyRect = pygame.rect.Rect(self.energyPositionX, self.energyPositionY, 223, 10)
        self.EnergyRect = pygame.rect.Rect(self.energyPositionX, self.energyPositionY, 0, 10)

        self.facing = facing

        self.currentAttack = self.attackAnimation

        if attackNumber > 2:
            self.lastAttack = self.attackAnimation3
        else:
            self.lastAttack = self.attackAnimation2
        
        self.stunned = False
        self.dead = False

        self.opp = None

        self.isTurned = False

        self.knockedBack = False
        self.knockCount = 0
        self.knockBackSpeed = None

        self.specialAttackRange = specialAttackRange



    def rotate_animations(self, flip):
        self.idleAnimation = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.animationsDir + "/idle" + "/" + file.name), (self.newWidth, self.newHeight)), flip, False) for file in os.scandir(self.animationsDir + "/idle")]
        self.attackAnimation = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.animationsDir + "/attack" + "/" + file.name), (self.newWidth, self.newHeight)), flip, False) for file in os.scandir(self.animationsDir + "/attack")]
        self.crouchAnimation = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.animationsDir + "/crouch" + "/" + file.name), (self.newWidth, self.newHeight)), flip, False) for file in os.scandir(self.animationsDir + "/crouch")]
        self.runAnimation = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.animationsDir + "/run" + "/" + file.name), (self.newWidth, self.newHeight)), flip, False) for file in os.scandir(self.animationsDir + "/run")]
        self.attackAnimation2 = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.animationsDir + "/secondAttack" + "/" + file.name), (self.newWidth, self.newHeight)), flip, False)  for file in os.scandir(self.animationsDir + "/secondAttack")]
        if self.attackNumber == 3:
            self.attackAnimation3 = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.animationsDir + "/thirdAttack" + "/" + file.name), (self.newWidth, self.newHeight)), flip, False)  for file in os.scandir(self.animationsDir + "/thirdAttack")]
        self.hurtAnimation = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.animationsDir + "/hurt" + "/" + file.name), (self.newWidth, self.newHeight)), flip, False) for file in os.scandir(self.animationsDir + "/hurt")]
        self.jumpAnimation = [pygame.transform.flip(pygame.transform.scale(pygame.image.load(self.animationsDir + "/jump" + "/" + file.name), (self.newWidth, self.newHeight)), flip, False) for file in os.scandir(self.animationsDir + "/jump")]



    def attack(self):
        if not self.dead:
            self.currentAnimation = self.currentAttack
            self.currentFrame = 0
            self.isAnimating = True
            self.animationSpeed = self.attackSpeed
    
            if self.currentAttack == self.attackAnimation:
                self.currentAttack = self.attackAnimation2
            elif self.currentAttack == self.attackAnimation2 and self.attackNumber == 3:
                self.currentAttack = self.attackAnimation3
            else:
                self.currentAttack = self.attackAnimation
    
            self.last_attack_time = pygame.time.get_ticks()

    def jump(self):
        if self.yPos == self.groundHeight:  # Only allow jumping if character is on the ground
            self.currentAnimation = self.jumpAnimation
            self.animationSpeed = 0.5
            self.isAnimating = True
            self.currentFrame = 0
            self.yVelocity = self.jumpHeight  # Adjust initial upward velocity
            self.last_jump_time = pygame.time.get_ticks()  # Store the time of the last jump
    
    def takeDmg(self, dmg, other):
        # calculate the precentage of the health
        
        onePrecent = self.health / 100
        precentToTake = dmg / onePrecent

        self.healthPrecent -= precentToTake
        self.hpRect = pygame.rect.Rect(self.barPositionX, self.barPositionY, self.healthPrecent* 2 * 1.5, 20)


        if other.specialEnergy < 100: # increases special energy bar every hit
            other.specialEnergy += 10
            other.EnergyRect = pygame.rect.Rect(other.energyPositionX, other.energyPositionY, other.EnergyRect.width + 223/10, 10)
        
        # handles hit deaths and stuns
        if self.healthPrecent <= 0:
            self.dead = True
        else:
            self.stunned = True 
    

    def update(self):
        if not self.dead and not self.stunned:

            self.currentFrame += self.animationSpeed

            if self.currentFrame >= len(self.currentAnimation) - 1:
                self.currentFrame = 0
    
                if self.currentAnimation == self.idleAnimation or self.currentAnimation == self.runAnimation:
                    if self.currentAnimation == self.idleAnimation:
                        self.animationSpeed = 0.1
                    else:
                        self.animationSpeed = 0.25
                else:
                    self.currentAnimation = self.idleAnimation
                    self.isAnimating = False
                    self.animationSpeed = 0.25
            
            self.yPos += self.yVelocity
            self.xPos += self.xVelocity
    
            # Update isMoving flag based on xVelocity
            self.isMoving = self.xVelocity != 0
    
            # Update the current animation based on the character's xVelocity and isMoving flag
            if not self.isAnimating:
                if self.isMoving:
                    self.currentAnimation = self.runAnimation
                    self.animationSpeed = 0.35
                elif not self.isMoving and self.currentAnimation != self.idleAnimation:
                    self.currentAnimation = self.idleAnimation
                    self.animationSpeed = 0.1
    
            frame = self.currentAnimation[int(self.currentFrame) % len(self.currentAnimation)]

            self.currentRect = frame.get_rect()

            if self.realType == 1:
                if self.xVelocity < 0:
                    self.facing = "left"
                    self.isTurned = True
                elif self.xVelocity > 0:
                    self.facing = "right"
                    self.isTurned = False
            else:
                if self.xVelocity < 0:
                    self.facing = "left"
                    self.isTurned = False
                elif self.xVelocity > 0:
                    self.facing = "right"
                    self.isTurned = True  

            if self.isTurned:
                screen.blit(pygame.transform.flip(frame, True, False), (self.xPos, self.yPos))
            else:
                screen.blit(frame, (self.xPos, self.yPos))
            
            if self.currentAnimation != self.jumpAnimation:
                if self.yPos < self.groundHeight and self.currentAnimation != self.jumpAnimation:
                    self.yVelocity += GRAVITY//2
                elif self.yPos >= self.groundHeight:
                    self.yPos = self.groundHeight
                    self.yVelocity = 0
                    if self.currentAnimation == self.jumpAnimation:
                        self.isAnimating = False
        
                self.yPos += self.yVelocity
        elif self.dead:

            if self.currentAnimation != self.deathAnimation:
                self.currentFrame = 0
                self.animationSpeed = 0.25
                self.currentAnimation = self.deathAnimation
                frame = self.currentAnimation[int(self.currentFrame) % len(self.currentAnimation)]

            # while the frame is not the last frame increase the current frame

            if self.currentFrame < len(self.currentAnimation) - 1:
                self.currentFrame += self.animationSpeed
                frame = self.currentAnimation[int(self.currentFrame) % len(self.currentAnimation)]
            else:
                frame = self.currentAnimation[len(self.currentAnimation) - 1]
            screen.blit(frame, (self.xPos, self.yPos))

        elif self.stunned:
            if self.currentAnimation != self.hurtAnimation:
                self.currentFrame = 0
                self.animationSpeed = 0.1
                self.currentAnimation = self.hurtAnimation
                frame = self.currentAnimation[int(self.currentFrame) % len(self.currentAnimation)]
            
            if self.currentFrame >= len(self.currentAnimation) - 1:
                self.stunned = False
            
            if self.stunned:
                frame = self.currentAnimation[int(self.currentFrame) % len(self.currentAnimation)]
                screen.blit(frame, (self.xPos, self.yPos))
                self.currentFrame += self.animationSpeed
        
        if self.knockedBack:

            if self.knockBackSpeed < 0:
                if self.knockCount < 200 and self.xPos > 0:
                    self.xPos += self.knockBackSpeed
                    self.knockCount += 20
                else:
                    self.knockedBack = False
                    self.knockCount = 0
            else:
                if self.knockCount < 200 and self.xPos < WIDTH - self.newWidth:
                    self.xPos += self.knockBackSpeed
                    self.knockCount += 20
                else:
                    self.knockedBack = False
                    self.knockCount = 0
            if self.knockCount < 200 and self.xPos > -50 and self.xPos < 800:
                self.xPos += self.knockBackSpeed
                self.knockCount += 20
            else:
                self.knockedBack = False
                self.knockCount = 0
            

        pygame.draw.rect(screen, white, self.emptyHpRect)
        pygame.draw.rect(screen, red, self.hpRect)

        pygame.draw.rect(screen, white, self.emptyEnergyRect)
        pygame.draw.rect(screen, (0, 0, 255), self.EnergyRect)


class warrior(character):
    def __init__(self, type, xPos, yPos, groundHeight, attackDamage, specialDamage, attackCooldown, jumpCooldown, jumpHeight, attackSpeed, health, facing, attackNumber, attackRange, specialAttackRange, rType):
        super().__init__(type, xPos, yPos, groundHeight, attackDamage, specialDamage, attackCooldown, jumpCooldown, jumpHeight, attackSpeed, health, facing, attackNumber, attackRange, specialAttackRange, rType)
    def specialAttack():
        pass

independent = []

class adventurer(character):
    def __init__(self, type, xPos, yPos, groundHeight, attackDamage, specialDamage, attackCooldown, jumpCooldown, jumpHeight, attackSpeed, health, facing, attackNumber, attackRange, specialAttackRange, rType):
        super().__init__(type, xPos, yPos, groundHeight, attackDamage, specialDamage, attackCooldown, jumpCooldown, jumpHeight, attackSpeed, health, facing, attackNumber, attackRange, specialAttackRange, rType)
        self.special_attack_start_time = None
        self.wind_sound_played = False
        self.cut_sound_played = False
        self.special_attack_activated = False

    def specialAttack(self):
        pass

class reaper(character):
    def __init__(self, type, xPos, yPos, groundHeight, attackDamage, specialDamage, attackCooldown, jumpCooldown, jumpHeight, attackSpeed, health, facing, attackNumber, attackRange, specialAttackRange, rType):
        super().__init__(type, xPos, yPos, groundHeight, attackDamage, specialDamage, attackCooldown, jumpCooldown, jumpHeight, attackSpeed, health, facing, attackNumber, attackRange, specialAttackRange, rType)
    def specialAttack():
        pass

class wizard(character):
    def __init__(self, type, xPos, yPos, groundHeight, attackDamage, specialDamage, attackCooldown, jumpCooldown, jumpHeight, attackSpeed, health, facing, attackNumber, attackRange, specialAttackRange, rType):
        super().__init__(type, xPos, yPos, groundHeight, attackDamage, specialDamage, attackCooldown, jumpCooldown, jumpHeight, attackSpeed, health, facing, attackNumber, attackRange, specialAttackRange,rType)
        self.special_attack_start_time = None
    def specialAttack(self):
        pass

def collidesWith(player1, player2):
    xPos1, yPos1 = player1.xPos, player1.yPos
    xPos2, yPos2 = player2.xPos, player2.yPos

    # distance formula
    distance = math.sqrt(math.pow((xPos1 - xPos2), 2) + math.pow((yPos1 - yPos2), 2))

    # warrior distance = 80
    # adventurer distance = 100

    return distance

class independentAnimations:
    def __init__(self, type, directory, xPos, yPos, xVelocity, yVelocity, animationSpeed, flipped):
        self.type = type
        self.flipped = flipped
        self.directory = directory
        self.xPos = xPos
        self.yPos = yPos
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity
        self.finished = False

        if type == "normal":
            self.frames = [pygame.transform.flip(pygame.image.load(f"{directory}/{file.name}"), flipped, False) for file in os.scandir(directory)]
        else:
            self.image = pygame.image.load(self.directory)

        if type == "normal":
            self.frameAmount = len(self.frames) - 1
            self.currentFrame = 0
            self.animationSpeed = animationSpeed
    
    def update(self):

        if self.type == "normal":
            frame = self.frames[int(self.currentFrame) % self.frameAmount]
    
            if self.currentFrame < self.frameAmount:
                self.currentFrame += self.animationSpeed
            else:
                self.finished = True
            
            screen.blit(frame, (self.xPos, self.yPos))
        else:
            screen.blit(self.image, (self.xPos, self.yPos))

        self.xPos += self.xVelocity
        self.yPos += self.yVelocity




        
def startGame(char, client):

    countSound = pygame.mixer.Sound("sounds/countSound.mp3")
    client.send("getChar".encode(TYPE))
    opponentCharacter = client.recv(1024).decode(TYPE)

    victoryScreen = pygame.image.load("images/victoryScreen.png")
    defeatScreen = pygame.image.load("images/defeatScreen.png")

    background = pygame.image.load("maps/secondMap.png")
    groundHeight = 200
    originalPlayerHeight = (HEIGHT - groundHeight) // 2 + 95

    # creating all character instances

    adventurer1 = adventurer("adventurer", 100, originalPlayerHeight, originalPlayerHeight, 30, 55, 1000, 400, -25, 0.35, 550, "right", 3, 105, 600, 1)
    adventurer2 = adventurer("adventurer", WIDTH - 200 - 100, originalPlayerHeight, originalPlayerHeight, 30, 55, 450, 400, -25, 0.35, 550, "left", 3, 105, 600, 2)

    warrior1 = warrior("warrior", 100, originalPlayerHeight, originalPlayerHeight, 35, 125, 1000, 600, -20, 0.45, 850, "right", 2, 105, 600, 1)
    warrior2 = warrior("warrior", WIDTH - 200 - 100, originalPlayerHeight, originalPlayerHeight, 35, 125, 1000, 600, -20, 0.45, 850, "left", 2, 105, 600, 2)

    reaper1 = reaper("reaper", 100, originalPlayerHeight, originalPlayerHeight, 40, 125, 2000, 600, -30, 0.24, 800, "right", 2, 105, 600, 1)
    reaper2 = reaper("reaper", WIDTH - 100 - 200, originalPlayerHeight, originalPlayerHeight, 40, 125, 2000, 600, -30, 0.24, 800, "left", 2, 105, 600, 2)

    wizard1 = wizard("wizard", 100, originalPlayerHeight, originalPlayerHeight, 35, 125, 1000, 600, -20, 0.45, 600, "right", 2, 150, 600, 1)
    wizard2 = wizard("wizard", WIDTH - 100 - 200, originalPlayerHeight, originalPlayerHeight, 35, 125, 1000, 600, -20, 0.45, 600, "left", 2, 150, 600, 2)

    seconds = 0
    minutes = 0
    timeString = "0:00"
    lastSecondTime = pygame.time.get_ticks()

    timeFont = pygame.font.Font("fonts/Gameplay.ttf", 20)
    timeText = timeFont.render(timeString, True, (0, 0, 0))

    defeatReturnToMenu = button("RETURN TO MENU", (0,0,0), red, 0, HEIGHT//2 + 250, True, "fonts/Gameplay.ttf", 50, True, None, 40, 10)
    victoryReturnToMenu = button("RETURN TO MENU", (0,0,0), yellow, 0, HEIGHT//2 + 250, True, "fonts/Gameplay.ttf", 50, True, None, 40, 10)

    if char == "warrior":
        playerCharacter = warrior1
    elif char == "adventurer":
        playerCharacter = adventurer1
    elif char == "reaper":
        playerCharacter = reaper1
    elif char == "wizard":
        playerCharacter = wizard1

    if opponentCharacter == "warrior":
        opponentCharacter = warrior2
    elif opponentCharacter == "adventurer":
        opponentCharacter = adventurer2
    elif opponentCharacter == "reaper":
        opponentCharacter = reaper2
    elif opponentCharacter == "wizard":
        opponentCharacter = wizard2
        
    playerCharacter.opp = opponentCharacter
    opponentCharacter.opp = playerCharacter


    straightSlash = pygame.mixer.Sound("sounds/straightSlash.mp3")
    cleaveSlash = pygame.mixer.Sound("sounds/cleaveSlash.mp3")
    missSlash = pygame.mixer.Sound("sounds/missSlash.mp3")
    spinningSlash = pygame.mixer.Sound("sounds/spinningSlash.mp3")

    firstMagic = pygame.mixer.Sound("sounds/firstMagic.mp3")
    secondMagic = pygame.mixer.Sound("sounds/secondMagic.mp3")

    run = True

    opponentCharacter.rotate_animations(True)

    barString = ""
    healthBar = None

    barString += playerCharacter.type.lower()
    barString += "vs"
    barString += opponentCharacter.type.lower()
    barString += ".png"

    barDir = "../Hackathon - Destruction/gameGuis"

    
    for bar in os.scandir(barDir):
        nameOfBar = bar.name.lower()

        if nameOfBar == barString:
            healthBar = pygame.image.load(f"{barDir}/{bar.name}")

    font = pygame.font.Font("fonts/Gameplay.ttf", 200)

    countText = font.render("3", True, (255, 255, 255))
    countText2 = font.render("2", True, (255, 255, 255))
    countText3 = font.render("1", True, (255, 255, 255))
    countText4 = font.render("FIGHT", True, (255, 0, 0))

    currentText = countText

    def handleOpponent():   
        nonlocal opponentCharacter
        while run:
            try:
                messages = client.recv(4128).decode(TYPE)
                for message in messages.strip().split('\n'):

                    #print(f"Received message: {message}")
                    
                    if message.split(":")[0] == "velo":
                        try:
                            opponentCharacter.xVelocity = int(message.split(":")[1]) * -1
                            if opponentCharacter.xVelocity != 0:
                                opponentCharacter.xPos = 1000 - int(message.split(":")[2])
                                opponentCharacter.yPos = int(message.split(":")[3])
                        except:
                            pass
                    elif message.split(":")[0] == "attack":
                        try:
                            sound = message.split(":")[1]
                            print("played sound")
                            pygame.mixer.Sound(f"sounds/{sound}.mp3").play()
                            opponentCharacter.attack()
                        except:
                            pass
                    elif message == "jump":
                        try:
                            opponentCharacter.jump()
                        except:
                            pass
                    elif message.split(":")[0] == "dmg":
                        try:
                            playerCharacter.takeDmg(int(message.split(":")[1]), opponentCharacter)
                            independent.append(independentAnimations("normal", "../Hackathon - Destruction/bloodAnimations/rightBlood", playerCharacter.xPos - 75, opponentCharacter.yPos, 0, 0, 0.3, True))
                        except:
                            pass
                        
                    elif message.split(":")[0] == "knockback":
                        try:
                            playerCharacter.knockedBack = True
                            playerCharacter.knockBackSpeed = int(message.split(":")[1])*-1
                            playerCharacter.knockCount = 0
                            pygame.mixer.Sound("sounds/knockbackSound.mp3").play()
                        except:
                            pass

                    if playerCharacter.dead or opponentCharacter.dead:
                        return
                    
            except socket.error:
                pass


    handleOpp = threading.Thread(target=handleOpponent)
    handleOpp.start()

    playerCharacter.stunned = True
    opponentCharacter.stunned = True

    hasStarted = False
    lastSecond = pygame.time.get_ticks()

    countSound.play()

    addedPoints = False

    while run:
        clock.tick(FPS)

        mousePosition = pygame.mouse.get_pos()
        mouseRect = pygame.rect.Rect(mousePosition[0], mousePosition[1], 1, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if playerCharacter.dead:
                if event.type == pygame.MOUSEBUTTONDOWN and defeatReturnToMenu.hovered:
                    buttonClickSound.play()
                    return "MENU"
            if opponentCharacter.dead:
                if event.type == pygame.MOUSEBUTTONDOWN and victoryReturnToMenu.hovered:
                    buttonClickSound.play()
                    return "MENUQUIT"
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                currentAttackTime = pygame.time.get_ticks()

                cooldown_passed = currentAttackTime - playerCharacter.last_attack_time

                if playerCharacter.attackNumber > 2:

                    if cooldown_passed >= playerCharacter.attackCooldown + 200 and playerCharacter.currentAttack != playerCharacter.attackAnimation3:
                        playerCharacter.currentAttack = playerCharacter.attackAnimation
                else:
                    if cooldown_passed >= playerCharacter.attackCooldown + 200 and playerCharacter.currentAttack != playerCharacter.attackAnimation2:
                        playerCharacter.currentAttack = playerCharacter.attackAnimation
                        
                if not playerCharacter.isAnimating and cooldown_passed >= playerCharacter.attackCooldown or playerCharacter.currentAttack == playerCharacter.lastAttack and not playerCharacter.isAnimating or playerCharacter.currentAttack == playerCharacter.attackAnimation2 and not playerCharacter.isAnimating and not playerCharacter.dead and not playerCharacter.stunned and not opponentCharacter.dead:

                    playerCharacter.attack()

                    if collidesWith(playerCharacter, opponentCharacter) <= playerCharacter.attackRange and (playerCharacter.xPos < opponentCharacter.xPos and playerCharacter.facing == "right" or playerCharacter.xPos > opponentCharacter.xPos and playerCharacter.facing == "left"):
                        client.send(f"dmg:{playerCharacter.attackDamage}\n".encode(TYPE))
                        opponentCharacter.takeDmg(playerCharacter.attackDamage, playerCharacter)

                        independent.append(independentAnimations("normal", "bloodAnimations/rightBlood", opponentCharacter.xPos+100, opponentCharacter.yPos, 0, 0, 0.3, False))

                        if (playerCharacter.attackNumber == 3 and playerCharacter.currentAttack == playerCharacter.attackAnimation) or (playerCharacter.attackNumber == 2 and playerCharacter.currentAttack == playerCharacter.attackAnimation):
                            if playerCharacter.facing == "right":
                                opponentCharacter.knockedBack = True
                                opponentCharacter.knockBackSpeed = 20
                                opponentCharacter.knockCount = 0
                                pygame.mixer.Sound("sounds/knockbackSound.mp3").play()

                            elif playerCharacter.facing == "left":
                                opponentCharacter.knockedBack = True
                                opponentCharacter.knockBackSpeed = -20
                                opponentCharacter.knockCount = 0
                                pygame.mixer.Sound("sounds/knockbackSound.mp3").play()

                            client.send(f"knockback:{opponentCharacter.knockBackSpeed}\n".encode(TYPE))
                        
                        if char == "warrior" or char == "reaper": 
                            if playerCharacter.currentAttack == playerCharacter.attackAnimation:
                                straightSlash.play()
                                playedSound = "straightSlash"
                            else:
                                cleaveSlash.play()
                                playedSound = "cleaveSlash"
                        elif char == "adventurer":
                            if playerCharacter.currentAttack == playerCharacter.attackAnimation:
                                cleaveSlash.play()
                                playedSound = "cleavetSlash"
                            if playerCharacter.currentAttack == playerCharacter.attackAnimation2:
                                straightSlash.play()
                                playedSound = "straightSlash"
                            if playerCharacter.currentAttack == playerCharacter.attackAnimation3:
                                spinningSlash.play()
                                playedSound = "spinningSlash"
                        elif char == "wizard":
                            if playerCharacter.currentAttack == playerCharacter.attackAnimation:
                                firstMagic.play()
                                playedSound = "firstMagic"
                            if playerCharacter.currentAttack == playerCharacter.attackAnimation2:
                                secondMagic.play()           
                                playedSound = "secondMagic"                 
                    else:
                        if not playerCharacter.dead:
                            missSlash.play()
                            playedSound = "missSlash"

                    # attack sound handling
                    if not playerCharacter.dead:
                        client.send(f"attack:{playedSound}\n".encode(TYPE))
                    continue
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_time = pygame.time.get_ticks()
                    cooldown_passed = current_time - playerCharacter.last_jump_time >= playerCharacter.jumpCooldown

                    canJump = not playerCharacter.isAnimating and playerCharacter.yPos == playerCharacter.groundHeight and cooldown_passed and not playerCharacter.dead and not playerCharacter.stunned

                    if canJump:
                        playerCharacter.jump()
                        client.send("jump\n".encode(TYPE))
            
                elif event.key == pygame.K_r:

                    canAttack = not playerCharacter.isAnimating and not playerCharacter.stunned and not playerCharacter.dead and not opponentCharacter.dead
                    barFull = 220 == playerCharacter.EnergyRect.width
                    didFace = (opponentCharacter.xPos < playerCharacter.xPos and playerCharacter.facing == "left") or (opponentCharacter.xPos > playerCharacter.xPos and playerCharacter.facing == "right")
                    isTheSameHeight = playerCharacter.yPos > opponentCharacter.yPos-50 and playerCharacter.yPos < opponentCharacter.yPos + 50

                    inRange = math.sqrt(math.pow(opponentCharacter.xPos - playerCharacter.xPos, 2) + math.pow(opponentCharacter.yPos - playerCharacter.yPos, 2)) <= playerCharacter.specialAttackRange
                    
                    if canAttack and barFull and didFace and isTheSameHeight and inRange:
                        playerCharacter.EnergyRect = pygame.rect.Rect(playerCharacter.energyPositionX, playerCharacter.energyPositionY, 0, playerCharacter.EnergyRect.height)



        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] and not playerCharacter.stunned and not playerCharacter.dead and playerCharacter.xPos < 800:
            playerCharacter.xVelocity = 12
            playerCharacter.moving = True
        elif keys[pygame.K_a] and not playerCharacter.stunned and not playerCharacter.dead and playerCharacter.xPos > -50:
            playerCharacter.xVelocity = -12
            playerCharacter.moving = True
        else:
            playerCharacter.xVelocity = 0
            playerCharacter.moving = False

        screen.blit(background, (0, 0))
        if not playerCharacter.dead and not opponentCharacter.dead:
            screen.blit(healthBar, (0, 0))

        playerCharacter.update()
        opponentCharacter.update()

        client.send(f"velo:{playerCharacter.xVelocity}:{playerCharacter.xPos}:{playerCharacter.yPos}\n".encode(TYPE))

        currentTime = pygame.time.get_ticks()

        if currentTime - lastSecondTime >= 1000:
            if seconds == 60:
                minutes += 1
                seconds = 0
            else:
                seconds += 1

            if seconds < 10:
                timeString = f"{minutes}:0{seconds}"
                
            else:
                timeString = f"{minutes}:{seconds}"

            lastSecondTime = pygame.time.get_ticks()

        timeText = timeFont.render(timeString, True, (255, 255, 255))

        screen.blit(timeText, (WIDTH//2 - 23, 75))

        if playerCharacter.dead:
            screen.blit(defeatScreen, (0, 0))
            defeatReturnToMenu.update(mouseRect)

        elif opponentCharacter.dead:
            if addedPoints == False:
                pointsFile = open("points", "r")
                points = int(pointsFile.read()) + 10
                pointsFile.close()
    
                pointsFile = open("points", "w")
                pointsFile.write(str(points))
                pointsFile.close()
                addedPoints = True

            screen.blit(victoryScreen, (0, 0))
            victoryReturnToMenu.update(mouseRect)


        for animation in independent:
            animation.update()


        if hasStarted == False:
            playerCharacter.stunned = True
            opponentCharacter.stunned = True
            currentSecond = pygame.time.get_ticks()

            if currentSecond - lastSecond >= 1000:
                lastSecond = currentSecond
                if currentText == countText:
                    currentText = countText2
                elif currentText == countText2:
                    currentText = countText3
                elif currentText == countText3:
                    currentText = countText4
                else:
                    playerCharacter.stunned = False
                    opponentCharacter.stunned = False
                    hasStarted = True

            if currentText == countText4:
                screen.blit(currentText, (175, 200))
            else:
                screen.blit(currentText, (400, 200))
        
        pygame.display.update()


client = None

while True:
    if client is None:
        client = manageSocket(client, "connect")

    result = mainMenu() # calls the main menu and gets the name of the button the user clicked in the menu

    # uses the result to determine which function to call
    if result == "HELP":
        help()
    if result == "SETTINGS":
        volumePrecentage = settings(volumePrecentage) # sets the volume to the new volume the user selected (this way the rect will be the same width you left it when you go back to settings)
    if result == "STORE":
        store()
    if result == "PLAY":
        chosenCharacter = characterSelection()
        if chosenCharacter != "QUIT":

            client.send(f"char:{chosenCharacter}".encode(TYPE))
            message = client.recv(1024).decode(TYPE)

            if message != "ready": 
                waitingResult = waitingRoom()
                if waitingResult == "ready":
                    
                    gameResult = startGame(chosenCharacter, client)

                    client.send("quit".encode(TYPE))
                    client = manageSocket(client, "disconnect")
                    client = None
                    continue

                if waitingResult == "QUIT":
                    client.send("quit".encode(TYPE))
                    client = manageSocket(client, "disconnect")
                    client = None
                    continue
            elif message == "ready":
                result = startGame(chosenCharacter, client)
                client.send("quit".encode(TYPE))
                client = manageSocket(client, "disconnect")
                client = None
                continue

    if result == "QUIT":
        if client is not None:
            client.send("quit".encode(TYPE))
            client = manageSocket(client, "disconnect")
        break

pygame.quit() # ends the program