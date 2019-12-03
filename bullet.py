import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    #一个对飞船的子弹进行管理的类
    def __init__(self,ai_setting,screen,ship):
        super(Bullet,self).__init__()
        self.screen = screen
        
        #在(0,0)处创建一个子弹的图像 pygame.Rect应该是创建矩形的方法
        self.rect = pygame.Rect(0,0,ai_setting.bullet_width,ai_setting.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        # 存储用小数表示的子弹的位置
        self.y = float(self.rect.y)
        
        self.color = ai_setting.bullet_color
        self.speed_factor = ai_setting.bullet_speed_factor
     
    def update(self):
        # 向上移动子弹
        self.y -= self.speed_factor #更新表示子弹的小数值
        
        #更新子弹的位置
        self.rect.y = self.y
        
    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)
        
        
        
        