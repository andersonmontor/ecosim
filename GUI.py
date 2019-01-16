import pygame as pg

WINDOW_HEIGHT = 728
WINDOW_WIDTH = 1024
MAX_FPS = 60

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


class GUI:

	def start(self):
		pg.init()
		pg.display.set_caption("EcoSim")

		self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

		self.clock = pg.time.Clock()
		self.clock.tick(MAX_FPS)

	def handle_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				print ("exit detected")
				self.simulator.running = False

	def draw_phase(self):
		if self.clock.get_fps() != 0:
			self.delta = (1. / self.clock.get_fps()) * MAX_FPS

		else:
			self.delta = 1.

		# Clear screen
		self.screen.fill(WHITE)

		# - Draw things

		# -- Draw NPCs
		for npc in self.simulator.npc_list:
			if npc.showing():
				pg.draw.circle(self.screen, GREEN, (npc.x, npc.y), 10)

		# Update
		pg.display.update()
		self.clock.tick(MAX_FPS)
