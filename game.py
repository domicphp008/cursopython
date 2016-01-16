from Abertura import WIDTH, MAXWIDTH, HEIGHT
 
import pygame
 
from TextHandler import TextHandler
 
from pygame.locals import *
from Funsoes import *
 
from Campo import Campo
from Caverna import Caverna
from SalaDoChefe import SalaDoChefe
from Dungeon import Dungeon
 
from Pilastra import Pilastra
 
from Sword import Sword
 
from ItemMenu import ItemMenu
from Escroto import Escroto
 
from DeathAnimation import DeathAnimation
 
from Bitch import Bitch
from Lesma import Lesma
from Planta import Planta
from Sniper import Sniper
from Zumbi import Zumbi
 
from Atk import Atk
from ZumbiAtk import ZumbiAtk
 
import pickle
 
from Player import Player
 
class Game(object):
    def main (self, Surface):
         
        while True:
            Surface.fill((0,0,0))
            dt = self.time
            self.mainClock.tick(30)
            for cell in self.tilemap.layers['triggers'].collide(self.player.collisionRect, 'Porta'):
 
                self.tilemap.StopSounds()
                 
                self.Escroto.SaveTilemap(self.Location+'.tilemap', self.tilemap)
                 
                if self.Location == 'Caverna' and cell['Porta'] == 'Dungeon' or self.Location == 'Dungeon' and cell['Porta'] == 'Caverna':
                    play(pygame.mixer.Sound(resources.file_path('sfx_teleporte.ogg', 'Musica')), 1, self.musicPlaying)
                 
                self.Location = cell['Porta']
                 
                NewSurface = pygame.Surface.copy(Surface)
                self.tilemap.draw(NewSurface)
                 
                del self.tilemap
                 
                if self.Location == 'Campo':
                    self.tilemap = Campo(self.width, self.height, self)
                elif self.Location == 'Caverna':
                    self.tilemap = Caverna(self.width, self.height, self)
                elif self.Location == 'Dungeon':
                    self.tilemap = Dungeon(self.width, self.height, self)
                else:
                    self.tilemap = SalaDoChefe(self.width, self.height, self)
                     
                    self.player.Reset((cell['PlayerX'] - 16, cell['PlayerY']-28))
                    self.player.kill()
                    self.player.add([self.tilemap.SpritesToChoose])
                             
                    self.tilemap.set_focus(self.player.collisionRect.centerx, self.player.collisionRect.centery)
                 
                if self.Location != 'Sala do Mestre':
                    self.tilemap.Reload(self, (cell['PlayerX']-16, cell['PlayerY']-28))
                     
                    for sprite in np.array(self.tilemap.Holes):
                        if self.player.collisionRect.colliderect(sprite.rect):
                            sprite.kill()
                            del sprite
                 
                FadeOut(self, NewSurface, Surface)
                self.ResizeScreen(Surface.get_width(), Surface.get_height())
                 
                         
                self.Pause = True
                self.first = True
                 
                 
 
            if self.Master:
                self.Location = 'Dungeon'
                 
                play(self.Sounds['Jóia'], 1, self.musicPlaying)
                NewSurface = pygame.Surface.copy(Surface)
                NewSurface.blit(self.tilemap.images['background'], ((self.width-WIDTH)//2,0))
                self.tilemap.draw(NewSurface)
                 
                del self.tilemap
                 
                self.tilemap = Dungeon(self.width, self.height, self)
                self.tilemap.Reload(self, (664, 28))
                 
                self.tilemap.set_focus(self.player.collisionRect.centerx, self.player.collisionRect.centery)
                 
                FadeOut(self,NewSurface, Surface)
                 
                for sprite in self.tilemap.Holes:
                    if self.player.collisionRect.colliderect(sprite.rect):
                        sprite.kill()
                        del sprite
                         
                self.Pause = True
                self.first = True
 
                bloqueio = Pilastra(self.tilemap.images['bloqueio'], 'bloqueio', (656, 12), (self.tilemap.SpritesToChoose, self.tilemap.Pilastras))
                for cell in self.tilemap.layers['triggers'].collide(bloqueio.rect, 'block'):
                    if 'a' in cell['block']:
                        cell['block'] = 'ftlrb'
 
            for event in pygame.event.get():
                BASIC_GAME_Events(self, event, Surface)
                 
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        play(self.Sounds['MenuSelect'], 1, self.musicPlaying)
                        if self.Pause:
                            if self.menu:
                                if self.Menu.name == 'Escroto':
                                    self.menu = False
                                    self.Pause = False
                                    self.tilemap.UnpauseSounds()
                                else:
                                    self.Menu = self.Escroto
 
                        else:
                            if (self.Location == 'Campo' and not self.tilemap.Moshiro.talking and not self.tilemap.Lisa.talking) or self.Location != 'Campo': 
                                self.Pause = True
                                self.menu = True
                                self.Menu = self.Escroto
                                self.tilemap.PauseSounds()
 
                    if event.key == K_RETURN:
                        #Menu de Gente Grande
                        play(self.Sounds['MenuSelect'], 1, self.musicPlaying)
                        if self.Pause:
                            if self.menu:
                                if self.Menu.name == 'ItemMenu':
                                    if self.Menu.menu == 'Ferramenta':
                                        for key in self.Menu.Itens:
                                            if self.Menu.Itens[key]['Coluna'] == self.Menu.selected[0] and self.Menu.Itens[key]['Linha'] == self.Menu.selected[1]:
                                                self.Menu.Itens[self.Menu.using]['Usando'] = False
                                                self.Menu.Itens[key]['Usando'] = True
                                                self.Menu.using = key
                                                self.player.item = key
                                    self.Pause = False
                                    self.menu = False
                                    self.tilemap.UnpauseSounds()
                                else:
                                    self.Menu = self.ItemMenu
                         
                        else:
                            if (self.Location == 'Campo' and not self.tilemap.Moshiro.talking and not self.tilemap.Lisa.talking) or self.Location != 'Campo': 
                                self.Pause = True
                                self.menu = True
                                self.Menu = self.ItemMenu
                                self.tilemap.PauseSounds()
 
                    if event.key == K_a:
                        if not self.Pause:
                            self.tilemap.EventGet(self)
                             
                        else:
                            if self.Menu.name == 'Escroto':
                                play(self.Sounds['MenuSelect'], 1, self.musicPlaying)
                                if self.Menu.selected == 0 or self.Menu.selected == 4 or self.Menu.selected == 5:
                                    self.Menu.selected = 0
                                    self.Menu.Max = 2
                                    self.Menu.Min = 0
                                    self.menu = False
                                    self.Pause = False
                                    self.tilemap.UnpauseSounds()
                                elif self.Menu.selected == 1 and self.Location != 'Sala do Mestre':
                                    self.Menu.selected = 3
                                    self.Menu.salvando = True
                                elif self.Menu.selected == 2:
                                    self.Menu.selected = 5
                                    self.Menu.Max = 6
                                    self.Menu.Min = 5
                                elif self.Menu.selected == 6:
                                    terminate()
 
 
                    if event.key == K_s and not self.player.atking and not self.Pause:
                        tileX = testX1 = (self.player.collisionRect.centerx // 16)*16
                        tileY = testY1 = (self.player.collisionRect.centery // 12)*12
                        if self.player.direction == 0:
                            testY1 += 12
                        elif self.player.direction == 2:
                            testY1 -= 12
                        elif self.player.direction == 3:
                            testX1 -= 16
                        else:
                            testX1 += 16
                        colide = False
 
                        for enemie in self.tilemap.Enemies:
                            if pygame.rect.Rect(testX1, testY1, 16,12).colliderect(enemie.collisionRect):
                                colide = True
                                break
 
                        if not colide:
                            if self.player.item == 'Pá':
                                self.player.spritesheet = self.player.PaSheet
                                self.player.number_of_sprite = 0
                                self.player.cont = 0
                                                 
                                self.player.image = self.player.spritesheet[self.player.direction
                                ][self.player.number_of_sprite]
 
                                self.player.digging = True
 
                                self.player.collisionRect.centerx = tileX + 8
                                self.player.collisionRect.centery = tileY + 6
                                                 
                                self.player.rect = pygame.rect.Rect(self.player.rect.left - 16, 
                                                                            self.player.rect.top - 20, 
                                                                            48, 44)
 
                            for hole in self.tilemap.Holes:
                                if pygame.rect.Rect(testX1, testY1, 16,12).colliderect(hole.rect):
                                    colide = True
                                    break
                                     
                            if self.player.item == 'Bomba' and len(self.tilemap.Bombas) == 0 and not colide:
                                if len(self.tilemap.Bombas) == 0:
                                    play(self.Sounds['Bomba'], 1, self.musicPlaying)
                                    if len(self.tilemap.layers['triggers'].collide(pygame.rect.Rect(testX1 + 7, testY1 + 5, 1,1), 'block')) == 0:
                                        Pilastra(self.images['Bomba'], 'Bomba', (testX1, testY1), (self.tilemap.Bombas, self.tilemap.SpritesToChoose))
                                        self.player.collisionRect.centerx = tileX + 8
                                        self.player.collisionRect.centery = tileY + 6
                                    else:
                                        Pilastra(self.images['Bomba'], 'Bomba', (tileX, tileY), (self.tilemap.Bombas, self.tilemap.SpritesToChoose))
                                        self.player.collisionRect.centerx = tileX + (tileX - testX1) + 8
                                        self.player.collisionRect.centery = tileY + (tileY - testY1) + 6
 
                            if self.player.item == 'Martelo':
                                self.player.spritesheet = self.player.MarteloSheet
                                self.player.number_of_sprite = 0
                                self.player.cont = 0
                                                 
                                self.player.image = self.player.spritesheet[
                                self.player.direction][self.player.number_of_sprite]
 
                                self.player.martelando = True
 
                                self.player.collisionRect.centerx = tileX + 8
                                self.player.collisionRect.centery = tileY + 6
 
                    if self.menu:
                        play(self.Sounds['MenuMove'], 1, self.musicPlaying)
                        if self.Menu.name == 'ItemMenu':
                            if event.key == K_UP:
                                self.Menu.selected[1] -= 1
                            if event.key == K_DOWN:
                                self.Menu.selected[1] += 1
                            if event.key == K_LEFT:
                                self.Menu.selected[0] -= 1
                            if event.key == K_RIGHT:
                                self.Menu.selected[0] += 1
                             
                        else:
                            if event.key == K_UP:
                                if self.Menu.selected < self.Menu.Max + 1:
                                    self.Menu.selected -= 1
                            if event.key == K_DOWN:
                                if self.Menu.selected < self.Menu.Max + 1:
                                    self.Menu.selected += 1
                             
                                    #if self.selected == 3:
                                        #self.selected = 0
             
            self.tilemap.Actions(self)
 
            if self.first:
                if self.Location == 'Sala do Mestre':
                    NewSurface.fill((0,0,0))
                    NewSurface.blit(self.tilemap.images['background'], (((self.width-WIDTH)//2,0)))
                self.tilemap.draw(NewSurface)
                 
                FadeIn(self,NewSurface, Surface)
                 
                del NewSurface
                 
                self.first = False
                self.second = True
                if self.Master:
                    self.Master = False
                    self.Escroto.SaveGame(self,'CheckPoint.save', 0 ,2,0)
             
            elif self.second:
                self.Pause = False
                self.second = False
                if self.musicPlaying:
                    self.tilemap.InicializeSounds()
                    if self.Location == 'Sala do Mestre':
                        pygame.mixer.Sound(resources.file_path('sfx_mestre_intro.ogg','Musica')).play(0)
                 
            if not self.Pause:
                self.tilemap.update(dt, self)
             
            if self.Location == 'Sala do Mestre':
                Surface.fill((0,0,0))
                Surface.blit(self.tilemap.images['background'], ((self.width-WIDTH)//2,0))
             
            self.tilemap.draw(Surface)
            if self.menu:
                self.Menu.update(dt, self)
            if self.menu:
                self.Menu.draw(self, Surface)
 
            else:
                BlitLife(Surface, self, self.Heart, self.images['Stamina'], self.tools[0][self.choosed[self.player.item]])
             
            if self.PegouJóia:
                play(self.Sounds['Jóia'], 1, self.musicPlaying)
                self.Escroto.SaveGame(self,'CheckPoint.save', 0 ,2,0)
                self.PegouJóia = False
                 
            TransformSurfaceScale(Surface, self.width, self.height, self.rect)
            pygame.display.update()
             
 
            if self.Location == 'Campo':
                self.tilemap.SetSound(self)
 
                for npc in self.tilemap.NPCs:
                    if npc.talking:
                        self.tilemap.PauseEspecial()
                        npc.display(Surface, self)
                 
 
            if self.player.vida <= 0:
                self.tilemap.StopSounds()
                self.Died(Surface)
            elif 0 < self.player.vida <= 2:
                if self.musicPlaying:
                    if self.Sounds['Morrendo'].get_num_channels() == 0:
                        self.Sounds['Morrendo'].play(-1)
            else:
                if self.Sounds['Morrendo'].get_num_channels() > 0:
                    self.Sounds['Morrendo'].stop()
     
    def ResizeScreen(self, newWidth, newHeight):
        """
        Função que faz o resize da jogo
        de forma que o jogo seja compátivel com qualquer modo de tela entre 4:3 e 16:9
        """
        #precisamos primeiro calcular o tamanho da imagem que será disponibilizada no novo
        #tamanho de tela
        #Formato 16:9 ou 4:3
        #Usaremos a altura como padrão
        Hfator_widscreen = newHeight/9
        Hfator_oldscreen = newHeight/3
 
        #Teste, tela 200/120
 
        MAXW_widscreen = 16*Hfator_widscreen #213,33333
        MAXW_oldscreen = 4*Hfator_oldscreen #160
 
        if newWidth > MAXW_widscreen:
            self.width = self.tilemap.view_w = round(16*HEIGHT/9)
 
        elif newWidth <= MAXW_widscreen and newWidth >= MAXW_oldscreen:
            #Se isso for verdade devemos modificar o tamanho e posição
            #de algumas sprites do jogo
            #Antes, vamos calcular o novo tamanho de tela no tilemap
            self.width = round(newWidth/(newHeight/HEIGHT))
            self.tilemap.view_w = self.width
        else:
            self.width = WIDTH
            self.tilemap.view_w = WIDTH
         
        self.rect = pygame.rect.Rect((0,0), (self.width, self.height))
        self.tilemap.viewport = Rect((0,0), (self.width, self.height))
        self.tilemap.set_focus(self.player.collisionRect.centerx, self.player.collisionRect.centery, True)
         
        self.ModificaTamanho()
     
    def ModificaTamanho(self):
        #Vamos centralizar as posições dos menus
        for key in self.ItemMenu.Itens:
            self.ItemMenu.Itens[key]['Posição'][0] = self.ItemMenu.Itens[key]['Posição Inicial'] + (self.width-WIDTH)//2
         
        self.Escroto.x =  (self.width-WIDTH)//2
         
        #Vamos agora ampliar algumas as imagens transparentes
        self.InvisivelCima = pygame.transform.scale(self.InvisivelCima, (self.width, self.InvisivelCima.get_height()))
        self.ItemMenu.escuro = pygame.transform.scale(self.ItemMenu.escuro, (self.width, self.ItemMenu.escuro.get_height()))
             
        self.rect = pygame.rect.Rect((0,0), (self.width, self.height))
        self.tilemap.viewport = Rect((0,0), (self.width, self.height))
        self.tilemap.set_focus(self.player.collisionRect.centerx, self.player.collisionRect.centery, True)
             
         
    def CreateGame(self, music):
        self.mainClock = pygame.time.Clock()
        self.FPS = 30
        self.musicPlaying = music
        self.Pause = False
 
        self.menu = False
        self.Menu = None
 
        self.Master = False
 
        self.width = WIDTH
        self.height = HEIGHT
        self.rect = pygame.rect.Rect(0, 0, self.width, self.height)
         
        self.first = self.second = False
         
        self.time = 0.033
         
        self.menuHeart = load_sheet('menu_pause_coracao.png', 'Menus', 9, 8)
        self.Heart = load_sheet('menu_hud_coracao.png', 'Imagens', 9, 8)
        self.InvisivelCima = pygame.image.load(resources.file_path('menu_hud_escuro.png', 'Imagens')).convert_alpha()
        self.tools = load_sheet('menu_hud_ferramenta.png', 'Imagens', 26, 8)
         
        self.images = {'Player': {'MoveSheet': load_sheet('spr_pla_andando.png','Imagens', 48, 60),
                                  'AtkSheet': load_sheet('spr_pla_ataque.png','Imagens', 48, 60),
                                  'StopSheet': load_sheet('spr_pla_parado.png','Imagens', 48, 60)},
                        
                       'EnemyDeath': load_sheet('spr_obj_inimigomorto.png', 'Imagens', 16, 20),
 
 
                       'Sword': load_sheet('spr_pla_espada.png','Imagens', 48, 60),
 
                       'Hole': pygame.image.load(resources.file_path('spr_obj_buraco.png', 'Imagens')).convert_alpha(),
                       'Rachadura': pygame.image.load(resources.file_path('spr_obj_rachadura.png', 'Imagens')).convert_alpha(),
                       'Bomba': load_sheet('spr_obj_bomba.png', 'Imagens',16,12),
                       'Explosion': load_sheet('spr_obj_explosao.png', 'Imagens',48,36),
                       'Stamina': pygame.image.load(resources.file_path('menu_hud_stamina.png', 'Imagens')).convert_alpha(),
                       'StaminaMenu': pygame.image.load(resources.file_path('menu_pause_stamina.png', 'Menus')).convert_alpha(),
                       'Coracao': pygame.image.load(resources.file_path('spr_obj_coracao.png', 'Imagens')).convert_alpha(),
                       'FalaEscuro': pygame.transform.scale(self.InvisivelCima, (178, 36)).convert_alpha()}
 
        self.Sounds = {'Espada': {'Swing': pygame.mixer.Sound(resources.file_path('sfx_espada.ogg', 'Musica')),
                                  'Parede': pygame.mixer.Sound(resources.file_path('sfx_wallhit.ogg', 'Musica')),
                                  'Acertou': pygame.mixer.Sound(resources.file_path('sfx_acertando.ogg', 'Musica'))},
                       'Bomba': pygame.mixer.Sound(resources.file_path('sfx_bomba.ogg', 'Musica')),
                       'Moshiro': 'ost_moshiro.ogg',
                       'Cavando': pygame.mixer.Sound(resources.file_path('sfx_cavando.ogg', 'Musica')),
                       'MenuSelect':pygame.mixer.Sound(resources.file_path('sfx_menu_select.ogg', 'Musica')),
                       'MenuMove': pygame.mixer.Sound(resources.file_path('sfx_menu_move.ogg', 'Musica')),
                       'Jóia': pygame.mixer.Sound(resources.file_path('sfx_joia.ogg', 'Musica')),
                       'Morrendo':pygame.mixer.Sound(resources.file_path('sfx_morrendo.ogg', 'Musica')),
                       'Martelo': pygame.mixer.Sound(resources.file_path('sfx_martelo.ogg', 'Musica')),
                       'Buraco': pygame.mixer.Sound(resources.file_path('sfx_cavando.ogg', 'Musica')),
                       'Coração': pygame.mixer.Sound(resources.file_path('sfx_heart.ogg', 'Musica'))}
 
        self.choosed = {'Pá': 0, 'Martelo': 1, 'Bomba': 2}
 
        self.ItemMenu = ItemMenu()
        self.Escroto = Escroto()
         
        self.Campo = Campo(self.width, self.height, self)
        self.Dungeon = Dungeon(self.width, self.height, self)
        self.Caverna = Caverna(self.width, self.height, self)
         
        self.player = Player(self.images['Player'], (self.Campo.start_cell.px - 16, self.Campo.start_cell.py-28), [self.Campo.SpritesToChoose])
 
        self.Location = 'Campo'
        self.tilemap = self.Campo
         
        self.Delivered = 0
         
        self.PegouJóia = False
         
        #Vampos criar os canais onde os efeitos sonoros devem ser colocados
 
 
    def NewGame(self, Surface, music):
        self.CreateGame(music)
 
        if self.musicPlaying:
            self.tilemap.InicializeSounds()
            self.tilemap.SetSound(self)
 
        self.Pause = True
        dt = self.time
         
        self.ResizeScreen(Surface.get_width(), Surface.get_height())
         
        self.tilemap.update(dt, self)
        self.tilemap.Lisa.image = self.tilemap.Lisa.spritesheet[self.tilemap.Lisa.AllDirection['Up']][self.tilemap.Lisa.number_of_sprite]
        self.tilemap.Moshiro.display(Surface, self, False)
        self.tilemap.Moshiro.MoshiroAndando(Surface, self)
        self.tilemap.Lisa.image = self.tilemap.Lisa.spritesheet[self.tilemap.Lisa.AllDirection['Left']][self.tilemap.Lisa.number_of_sprite]
        self.tilemap.Lisa.display(Surface, self, False)
        self.Pause = False
         
        self.SaveTilemaps()
        self.Escroto.SaveGame(self,'CheckPoint.save',0,2,0)
         
        self.main(Surface)
     
 
    def LoadGame(self, Surface, music, Things_To_Dump, died = False):
        self.CreateGame(music)
         
        self.Location = Things_To_Dump[0]
 
        if self.Location == 'Campo':
            self.tilemap = self.Campo
        elif self.Location == 'Dungeon':
            self.tilemap = self.Dungeon
        else:
            self.tilemap = self.Caverna
         
        self.player.kill()
        self.player.add([self.tilemap.SpritesToChoose])
 
        #Agora vamos atualizar as informações do tilemap onde o player se encontra
        #Primeiro as informações do Player
          
        self.player.direction = Things_To_Dump[2][0]
        self.player.number_of_sprite= Things_To_Dump[2][1]
        self.player.collisionRect = Things_To_Dump[2][2]
        self.player.placedPositions = Things_To_Dump[2][3]
        self.player.Justdied = Things_To_Dump[2][4]
        self.player.vida = Things_To_Dump[2][5]
        self.player.vx = Things_To_Dump[2][6]
        self.player.vy = Things_To_Dump[2][7]
        self.player.cooldown = Things_To_Dump[2][8]
        self.player.imunity = Things_To_Dump[2][9]
        self.player.alive = Things_To_Dump[2][10]
        self.player.atking = Things_To_Dump[2][11]
        self.player.digging = Things_To_Dump[2][12]
        self.player.digged = Things_To_Dump[2][13]
        self.player.first_pressed = Things_To_Dump[2][14]
        self.player.pressed = Things_To_Dump[2][15]
        self.player.cont = Things_To_Dump[2][16]
        self.player.cont2 = Things_To_Dump[2][17]
        self.player.numbX = Things_To_Dump[2][18]
        self.player.numbY = Things_To_Dump[2][19]
        self.player.item = Things_To_Dump[2][20]
        self.player.Undelivered = Things_To_Dump[2][21]
         
        if self.player.atking:
            self.player.spritesheet = self.player.atkSheet
        elif self.player.digging:
            self.player.spritesheet = self.player.PaSheet
        elif self.player.vx != 0 or self.player.vy != 0:
            self.player.spritesheet = self.player.MoveSheet
        else:
            self.player.spritesheet = self.player.StopSheet
         
        #Construimos as Espadas do jogo        
        for SwordInfo in Things_To_Dump[3]:
            sword = Sword(self.images['Sword'], (self.player.rect.x - 16, self.player.rect.y - 20), 'Sword', self.player.direction, (self.tilemap.SpritesToChoose, self.tilemap.Swords))
            sword.number_of_sprite = SwordInfo[0]
            sword.image = sword.spritesheet[sword.direction][sword.number_of_sprite]
            sword.cont = SwordInfo[1]
            sword.rect = SwordInfo[2]
         
        #Construimos os inimigos do jogo        
        for EnemieInfo in Things_To_Dump[4]:
            if 'Lesma' == EnemieInfo[0]:
                inimigo = Lesma(self.tilemap.images['Lesma'], (0,0), 'Lesma', (self.tilemap.SpritesToChoose, self.tilemap.Enemies))
            elif 'Bitch' == EnemieInfo[0]:
                inimigo = Bitch(self.tilemap.images['Bitch'], (0,0), 'Bitch', (self.tilemap.SpritesToChoose, self.tilemap.Enemies))
            elif 'Planta' == EnemieInfo[0]:
                inimigo = Planta(self.tilemap.images['Planta'], (0,0), 'Planta', (self.tilemap.SpritesToChoose, self.tilemap.Enemies))
            elif 'Sniper' == EnemieInfo[0]:
                inimigo = Sniper(self.tilemap.images['Sniper'], (0,0), 'Sniper', (self.tilemap.SpritesToChoose, self.tilemap.Enemies))
            else:
                inimigo = Zumbi(self.tilemap.images['Zumbi'], (0,0), 'Zumbi', (self.tilemap.SpritesToChoose, self.tilemap.Enemies))
             
            inimigo.burn = EnemieInfo[1]
            inimigo.collisionRect = EnemieInfo[2]
            inimigo.direction = EnemieInfo[3]
            inimigo.number_of_sprite = EnemieInfo[4]
            inimigo.vida = EnemieInfo[5]
            inimigo.cooldown = EnemieInfo[6]
            inimigo.Max = EnemieInfo[7]
            inimigo.vy = EnemieInfo[8]
            inimigo.vx = EnemieInfo[9]
            inimigo.alive = EnemieInfo[10]
            inimigo.cont = EnemieInfo[11]
            inimigo.numbX = EnemieInfo[12]
            inimigo.numbY = EnemieInfo[13]
            inimigo.atking = EnemieInfo[14]
            inimigo.originalPosition = EnemieInfo[15]
            if not inimigo.alive:
                if inimigo.burn:
                    inimigo.image = inimigo.cinzas
                else:
                    inimigo.image = inimigo.deadImage
         
        #Construcao de Bombas
        for BombaInfo in Things_To_Dump[5]:
            Bomba = Pilastra(self.images['Bomba'], 'Bomba', (0,0), (self.tilemap.SpritesToChoose, self.tilemap.Bombas))
            Bomba.cont = BombaInfo[0]
            Bomba.number_of_sprite = BombaInfo[1]
            Bomba.rect = BombaInfo[2]
         
        #Construcao de Explosoes
        for ExploInfo in Things_To_Dump[6]:
            Explosion = Explosion(self.images['Explosion'], (0,0), 'Explosion', 0, (self.tilemap.Bombas, self.tilemap.SpritesToChoose))
            Explosion.cont = ExploInfo[0]
            Explosion.number_of_sprite = ExploInfo[1]
            Explosion.rect = ExploInfo[2]
         
        #Contrucao de Animacoes
        for AniInfo in Things_To_Dump[7]:
            Animation = DeathAnimation(self.images[AniInfo[0]], (0,0), AniInfo[0], [self.tilemap.SpritesToChoose])
            Animation.rect = AniInfo[1]
            Animation.image = AniInfo[2]
            Animation.number_of_sprite = AniInfo[3]
            Animation.cont = AniInfo[4]
         
        #Construcao de Atks
        for ATKinfo in Things_To_Dump[8]:
            if ATKinfo[0] == 'AtkZumbi':
                ATK = ZumbiAtk(self.tilemap.images['Zumbi']['Atk'], (0,0), ATKinfo[4], ATKinfo[0], [self.tilemap.SpritesToChoose], [enemy for enemy in self.tilemap.Enemies if enemy.nome == 'Zumbi'][0])
            else:
                if 'Sniper' in ATKinfo[0]:
                    ATK = Atk(self.tilemap.images['Sniper']['Atk'], (0,0), ATKinfo[4], ATKinfo[0], ATKinfo[1], [self.tilemap.SpritesToChoose])
                else:
                    ATK = Atk(self.tilemap.images['Planta']['Atk'], (0,0), ATKinfo[4], ATKinfo[0], ATKinfo[1], [self.tilemap.SpritesToChoose])
             
            ATK.number_of_sprite = ATKinfo[2]
            ATK.alive = ATKinfo[3]
            ATK.rect = ATKinfo[5]
            ATK.Max = ATKinfo[6]
            ATK.cont = ATKinfo[7]
         
        #Colocando o menu de Itens
        self.ItemMenu.Itens = Things_To_Dump[9].Itens
        self.ItemMenu.selected = Things_To_Dump[9].selected
        self.ItemMenu.using = Things_To_Dump[9].using
        self.ItemMenu.menu = Things_To_Dump[9].menu
        self.ItemMenu.Fala = Things_To_Dump[9].Fala
         
         
        self.Campo.AdjustTileHoleAndRachadura(Things_To_Dump[1][0], self)
        self.Campo.AdjustJewels(Things_To_Dump[1][0], self)
         
        self.Caverna.AdjustTileHoleAndRachadura(Things_To_Dump[1][1], self)
        self.Caverna.AdjustJewels(Things_To_Dump[1][1], self)
         
        self.Dungeon.AdjustTileHoleAndRachadura(Things_To_Dump[1][2], self)
        self.Dungeon.AdjustJewels(Things_To_Dump[1][2], self)
         
        #Verificamos o numero de joias devolvidas
        self.Delivered = Things_To_Dump[10]
         
        #E por ultimo vemos se ja dialogamos com o sr moshiro ou nao
        self.Campo.Moshiro.first = Things_To_Dump[11]
 
        self.tilemap.set_focus(self.player.collisionRect.centerx, self.player.collisionRect.centery)
         
        if not died:
            self.Escroto.SaveGame(self,'CheckPoint.save', 0, 2,0)
         
        if self.musicPlaying:
            self.tilemap.InicializeSounds()
            self.tilemap.SetSound(self)
         
        self.SaveTilemaps()
         
       #self.ItemMenu.Itens['Safira']['Possui'] = True
       #self.ItemMenu.Itens['Safira']['Delivered'] = True
       #self.Delivered += 1
        self.ResizeScreen(Surface.get_width(), Surface.get_height())  
        self.main(Surface)
     
    def SaveTilemaps(self):
        self.Escroto.SaveTilemap('Campo.tilemap', self.Campo)
        self.Escroto.SaveTilemap('Caverna.tilemap', self.Caverna)
        self.Escroto.SaveTilemap('Dungeon.tilemap', self.Dungeon)
         
        del self.Campo
        del self.Caverna
        del self.Dungeon
     
    def winGame(self, Surface):
        #self.tilemap.Moshiro.display(Surface, self, music = False)
        pygame.mixer.music.load(resources.file_path('ost_moshiro_presto.ogg', 'Musica'))
        pygame.mixer.music.play(-1, 0.0)
        if self.player.collisionRect.x != 448 or self.player.collisionRect.y != 144:
            self.MovePlayer(Surface)
         
         
        self.tilemap.Moshiro.moshiroAndandoFinal(Surface, self)
        self.player.image = self.player.StopSheet[2][0]
         
        self.tilemap.Moshiro.display(Surface, self, False, False)
         
        for pilastra in self.tilemap.Pilastras:
            if pilastra.nome == 'RuinaFinal':
                pilastra.number_of_sprite = 1
                pilastra.image = pilastra.spritesheet[0][pilastra.number_of_sprite]
         
        contador = 0
        limite = 2
         
        self.tilemap.StopSounds()
        pygame.mixer.music.load(resources.file_path('ost_ending.ogg', 'Musica'))
        pygame.mixer.music.play(0, 0.0)
         
        while contador < limite:
            contador += self.mainClock.tick(30)/1000
             
            for event in pygame.event.get():
                QUIT_Event(event)
                Surface = VIDEORESIZE_Event(self, event, Surface)
             
            self.tilemap.draw(Surface)
 
            TransformSurfaceScale(Surface, self.width, self.height, self.rect)
            pygame.display.flip()
         
        #Fade para o Branco
        NewSurface = pygame.Surface.copy(Surface)
        NewSurface.fill((255,255,255))
         
        FadeIn(self,NewSurface, Surface)
        selected = 0
        self.images['Ending'] = load_sheet('menu_final.png', 'Menus', MAXWIDTH, HEIGHT)
         
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate ()
                if event.type == KEYUP:
                    if event.key == ord('m'):
                        if self.musicPlaying:
                            pygame.mixer.music.stop()
                        else:
                            pygame.mixer.music.play(-1, 0.0)
                         
                        self.musicPlaying = not self.musicPlaying
                 
                if event.type == KEYDOWN:
                    if event.key == K_a:
                        if selected < len(self.images['Ending'][0]) - 1:
                            selected += 1
                        else:
                            terminate()
                 
                Surface = VIDEORESIZE_Event(self, event, Surface)
             
            Surface.blit(self.images['Ending'][0][selected], (- (MAXWIDTH-self.width)//2,0))
             
            TransformSurfaceScale(Surface, self.width, self.height, self.rect)
            pygame.display.flip()
            self.mainClock.tick(self.FPS)
         
     
    def MovePlayer(self, Surface):
        #É preciso calcular a tragetória do player para que ele fique de frente para 
        #o sr moshiro (432, 144) 432 + 16 = 448
        posY = self.tilemap.Moshiro.collisionRect.bottom
        posX = self.tilemap.Moshiro.collisionRect.right
         
        tileX = (self.player.collisionRect.centerx // 16)
        tileY = (self.player.collisionRect.centery // 12)
         
        distY = posY - self.player.collisionRect.bottom
         
         
        #Temos que olhar para posição do retângulo do player como um todo
        #Caso o player esteja na linha dos tilesY 11 precisamos ver se
        #o fundo dele nao encosta na tile block
        if tileY == 11:
            #Caso o player esteja na linha dos tilesY 11 precisamos ver se
            #o fundo dele nao encosta na tile block
            if self.player.collisionRect.bottom > 144:
                self.player.AndaAutomatico(2, (self.player.collisionRect.x, 144), self, Surface)
        elif tileY == 12:
            #Caso o player esteja na linha de tilesY 12 ele precisa se deslocar para cima 
            #ou para baixo dependendo do valor da distância em y
            if self.player.collisionRect.x < posX:
                if distY <= 0:
                    self.player.AndaAutomatico(0, (self.player.collisionRect.x, posY+12), self, Surface)
                else:
                    self.player.AndaAutomatico(2, (self.player.collisionRect.x, posY-12), self, Surface)
        else:
            #Neste último caso ele só pode estar na linha de 13 e logo devemos ver se o topo dele nao bate no block
            if self.player.collisionRect.bottom < posY+12 and self.player.collisionRect.x < posX:
                self.player.AndaAutomatico(0, (self.player.collisionRect.x, posY+12), self, Surface)
             
        #Em seguida é preciso fazer o player se mover horizontalmente
        self.player.AndaAutomatico(1, (posX, self.player.collisionRect.bottom), self, Surface)
         
        #E por fim move-lo verticalmente novamente
        distY = posY - self.player.collisionRect.bottom
         
        if distY > 0:
            self.player.AndaAutomatico(0, (self.player.collisionRect.x, posY), self, Surface)
        else:
            self.player.AndaAutomatico(2, (self.player.collisionRect.x, posY), self, Surface) 
         
 
    def Died(self, Surface):
         
        #Leva o player girando para o centro da Tela
        if self.musicPlaying:
            pygame.mixer.Sound(resources.file_path('ost_gameover.ogg', 'Musica')).play()
         
        cont = 0
        dt = self.time
        self.mainClock.tick(30)
         
 
        girando = load_sheet('spr_pla_olhosfechados.png', 'Imagens', 48,60)
        caindo = load_sheet('spr_pla_morto.png', 'Imagens', 48,60)
        sr_moshiro = load_sheet('menu_gameover_moshiro.png', 'Menus', MAXWIDTH,HEIGHT)
        menu = load_sheet('menu_gameover.png', 'Menus', WIDTH, HEIGHT)
 
 
        numero_da_imagem = 0
        Max = len(girando)
         
        self.ResizeScreen(Surface.get_width(), Surface.get_height())
        #Começa a mostrar a animação do player girando
        while cont < 2:
            dt = 2*self.time
            self.mainClock.tick(self.FPS//2)
            imagem = girando[numero_da_imagem][0]
 
            numero_da_imagem += 1
            if numero_da_imagem == Max:
                numero_da_imagem = 0
 
            Surface.fill((0,0,0))
            Surface.blit(imagem, (56+ + (self.width - WIDTH)//2,34))
            TransformSurfaceScale(Surface, self.width, self.height, self.rect)
            pygame.display.flip()
            cont += dt
 
        #Passa a Fazer o player cai
 
        numero_da_imagem = 0
        Max = len(caindo[0])
 
        while numero_da_imagem != Max:
            dt = 4*self.time
            self.mainClock.tick(self.FPS//4)
            imagem = caindo[0][numero_da_imagem]
            numero_da_imagem += 1
 
            Surface.fill((0,0,0))
            Surface.blit(imagem, (56 + (self.width - WIDTH)//2,34))
            TransformSurfaceScale(Surface, self.width, self.height, self.rect)
            pygame.display.update()
 
        pygame.time.wait(1000)
 
        #Fade para o Branco
        NewSurface = pygame.Surface.copy(Surface)
        NewSurface.fill((255,255,255))
         
        FadeIn(self,NewSurface, Surface)
 
        #Sr.Moshiro Falando
        texto = "Estou decepcionado com você"
        font = pygame.font.SysFont("Calibri", 14)
 
        display = TextHandler(texto, pygame.rect.Rect(20, 85, 123, 35), Surface, self, font,[[sr_moshiro, [-(MAXWIDTH - self.width)//2,0], 0, 3*self.time, 0], [pygame.transform.scale(self.images['FalaEscuro'], (214, 36)).convert_alpha(), (0, 84)]], life = False)
         
        del display
         
        #Colocando o Menu de Escolha
        Choose = False
        self.selected = 0
        while not Choose:
            for event in pygame.event.get():
                if event.type == QUIT:
                    terminate()
                if event.type == KEYDOWN:
                    if event.key == K_DOWN:
                        self.selected += 1
                    if event.key == K_UP:
                        self.selected -= 1
                    if event.key == K_a:
                        if self.selected == 0:
                            Archive = open('CheckPoint.save', 'rb')
                            Things_to_Dump = pickle.load(Archive)
                            self.LoadGame(Surface, self.musicPlaying, Things_to_Dump, died = True)
                        else:
                            terminate ()
 
            if self.selected > 1:
                self.selected = 0
            if self.selected < 0:
                self.selected = 1
             
            Surface.fill((0,0,0))
            Surface.blit(menu[0][self.selected], ((self.width - WIDTH)//2,0))
            TransformSurfaceScale(Surface, self.width, self.height, self.rect)
            pygame.display.update()
 
if __name__ == '__main__':
    pygame.init()
    Surface = pygame.display.set_mode((WIDTH,HEIGHT),HWSURFACE|DOUBLEBUF|RESIZABLE)
    pygame.display.set_caption('Cata Jóia')
    Game().main(Surface, True)
