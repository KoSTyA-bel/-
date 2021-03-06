# Импортируем библиотеки
from pygame import *
from player import *
from blocks import *
from readlevel import *
from startwindow import *
from monsters import *
from camera import Camera
from settings import *

pygame.display.set_caption(GAME_NAME)
font_lvl = pygame.font.SysFont(None, 50)
window = pygame.display.set_mode(DISPLAY)
screen = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))

def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l+WIN_WIDTH / 2, -t+WIN_HEIGHT / 2

    l = min(0, l)                           # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)   # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t) # Не движемся дальше нижней границы
    t = min(0, t)                           # Не движемся дальше верхней границы

    return Rect(l, t, w, h)

def pause():
    punkts = [(WIN_WIDTH / 2 - 90, 300, u'Continue', (11, 0, 77), (30,250,30), 0),
          (WIN_WIDTH / 2 - 50, 340, u'Exit', (11, 0, 77), (250,30,30), 1)]
    game = Menu(punkts)
    game.showMenu()

def endgame():
    punkts = [(320, 300, u'The end', (250,30,30), (250,30,30), 0)]
    game = Menu(punkts)
    game.showMenu()

def playLvl(way, num, lvl_name):
    if num != 1:
        punkts = [(WIN_WIDTH / 2 - 50, 300, u'Next', (11, 0, 77), (30,250,30), 0),
            (WIN_WIDTH / 2 - 50, 340, u'Exit', (11, 0, 77), (250,30,30), 1)]
    else:
        punkts = [(WIN_WIDTH / 2 - 50, 300, u'Play', (11, 0, 77), (30,250,30), 0),
            (WIN_WIDTH / 2 - 50, 340, u'Exit', (11, 0, 77), (250,30,30), 1)]

    game = Menu(punkts)
    game.showMenu()
    
    Lvl = Level(way)
    timer = pygame.time.Clock()
    screen = pygame.display.set_mode(DISPLAY) # Создаем окошко
    bg = Surface((WIN_WIDTH,WIN_HEIGHT)) # Создание видимой поверхности
                                         # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом

    #создаём героя
    hero = Player(Lvl.getPlayerX(), Lvl.getPlayerY()) # создаем героя по (x,y) координатам
    left = right = up = False # по умолчанию - стоим

    entities = Lvl.getEntities()
    platforms = Lvl.getPlatforms()
    monsters = Lvl.getMonsters()
    entities.add(hero)

    camera = Camera(camera_configure, len(Lvl.getLvl()[0])*PLATFORM_WIDTH, len(Lvl.getLvl())*PLATFORM_HEIGHT)
    #Delete useless sings
    del(punkts)
    del(Lvl)
    del(game)
    show_fps = False;

    while True: # Основной цикл программы
        #фПС
        timer.tick(50)
        for event in pygame.event.get():
            # Обрабатываем закрытие игры
            if event.type == QUIT:
                raise SystemExit
            # Обрабатываем нажатую кнопку
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    up = True
                if event.key == K_LEFT:
                    left = True
                if event.key == K_RIGHT:
                    right = True
                if event.key == K_f:
                    show_fps = not show_fps
                if event.key == K_ESCAPE:
                    pause()

            # Обрабатываем отжатую кнопку
            if event.type == KEYUP:
                if event.key == K_UP:
                    up = False
                if event.key == K_RIGHT:
                    right = False
                if event.key == K_LEFT:
                    left = False
        # Каждую итерацию необходимо всё перерисовывать
        screen.blit(bg, (0,0))
        monsters.update(platforms)
        camera.update(hero) # центризируем камеру относительно персонажа
        hero.update(left, right, up, platforms, entities) # передвижение
        
        #Рисуем платформы
        for entity in entities:
            screen.blit(entity.image, camera.apply(entity))
        
        #Отображаем название уровня
        screen.blit(font_lvl.render(lvl_name, True, "#8bfff4"), (10,10))
        
        if show_fps:
            screen.blit(font_lvl.render("{}".format(str(timer)[11:13]), True, "#8bfff4"), (WIN_WIDTH - 40, 0))
        
        pygame.display.update()     # обновление и вывод всех изменений на экран
        
        if hero.isWin(): 
            break
        
        if not hero.isLive():
            time.wait(300)
            hero.teleporting()

def main():
    playLvl('levels/2.txt', 1, "Cave")
    playLvl('levels/1.txt', 2, "Bad tonnels")
    endgame()
    
if __name__ == "__main__":
    main()