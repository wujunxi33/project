import pygame
import sys
BOARD_SIZE = 15 
GRID_SIZE = 60   
PIECE_RADIUS = 25  
LINE_WIDTH = 2    
BOARD_COLOR = (220, 179, 92)  
LINE_COLOR = (0, 0, 0)        
BLACK = (0, 0, 0)             
WHITE = (255, 255, 255)       
HIGHLIGHT_COLOR = (255, 0, 0) 
BOARD_WIDTH = BOARD_SIZE * GRID_SIZE
BOARD_HEIGHT = BOARD_SIZE * GRID_SIZE
MARGIN_X = (1080 - BOARD_WIDTH) // 2
MARGIN_Y = (2198 - BOARD_HEIGHT) // 2
class GomokuGame:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((1080, 2198))
		pygame.display.set_caption("五子棋")
		self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
		self.current_player = 1  
		self.game_over = False
		self.last_move = None
		self.font = pygame.font.SysFont('黑体', 30)
	def draw_board(self):
		self.screen.fill(BOARD_COLOR)
		for i in range(BOARD_SIZE)：
			pygame.draw.line(self.screen, LINE_COLOR, 
							(MARGIN_X, MARGIN_Y + i * GRID_SIZE), 
							(MARGIN_X + BOARD_WIDTH, MARGIN_Y + i * GRID_SIZE), 
							LINE_WIDTH)
			pygame.draw.line(self.screen, LINE_COLOR, 
							(MARGIN_X + i * GRID_SIZE, MARGIN_Y), 
							(MARGIN_X + i * GRID_SIZE, MARGIN_Y + BOARD_HEIGHT), 
							LINE_WIDTH)
		for row in range(BOARD_SIZE):
			for col in range(BOARD_SIZE):
				if self.board[row][col] == 1:  
					pygame.draw.circle(self.screen, BLACK, 
									 (MARGIN_X + col * GRID_SIZE, MARGIN_Y + row * GRID_SIZE), 
									 PIECE_RADIUS)
				elif self.board[row][col] == 2:  
					pygame.draw.circle(self.screen, WHITE, 
									 (MARGIN_X + col * GRID_SIZE, MARGIN_Y + row * GRID_SIZE), 
									 PIECE_RADIUS)
		if self.last_move:
			row, col = self.last_move
			pygame.draw.circle(self.screen, HIGHLIGHT_COLOR, 
							 (MARGIN_X + col * GRID_SIZE, MARGIN_Y + row * GRID_SIZE), 
							 PIECE_RADIUS // 2, 2)
		player_text = "当前: 黑棋" if self.current_player == 1 else "当前: 白棋"
		text_surface = self.font.render(player_text, True, BLACK)
		self.screen.blit(text_surface, (50, 50))
		if self.game_over:
			winner = "黑棋获胜!" if self.check_win(1) else "白棋获胜!"
			text_surface = self.font.render(winner, True, (255, 0, 0))
			text_rect = text_surface.get_rect(center=(1080//2, 100))
			self.screen.blit(text_surface, text_rect)
	def handle_click(self, pos):
		if self.game_over:
			return
		x, y = pos
		col = round((x - MARGIN_X) / GRID_SIZE)
		row = round((y - MARGIN_Y) / GRID_SIZE)
		if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and self.board[row][col] == 0:
			self.board[row][col] = self.current_player
			self.last_move = (row, col)

			if self.check_win(self.current_player):
				self.game_over = True
			else:
				# 切换玩家
				self.current_player = 3 - self.current_player  # 1->2, 2->1
	
	def check_win(self, player):
		if not self.last_move:
			return False
		
		directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 四个方向
		row, col = self.last_move
		
		for dr, dc in directions:
			count = 1  # 当前位置已经有一个棋子
			
			# 正向检查
			r, c = row + dr, col + dc
			while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
				count += 1
				r += dr
				c += dc
			
			# 反向检查
			r, c = row - dr, col - dc
			while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
				count += 1
				r -= dr
				c -= dc
			
			if count >= 5:
				return True
		
		return False
	
	def reset_game(self):
		self.board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
		self.current_player = 1
		self.game_over = False
		self.last_move = None
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:  # 左键点击
						self.handle_click(event.pos)
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:  # 按R键重置游戏
						self.reset_game()
			
			self.draw_board()
			pygame.display.flip()
if __name__ == "__main__":
	game = GomokuGame()

	game.run()
