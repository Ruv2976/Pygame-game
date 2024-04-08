from pygame import *
from random import *
 
misses = 0
ufoCount = 0
skibidiCount = 0

bulletsSpeed = 1

fps = 60
 
init()
 
window = display.set_mode((700,500))
display.set_caption('Shooter')

clock = time.Clock()
 
mixer.init()
mixer.music.load('assets/space.ogg')
#mixer.music.play()
 
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, speed = 5, w = 65, h = 65):
        super().__init__()
        self.w = w
        self.h = h
        self.image = transform.scale(image.load(img), (self.w, self.h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
 
    def paint(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
 
class Rocket(GameSprite):
    def move(self):
        if (keys[K_a] or keys[K_LEFT])  and self.rect.x > 20: self.rect.x -= self.speed
        if (keys[K_d] or keys[K_RIGHT]) and self.rect.x < 640: self.rect.x += self.speed
 
class Ufo(GameSprite):
    def update(self, ignoreMisses=False):
        global misses
        self.rect.y += self.speed
        if self.rect.y >= 500:
            if not ignoreMisses: misses += 1
            self.rect.y = -50
            self.rect.x = randint(10, 630)
 
class Bullet(GameSprite):
    def update(self, skbd=False):
        if skbd:
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()

timer = 0

class SKIBIDIDOPDOP(GameSprite):
    def update(self, group:sprite.Group):
        global timer
        if self.rect.y < window.get_height() / 6:
            self.rect.y += 1
        else:
            if timer == fps:
                group.add(Bullet('assets/bullet.png', self.rect.centerx-7, self.rect.bottom, 3, 15, 30))
                timer = 0
            else:
                timer += 1

        if self.rect.x < rocket.rect.x:
            self.rect.x += 3
        elif self.rect.x > rocket.rect.x:
            self.rect.x -= 3
        else: #none
            pass
 
rocket = Rocket('assets/rocket.png', 300, 430, 10)
background = transform.scale(image.load('assets/galaxy.jpg'), (700,500))

f = font.Font(None, 45)

ufos = sprite.Group()
ufos.add([
    Ufo('assets/ufo.png', randint(10, 630), 0, 1),
    Ufo('assets/ufo.png', randint(10, 630), 0, 1),
    Ufo('assets/ufo.png', randint(10, 630), 0, 1),
    Ufo('assets/ufo.png', randint(10, 630), 0, 1),
    Ufo('assets/ufo.png', randint(10, 630), 0, 1)
])

asteroids = sprite.Group()
asteroids.add([
    Ufo('assets/asteroid.png', randint(10, 630), 0, 4),
    Ufo('assets/asteroid.png', randint(10, 630), 0, 4),
])
 
bullets = sprite.Group()

enemyBullets = sprite.Group()

s = sprite.Group()
r = sprite.Group()
skibidi = SKIBIDIDOPDOP('assets/skibidi.png', window.get_width() / 2, 0, 0, 100, 100)
s.add(skibidi)
r.add(rocket)
skbd = False

game = True
while game:
    keys = key.get_pressed()
    for e in event.get():
        if e.type == QUIT: game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                bullets.add(Bullet('assets/bullet.png', rocket.rect.centerx-7, rocket.rect.top, 30, 15, 30))
                #mixer.Sound('fire.ogg').play()
                #print(bullets)
    #printing
    window.blit(background, (0,0))
    rocket.paint()
    
    #moves
    rocket.move()
    if ufoCount >= 30 and not skbd:
        ufoCount = 0
        misses = 0
        skbd = True
    
    if skbd:
        for ufo in ufos: ufos.remove(ufo)

        skibidi.paint()
        skibidi.update(enemyBullets)

        enemyBullets.draw(window)
        enemyBullets.update(skbd)


    if misses < 5 and skibidiCount < 100: 
        ufos.draw(window)
        ufos.update()
        asteroids.draw(window)
        asteroids.update(True)
        bullets.draw(window)
        bullets.update()
        mc = f.render(f'Misses: {misses}', True, (255, 255, 255))
        window.blit(mc, (0, 0))
    else:
        if skbd: window.blit(transform.scale(image.load('assets/maxresdefault.jpg'), (700,500)), (0,0))
        lose = f.render('lose' if skibidiCount < 100 else 'u won', True, (255, 255, 255))
        window.blit(lose, (0, 0))

        for ufo in ufos: ufos.remove(ufo)

        if keys[K_r]: 
            misses = 0
            ufoCount = 0
            if skbd:
                #skibidi.kill()
                skbd = False
                skibidiCount = 0
                skibidi.rect.y = 0
 
    #collisions
    sprite.groupcollide(bullets, asteroids, True, False)
    if sprite.groupcollide(bullets, ufos, True, True):
        ufoCount += 1

    if sprite.groupcollide(s, bullets, False, True): skibidiCount += 1
       
    if len(ufos) < 5 and not skbd:
        ufos.add(Ufo('assets/ufo.png', randint(10, 630), 0, 1))

    if len(asteroids) < 2:
        asteroids.add(Ufo('assets/asteroid.png', randint(10, 630), 0, 4))
 
    if sprite.spritecollide(rocket, ufos, True) or sprite.spritecollide(rocket, asteroids, True) or sprite.groupcollide(r, enemyBullets, False, True):
        misses += 1
 
    display.update()
    clock.tick(fps)
 