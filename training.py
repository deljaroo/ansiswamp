import random

"""
for each card:
	in hand
	in hut
	in water
	in play
	used
	hidden
is it spring
is it summer spades
is it summer diamonds
is it summer clubs
is it summer hearts
is it fall
is it winter
are you frog
"""

class GameState:
	
class Strand:
	def __init__(self, based_on = False):
		if based_on:
			pass
		else:
			self.card_data = {}
			for rank in range(10):
				self.card_data["rank"+str(rank)] = {}
				for suit in range(4):
					self.card_data["rank"+str(rank)]["suit"+str(suit)] = {}
					for item in ("hand", "hut", "water", "play", "used", "hidden"):
						self.card_data["rank+str(rank)"]["suit"+str(suit)][item] = random.random()
			self.spring = random.random()
			self.summer_s = random.random()
			self.summer_d = random.random()
			self.summer_c = random.random()
			self.summer_h = random.random()
			self.fall = random.random()
			self.winter = random.random()
			self.frog = random.random()
	def getChoice(self, game_state_data):
		
class Dna:
	def __init__(self):
		self.situation_strands = {
			2: Strand(),
			3: Strand(),
			4: Strand(),
			5: Strand(),
			6: Strand(),
			7: Strand(),
			8: Strand(),
			9: Strand(),
			10: Strand(),
			11: Strand(),
			12: Strand(),
		}