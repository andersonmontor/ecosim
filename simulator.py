import random as r
from math import sqrt
import config as c
import itemsloader as il
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

	def get_magnitude(self):
		return sqrt(self.x * self.x + self.y * self.y)

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


class WorldEntity:

	id = -1
	name = ""
	inventory = {}
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

	def removeItem(self, itemobj, quant):
		if itemobj in self.inventory.keys():
			self.inventory[itemobj] -= quant
			if self.inventory[itemobj] <= 0:
				del self.inventory[itemobj]

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

	money = 0
	controller = None  # controller object(AI/human player)
	base_speed = 1

	def __init__(self, name, x, y, simobj):
		super().__init__(name, x, y)
		self.controller = AI.NPC_AI(self, simobj)
		self.capacity = c.DEFAULT_CAP

	def movespeed(self):
		return self.base_speed


class Shop(WorldEntity):

	owner = None  # NPC object

	def __init__(self, name, x, y, item):
		super().__init__(name, x, y)
		self.item_output = item
		self.capacity = c.DEFAULT_CAP * c.SHOP_CAP_MULTI
		self.prod_cooldown = 0

	def produce(self, delta, batch_size):

		if self.prod_cooldown > 0:
			self.prod_cooldown -= delta
		elif self.has_enough_res(batch_size):
			for res, qnt in self.item_output.recipe.items():
				self.removeItem(res, qnt * batch_size)

			self.addItem(self.item_output, batch_size)
			self.prod_cooldown = c.BASE_PCOOLDOWN

	def has_enough_res(self, batch_size):

		for res, qnt in self.item_output.recipe.items():
			if res not in self.inventory.keys():
				return False
			if self.inventory[res] < qnt * batch_size:
				return False

		return True


class Simulator:

	def __init__(self, guiobj):
		self.gui = guiobj
		guiobj.simulator = self
		self.npc_list = []
		self.shop_list = []
		self.MAX_X = c.WORLD_WIDTH
		self.MAX_Y = c.WORLD_HEIGHT
		self.elapsed_time = 0

	def main_loop(self):

		self.gui.start()
		self.world_gen()

		self.running = True
		while self.running:

			self.gui.handle_events()

			self.delta = self.gui.get_delta() * c.SIM_SPEED
			self.elapsed_time += self.delta

			# Prep entities for frame
			for ent in self.npc_list + self.shop_list:
				ent.begin_frame()

			# Let NPCs play
			for npc in self.npc_list:
				npc.controller.play()

			self.gui.draw_phase()

	def world_gen(self):

		for i in range(500):
			x = r.randint(0, c.WORLD_WIDTH)
			y = r.randint(0, c.WORLD_HEIGHT)
			new_npc = NPC("NPC %d" % i, x, y, self)
			self.addNPC(new_npc)

		for i in range(50):
			x = r.randint(0, c.WORLD_WIDTH)
			y = r.randint(0, c.WORLD_HEIGHT)
			new_shop = Shop("SHOP %d" % i, x, y, il.ITEMDEFS_N["Iron Ore"])
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
