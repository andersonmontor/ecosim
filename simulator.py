import GUI


class Item:

	id = -1
	name = ""
	recipe = {}  # dict of IDs of items and amounts


class WorldEntity:

	name = ""
	inventory = {}
	x = 0
	y = 0

	def __init__(self, name, x, y):
		self.name = name
		self.x = x
		self.y = y

	def showing(self):
		return True


class NPC(WorldEntity):

	money = 0.0
	controller = None  # controller object
	base_speed = 1

	def movespeed(self):
		return self.base_speed


class Shop(WorldEntity):

	owner = None  # NPC object


class Simulator:

	def __init__(self, guiobj):
		self.gui = guiobj
		guiobj.simulator = self
		self.npc_list = []
		self.MAX_Y = GUI.WINDOW_HEIGHT
		self.MAX_X = GUI.WINDOW_WIDTH

	def main_loop(self):

		self.gui.start()

		self.world_gen()

		self.running = True
		while self.running:

			self.gui.handle_events()

			# Simulator logic'

			self.gui.draw_phase()

	def world_gen(self):
		new_npc = NPC("Teste", 200, 200)
		self.npc_list.append(new_npc)
