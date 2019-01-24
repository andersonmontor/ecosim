ITEMDEFS = []
ITEMDEFS_N = {}  # Items objects indexed by name in a dict


class Item:

	def __init__(self, id, name, volume, base_price):
		self.id = id
		self.name = name
		self.volume = volume
		self.base_price = base_price
		self.recipe = {}

	def add_input(self, item, quant):
		self.recipe[item] = 0

	def print_item(self):
		print("------------ ITEM ------------")
		print("ID:", self.id)
		print("Name:", self.name)
		print("Volume:", self.volume)
		print("Base price:", self.base_price)
		for key, val in self.recipe.items():
			print("Input: %s(%d)" % (ITEMDEFS[key].name, val))

		print("------------------------------")


def load_items():
	global ITEMDEFS
	global ITEMDEFS_N

	f = open("items.txt")
	for line in f.readlines():
		if not line.startswith('#'):
			fields = line.split(',')
			id = int(fields[0].strip())
			name = fields[1].strip()
			volume = int(fields[2].strip())
			base_price = int(fields[3].strip())

			itemobj = Item(id, name, volume, base_price)
			if len(fields) > 4:
				rfields = fields[4].strip().split('|')
				for rf in rfields:
					rf = rf.split(':')
					itemobj.add_input(ITEMDEFS[int(rf[0])], int(rf[1]))

			ITEMDEFS.append(itemobj)
			ITEMDEFS_N[name] = itemobj

	f.close()


load_items()
