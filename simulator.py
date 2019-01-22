import config as c
import AI
import random as r


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

	def get_magnitude(self):
		return (self.x ** 2 + self.y ** 2)**0.5

	def normalize(self):
		self.divide(self.get_magnitude())

	def get_rounded(self):
		x = round(self.x)
		y = round(self.y)

		return Vector(x, y)

	def str(self):
		return ("(%d, %d)" % (self.x, self.y))

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

	def distance_to_entity(self, other):
		vec = self.pos.vector_to_other(other.pos)
		return vec.get_magnitude()


class NPC(WorldEntity):

	money = 0.0
	controller = None  # controller object(AI/human player)
	base_speed = 1

	def __init__(self, name, x, y, simobj):
		super().__init__(name, x, y)
		self.controller = AI.NPC_AI(self, simobj)

	def movespeed(self):
		return self.base_speed


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

		for i in range(2000):
			x = r.randint(0, c.WORLD_WIDTH)
			y = r.randint(0, c.WORLD_HEIGHT)
			new_npc = NPC("NPC %d" % i, x, y, self)
			self.addNPC(new_npc)

		for i in range(50):
			x = r.randint(0, c.WORLD_WIDTH)
			y = r.randint(0, c.WORLD_HEIGHT)
			new_shop = Shop("SHOP %d" % i, x, y)
			self.addShop(new_shop)

	def addNPC(self, npcobj):
		self.npc_list.append(npcobj)

	def addShop(self, shopobj):
		self.shop_list.append(shopobj)

	def move_to_dir(self, entity, vecdir):
		if entity.ready:
			vecdir.normalize()
			vecdir.multiply(entity.movespeed() * self.delta)
			entity.pos.add(vecdir)

			entity.ready = False
			return True

	def move_to_ent(self, source, dest):
		direction = source.direction_to_entity(dest)
		self.move_to_dir(source, direction)
