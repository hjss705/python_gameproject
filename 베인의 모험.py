import sys
import time
import pygame

pygame.init()

white = (255, 255 ,255)

#초기화면 이미지파일,사운드파일
titleIMG = pygame.image.load('images/title.png')
startIMG = pygame.image.load('images/starticon.png')
quitIMG = pygame.image.load('images/quiticon.png')
clickStartIMG = pygame.image.load('images/clickedStartIcon.png')
clickQuitIMG = pygame.image.load('images/clickedQuitIcon.png')
explosion_sound = pygame.mixer.Sound('explosion.wav')
startmusic = pygame.mixer.Sound('startmusic.wav')

#초기화면 구성사이즈 및 이름
display_width = 800
display_height = 400
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('베인의 모험')

clock = pygame.time.Clock()

#스타트버튼 또는 종료버튼을 누를시 동작되게 설정
class Button:
    def __init__(self, img_in, x, y, width, height, img_act, x_act,y_act,action =None):
        mouse = pygame.mouse.get_pos() #마우스 좌표 저장
        click = pygame.mouse.get_pressed() #클릭시
        if x + width > mouse[0] > x and y + height > mouse[1] > y: #이미지 안에 있으면
            gameDisplay.blit(img_act,(x_act, y_act)) #클릭 이미지 로드
            if click[0] and action != None:
                time.sleep(1)                  # 1초동안 지연
                action()                       # 지정함수 호출
        else:
            gameDisplay.blit(img_in,(x,y))         #마우스가 이미지 바깥이면 일반 이미지 로드

#게임종료
def quitgame():
    pygame.quit()
    sys.exit()


#초기화면
def mainmenu():
    global titletext,startButton,quitButton

    menu = True

    pygame.mixer.Sound.play(startmusic)

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        gameDisplay.fill(white)

        titletext = gameDisplay.blit(titleIMG, (100,50))
        startButton = Button(startIMG,280,260,60,20,clickStartIMG,273,258,selectScreen)
        quitButton = Button(quitIMG,445,260,60,20,clickQuitIMG,440,258,quitgame)
        pygame.display.update()
        clock.tick(15)

#게임실행화면으로 넘어가게하는함수
def selectScreen():
    import pygame
    import random
    from time import sleep


    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    pad_width = 1024
    pad_height = 512
    background_width = 1024
    aircraft_width = 90
    aircraft_height = 55
    poro_width = 110
    poro_height = 67

    temo1_width = 140
    temo1_height = 60
    temo2_width = 86
    temo2_height = 60

#라이프포인트를 구현
    def drawScore(count):
        global gamepad

        font = pygame.font.SysFont(None, 30)
        text = font.render('Life point = ' + str(count), True, RED)
        gamepad.blit(text, (0, 0))

#dispMessage함수를 사용해 게임오버를표시
    def gameOver():
        global gamepad
        pygame.mixer.Sound.play(explosion_sound)
        dispMessage('GAME OVER')

#게임화면에 표시될 텍스트 모양과 영역설정
    def textObj(text, font):
        textSurFace = font.render(text, True, WHITE)
        return textSurFace, textSurFace.get_rect()

#게임오버를 구현하기위한 함수 / 게임오버시 2초간정지후 다시시작
    def dispMessage(text):
        global gamepad

        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = textObj(text, largeText)
        TextRect.center = ((pad_width / 2), (pad_height / 2))
        gamepad.blit(TextSurf, TextRect)
        pygame.display.update()
        sleep(2)
        runGame()
#적들과 충돌시 발생하는 문구
    def crash():
        global gamepad
        pygame.mixer.Sound.play(explosion_sound)
        dispMessage('Die .. !')

#게임판에 그려지는 모든객체
    def drawObject(obj, x, y):
        global gamepad
        gamepad.blit(obj, (x, y))

#게임이 구동되는 함수
    def runGame():
        global gamepad, clock, aircraft, background1, background2
        global poro, temos, bullet, boom , shot_sound

        isShotporo = False
        boom_count = 0

        poro_passed = 3

        bullet_xy = []

        x = pad_width * 0.01
        y = pad_height * 0.75
        y_change = 0

        background1_x = 0
        background2_x = background_width

        poro_x = pad_width
        poro_y = random.randrange(0, pad_height)

        temo_x = pad_width
        temo_y = random.randrange(0, pad_height)
        random.shuffle(temos)
        temo = temos[0]

        crashed = False
        while not crashed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        y_change = -5
                    elif event.key == pygame.K_DOWN:
                        y_change = 5

                    elif event.key == pygame.K_LCTRL:
                        pygame.mixer.Sound.play(shot_sound)
                        bullet_x = x + aircraft_width
                        bullet_y = y + aircraft_height / 2
                        bullet_xy.append([bullet_x, bullet_y])

                    elif event.key == pygame.K_SPACE:
                        sleep(5)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        y_change = 0

            y += y_change
            gamepad.fill(WHITE)

            background1_x -= 2
            background2_x -= 2

            if background1_x == -background_width:
                background1_x = background_width

            if background2_x == -background_width:
                background2_x = background_width

            drawObject(background1, background1_x, 0)
            drawObject(background2, background2_x, 0)

            drawScore(poro_passed)

            if poro_passed == 0:
                gameOver()

            y += y_change
            if y < 0:
                y = 0
            elif y > pad_height - aircraft_height:
                y = pad_height - aircraft_height

            poro_x -= 9
            if poro_x <= 0:
                poro_passed -= 1
                poro_x = pad_width
                poro_y = random.randrange(0, pad_height)

            if temo == None:
                temo_x -= 14
            else:
                temo_x -= 14

            if temo_x <= 0:
                temo_x = pad_width
                temo_y = random.randrange(0, pad_height)
                random.shuffle(temos)
                temo = temos[0]

            if len(bullet_xy) != 0:
                for i, bxy in enumerate(bullet_xy):
                    bxy[0] += 15
                    bullet_xy[i][0] = bxy[0]
                    if bxy[0] > poro_x:
                        if bxy[1] > poro_y and bxy[1] < poro_y + poro_height:
                            bullet_xy.remove(bxy)
                            isShotporo = True
                    if bxy[0] >= pad_width:
                        try:
                            bullet_xy.remove(bxy)
                        except:
                            pass

            if x + aircraft_width > poro_x:
                if (y > poro_y and y < poro_y + poro_height) or \
                        (y + aircraft_height > poro_y and y + aircraft_height < poro_y + poro_height):
                    crash()

            if temo[1] != None:
                if temo[0] == 0:
                    temo_width = temo1_width
                    temo_height = temo1_height
                elif temo[0] == 1:
                    temo_width = temo2_width
                    temo_height = temo2_height

                if x + aircraft_width > temo_x:
                    if (y > temo_y and y < temo_y + temo_height) or \
                            (y + aircraft_height > temo_y and y + aircraft_height < temo_y + temo_height):
                        crash()

            # drawObject(poro, poro_x, poro_y)
            drawObject(aircraft, x, y)

            if len(bullet_xy) != 0:
                for bx, by in bullet_xy:
                    drawObject(bullet, bx, by)

            if not isShotporo:
                drawObject(poro, poro_x, poro_y)
            else:
                drawObject(boom, poro_x, poro_y)
                boom_count += 1
                if boom_count > 5:
                    boom_count = 0
                    poro_x = pad_width
                    poro_y = random.randrange(0, pad_height - poro_height)
                    isShotporo = False
                    pygame.mixer.Sound.play(porodie_sound)

            if temo[1] != None:
                drawObject(temo[1], temo_x, temo_y)

            pygame.display.update()
            clock.tick(60)
        pygame.quit()
        quit()

    def initGame():
        global gamepad, clock, aircraft, background1, background2
        global poro, temos, bullet, boom, explosion_sound , shot_sound , porodie_sound

        temos = []

        pygame.init()
        gamepad = pygame.display.set_mode((pad_width, pad_height))
        pygame.display.set_caption('베인의 모험')
        aircraft = pygame.image.load('images/click.png')
        background1 = pygame.image.load('images/background.png')
        background2 = background1.copy()
        poro = pygame.image.load('images/poro.png')
        temos.append((0, pygame.image.load('images/temo1.png')))
        temos.append((1, pygame.image.load('images/temo2.png')))
        explosion_sound = pygame.mixer.Sound('explosion.wav')
        shot_sound = pygame.mixer.Sound('shot.wav')
        porodie_sound = pygame.mixer.Sound('porodie.wav')

        boom = pygame.image.load('images/boom.png')

        for i in range(3):
            temos.append((i + 2, None))

        bullet = pygame.image.load('images/bullet.png')

        clock = pygame.time.Clock()
        runGame()

    if __name__ == '__main__':
        initGame()
mainmenu()
game_loop()