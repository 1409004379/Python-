import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    #表示单个外星人的类
    
    def __init__(self,ai_setting,screen):
        super(Alien,self).__init__()
        self.ai_setting = ai_setting
        self.screen = screen
        
        #加载外星人的图像
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        
        # 外星人最初都在屏幕的左上角 将外新人的左边距都设置为外星人的宽 将外星人的上边距设置为外星人图片的高
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        
        # 存储外星人的准确位置
        self.x = float(self.rect.x)
    
    def update(self):
        self.x += self.ai_setting.alien_speed_factor * self.ai_setting.fleet_drection
        self.rect.x = self.x
        
    def check_edges(self):
        # 如果外星人位于屏幕边缘,就返回True
       screen_rect = self.screen.get_rect()
       if self.rect.right >= screen_rect.right:
           return True
       elif self.rect.left <=0:
           return True
    
    def blitme(self):
        self.screen.blit(self.image,self.rect)