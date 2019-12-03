import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
    def __init__(self,ai_setting,screen):
        
        super(Ship,self).__init__()
        #初始化飞船 并设置其初始位置
        self.screen = screen
        
        self.ai_setting = ai_setting
        
        #加载飞船图像 并获取其外接矩形
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        print(self.image.get_rect())
        self.screen_rect = screen.get_rect()
        
        #将每艘飞船放在屏幕底部中央
        self.rect.centerx =  self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        
        #在飞船的center中存储小数值
        self.center = float(self.rect.centerx)
        
        
        #移动标志
        self.moving_right = False
        self.moving_left = False
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
           self.center += self.ai_setting.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
           self.center -= self.ai_setting.ship_speed_factor
            
        self.rect.centerx = self.center    
    
    def center_ship(self):
        self.center = self.screen_rect.centerx

        
    def blitme(self):
        #在指定位置上绘制飞船
        self.screen.blit(self.image,self.rect)
        
        
        
        