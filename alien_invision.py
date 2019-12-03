import sys
import pygame
from settings import Settings
import game_fuctions as gf
from ship import Ship
from pygame.sprite import  Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
def run_game():
    
    #引入导入的模块
    ai_settings = Settings()
    
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    screen =pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alien Invision") #设置标题
    # bg_color = ai_settings.bg_color #这里表示的是一个RGB色值
    
    # 创建play按钮
    play_button = Button(ai_settings,screen,'PLAY')
    
     
    ship = Ship(ai_settings,screen)
    
    
    #创建一个存储子弹的编组
    bullets = Group()
    
    #创建一个存储外星人的编组
    aliens = Group()
    
    #创建外星人群
    gf.create_fleet(ai_settings,screen,aliens,ship)
    
    
    
    #创建一个用于统计游戏存储信息的实例
    stats = GameStats(ai_settings)
    
    
    # 创建记分牌
    sb = Scoreboard(ai_settings,screen,stats)
    
    # 开始游戏的主循环
    while True:
        #监视键盘和鼠标事件
        gf.check_envents(ai_settings,screen,ship,bullets,stats,play_button,aliens,sb)
        gf.update_screen(ai_settings,screen,ship,bullets,aliens,stats,play_button,sb)

        if  stats.game_active:
            # 每次循环都调用飞船的更新方法
            ship.update() 

            gf.update_bullets(bullets,aliens,ai_settings,ship,screen,stats,sb)
            
            
            #不断地 更新外星人的位置
            
            gf.update_alien(ai_settings,aliens,ship,screen,stats,bullets,sb)
            
        
            # gf.update_screen(ai_settings,screen,ship,bullets,aliens,stats,play_button)
        
run_game()