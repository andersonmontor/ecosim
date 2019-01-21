import pygame as pg
import config as c


# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


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
			return (1. / self.clock.get_fps()) * c.MAX_FPS
		else:
			return 1.

	def draw_phase(self):

		# Clear screen
		self.screen.fill(WHITE)

		# - Draw things

		# -- Draw NPCs
		for npc in self.simulator.npc_list:
			if npc.showing():
				pg.draw.circle(self.screen, GREEN, (npc.pos.x, npc.pos.y), 10)

		# -- Draw SHOPs
		for shop in self.simulator.shop_list:
			if shop.showing():
				rect = pg.Rect(shop.pos.x, shop.pos.y, 40, 40)
				pg.draw.rect(self.screen, BLUE, rect)

		# Update
		pg.display.update()
		self.clock.tick(c.MAX_FPS)
