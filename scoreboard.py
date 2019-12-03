import pygame.font
from ship import Ship
from pygame.sprite import Group
class Scoreboard():
    #   显示得分信息的类
    def __init__(self,ai_settings,screen,stats):
        # 初始化得分显示所涉及的属性
        self.screen = screen
        self.ai_settings = ai_settings
        self.stats = stats
        self.screen_rect =  screen.get_rect()
        
        # 显示得分信息时所用的字体
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont('Helvetica',48)
        
        # 准备初始得分对象  和最高分的对象 等级图像
        
        self.prep_score()
        
        self.prep_high_score()
        
        self.prep_level()
        
        self.prep_ship()
        
    def prep_ship(self):
       #显示还剩下几艘飞船
       self.ships = Group()
       for ship_number in range(self.stats.ships_left):
           ship = Ship(self.ai_settings,self.screen)
           ship.rect.x = 10 + ship_number*ship.rect.width
           ship.rect.y = 10
           self.ships.add(ship)
           
       
    def prep_score(self):
        
        # 在此做千分位的分隔
        '''
        “函数round() 通常让小数精确到小数点后多少位，
        其中小数位数是由第二个实参指定的。
        然而，如果将第二个实参指定为负数，
        round() 将圆整到最近的10、100、1000等整数倍。
        ❶处的代码让Python将stats.score 的值圆整到最近的10的整数倍，
        并将结果存储到rounded_score 中”
        '''
        rounded_score = int(round(self.stats.score,-1)) #❶
               
        # 将得分转换为屏幕可见的对象
        score_str = '{:,}'.format(rounded_score)
        
        # 通过字体的方法 render一个图像出来
        self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)

        #将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20  
        
    def prep_high_score(self):
        # 将最高分的数字转换为图像
        high_score = int(round(self.stats.high_score,-1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.ai_settings.bg_color)
        
        # 将最高得分放在屏幕的右上角
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top +20
    
    def prep_level(self):
        self.level_image = self.font.render(str(self.stats.level),True,self.text_color,self.ai_settings.bg_color)
        
        # 将等级放在得分的下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.bottom + 10
        self.level_rect.right = self.screen_rect.right - 20
    
    def show_score(self):
        # 在屏幕上显示得分
        self.screen.blit(self.score_image,self.score_rect)
        
        # 将最高分放在屏幕的顶部中央
        self.screen.blit(self.high_score_image,self.high_score_rect)
        
        self.screen.blit(self.level_image,self.level_rect)
        
        self.ships.draw(self.screen)