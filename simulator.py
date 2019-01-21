import config as c
import AI


# Kind of a point too...
class Vector:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def multiply(self, scalar):
		self.x *= scalar
		self.y *= scalar

	def divide(self, scalar):
		self.x /= scalar
		self.y /= scalar

	def add(self, other):
		self.x += other.x
		self.y += other.y

	def sub(self, other):
		self.x -= other.x
		self.y -= other.y

	def normalize(self):
		mag = (self.x ** 2 + self.y ** 2)**0.5
		self.divide(mag)

	def vector_to_other(self, other):
		x = other.x - self.x
		y = other.y - self.y

		return Vector(x, y)


class Item:

	id = -1
	name = ""
	volume = 1
	recipe = {}  # dict of IDs of items and amounts


class WorldEntity:

	id = -1
	name = ""
	inventory = {}
	capacity = 1000
	ready = True

	def __init__(self, name, x, y):
		self.name = name
		self.pos = Vector(x, y)

	def showing(self):
		return True

	def addItem(self, itemobj, quant):
		if self.haveRoomFor(itemobj, quant):
			if itemobj in self.inventory.keys():
				self.inventory[itemobj] += quant
			else:
				self.inventory[itemobj] = quant
			return True
		else:
			return False

	def haveRoomFor(self, itemobj, quant):
			return (self.usedCapacity() + (itemobj.volume * quant)) \
				<= self.capacity

	def usedCapacity(self):
		used = 0
		for key, val in self.inventory.items():
			used += key.volume * val
		return used

	def begin_frame(self):
		self.ready = True

	def direction_to_entity(self, other):
		vec = self.pos.vector_to_other(other.pos)
		vec.normalize()

		return vec


class NPC(WorldEntity):

	money = 0.0
	controller = None  # controller object(AI/human player)
	base_speed = 1

	def __init__(self, name, x, y):
		super().__init__(name, x, y)
		self.controller = AI.NPC_AI()
		self.controller.npc = self

	def movespeed(self):
		return self.base_speed

	def move_this_direction(self, vecdir):
		if self.ready:
			vecdir.normalize()
			vecdir.multiply(self.movespeed())
			self.pos.add(vecdir)

			self.ready = False
			return True


class Shop(WorldEntity):

	owner = None  # NPC object
	itemproduction = None  # Item object


class Simulator:

	def __init__(self, guiobj):
		self.gui = guiobj
		guiobj.simulator = self
		self.npc_list = []
		self.shop_list = []
		self.MAX_X = c.WORLD_WIDTH
		self.MAX_Y = c.WORLD_HEIGHT

	def main_loop(self):

		self.gui.start()

		self.world_gen()

		self.running = True
		while self.running:

			self.gui.handle_events()

			self.delta = self.gui.get_delta() * c.SIM_SPEED

			# Prep entities for frame
			for ent in self.npc_list + self.shop_list:
				ent.begin_frame()

			# Let NPCs play
			for npc in self.npc_list:
				npc.controller.play()

			self.gui.draw_phase()

	def world_gen(self):
		new_npc = NPC("Teste", 200, 200)
		new_shop = Shop("Test shop", 500, 500)
		self.addNPC(new_npc)
		self.addShop(new_shop)

	def addNPC(self, npcobj):
		self.npc_list.append(npcobj)

	def addShop(self, shopobj):
		self.shop_list.append(shopobj)
