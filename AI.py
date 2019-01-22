import random as r


class NPC_AI:

	def __init__(self, npcobj, simobj):
		self.npc = npcobj
		self.sim = simobj
		self.state = "IDLE"
		self.target = None

	def play(self):
		if not self.target:
			self.target = r.choice(self.sim.shop_list)

		distance = self.npc.distance_to_entity(self.target)
		if distance > 5:
			self.sim.move_to_ent(self.npc, self.target)
		else:
			self.target = None
