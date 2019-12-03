class GameStats():
    # 跟踪游戏的统计信息
    def __init__(self,ai_settings):
      
        self.ai_settings = ai_settings
        self.reset_stats()
        
        # 在任何情况下都不能重置最高分
        self.high_score = 0
        
        
        # 表示游戏是否仍在进行 让游戏一开始处于非活动状态
        self.game_active = False
        
        
    def reset_stats(self):
        # 初始化在游戏运行期间可能变化的统计信息
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0 #每次开始游戏都要重新计分
        
        self.level = 1 #每次开始游戏都将等级重新划分
        
        
