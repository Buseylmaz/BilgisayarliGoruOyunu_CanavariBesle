import time
import pygame,random
import mediapipe as mp
import numpy as np
import cv2

#Webcam ayarlama
webcam=cv2.VideoCapture(0)
webcam.set(3,1280)
webcam.set(4,720)

#pygame hazırlama
pygame.init()

#pencere oluşturma
genislik,yukseklik=1280,720
pencere=pygame.display.set_mode((genislik,yukseklik))

# Oyun Başlığı
pygame.display.set_caption('CANAVARI BESLE')

#Oyun arkaplan şarkısı ve efeklerin eklenmesi
pygame.mixer.music.load("Başlangıç.wav")
pygame.mixer.music.play(-1,0.0)
yemYemeSesi=pygame.mixer.Sound("Yeme.wav")

#FPS degerleri
saat=pygame.time.Clock()
FPS=30

#Karekter
oyuncu=pygame.image.load("oyuncu.png")
oyuncuKordinat=oyuncu.get_rect()
#ve yem tanımlama
yem=pygame.image.load("OyuncuYemi.png")
yemKordinat=yem.get_rect()

#Düşman yem tanımlama
düsmanYem=pygame.image.load("düsmanYem.png")
düsmanYemKordinat=düsmanYem.get_rect()

#Arkaplan
backGround=pygame.image.load("Background.jpg")
backGroundKordinat=backGround.get_rect()
#ve Gameover tanımlama
gameOver=pygame.image.load("game-over.png")
gameOverKordinat=gameOver.get_rect()


#kordinatlar
yemKordinat.topleft=(250,250)
düsmanYemKordinat.topright=(300, 300)
backGroundKordinat.center=(1280,720)
gameOverKordinat.center=(640,500)


#Yazı font ayarı
font=pygame.font.Font("Font.ttf", 64)

#Degişkenler
x,y,=500,500
skor=0
durum=True


#El modeli degişkeni //Mediapipe
elModeli= mp.solutions.hands

def SkorGoster(durum, renk, font, boyut):
    skorFont = pygame.font.SysFont(font, boyut)
    skorYazi = skorFont.render('Skor : ' + str(skor), True, (255, 255, 255), (107, 56, 147))
    skorKordinat = skorYazi.get_rect()
    skorKordinat.topleft = (20, 20)

    if durum == 1:
        skorKordinat.midtop = (genislik/10, 15)
    else:
        skorKordinat.midtop = (genislik/2, yukseklik/1.25)

    pencere.blit(skorYazi, skorKordinat)

def OyunKaybedildi():
    olYazi = font.render("ÖLDÜNÜZ ", True, (255, 255, 255), (111, 102, 131))
    olYaziKordinat = olYazi.get_rect()

    olYaziKordinat.midtop = (genislik/2, yukseklik/4)

    pencere.blit(gameOver,gameOverKordinat)
    pencere.blit(olYazi, olYaziKordinat)

    SkorGoster(0, (255, 255, 255), 'times', 20)
    skor=0
    pygame.display.flip();
    time.sleep(3);



#Oyun döngüsünün oluşturulması ve el modeli
with elModeli.Hands(min_tracking_confidence=0.5,min_detection_confidence=0.5,) as el:
    while durum:
        for etkinlik in pygame.event.get():
            if etkinlik.type==pygame.QUIT:
                durum=False

        #Bilgisayarlı görü ve opencv kodlarının hazırlanması
        kontrol,cerceve=webcam.read()

        cerceve=cv2.flip(cerceve,1)
        rgb=cv2.cvtColor(cerceve,cv2.COLOR_BGR2RGB)

        sonuc=el.process(rgb)

        if sonuc.multi_hand_landmarks:
            for elLandmark in sonuc.multi_hand_landmarks:
                for kordinat in elModeli.HandLandmark:
                    isaret=elLandmark.landmark[8]
                    x=int(isaret.x*genislik)
                    y=int(isaret.y*yukseklik)



        oyuncuKordinat.center=(x, y)
        rgb=np.rot90(rgb)
        img=pygame.surfarray.make_surface(rgb).convert()
        img=pygame.transform.flip(img,True,False)
        pencere.blit(img,(0,0))
        pencere.blit(backGround,backGroundKordinat)
        pencere.blit(oyuncu, oyuncuKordinat)
        pencere.blit(yem,yemKordinat)
        pencere.blit(düsmanYem, düsmanYemKordinat)


        if oyuncuKordinat.colliderect(yemKordinat):
            yemYemeSesi.play()
            yemKordinat.x=random.randint(0,genislik-32)
            yemKordinat.y=random.randint(121,yukseklik-32)
            düsmanYemKordinat.x = random.randint(0, genislik - 32)
            düsmanYemKordinat.y = random.randint(121, yukseklik - 32)
            skor+=1

        if oyuncuKordinat.colliderect(düsmanYemKordinat):
            yemYemeSesi.play()
            OyunKaybedildi()

        pygame.display.update()
        saat.tick(FPS)
    pygame.quit()





