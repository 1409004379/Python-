#创建一个设置的模块 保存用户的设置信息

#存储外星人入侵的所有设置的类
class Settings():
    def __init__(self):
        self.screen_width=1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        self.ship_speed_factor = 15.5 #飞船的速度
        self.ship_limit = 3
        
        #创建子弹的设置
        self.bullet_speed_factor = 10
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 30
        
        #创建外星人的设置
        self.alien_speed_factor =10 #横移的速度
        self.fleet_drop_speed = 20 #下降的速度
        self.fleet_drection = 1 # -1表示左移 1表示右移
        
        # 以什么样的节奏加快游戏的速度
        self.speed_scale = 1.1
        
        # 游戏加快节奏后 提高游戏得分的点数
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()   
             
        
    def initialize_dynamic_settings(self):
        
        # 初始化随游戏进行而变化的节奏
        self.ship_speed_factor = 15.5
        self.bullet_speed_factor = 10
        self.alien_speed_factor = 10
        self.fleet_drection = 1 #1表示右移为正向,-1表示为负向
        
        self.alien_points = 50
        
        
    def increase_speed(self):
        
        # 提升速度
        self.ship_speed_factor *= self.speed_scale
        self.bullet_speed_factor *= self.speed_scale
        self.alien_speed_factor *= self.speed_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)
          
        