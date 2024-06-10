import pygame
import random as rand

# 全局變數class(每局不更新)
class Snake():
    white = (255, 255, 255)  # 白色RGB
    black = (0, 0, 0)  # 黑色RGB
    red = (255, 0, 0)  # 紅色RGB
    green = (0, 255, 0)  # 綠色RGB
    yello = (255, 255, 0) # 黃色RGB
    display_width = 500  # 畫面寬度，*10倍因為50太小
    display_height = 500  # 畫面高度，*10倍因為50太小
    snake_size = 10  # 蛇身方塊尺寸，*10倍因為1太小
    score_list = []  # 歷史紀錄

    # 區域變數init(每局更新)
    def __init__(self):
        self.snake_pos = [100, 50]  # 蛇頭初始位置
        self.snake_body = [[100, 50]] # 蛇身體組成的list
        self.food_pos = [rand.randint(0, (Snake.display_width // Snake.snake_size) - 1) * Snake.snake_size,
                         rand.randint(0, (Snake.display_height // Snake.snake_size) - 1) * Snake.snake_size] # 食物位置網格算法
        self.food_set = True # 食物是否存在之旗標
        self.score = 0 # 分數
        self.snake_speed = 10  # 蛇的速度
        self.direction = "" # 初始方向

    # 區域變數init(每局更新)
    def init_food_and_body(self):
        self.snake_pos = [100, 50] # 每個蛇身座標變量
        self.snake_body = [[100, 50]] # 蛇身體組成的list
        self.food_pos = [rand.randint(0, (Snake.display_width // Snake.snake_size) - 1) * Snake.snake_size,
                         rand.randint(0, (Snake.display_height // Snake.snake_size) - 1) * Snake.snake_size] # 食物位置網格算法
        self.food_set = True # 食物是否存在之旗標
        self.score = 0 # 分數
        self.snake_speed = 10 # 蛇的速度
        self.direction = ""  # 初始方向

    def display_when_gaming(self, game_window):
        game_window.fill(Snake.black) # 先填滿畫面為黑色
        for pos in self.snake_body:
            pygame.draw.rect(game_window, Snake.white, pygame.Rect(pos[0], pos[1], Snake.snake_size, Snake.snake_size)) # 顯示蛇身為白色(rect為方形)
        pygame.draw.rect(game_window, Snake.red, pygame.Rect(self.food_pos[0], self.food_pos[1], Snake.snake_size, Snake.snake_size)) # 顯示出食物為紅色(rect為方形)

    def move(self):
        # 如果有輸入則執行以下for區塊
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 如果按叉叉則執行關閉程序
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w: # 上下左右或wasd控制
                    if self.direction != "DOWN":
                        self.direction = "UP"  # 要往上同時上一個動作並不是往下(避免直接掉頭)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if self.direction != "UP":
                        self.direction = "DOWN"  # 要往下同時上一個動作並不是往上(避免直接掉頭)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    if self.direction != "RIGHT":
                        self.direction = "LEFT"  # 要往左同時上一個動作並不是往右(避免直接掉頭)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    if self.direction != "LEFT":
                        self.direction = "RIGHT"  # 要往右同時上一個動作並不是往左(避免直接掉頭)

        # 如果沒有輸入則執行以下if區塊
        if self.direction == "UP":
            self.snake_pos[1] -= Snake.snake_size # 往上，頭部y座標量減去一個蛇身
        if self.direction == "DOWN":
            self.snake_pos[1] += Snake.snake_size # 往下，頭部y座標量加上一個蛇身
        if self.direction == "LEFT":
            self.snake_pos[0] -= Snake.snake_size # 往左，頭部x座標量減去一個蛇身
        if self.direction == "RIGHT":
            self.snake_pos[0] += Snake.snake_size # 往右，頭部x座標量減去一個蛇身

        self.snake_body.insert(0, list(self.snake_pos)) # 利用Q原理更新蛇頭更新到蛇身list 0的位置，其餘元素往後推達成模擬蛇正在前進(長度暫時增加)
        if self.snake_pos == self.food_pos:
            self.score += 1
            self.food_set = False # 食物被吃掉，旗標失效
            self.acc_speed()  # 增加速度
        else:
            self.snake_body.pop() # 如果沒吃到，則利用Q原理除去list最後一節來模擬蛇正在前進(去除後長度不變)

        if not self.food_set: # 如果食物旗標為false，則進行set_food函式
            self.set_food()

        self.food_set = True # 食物旗標恢復

    def set_food(self):
        self.food_pos = [rand.randint(0, (Snake.display_width // Snake.snake_size) - 1) * Snake.snake_size,
                         rand.randint(0, (Snake.display_height // Snake.snake_size) - 1) * Snake.snake_size] # 食物位置網格算法

    def bump_into_wall(self):
        if self.snake_pos[0] < 0 or self.snake_pos[0] >= Snake.display_width or self.snake_pos[1] < 0 or self.snake_pos[1] >= Snake.display_height: # 如果超出地圖範圍
            return True
        else:
            return False

    def bump_into_self(self):
        for block in self.snake_body[1:]:  # 利用for迴圈遍歷除了蛇頭的蛇身部位
            if self.snake_pos == block: # 比較蛇頭和蛇身座標是否一樣
                return True
        return False

    def acc_speed(self):
        self.snake_speed += 1 #增加速度

    def display_after_gaming(self, game_window):
        game_window.fill(Snake.black)  # 先填滿畫面為黑色
        font = pygame.font.SysFont("SimHei", 30)  # 設置字形和字體大小
        score_surface = font.render('Game Over!', True, Snake.yello)  # 將Game Over!轉換為畫面
        score_rect = score_surface.get_rect()  # 獲取分數畫面的矩形區域
        score_rect.midtop = (Snake.display_width / 2, 10)  # 設置分數顯示的位置，水平居中，垂直方向上距離窗口頂部 15 個像素
        game_window.blit(score_surface, score_rect)  # 將分數繪製到畫面
        pygame.display.update()  # 更新畫面，顯示Game Over!
        pygame.time.wait(2000)  # 畫面停留 2 秒

        game_window.fill(Snake.black)  # 先填滿畫面為黑色
        # 顯示當局分數區塊
        font = pygame.font.SysFont("SimHei", 30)  # 設置字形和字體大小
        score_surface = font.render('Score : ' + str(self.score), True, Snake.green)  # 將當前遊戲得分轉換為畫面
        score_rect = score_surface.get_rect()  # 獲取分數畫面的矩形區域
        score_rect.midtop = (Snake.display_width / 2, 10)  # 設置分數顯示的位置，水平居中，垂直方向上距離窗口頂部 15 個像素
        game_window.blit(score_surface, score_rect)  # 將分數繪製到畫面
        pygame.display.update()  # 更新畫面，顯示分數
        pygame.time.wait(2000)  # 畫面停留 2 秒

        game_window.fill(Snake.black)  # 先填滿畫面為黑色
        # 顯示歷史分數列表區塊
        self.score_list.append(self.score)  # 將當前遊戲得分添加到歷史分數列表中
        self.score_list.sort(reverse=True)  # 將歷史分數列表從大到小排序
        font = pygame.font.SysFont("SimHei", 30)  # 設置字形和字體大小
        y_pos = 10  # 初始化 y 座標位置
        for i, score in enumerate(self.score_list):  # 遍歷歷史分數列表
            score_surface = font.render('Rank {}: {}'.format(i + 1, score), True, Snake.green)  # 將每個歷史分數排名轉換為畫面
            score_rect = score_surface.get_rect()  # 獲取分數畫面的矩形區域
            score_rect.midtop = (Snake.display_width / 2, y_pos)  # 設置每個分數顯示的位置
            game_window.blit(score_surface, score_rect)  # 將分數表面對象繪製到畫面上
            y_pos += 30  # 增加 y 座標位置，讓下一個分數顯示在前一個分數的下方
        pygame.display.update()  # 更新遊戲視窗，以顯示歷史分數列表
        pygame.time.wait(2000)  # 畫面停留 2 秒
        if len(self.score_list) == 10:  # 當排行榜為10的時候清空排行榜
            self.score_list.clear()  # 清空分數list


pygame.init()# 初始化pygame
game_window = pygame.display.set_mode((Snake.display_width, Snake.display_height)) # 創造窗口
pygame.display.set_caption("貪吃蛇(按下wasd或上下左右開始操作)") # 執行畫面的名字
fps = pygame.time.Clock() # 畫面更新時鐘
snake_game = Snake() # 創立物件

while True:
    snake_game.move() # 偵測鍵盤以移動蛇
    if snake_game.food_set == False: # 雙重檢查食物旗標(move裡已經檢查一次)
        snake_game.set_food() # 設置食物
        snake_game.food_set = True # 食物旗標恢復

    snake_game.display_when_gaming(game_window) # 顯示畫面
    if snake_game.bump_into_wall() or snake_game.bump_into_self(): # 如果撞牆或撞到自己
        snake_game.display_after_gaming(game_window) # 顯示分數排名畫面
        snake_game.init_food_and_body() # 初始化所有變數

    pygame.display.update() # 畫面更新
    fps.tick(snake_game.snake_speed) # 畫面時鐘更新
