import pygame
import random

def game(nation): # nation potrzebne do wyboru czołgu
    """
    Gra "Battle City 1941" ispirowana klasyczną grą "Battle City".
    """
    pygame.init()

    screen_width = 1200 # szerokość ekranu
    screen_height = 700 # długość ekranu

    win = pygame.display.set_mode((screen_width,screen_height)) # wymiary okienka gry
    pygame.display.set_caption("Battle City 1941") # tytuł gry

    #tło
    bg=pygame.image.load('images/background.png')
    #mury
    brick=pygame.image.load('images/brick.png')
    brick_with_cracks=pygame.image.load('images/brick with cracks.png')
    concrete=pygame.image.load('images/concrete.png')
    #pociski
    bullet_down=pygame.image.load('images/bullet down.png')
    bullet_up=pygame.image.load('images/bullet up.png')
    bullet_left=pygame.image.load('images/bullet left.png')
    bullet_right=pygame.image.load('images/bullet right.png')
    enemy_bullet_down=pygame.image.load('images/enemy bullet down.png')
    enemy_bullet_up=pygame.image.load('images/enemy bullet up.png')
    enemy_bullet_left=pygame.image.load('images/enemy bullet left.png')
    enemy_bullet_right=pygame.image.load('images/enemy bullet right.png')
    #baza
    military_base=pygame.image.load('images/base.png')
    #efekty dźwiękowe
    tank_shot=pygame.mixer.Sound('sounds/tank shot.wav')
    no_ammo=pygame.mixer.Sound('sounds/no ammo.wav')
    hit=pygame.mixer.Sound('sounds/hit.wav')
    collision=pygame.mixer.Sound('sounds/collision wall.wav')

    clock = pygame.time.Clock() # zegar

    class player():
        """
        Klasa player() opisuje czołg gracza.
        """
        def __init__(self, x, y):
            """
            Metoda __init__(self,x,y) tworzy czołg gracza. Przyjmuje pozycję początkową x,y.
            Ustawia parametry czołgu w zależności od wybranego rodzaju - nation.
            """
            self.x = x
            self.y = y
            if nation == "soviet":
                # grafiki
                self.drive_right=pygame.image.load('images/soviet right.png')
                self.drive_left=pygame.image.load('images/soviet left.png')
                self.drive_up=pygame.image.load('images/soviet up.png')
                self.drive_down=pygame.image.load('images/soviet down.png')
                self.vel = 3 # szybkość czołgu
                self.ammo = 4 # amunicja czołgu
                self.hpmax = 2 # maksymalne punkty życia
                self.hp = 2 # aktulane punkty życia
                
            elif nation == "american":
                # grafiki
                self.drive_right=pygame.image.load('images/american right.png')
                self.drive_left=pygame.image.load('images/american left.png')
                self.drive_up=pygame.image.load('images/american up.png')
                self.drive_down=pygame.image.load('images/american down.png')
                self.vel = 3 # szybkość czołgu
                self.ammo = 3 # amunicja czołgu
                self.hpmax = 3 # maksymalne punkty życia
                self.hp = 3 # aktulane punkty życia

            elif nation == "british":
                # grafiki
                self.drive_right=pygame.image.load('images/british right.png')
                self.drive_left=pygame.image.load('images/british left.png')
                self.drive_up=pygame.image.load('images/british up.png')
                self.drive_down=pygame.image.load('images/british down.png')
                self.vel = 2
                self.ammo = 3
                self.hpmax = 4
                self.hp = 4 # aktulane punkty życia

            elif nation == "french":
                # grafiki
                self.drive_right=pygame.image.load('images/french right.png')
                self.drive_left=pygame.image.load('images/french left.png')
                self.drive_up=pygame.image.load('images/french up.png')
                self.drive_down=pygame.image.load('images/french down.png')
                self.vel = 4 # szybkość czołgu
                self.ammo = 3 # amunicja czołgu
                self.hpmax = 2 # maksymalne punkty życia
                self.hp = 2 # aktulane punkty życia

                
            self.width = 42 # szerokość czołgu
            self.height = 100 # wysokość czołgu
            self.left = False
            self.right = False
            self.up = True # czołg zaczyna zwrócony w górę
            self.down = False
            self.hitbox = (self.x, self.y, self.width, self.height) # hitbox czołgu

        def draw(self,win):
            """
            Funkcja draw(self,win) służy do rysowania czołgu gracza i jego paska życia.
            """
            if self.left:
                win.blit(self.drive_left, (self.x,self.y))

            elif self.right:
                win.blit(self.drive_right, (self.x,self.y))

            elif self.up:
                win.blit(self.drive_up, (self.x,self.y))

            elif self.down:
                win.blit(self.drive_down, (self.x,self.y))

            pygame.draw.rect(win,(255,0,0), (self.x+(self.width//2-25),self.y -20, 50, 10 )) # czerwony pasek
            pygame.draw.rect(win,(0,255,0), (self.x+(self.width//2-25),self.y -20, 50 - ((50//self.hpmax)*(self.hpmax - self.hp)), 10 )) # pasek życia zielony

            self.hitbox = (self.x, self.y, self.width, self.height)

    class projectile():
        """
        Klasa projectile() opisuje pociski gracza.
        """
        
        def __init__(self, x, y, direction):
            """
            Metoda __init__(self,x,y,direction) tworzy pocisk garcza w punkcie o współrzędnych x,y zwrócony w stronę równą direction.
            """
            self.x = x
            self.y = y
            self.direction = direction # kierunek pocisku
            self.velx = 0 # szybkość po x
            self.vely = 0 # szybkość po y

        def draw(self,win):
            """
            Funkcja draw(self,win) rysuje pocisk gracza lecący w kierunku równym direction.
            """
            if self.direction == "down":
                win.blit(bullet_down,(self.x,self.y))
                self.velx = 0
                self.vely = 5
            elif self.direction == "up":
                win.blit(bullet_up,(self.x,self.y))
                self.velx= 0
                self.vely = -5
            elif self.direction == "right":
                win.blit(bullet_right,(self.x,self.y))
                self.velx = 5
                self.vely = 0
            elif self.direction == "left":
                win.blit(bullet_left,(self.x,self.y))
                self.velx = -5
                self.vely = 0

    class enemy_projectile():
        """
        Klasa projectile() opisuje pociski wroga.
        """
        
        def __init__(self, x, y, direction):
            """
            Metoda __init__(self,x,y,direction) tworzy pocisk wroga w punkcie o współrzędnych x,y zwrócony w stronę równą direction.
            """
            self.x = x
            self.y = y
            self.direction = direction
            self.velx = 0
            self.vely = 0

        def draw(self,win):
            """
            Funkcja draw(self,win) rysuje pocisk wroga lecący w kierunku równym direction.
            """
            if self.direction == "down":
                win.blit(enemy_bullet_down,(self.x,self.y))
                self.velx = 0
                self.vely = 5
            elif self.direction == "up":
                win.blit(enemy_bullet_up,(self.x,self.y))
                self.velx= 0
                self.vely = -5
            elif self.direction == "right":
                win.blit(enemy_bullet_right,(self.x,self.y))
                self.velx = 5
                self.vely = 0
            elif self.direction == "left":
                win.blit(enemy_bullet_left,(self.x,self.y))
                self.velx = -5
                self.vely = 0

    class enemy():
        """
        Klasa enemy() opisuje czołg wroga.
        """

        def __init__(self,x,y,nation):
            """
            Metoda __init__(self,x,y) tworzy czołg gracza. Przyjmuje pozycję początkową x,y.
            Ustawia parametry czołgu w zależności od wybranego rodzaju - nation.
            """
            self.x = x
            self.y = y
            self.nation = nation
            if self.nation == "german":
                # grafiki
                self.drive_right=pygame.image.load('images/german right.png')
                self.drive_left=pygame.image.load('images/german left.png')
                self.drive_up=pygame.image.load('images/german up.png')
                self.drive_down=pygame.image.load('images/german down.png')
                self.vel = 3 # szybkość czołgu
                self.hpmax = 3 # amunicja czołgu
                self.hp = 3 # maksymalne punkty życia
                self.ammo = 3
                
            elif self.nation == "italian":
                # grafiki
                self.drive_right=pygame.image.load('images/italian right.png')
                self.drive_left=pygame.image.load('images/italian left.png')
                self.drive_up=pygame.image.load('images/italian up.png')
                self.drive_down=pygame.image.load('images/italian down.png')
                self.vel = 4 # szybkość czołgu
                self.ammo = 3 # amunicja czołgu
                self.hpmax = 2 # maksymalne punkty życia
                self.hp = 2 # aktulane punkty życia

            elif self.nation == "japanese":
                # grafiki
                self.drive_right=pygame.image.load('images/japanese right.png')
                self.drive_left=pygame.image.load('images/japanese left.png')
                self.drive_up=pygame.image.load('images/japanese up.png')
                self.drive_down=pygame.image.load('images/japanese down.png')
                self.vel = 3 # szybkość czołgu
                self.ammo = 4 # amunicja czołgu
                self.hpmax = 2 # maksymalne punkty życia
                self.hp = 2 # aktulane punkty życia

            elif self.nation == "waffen-ss":
                # grafiki
                self.drive_right=pygame.image.load('images/waffen-ss right.png')
                self.drive_left=pygame.image.load('images/waffen-ss left.png')
                self.drive_up=pygame.image.load('images/waffen-ss up.png')
                self.drive_down=pygame.image.load('images/waffen-ss down.png')
                self.vel = 2 # szybkość czołgu
                self.ammo = 3 # amunicja czołgu
                self.hpmax = 4 # maksymalne punkty życia
                self.hp = 4 # aktulane punkty życia
                
            self.width = 100 # szerokość czołgu
            self.height = 42 # wysokość czołgu
            self.hitbox = (self.x, self.y, self.width, self.height) # hitbox czołgu
            self.left = False
            self.right = False
            self.up = False
            self.down = False
            self.newpos = [(random.randint(400,600)//self.vel)*self.vel,(random.randint(400,600)//self.vel)*self.vel] # cel, do którego ma jechać czołg
                        
        def move(self):
            """
            Funkcja move(self) służy do tworzenia losowego ruchu czołgu wroga.
            """
            
            if self.x != self.newpos[0] or self.y != self.newpos[1]: # gdy czołg wroga nie dotarł do celu
                
                if self.x > self.newpos[0]: # gdy cel po lewej
                    self.x -= self.vel
                    self.left = True
                    self.right = False
                    self.up = False
                    self.down = False
                    self.width = 100
                    self.height = 42
                    
                elif self.x < self.newpos[0]: # gdy cel po prawej
                    self.x += self.vel
                    self.left = False
                    self.right = True
                    self.up = False
                    self.down = False
                    self.width = 100
                    self.height = 42
                    
                if self.x == self.newpos[0] and self.y < self.newpos[1]: # gdy czołg na dobrych x i do góry od celu
                    self.y += self.vel
                    self.left = False
                    self.right = False
                    self.up = False
                    self.down = True
                    self.width = 42
                    self.height = 100

                elif self.x == self.newpos[0] and self.y > self.newpos[1]: # gdy czołg na dobrych x i na dół od celu
                    self.y -= self.vel
                    self.left = False
                    self.right = False
                    self.up = True
                    self.down = False
                    self.width = 42
                    self.height = 100

            else: # gdy dotrze do celu
                self.newpos = [(random.randint(50,1150)//self.vel)*self.vel,(random.randint(150,650)//self.vel)*self.vel] # wylosuj nowy cel
            

        def draw(self,win):
            """
            Funkcja draw(self,win) służy do rysowania czołgu wroga i jego paska życia.
            """
            if self.hp > 0: # gdy czołg ma punkty życia
                self.move() # ruszaj czołg wroga
                if self.left:
                    win.blit(self.drive_left, (self.x,self.y))

                elif self.right:
                    win.blit(self.drive_right, (self.x,self.y))

                elif self.up:
                    win.blit(self.drive_up, (self.x,self.y))

                elif self.down:
                    win.blit(self.drive_down, (self.x,self.y))

                pygame.draw.rect(win,(255,0,0), (self.x+(self.width//2-25),self.y -20, 50, 10 )) #hp bar
                pygame.draw.rect(win,(0,255,0), (self.x+(self.width//2-25),self.y -20, 50 - ((50//self.hpmax)*(self.hpmax - self.hp)), 10 )) #hp bar

                self.hitbox = (self.x, self.y, self.width, self.height)
                #pygame.draw.rect(win, (255,0,0), self.hitbox, 2)



    class wall():
        """
        Klasa wall() opisuje mury ceglane, cegalne popękane i betonowe.
        """

        def __init__(self,x,y, state):
            """
            Metoda __init__(self,x,y,state) tworzy mur. Przyjmuje pozycję początkową x,y.
            Ustawia parametry muru w zależności od wybranego rodzaju - state.
            """
            self.x = x
            self.y = y
            self.state = state # "" - ceglany, "cracks" - ceglany popękany, "concrete" - betonowy (niezniszczalny)
            self.width = 42 # szerokość muru
            self.height = 42 # wysokość muru
            self.hitbox = (self.x, self.y, self.width, self.height) # hitbox muru
            self.hp = 2 # aktualne punkty życia muru

        def draw(self,win):
            """
            Funkcja draw(self,win) służy do rysowania muru w zależności od state.
            """
            if self.state == "cracks":
                if self.hp > 0:
                    win.blit(brick_with_cracks, (self.x, self.y))
            elif self.state == "concrete":
                win.blit(concrete, (self.x, self.y))
            else:
                if self.hp > 0:
                    win.blit(brick, (self.x, self.y))

    class base():
        """
        Klasa base() opisuje bazę gracza.
        """
        def __init__(self,x,y):
            """
            Metoda __init__(self,x,y,state) tworzy mur. Przyjmuje pozycję początkową x,y.
            """
            self.x = x
            self.y = y
            self.width = 84 # szerokość bazy
            self.height = 84 # wysokość bazy
            self.hitbox = (self.x, self.y, self.width, self.height) # hitbox bazy
            self.hp = 5 # aktualne punkty życia
            self.hpmax = 5 # maksymalne punkty życia
            
        def draw(self,win):
            """
            Funkcja draw(self,win) służy do rysowania bazy gracza i jej paska życia.
            """
            win.blit(military_base, (self.x,self.y))
            pygame.draw.rect(win,(255,0,0), (self.x+(self.width//2-25),self.y -20, 50, 10 )) #hp bar
            pygame.draw.rect(win,(0,255,0), (self.x+(self.width//2-25),self.y -20, 50 - ((50//self.hpmax)*(self.hpmax - self.hp)), 10 )) #hp bar
            

    def redrawGameWindow():
        """
        Funkcja redrawGameWindow() służy do aktualizowania okienka gry.
        """
        win.blit(bg, (0,0)) # rysuj tło
        text = font.render('Score: ' + str(score), 1, (0,0,0)) # stwórz napis z punktami
        win.blit(text, (10,10)) # rysuj licznki punktów
        tank_base.draw(win) # rysuj bazę gracza
        tank.draw(win) # rysuj czołg gracza
        for et in enemy_list: # rysuj czołgi wroga
            et.draw(win)
        for bullet in bullets: # rysuj pociski gracza
            bullet.draw(win)
        for w in wall_list: # rysuj mury
            w.draw(win)
        for enemy_bullet in enemy_bullets: # rysuj pociski wroga
            enemy_bullet.draw(win)

        pygame.display.update() # aktualizuj okienko gry

    # główne opcje
    font = pygame.font.SysFont('comicsans', 30, True) # ustaw czcionkę
    tank = player(450, 600) # stwórz czołg gracza
    tank_base = base(558,600) # stwórz bazę gracza
    shoot = 0 # zmienna shoot, by pociski się nie dublowały przy pojedynczym naciśnięciu spacji
    score = 0 # punkty
    bullets = [] # lista pocisków gracza
    enemy_bullets = [] # lista pocisków wroga
    enemy_list=[enemy(9,9,"german"),enemy(40,160,"italian"),enemy(999,9,"japanese"),enemy(1100,160,"waffen-ss")] # lista czołgów wroga
    wall_list = [wall(670,684,""),wall(670,642,""), wall(670,600,""),wall(670,558,""), wall(670,516,""),wall(628,516,""),wall(586,516,""),wall(544,516,""),
                 wall(502,516,""),wall(502,558,""),wall(502,600,""),wall(502,642,""),wall(502,684,""), wall(320,125,""),wall(840,125,""),
                 wall(320,558,"concrete"),wall(840,558,"concrete"),wall(320,600,""),wall(320,642,""),wall(320,684,""),wall(840,600,""),wall(840,642,""),
                 wall(840,684,""),wall(320,516,""),wall(320,474,""),wall(320,432,""),wall(840,516,""),wall(840,474,""),wall(840,432,""),wall(320,167,""),
                 wall(320,209,""),wall(320,251,""),wall(840,167,""),wall(840,209,""), wall(840,251,""),wall(236,209,""), wall(670,280,""),wall(670,322,""),
                 wall(670,364,""), wall(278,209,""),wall(194,209,""),wall(152,209,""), wall(628,364,""),wall(586,364,""), wall(544,364,""),wall(502,364,""),
                 wall(502,322,""),wall(502,280,""),wall(544,280,""),wall(586,280,""),wall(628,280,""),wall(158,345,""),wall(116,345,""),wall(137,387,""),
                 wall(137,429,""),wall(137,471,""),wall(137,658,""),wall(137,616,""),wall(110,209,""),wall(68,209,""),wall(26,209,""),wall(-16,209,""),
                 wall(882,209,""),wall(924,209,""),wall(966,209,""),wall(1008,209,""),wall(1050,209,""),wall(1092,209,""), wall(1134,209,""),wall(1176,209,""),
                 wall(1158,550,""),wall(1116,550,""),wall(1074,550,""),wall(1158,350,""), wall(1116,350,""),wall(1074,350,"")] # lista murów

# pętla gry
    run = True # włącznik
    while run:
        
        clock.tick(30) # klatki na sekundę
        
        for event in pygame.event.get(): # wyjście przyciskiem "x"
            if event.type == pygame.QUIT:
                run = False

        if len(enemy_list) == 0: # warunki zwycięstwa
            with open ("highscore.txt","r") as score_sheet: # przeczytaj wyniki
                current_score = score_sheet.read()
            with open("highscore.txt","w") as score_sheet: # dopisz nowy wynik
                score_sheet.write(current_score+str(score)+'\n')
            run = False # wyłącz grę
            print("YOU'VE WON!") # wyświetl komunikat o wygranej

        if tank_base.hp <= 0: # warunki porażki
            with open ("highscore.txt","r") as score_sheet: # przeczytaj wyniki
                current_score = score_sheet.read()
            with open("highscore.txt","w") as score_sheet: # dopisz nowy wynik
                score_sheet.write(current_score+str(score)+'\n')
            run = False # wyłącz grę
            print("YOU'VE LOST!") # wyświetl komunikat o przegranej

        if tank.hp <=0: # respawn czołgu
            score -= 1
            tank.x = 450
            tank.y = 600
            tank.hp = tank.hpmax
            tank.left = False
            tank.right = False
            tank.up = True
            tank.down = False
            
        if (tank.x <0 or tank.x>1200 or tank.y <0 or tank.y > 700): # reset, gdy czołg wyrzucony z mapy
            tank.x = 450
            tank.y = 600
            tank.hp = tank.hpmax
            tank.left = False
            tank.right = False
            tank.up = True
            tank.down = False

        if shoot > 0: # załatwia dublujące się pociski przy pojedynczym naciśnięciu spacji
            shoot += 1
        if shoot > 3:
            shoot = 0

        
        for bullet in bullets: # pętla przez pociski
            
            for et in enemy_list: # pętla przez czołgi wroga
                if et.hp > 0: # gdy czołg wroga ma punkty życia
                    if bullet.y + 5 < et.hitbox[1] + et.hitbox[3] and bullet.y + 5 > et.hitbox[1] and bullet.x + 5 > et.hitbox[0] and bullet.x + 5 < et.hitbox[0] + et.hitbox[2]:
                            hit.play() # zagraj uderzenie
                            et.hp -= 1 # odejmij punkt życia czołgu wroga
                            score += 1 # dodaj punkt
                            bullets.pop(bullets.index(bullet)) # usuń pocisk z listy
                            break # załatwie bullets.pop error
                        
                else: # wrogi czołg zniszczony
                    enemy_list.pop(enemy_list.index(et)) # usuń czołg wroga z listy

            for w in wall_list: # pętla przez mury
                if w.hp > 0 and (w.state == "" or w.state == "cracks"): # uderzenia w mury ceglane
                    if bullet.y + 5 < w.hitbox[1] + w.hitbox[3] and bullet.y + 5 > w.hitbox[1] and bullet.x + 5 > w.hitbox[0] and bullet.x + 5 < w.hitbox[0] + w.hitbox[2]:
                            hit.play() # zagraj uderzenie
                            w.hp -= 1 # odejmij punkt życia czołgu wroga
                            w.state = "cracks" # zmień state z "" na "cracks"
                            bullets.pop(bullets.index(bullet)) # usuń pocisk z listy
                            break # załatwie bullets.pop error
                        
                elif w.state == "concrete": # uderzenia w mur betonowy
                    if bullet.y + 5 < w.hitbox[1] + w.hitbox[3] and bullet.y + 5 > w.hitbox[1] and bullet.x + 5 > w.hitbox[0] and bullet.x + 5 < w.hitbox[0] + w.hitbox[2]:
                            hit.play() # zagraj uderzenie
                            bullets.pop(bullets.index(bullet)) # usuń pocisk z listy
                            break # załatwie bullets.pop error

                else:
                    wall_list.pop(wall_list.index(w)) # usuń mur z listy
            
            if bullet.x + 5 < 1200 and bullet.x + 5 > 0 and bullet.y + 5 > 0 and bullet.y + 5 < 700: # gdy pocisk na mapie
                bullet.x += bullet.velx # przesuwaj pocisk po x
                bullet.y += bullet.vely # przesuwaj pocisk po y
            else:
                bullets.pop(bullets.index(bullet)) # usuń pocisk spoza mapy

        for w in wall_list: # pętla przez mury
            if ((tank.hitbox[1] < w.hitbox[1] + w.hitbox[3] and tank.hitbox[1] > w.hitbox[1]) and \
            (tank.hitbox[0] < w.hitbox[0] + w.hitbox[2] and tank.hitbox[0] > w.hitbox[0])) or \
            ((tank.hitbox[1] < w.hitbox[1] + w.hitbox[3] and tank.hitbox[1] > w.hitbox[1]) and \
            (tank.hitbox[0] + tank.hitbox[2] < w.hitbox[0] + w.hitbox[2] and tank.hitbox[0] + tank.hitbox[2] > w.hitbox[0])) or \
            ((tank.hitbox[1] < w.hitbox[1] + w.hitbox[3] and tank.hitbox[1] > w.hitbox[1]) and \
            (tank.hitbox[0] + tank.hitbox[2] < w.hitbox[0] + w.hitbox[2] and tank.hitbox[0] + tank.hitbox[2] > w.hitbox[0])) or \
            ((tank.hitbox[1] + tank.hitbox[3] < w.hitbox[1] + w.hitbox[3] and tank.hitbox[1] + tank.hitbox[3] > w.hitbox[1]) and \
            (tank.hitbox[0] < w.hitbox[0] + w.hitbox[2] and tank.hitbox[0] > w.hitbox[0])) or \
            ((tank.hitbox[1] + tank.hitbox[3] < w.hitbox[1] + w.hitbox[3] and tank.hitbox[1] + tank.hitbox[3] > w.hitbox[1]) and \
            (tank.hitbox[0] + tank.hitbox[2] < w.hitbox[0] + w.hitbox[2] and tank.hitbox[0] + tank.hitbox[2] > w.hitbox[0])) or \
            ((tank.hitbox[1] < w.hitbox[1] + w.hitbox[3] and tank.hitbox[1] > w.hitbox[1]) and \
            (tank.hitbox[0]+tank.hitbox[2]/2 < w.hitbox[0] + w.hitbox[2] and tank.hitbox[0]+tank.hitbox[2]/2 > w.hitbox[0])) or \
            ((tank.hitbox[1]+tank.hitbox[3]/2 < w.hitbox[1] + w.hitbox[3] and tank.hitbox[1]+tank.hitbox[3]/2 > w.hitbox[1] ) and \
            (tank.hitbox[0] < w.hitbox[0] + w.hitbox[2] and tank.hitbox[0] > w.hitbox[0])) or \
            ((tank.hitbox[1]+tank.hitbox[3]/2 < w.hitbox[1] + w.hitbox[3] and tank.hitbox[1]+tank.hitbox[3]/2 > w.hitbox[1]) and \
            (tank.hitbox[0] + tank.hitbox[2] < w.hitbox[0] + w.hitbox[2] and tank.hitbox[0] + tank.hitbox[2] > w.hitbox[0])) or \
            ((tank.hitbox[1] + tank.hitbox[3] < w.hitbox[1] + w.hitbox[3] and tank.hitbox[1] + tank.hitbox[3] > w.hitbox[1]) and \
            (tank.hitbox[0] + tank.hitbox[2]/2 < w.hitbox[0] + w.hitbox[2] and tank.hitbox[0] + tank.hitbox[2]/2 > w.hitbox[0])): # zderzenia czołgu z murem

                if tank.left:
                    tank.x += w.hitbox[0]+w.hitbox[2]-tank.hitbox[0]
                elif tank.right:
                    tank.x -= tank.hitbox[0]+tank.hitbox[2]-w.hitbox[0]
                elif tank.up:
                    tank.y += w.hitbox[1]+w.hitbox[3]-tank.hitbox[1]
                elif tank.down:
                    tank.y -= tank.hitbox[1]+tank.hitbox[3]-w.hitbox[1]
            
        for et in enemy_list: # pętla przez czołgi wroga
            for w in wall_list: # pętla przez mury
                if ((et.hitbox[1] < w.hitbox[1] + w.hitbox[3] and et.hitbox[1] > w.hitbox[1]) and \
                (et.hitbox[0] < w.hitbox[0] + w.hitbox[2] and et.hitbox[0] > w.hitbox[0])) or \
                ((et.hitbox[1] < w.hitbox[1] + w.hitbox[3] and et.hitbox[1] > w.hitbox[1]) and \
                (et.hitbox[0] + et.hitbox[2] < w.hitbox[0] + w.hitbox[2] and et.hitbox[0] + et.hitbox[2] > w.hitbox[0])) or \
                ((et.hitbox[1] < w.hitbox[1] + w.hitbox[3] and et.hitbox[1] > w.hitbox[1]) and \
                (et.hitbox[0] + et.hitbox[2] < w.hitbox[0] + w.hitbox[2] and et.hitbox[0] + et.hitbox[2] > w.hitbox[0])) or \
                ((et.hitbox[1] + et.hitbox[3] < w.hitbox[1] + w.hitbox[3] and et.hitbox[1] + et.hitbox[3] > w.hitbox[1]) and \
                (et.hitbox[0] < w.hitbox[0] + w.hitbox[2] and et.hitbox[0] > w.hitbox[0])) or \
                ((et.hitbox[1] + et.hitbox[3] < w.hitbox[1] + w.hitbox[3] and et.hitbox[1] + et.hitbox[3] > w.hitbox[1]) and \
                (et.hitbox[0] + et.hitbox[2] < w.hitbox[0] + w.hitbox[2] and et.hitbox[0] + et.hitbox[2] > w.hitbox[0])) or \
                ((et.hitbox[1] < w.hitbox[1] + w.hitbox[3] and et.hitbox[1] > w.hitbox[1]) and \
                (et.hitbox[0]+et.hitbox[2]/2 < w.hitbox[0] + w.hitbox[2] and et.hitbox[0]+et.hitbox[2]/2 > w.hitbox[0])) or \
                ((et.hitbox[1]+et.hitbox[3]/2 < w.hitbox[1] + w.hitbox[3] and et.hitbox[1]+et.hitbox[3]/2 > w.hitbox[1] ) and \
                (et.hitbox[0] < w.hitbox[0] + w.hitbox[2] and et.hitbox[0] > w.hitbox[0])) or \
                ((et.hitbox[1]+et.hitbox[3]/2 < w.hitbox[1] + w.hitbox[3] and et.hitbox[1]+et.hitbox[3]/2 > w.hitbox[1]) and \
                (et.hitbox[0] + et.hitbox[2] < w.hitbox[0] + w.hitbox[2] and et.hitbox[0] + et.hitbox[2] > w.hitbox[0])) or \
                ((et.hitbox[1] + et.hitbox[3] < w.hitbox[1] + w.hitbox[3] and et.hitbox[1] + et.hitbox[3] > w.hitbox[1]) and \
                (et.hitbox[0] + et.hitbox[2]/2 < w.hitbox[0] + w.hitbox[2] and et.hitbox[0] + et.hitbox[2]/2 > w.hitbox[0])): # zderzenia czołgu wroga z murem

                    if et.left:
                        et.x += (w.hitbox[0]+w.hitbox[2]-et.hitbox[0])//et.vel*et.vel
                    elif et.right:
                        et.x -= (et.hitbox[0]+et.hitbox[2]-w.hitbox[0])//et.vel*et.vel
                    elif et.up:
                        et.y += (w.hitbox[1]+w.hitbox[3]-et.hitbox[1])//et.vel*et.vel
                    elif et.down:
                        et.y -= (et.hitbox[1]+et.hitbox[3]-w.hitbox[1])//et.vel*et.vel

                    et.newpos = [(random.randint(100,1100)//et.vel)*et.vel,(random.randint(200,600)//et.vel)*et.vel] # ustaw nowy cel, by w końcu odjechał od muru
                    
            if ((et.hitbox[1] < tank_base.hitbox[1] + tank_base.hitbox[3] and et.hitbox[1] > tank_base.hitbox[1]) and \
                (et.hitbox[0] < tank_base.hitbox[0] + tank_base.hitbox[2] and et.hitbox[0] > tank_base.hitbox[0])) or \
                ((et.hitbox[1] < tank_base.hitbox[1] + tank_base.hitbox[3] and et.hitbox[1] > tank_base.hitbox[1]) and \
                (et.hitbox[0] + et.hitbox[2] < tank_base.hitbox[0] + tank_base.hitbox[2] and et.hitbox[0] + et.hitbox[2] > tank_base.hitbox[0])) or \
                ((et.hitbox[1] < tank_base.hitbox[1] + tank_base.hitbox[3] and tank.hitbox[1] > tank_base.hitbox[1]) and \
                (et.hitbox[0] + et.hitbox[2] < tank_base.hitbox[0] + tank_base.hitbox[2] and et.hitbox[0] + et.hitbox[2] > tank_base.hitbox[0])) or \
                ((et.hitbox[1] + et.hitbox[3] < tank_base.hitbox[1] + tank_base.hitbox[3] and et.hitbox[1] + et.hitbox[3] > tank_base.hitbox[1]) and \
                (et.hitbox[0] < tank_base.hitbox[0] + tank_base.hitbox[2] and et.hitbox[0] > tank_base.hitbox[0])) or \
                ((et.hitbox[1] + et.hitbox[3] < tank_base.hitbox[1] + tank_base.hitbox[3] and et.hitbox[1] + et.hitbox[3] > tank_base.hitbox[1]) and \
                (et.hitbox[0] + et.hitbox[2] < tank_base.hitbox[0] + tank_base.hitbox[2] and et.hitbox[0] + et.hitbox[2] > tank_base.hitbox[0])) or \
                ((et.hitbox[1] < tank_base.hitbox[1] + tank_base.hitbox[3] and et.hitbox[1] > tank_base.hitbox[1]) and \
                (et.hitbox[0]+et.hitbox[2]/2 < tank_base.hitbox[0] + tank_base.hitbox[2] and et.hitbox[0]+et.hitbox[2]/2 > tank_base.hitbox[0])) or \
                ((et.hitbox[1]+et.hitbox[3]/2 < tank_base.hitbox[1] + tank_base.hitbox[3] and et.hitbox[1]+et.hitbox[3]/2 > tank_base.hitbox[1] ) and \
                (et.hitbox[0] < w.hitbox[0] + tank_base.hitbox[2] and et.hitbox[0] > tank_base.hitbox[0])) or \
                ((et.hitbox[1]+et.hitbox[3]/2 < tank_base.hitbox[1] + tank_base.hitbox[3] and et.hitbox[1]+et.hitbox[3]/2 > tank_base.hitbox[1]) and \
                (et.hitbox[0] + et.hitbox[2] < tank_base.hitbox[0] + tank_base.hitbox[2] and et.hitbox[0] + et.hitbox[2] > tank_base.hitbox[0])) or \
                ((et.hitbox[1] + et.hitbox[3] < tank_base.hitbox[1] + tank_base.hitbox[3] and et.hitbox[1] + et.hitbox[3] > tank_base.hitbox[1]) and \
                (et.hitbox[0] + et.hitbox[2]/2 < tank_base.hitbox[0] + tank_base.hitbox[2] and et.hitbox[0] + et.hitbox[2]/2 > tank_base.hitbox[0])): # zderzenia czołgu wroga z bazą gracza

                    if et.left:
                        et.x += (tank_base.hitbox[0]+tank_base.hitbox[2]-et.hitbox[0])//et.vel*et.vel
                    elif et.right:
                        et.x -= (et.hitbox[0]+et.hitbox[2]-tank_base.hitbox[0])//et.vel*et.vel
                    elif et.up:
                        et.y += (tank_base.hitbox[1]+tank_base.hitbox[3]-et.hitbox[1])//et.vel*et.vel
                    elif et.down:
                        et.y -= (et.hitbox[1]+et.hitbox[3]-tank_base.hitbox[1])//et.vel*et.vel

                    et.newpos = [(random.randint(50,1150)//et.vel)*et.vel,(random.randint(150,650)//et.vel)*et.vel] # ustaw nowy cel, by w końcu odjechał od bazy

            if (et.x > tank_base.hitbox[0] and et.x < tank_base.hitbox[0] + tank_base.hitbox[2] and (et.down or et.up)) or \
               (et.y > tank_base.hitbox[1] and et.y < tank_base.hitbox[1] + tank_base.hitbox[3] and (et.left or et.right)) or \
               (et.x > tank.hitbox[0] and et.x < tank.hitbox[0] + tank.hitbox[2] and (et.down or et.up)) or \
               (et.y > tank.hitbox[1] and et.y < tank.hitbox[1] + tank.hitbox[3] and (et.left or et.right)):
                    decision = random.randint(1,10) # gdy gracz lub jego baza na linii strzału 10% szansy na strzał
            else:
                decision = random.randint(1,50) # inaczej 2% szansy na strzał 
                
            if decision == 1: # gdy wylosuje 1

                tank_shot.play() # zagraj strzał
                if et.ammo > 0:
                    et.ammo -= 1 # odejmij amunicję
                else:
                    et.ammo = 3 # resetuj amunicję

                # stwórz pocisk wroga
                if et.down:
                    enemy_bullets.append(enemy_projectile(et.x+et.width//2-4,et.y+et.height,"down"))
                elif et.up:
                    enemy_bullets.append(enemy_projectile(et.x+et.width//2-4,et.y-10,"up"))
                elif et.left:
                    enemy_bullets.append(enemy_projectile(et.x-et.width//4+12,et.y+et.height//2-7,"left"))
                elif et.right:
                    enemy_bullets.append(enemy_projectile(et.x+et.width,et.y+et.height//2-7,"right"))

            if et.x < 0 or et.x > 1200 or et.y < 0 or et.y >700: # reset czołgu wroga, gdy poza mapą
                et.x = 96
                et.y = 96
                    
        for eb in enemy_bullets: # pętla przez pociski wroga
            if tank.hp > 0: # gdy czołg gracza ma punkty życia
                if eb.y + 5 < tank.hitbox[1] + tank.hitbox[3] and eb.y + 5 > tank.hitbox[1] and eb.x + 5 > tank.hitbox[0] and eb.x + 5 < tank.hitbox[0] + tank.hitbox[2]:
                        hit.play() # zagraj uderzenie
                        tank.hp -= 1 # odejmij punkt życia czołgu wroga
                        enemy_bullets.pop(enemy_bullets.index(eb)) # usuń pocisk z listy
                        break # załatwie bullets.pop error

            for w in wall_list: # pętla przez mury
                if w.hp > 0 and (w.state == "" or w.state == "cracks"): # uderzenia w mury ceglane
                    if eb.y + 5 < w.hitbox[1] + w.hitbox[3] and eb.y + 5 > w.hitbox[1] and eb.x + 5 > w.hitbox[0] and eb.x + 5 < w.hitbox[0] + w.hitbox[2]:
                            hit.play() # zagraj uderzenie
                            w.hp -= 1 # odejmij punkt życia muru
                            w.state = "cracks" # zmień state z "" na "cracks"
                            enemy_bullets.pop(enemy_bullets.index(eb)) # usuń pocisk wroga z listy
                            break # załatwie bullets.pop error
                        
                elif w.state == "concrete": # uderzenia w mur betonowy
                    if eb.y + 5 < w.hitbox[1] + w.hitbox[3] and eb.y + 5 > w.hitbox[1] and eb.x + 5 > w.hitbox[0] and eb.x + 5 < w.hitbox[0] + w.hitbox[2]:
                            hit.play() # zagraj uderzenie
                            enemy_bullets.pop(enemy_bullets.index(eb)) # usuń pocisk wroga z listy
                            break # załatwie bullets.pop error

                else:
                    wall_list.pop(wall_list.index(w)) # usuń mur z listy
                    
            if tank_base.hp > 0:
                if eb.y + 5 < tank_base.hitbox[1] + tank_base.hitbox[3] and eb.y + 5 > tank_base.hitbox[1] and eb.x + 5 > tank_base.hitbox[0] and eb.x + 5 < tank_base.hitbox[0] + tank_base.hitbox[2]:
                        hit.play() # zagraj uderzenie
                        tank_base.hp -= 1 # odejmij punkt życia bazy
                        enemy_bullets.pop(enemy_bullets.index(eb)) # usuń pocisk wroga z listy
                        break # załatwie bullets.pop error
                
            if eb.x + 5 < 1200 and eb.x + 5 > 0 and eb.y + 5 > 0 and eb.y + 5 < 700: # gdy pocisk na mapie
                eb.x += eb.velx # przesuwaj pocisk wroga po x
                eb.y += eb.vely # przesuwaj pocisk wroga po y
            else:
                enemy_bullets.pop(enemy_bullets.index(eb)) # usuń pocisk spoza mapy
                
                    
        keys = pygame.key.get_pressed() # przyciski naciśnięte

        if keys[pygame.K_SPACE] and shoot == 0: # gdy naciśnięta spacja i shoot == 0

            if len(bullets) < tank.ammo:
                tank_shot.play() # zagraj strzał
                if tank.down: # stwórz pocisk
                    bullets.append(projectile(tank.x+tank.width//2-4,tank.y+tank.height,"down"))
                elif tank.up:
                    bullets.append(projectile(tank.x+tank.width//2-4,tank.y-10,"up"))
                elif tank.left:
                    bullets.append(projectile(tank.x-tank.width//4+12,tank.y+tank.height//2-7,"left"))
                elif tank.right:
                    bullets.append(projectile(tank.x+tank.width,tank.y+tank.height//2-7,"right"))
                shoot = 1 # ustaw shoot

            else:
                no_ammo.play() # inaczej zagraj brak amunicji

        if keys[pygame.K_LEFT] and tank.x > 0: # gdy naciśnięta strzałka w lewo i czołg na mapie
            tank.x -= tank.vel
            tank.left = True
            tank.right = False
            tank.up = False
            tank.down = False
            tank.width = 100
            tank.height = 42
            
        elif keys[pygame.K_RIGHT] and tank.x < screen_width - tank.width: # gdy naciśnięta strzałka w prawo i czołg na mapie
            tank.x += tank.vel
            tank.left = False
            tank.right = True
            tank.up = False
            tank.down = False
            tank.width = 100
            tank.height = 42
            
        elif keys[pygame.K_UP] and tank.y > 0: # gdy naciśnięta strzałka w górę i czołg na mapie
            tank.y -= tank.vel
            tank.left = False
            tank.right = False
            tank.up = True
            tank.down = False
            tank.width = 42
            tank.height = 100
            
        elif keys[pygame.K_DOWN] and tank.y < screen_height - tank.height: # gdy naciśnięta strzałka w dół i czołg na mapie
            tank.y += tank.vel
            tank.left = False
            tank.right = False
            tank.up = False
            tank.down = True
            tank.width = 42
            tank.height = 100
            
        redrawGameWindow() # aktualizuj okienko gry
                
    pygame.quit() # gry run = False, wyłącz

def main_menu():
    """
    Menu gry "Battle City 1941".
    """
    pygame.init()
    screen_width = 1200 # szerokość okienka
    screen_height = 700 # wysokość okienka
    main_win = pygame.display.set_mode((screen_width,screen_height)) # ustaw wymiary okienka
    pygame.display.set_caption("Battle City 1941 Menu") # ustaw tytuł menu
    bg=pygame.image.load('images/menu.png') # załaduj tło
    main_win.blit(bg, (0,0)) # ustaw obrazek tła

    class button():
        """
        Klasa button() opisuje przyciski menu.
        """
        def __init__(self, color, x ,y, width, height, text=''):
            """
            Metoda __init__(self, color, x ,y, width, height, text='') tworzy przycisk o kolorze - color z tekstem - text.
            """
            self.color = color
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.text = text

        def draw(self,win,outline=None):
            """
            Funkcja draw(self,win,outline=None) rysuje przycisk. Domyślnie ma wyłączoną ramkę
            """
            if outline: # gdy ramka włączona
                pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0) # rysuj ramkę
                
            pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0) # rysuj przycisk
            
            if self.text != '':
                font = pygame.font.SysFont('comicsans', 60)
                text = font.render(self.text, 1, (255,255,255))
                win.blit(text, (self.x + (self.width//2 - text.get_width()//2), self.y + (self.height//2 - text.get_height()//2))) # rysuj tekst

        def isOver(self, pos):
            """
            Funkcja isOver(self,pos) sprawdza czy kursor jest na przycisk. Zwraca True lub False.
            """
            if pos[0] > self.x and pos[0] < self.x + self.width:
                if pos[1] > self.y and pos[1] < self.y + self.height:
                    return True
            
            return False

    start_button = button((255,0,0), 150, 225, 300, 70, 'Start') # stwórz przycisk 'Start'
    start_button.draw(main_win, (255,255,255))
    rules_button = button((255,0,0), 150, 325, 300, 70, 'Rules') # stwórz przycisk 'Rules'
    rules_button.draw(main_win, (255,255,255))
    score_button = button((255,0,0), 150, 425, 300, 70, 'Highscores') # stwórz przycisk 'Highscores'
    score_button.draw(main_win, (255,255,255))
    author_button = button((255,0,0), 150, 525, 300, 70, 'About author') # stwórz przycisk 'About author'
    author_button.draw(main_win, (255,255,255))
    quit_button = button((255,0,0), 150, 625, 300, 70, 'Quit') # stwórz przycisk 'Quit'
    quit_button.draw(main_win, (255,255,255))
    tank_choice = False # ustaw zmienną wyboru czołgu na False
    run = True # włącznik
    while run:
        pygame.display.update() # aktualizuj okienko menu
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT: # wyjście przyciskiem "x"
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if start_button.isOver(pos):
                    pygame.draw.rect(main_win, (0,0,0), (500,225,1000,700),0)
                    
                    font = pygame.font.SysFont('comicsans', 60)
                    font_small = pygame.font.SysFont('comicsans', 30)
                    
                    title = font.render("Choose your tank:", 1, (255,255,255)) # czołgi z opisami
                    soviet_tank=pygame.image.load('images/soviet down.png')
                    soviet_label = font_small.render("Soviet", 1, (255,255,255))
                    soviet_vel = font_small.render("Speed: 3", 1, (255,255,255))
                    soviet_ammo = font_small.render("Ammo: 4", 1, (255,255,255))
                    soviet_hp = font_small.render("HP: 4", 1, (255,255,255))
                    
                    american_tank=pygame.image.load('images/american down.png')
                    american_label = font_small.render("American", 1, (255,255,255))
                    american_vel = font_small.render("Speed: 3", 1, (255,255,255))
                    american_ammo = font_small.render("Ammo: 3", 1, (255,255,255))
                    american_hp = font_small.render("HP: 3", 1, (255,255,255))
                    
                    british_tank=pygame.image.load('images/british down.png')
                    british_label = font_small.render("British", 1, (255,255,255))
                    british_vel = font_small.render("Speed: 2", 1, (255,255,255))
                    british_ammo = font_small.render("Ammo: 3", 1, (255,255,255))
                    british_hp = font_small.render("HP: 4", 1, (255,255,255))
                    
                    french_tank=pygame.image.load('images/french down.png')
                    french_label = font_small.render("French", 1, (255,255,255))
                    french_vel = font_small.render("Speed: 4", 1, (255,255,255))
                    french_ammo = font_small.render("Ammo: 3", 1, (255,255,255))
                    french_hp = font_small.render("HP: 2", 1, (255,255,255))

                    main_win.blit(title, (500, 225))
                    main_win.blit(soviet_tank, (520, 300))
                    main_win.blit(soviet_label, (510, 410))
                    main_win.blit(soviet_vel, (510, 440))
                    main_win.blit(soviet_ammo, (510, 460))
                    main_win.blit(soviet_hp, (510, 480))
                    
                    main_win.blit(american_tank, (670, 300))
                    main_win.blit(american_label, (640, 410))
                    main_win.blit(american_vel, (640, 440))
                    main_win.blit(american_ammo, (640, 460))
                    main_win.blit(american_hp, (640, 480))
                    
                    main_win.blit(british_tank, (820, 300))
                    main_win.blit(british_label, (810, 410))
                    main_win.blit(british_vel, (810, 440))
                    main_win.blit(british_ammo, (810, 460))
                    main_win.blit(british_hp, (810, 480))
                    
                    main_win.blit(french_tank, (970, 300))
                    main_win.blit(french_label, (960, 410))
                    main_win.blit(french_vel, (960, 440))
                    main_win.blit(french_ammo, (960, 460))
                    main_win.blit(french_hp, (960, 480))
                    
                    tank_choice = True # włącz wybór czołgu

                if tank_choice: # gdy włączony wybór czołgu
                    if pos[0] > 520 and pos[0] < 520 + 42:
                        if pos[1] > 300 and pos[1] < 300 + 100:
                            run = False
                            game("soviet")
                    if pos[0] > 670 and pos[0] < 670 + 42:
                        if pos[1] > 300 and pos[1] < 300 + 100:
                            run = False
                            game("american")
                    if pos[0] > 820 and pos[0] < 820 + 42:
                        if pos[1] > 300 and pos[1] < 300 + 100:
                            run = False
                            game("british")
                    if pos[0] > 970 and pos[0] < 970 + 42:
                        if pos[1] > 300 and pos[1] < 300 + 100:
                            run = False
                            game("french")
                
                if rules_button.isOver(pos):
                    pygame.draw.rect(main_win, (0,0,0), (500,225,1000,700),0) # zamaluj czarnym
                    font = pygame.font.SysFont('comicsans', 50)
                    title = font.render("The game rules:", 1, (255,255,255)) # zasady
                    rule_1 = font.render(" - Destroy all enemy tanks to win", 1, (255,255,255))
                    rule_2 = font.render(" - If your base falls you lose", 1, (255,255,255))
                    rule_3 = font.render(" - You gain points by hitting enemies", 1, (255,255,255))
                    good_luck = font.render("Good luck, Commander!", 1, (255,255,255))
                    main_win.blit(title, (500, 225))
                    main_win.blit(rule_1, (500, 275))
                    main_win.blit(rule_2, (500, 325))
                    main_win.blit(rule_3, (500, 375))
                    main_win.blit(good_luck, (500, 425))
                    tank_choice = False # wyłącz wybór czołgu
                    
                if score_button.isOver(pos):
                    pygame.draw.rect(main_win, (0,0,0), (500,200,1000,700),0) # zamaluj czarnym
                    font = pygame.font.SysFont('comicsans', 50)
                    title = font.render("Highscores:", 1, (255,255,255))
                    main_win.blit(title, (500, 225))
                    with open ("highscore.txt","r") as score_sheet:
                        current_score = score_sheet.read().split("\n")[:-1] 
                    current_score = list(map(int,current_score))
                    current_score.sort(reverse=True) # sortuj wyniki
                    current_score = list(map(str,current_score))
                    if len(current_score) >= 3: # gdy co najmniej trzy wypisz trzy
                        first_score=font.render("Best score ever: "+current_score[0]+" point(s)",1,(255,255,255))
                        second_score=font.render("Second best score: "+current_score[1]+" point(s)",1,(255,255,255))
                        third_score=font.render("Third best score: "+current_score[2]+" point(s)",1,(255,255,255))
                        main_win.blit(first_score, (500, 275))
                        main_win.blit(second_score, (500, 325))
                        main_win.blit(third_score, (500, 375))
                    elif len(current_score) == 2: # gdy dwa wypisz dwa
                        first_score=font.render("Best score ever: "+current_score[0]+" point(s)",1,(255,255,255))
                        second_score=font.render("Second best score: "+current_score[1]+" point(s)",1,(255,255,255))
                        main_win.blit(first_score, (500, 275))
                        main_win.blit(second_score, (500, 325))
                    elif len(current_score) == 1: # gdy jeden wypisz jeden
                        first_score=font.render("Best score ever: "+current_score[0]+" point(s)",1,(255,255,255))
                        main_win.blit(first_score, (500, 275))
                    else: # inaczej wypisz, że nie ma żadnego
                        no_highscore_yet=font.render("No highscore yet!",1,(255,255,255))
                        main_win.blit(no_highscore_yet, (500, 275))
                    tank_choice = False # wyłącz wybór czołgu
                    
                if author_button.isOver(pos):
                    pygame.draw.rect(main_win, (0,0,0), (500,200,1000,700),0) # zamaluj czarnym
                    font = pygame.font.SysFont('comicsans', 50)
                    title = font.render("About author:", 1, (255,255,255)) # o autorze
                    author_bio_1 = font.render("The author is Jakub Koral, student", 1, (255,255,255))
                    author_bio_2 = font.render("of Wroclaw University of Science", 1, (255,255,255))
                    author_bio_3 = font.render("and Technology. He was inspired", 1, (255,255,255))
                    inspiration_1 = font.render("by an old game called Battle City.", 1, (255,255,255))
                    main_win.blit(title, (500, 225))
                    main_win.blit(author_bio_1, (500, 275))
                    main_win.blit(author_bio_2, (500, 325))
                    main_win.blit(author_bio_3, (500, 375))
                    main_win.blit(inspiration_1, (500, 425))
                    tank_choice = False # wyłącz wybór czołgu
                if quit_button.isOver(pos):
                    run = False
                    
                    
    pygame.quit() # gry run = False, wyłącz

main_menu() # wywołaj menu gry
