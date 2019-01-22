import pygame as pg
import config as c


DEFAULT_FPS = 60

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)


class GUI:

	def start(self):
		pg.init()
		pg.display.set_caption("EcoSim")

		self.screen = pg.display.set_mode((self.simulator.MAX_X,
											self.simulator.MAX_Y))

		self.clock = pg.time.Clock()
		self.clock.tick(c.MAX_FPS)

	def handle_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.simulator.running = False

	def get_delta(self):
		if self.clock.get_fps() != 0:
			return (1. / self.clock.get_fps()) * DEFAULT_FPS
		else:
			return 1.

	def draw_rect_center(self, color, x, y, w, h):
		rect = pg.Rect(x - (w // 2), y - (h // 2), w, h)
		pg.draw.rect(self.screen, color, rect)

	def draw_phase(self):

		# Clear screen
		self.screen.fill(WHITE)

		# -- Draw NPCs
		for npc in self.simulator.npc_list:
			if npc.showing():
				rounded = npc.pos.get_rounded()
				pg.draw.circle(self.screen, GREEN, (rounded.x, rounded.y), 3)

		# -- Draw SHOPs
		for shop in self.simulator.shop_list:
			if shop.showing():
				rounded = shop.pos.get_rounded()
				self.draw_rect_center(BLUE, rounded.x, rounded.y,
					10, 10)

		# -- Draw FPS counter
		fpsfont = pg.font.SysFont('Comic Sans MS', 30)
		s_fps = fpsfont.render('FPS: %d' % (int(self.clock.get_fps())),
			True, BLACK)
		self.screen.blit(s_fps, (0, 0))

		# Update
		pg.display.update()
		self.clock.tick(c.MAX_FPS)
