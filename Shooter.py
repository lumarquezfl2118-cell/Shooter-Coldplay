from pygame import *
from random import randint
from time import sleep


class GameSprite(sprite.Sprite):
    #constructor de clase
    def __init__(self, player_image, player_x, player_y, player_speed, Largo, Ancho):
        
        #Sobre escribir el init de sprite
        #Usar un nuevo constructor
        super().__init__()

        # cada objeto debe almacenar la propiedad image
        self.image = transform.scale(image.load(player_image), (Largo, Ancho))
        self.speed = player_speed
    
        # cada objeto debe almacenar la propiedad rect (rectángulo) en la cual es ingresada
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    #método para dibujar el personaje en la ventana
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#clase del jugador principal
class Player(GameSprite):
    #método que implementar el control de objetos usando los botones de flechas del teclado
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 150:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 180:
            self.rect.y += self.speed

#Clase del Cazador
class Enemigo(GameSprite):
    salud = 2
    #movimiento del enemigo
    def update(self):
        if self.rect.y > 480:
            self.rect.x = randint(20, 780)
            self.rect.y = 0
        self.rect.y += self.speed

    def damage(self):
        global Puntaje
        self.salud -= 1
        if self.salud <= 0:
            self.kill()
            Puntaje += 1


#Clase jefe
class Jefe(GameSprite):
    salud = 50
    lado = 'izquierda'
    def update(self):
        if self.rect.x < 10:
            self.lado = 'derecha' 
        elif self.rect.x > 700:
            self.lado = 'izquierda'

        if  self.lado == "izquierda":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        
        if self.salud <= 0:
            self.kill()

    def damage(self):
        self.salud -= 1

    def fire(self):
        fire_ball = Bala('comet.png', jefe.rect.centerx, 120, -20, 30, 30)
        fire_balls.add(fire_ball)
    


#Clase bala
class Bala(GameSprite):
    def update(self):
        global fallo
        if self.rect.y < 0:
            self.kill()
            fallo = fallo + 1
        self.rect.y -= self.speed
        

            


#Crear una ventana
win_width = 800
win_height = 500

display.set_caption("Mono")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('Camino.png'), (800, 500))

jefe = Jefe('Ardilla.png', 400, 80, 6, 160, 200)
mono = Player('Chris.png', 500, 415, 25, 150, 180)



#Crear un grupo de bananas
bananas = sprite.Group()
cazadores = sprite.Group()
fire_balls = sprite.Group()
inicio = 1
finalizar = False
Puntaje = 0
fallo = 0


#Crear contadores
# cargando funciones de font de forma separada
font.init()
# durante el juego, creando inscripciones en tamaño 36
font = font.Font(None, 36)



run = True

while run:
    #el ciclo se ejecuta cada 0.05 segundos
    time.delay(50)

    # escribir texto en la pantalla
    puntuacion = font.render("Puntaje: " + str(Puntaje), 1, (255, 255, 255))
    fallos = font.render('Fallos: ' + str(fallo), 1, (255, 255, 255))
    vida_jefe = font.render('Vida Jefe: '+ str(jefe.salud), 1, (255, 0, 0))


    if inicio == 1:
        for i in range(5):
            cazador = Enemigo('Ardilla.png', randint(20, 750), 0, randint(1,4), 80, 80)
            cazadores.add(cazador)
            inicio = 0

    #Se comprueban todos los eventos que pueden suceder
    for e in event.get():
        #evento de clic del botón “cerrar”
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN and finalizar == False:
            if e.key == K_SPACE:
                banana = Bala('comet.png', mono.rect.centerx, mono.rect.y, 8, 20, 20)
                bananas.add(banana)
             #evento click para reiniciar el juego
        elif e.type == MOUSEBUTTONDOWN and finalizar==True:
            if e.button == 1:  # 1 es el botón izquierdo
                finalizar = False
                mono.rect.x = 400
                mono.rect.y = 415
                bananas.empty()
                cazadores.empty()
                fire_balls.empty()
                Puntaje = 0
                fallo = 0
                inicio = 1
                jefe.salud = 50
                jefe.rect.x = 400
                jefe.rect.y = 80


    # El True hace verdadero el Dokill, para el primer y segundo objeto
    collides = sprite.groupcollide(cazadores, bananas, False, True)     
    for c in collides:
        c.damage()
        if c.salud <= 0:
            cazador = Enemigo('Ardilla.png', randint(20, 780), 0, randint(1,4), 80, 80)
            cazadores.add(cazador)

    
    
    #Colicion de un objeto con un grupo de objetos
    if sprite.spritecollide(mono,cazadores, False) or fallo == 25:
        finalizar = True
        img  = transform.scale(image.load('Perdiste1.png'), (800, 500))
        window.blit(img, (0, 0))

    if sprite.spritecollide(mono, fire_balls, True):
        finalizar = True
        img  = transform.scale(image.load('Perdiste1.png'), (800, 500))
        window.blit(img, (0, 0))
    
    if fallo == 10:
        finalizar = True
        img = transform.scale(image.load('Sin meteoritos.png'), (800, 500))
        window.blit(img, (0, 0))

    if Puntaje >= 10 and sprite.spritecollide(mono, sprite.Group(jefe), False):
        finalizar = True
        img  = transform.scale(image.load('Perdiste1.png'), (800, 500))
        window.blit(img, (0, 0))

    if jefe.salud == 0:
        jefe.kill()
        finalizar = True
        img = transform.scale(image.load('Ganaste1.png'), (800, 500))
        window.blit(img, (0,0))

    if finalizar == False:
        #Se actualiza el fondo con cada iteración
        window.blit(background, (0, 0))
            
        if Puntaje >= 10:
            cazadores.empty()
            jefe.update()
            jefe.reset()
            window.blit(vida_jefe, (300,20))
            if sprite.spritecollide(jefe, bananas, True):
                jefe.damage()
                jefe.fire()
        

                
        #ejecuta el movimiento del objeto
        mono.update()
        bananas.update()
        cazadores.update()
        fire_balls.update() 
        

        mono.reset()
        bananas.draw(window)
        cazadores.draw(window)
        fire_balls.draw(window)

        window.blit(puntuacion, (10, 20))
        window.blit(fallos,(10, 40))




            
    display.update()

quit()