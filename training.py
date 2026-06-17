import random

"""
for each card:
	in hand
	in hut
	in hole
	in play
	in swamp
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

def cardString(rank, suit):
	return str(rank) + "of" + str(suit)

class GameStateMatrix:
	def __init__(self):
		self.card_data = {}
		for rank in range(1,11):
			self.card_data["rank"+str(rank)] = {}
			for suit in range(4):
				self.card_data["rank"+str(rank)]["suit"+str(suit)] = {}
				for item in ("hand", "hut", "hole", "play", "swamp", "hidden"):
					self.card_data["rank+str(rank)"]["suit"+str(suit)][item] = 0
		self.spring = 0
		self.summer_s = 0
		self.summer_d = 0
		self.summer_c = 0
		self.summer_h = 0
		self.fall = 0
		self.winter = 0
		self.frog = 0
	
class Strand:
	def __init__(self, based_on = False):
		if based_on:
			pass
		else:
			self.card_data = {}
			for rank in range(1,11):
				self.card_data["rank"+str(rank)] = {}
				for suit in range(4):
					self.card_data["rank"+str(rank)]["suit"+str(suit)] = {}
					for item in ("hand", "hut", "hole", "play", "swamp", "hidden"):
						self.card_data["rank+str(rank)"]["suit"+str(suit)][item] = random.random()
			self.spring = random.random()
			self.summer_s = random.random()
			self.summer_d = random.random()
			self.summer_c = random.random()
			self.summer_h = random.random()
			self.fall = random.random()
			self.winter = random.random()
			self.frog = random.random()
	def getCalculatedWeight(self, game_state_data):
		sum = 0
		for rank in range(1,11):
			for suit in range(4):
				for item in ("hand", "hut", "water", "play", "used", "hidden"):
					sum += self.card_data["rank+str(rank)"]["suit"+str(suit)][item] * game_state_data.card_data["rank+str(rank)"]["suit"+str(suit)][item]
		sum += self.spring * game_state_data.spring
		sum += self.summer_s * game_state_data.summer_s
		sum += self.summer_d * game_state_data.summer_d
		sum += self.summer_c * game_state_data.summer_c
		sum += self.summer_h * game_state_data.summer_h
		sum += self.fall * game_state_data.fall
		sum += self.winter * game_state_data.winter
		sum += self.frog * game_state_data.frog
		return sum
		
class Dna:
	def __init__(self):
		self.card_strands = {}
		for rank in range(1,11):
			for suit in range(4):
				self.card_strands[cardString(rank,suit)] = Strand()

class Player:
	def __init__(self, next_player):
		self.dna = Dna()
		self.hand = set()
		self.hole = set()
		self.score = 0
		self.next_player = next_player

def getLeadableCards(hand_of_cards, current_hut, current_season, is_trump_broken):
	if is_trump_broken:
		return hand_of_cards
	

player_three = Player(None)
player_two = Player(player_three)
player_one = Player(player_two)
player_three.next_player = player_one

elder = player_one
middle = player_two
youngest = player_three

for game in range(3): # three games per match
	elder, middle, youngest = middle, youngest, elder # cycle seats
	deck = [(r, s) for r in range(4) for s in range(10)]
	random.shuffle(deck)
	hut = deck.pop()
	water = [deck.pop(), deck.pop(), deck.pop()]
	for i in range(12):
		elder.hand.add(deck.pop())
	for i in range(12):
		middle.hand.add(deck.pop())
	for i in range(12):
		youngest.hand.add(deck.pop())
	# for now, we will just pick a random season and frog, we will train them on bidding once they can play well enough
	season = random.choice("spring", "summer_s", "summer_d", "summer_c", "summer_h", "fall", "winter")
	# let's make winter a little more rare since it's not a common thing, I think
	if season=="winter":
		season = random.choice("spring", "summer_s", "summer_d", "summer_c", "summer_h", "fall", "winter")
	frog = "all"
	if season != "winter":
		frog = random.choice(elder, middle, youngest)
	trump_broken = False
	who_has_lead = elder
	for hand in range(12): # twelve hands per game
		# lead
		leadable_cards = getLeadableCards(who_has_lead.hand, hut, season, trump_broken)