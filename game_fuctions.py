import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets,sb):
    # 检测是否有外星人到达了屏幕的底部
    screen_rect = screen.get_rect()
    
    for alien in aliens.sprites():
         if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理 表示玩家失败
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb)
            
            break     
            
def ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb):
    
    if stats.ships_left > 0:
        
    
        # 响应被外星人撞到的飞船
        stats.ships_left -= 1
        
        # 清空外星人和子弹列表
        aliens.empty()
        bullets.empty()
        
        # 更新显示剩余的飞船数
        sb.prep_ship()
        
        
        # 创建一群新的外星人 并将飞船重新放置在屏幕的底端中央
        create_fleet(ai_settings,screen,aliens,ship)
        
        ship.center_ship()
        
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
    

#键盘按下的事件监测
def check_keydown_events(event,ai_settings,screen,ship,bullets):
    # 响应按键
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    
        

#键盘抬起的事件监测
def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

# 管理屏幕事件
def check_envents(ai_settings,screen,ship,bullets,stats,play_button,aliens,sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
             check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type ==pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # “我们使用了pygame.mouse.get_pos() ，它返回一个元组，其中包含玩家单击时鼠标的x 和y 坐标”
             mouse_x,mouse_y =pygame.mouse.get_pos() 
             check_play_button(stats,play_button,mouse_x,mouse_y,ai_settings,screen,ship,aliens,bullets,sb)

#在玩家单击游戏的play按钮时开始游戏 
def check_play_button(stats,play_button,mouse_x,mouse_y,ai_settings,screen,ship,aliens,bullets,sb):
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        # 隐藏鼠标的光标
        pygame.mouse.set_visible(False)
        
        # 重置游戏的速度
        ai_settings.initialize_dynamic_settings()
        
        
        # 重置游戏的统计信息
        stats.reset_stats()
        stats.game_active = True    
        
        
        sb.prep_score()
        sb.prep_level()
        sb.prep_high_score() 
        sb.prep_ship()    
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        
        # 创建一群新的外星人 并将飞船放在屏幕底部中央
        create_fleet(ai_settings,screen,aliens,ship)
        ship.center_ship() 
         

# 更新外星人
def update_alien(ai_settings,aliens,ship,screen,stats,bullets,sb):
    
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    
    #检测飞船和外星人之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb)
        
    # 检测外星人是否到达了屏幕底部
    
    check_aliens_bottom(ai_settings,stats,screen,ship,aliens,bullets,sb)
    
# 更新子弹
def update_bullets(bullets,aliens,ai_settings,ship,screen,stats,sb):
            
    # 当对编组调用update时,编组自动对其中的每个精灵调用update 因此将为每个子弹调用 bullet.update()
    bullets.update()    
    #删除已消失的子弹
    
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    '''
    新增的这行代码遍历编组bullets 中的每颗子弹，
    再遍历编组aliens 中的每个外星人。每当有子弹和外星人的rect 重叠时，
    groupcollide() 就在它返回的字典中添加一个键-值对。
    两个实参True 告诉Pygame删除发生碰撞的子弹和外星人。
    （要模拟能够穿行到屏幕顶端的高能子弹——消灭它击中的每个外星人，
    可将第一个布尔实参设置为False ，并让第二个布尔实参为True 。
    这样被击中的外星人将消失，但所有的子弹都始终有效，直到抵达屏幕顶端后消失。）
    '''
    #检查是否有子弹与外星人的边缘碰撞
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    
    if collisions:
        for alienss in collisions.values():
            stats.score += ai_settings.alien_points*len(alienss)
            sb.prep_score()
            
        check_high_score(stats,sb)
        
        
    
    if len(aliens) == 0 :
        
        # 清空屏幕上的外星人后等级加一级
        stats.level +=1
        sb.prep_level()
        
        # 删除现有的子弹 新建一群外星人
        bullets.empty()
        create_fleet(ai_settings,screen,aliens,ship)
        ai_settings.increase_speed() #外星人被清空后增加游戏的速度

def fire_bullets(ai_settings,screen,ship,bullets):
    #创建一个子弹 并将其加入到编组bullets中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)


def update_screen(ai_settings,screen,ship,bullets,aliens,stats,play_button,sb):
    # 更新屏幕上的图像 每次进入都重新绘制
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人外面绘制所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    
    #开始绘制ship
    ship.blitme()
    
    sb.show_score()
    # 绘制外星人 对编组调用draw方法 编组内的每个元素都会执行相应的方法,绘制位置由传入的位置决定
    #传入的位置表示整个屏幕
    aliens.draw(screen)
    
    
    # 如果游戏处于非活动状态 就绘制play按钮
    if not stats.game_active:
        play_button.draw_button() 
    
    #让最近绘制的屏幕可见
    pygame.display.flip()
    

def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    # 将外星人整体下下移
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_drection  *= -1
        
      
    
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    #为了在屏幕的两侧空出两个外星人的边距
   
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height*row_number
    aliens.add(alien)


def get_number_alienx(ai_settings,alien_width):
    
    available_space_x = ai_settings.screen_width -2* alien_width
    # 两个外星人中间增加一个外星人的间距 表示X轴上有多少个外星人
    number_aliens_x = int(available_space_x/(alien_width*2))
    
    return number_aliens_x

def get_number_rows(ai_settings,ship_height,alien_height):
    # 计算屏幕可容纳多少行外星人
    available_space_y = ai_settings.screen_height - 3*alien_height -ship_height
    number_rows  = int(available_space_y /(2*alien_height))
    return number_rows 

def create_fleet(ai_settings,screen,aliens,ship):
    #创建外星人群
    #创建一个外星人 并计算一行可以容纳多少外星人
    #外星人的间距为外星人的宽度
   
    # 创建第一行外星人
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_alienx(ai_settings,alien.rect.width)
    number_aliens_row = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    
    for  alien_row in range(number_aliens_row):
         for alien_number in range(number_aliens_x):
             # 创建第一个外星人 并将其加入到当前行
             alien = Alien(ai_settings,screen)
             create_alien(ai_settings,screen,aliens,alien_number,alien_row)
    

def check_high_score(stats,sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()            