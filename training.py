import random

SPADES = 0
DIAMONDS = 1
CLUBS = 2
HEARTS = 3

"""
for each card:
	in hand
	in hut
	in hole
	is lead
	is followcard
	in swamp
	hidden
is it spring
is it summer spades
is it summer diamonds
is it summer clubs
is it summer hearts
is it fall
is it winter
is trump broken
are you frog
"""
class Card:
	def __init__(self, rank, suit):
		self.rank = rank
		self.suit = suit
	def __eq__(self, other):
		if not isinstance(other, Card):
			return NotImplemented
		return (self.suit, self.rank) == (other.suit, other.rank)
	def __hash__(self):
		return hash((self.suit, self.rank))
	def __lt__(self, other):
		return self.suit*10 + self.rank < other.suit*10 + self.rank
	def asTuple(self):
		return (self.rank, self.suit)
	def getCardPoints(self, lead_suit, trump_suit):
		if self.suit==trump_suit:
			return 10 + self.rank
		if self.suit==lead_suit:
			return self.rank
		return 0
	def __repr__(self):
		return ("A" if self.rank==1 else str(self.rank)) + "SDCH"[self.suit]
	
class GameStateMatrix:
	def __init__(self):
		self.card_data = {}
		for rank in range(1,11):
			self.card_data["rank"+str(rank)] = {}
			for suit in range(4):
				self.card_data["rank"+str(rank)]["suit"+str(suit)] = {}
				for item in ("hand", "hut", "hole", "lead", "follow", "swamp"):
					self.card_data["rank"+str(rank)]["suit"+str(suit)][item] = 0
				self.card_data["rank"+str(rank)]["suit"+str(suit)]["hidden"] = 1
		self.spring = 0
		self.summer_s = 0
		self.summer_d = 0
		self.summer_c = 0
		self.summer_h = 0
		self.fall = 0
		self.winter = 0
		self.broken = 0
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
					for item in ("hand", "hut", "hole", "lead", "follow", "swamp", "hidden"):
						self.card_data["rank"+str(rank)]["suit"+str(suit)][item] = random.random()
			self.spring = random.random()
			self.summer_s = random.random()
			self.summer_d = random.random()
			self.summer_c = random.random()
			self.summer_h = random.random()
			self.fall = random.random()
			self.winter = random.random()
			self.broken = random.random()
			self.frog = random.random()
	def getCalculatedWeight(self, game_state_data):
		sum = 0
		for rank in range(1,11):
			for suit in range(4):
				for item in ("hand", "hut", "hole", "lead", "follow", "swamp", "hidden"):
					sum += self.card_data["rank"+str(rank)]["suit"+str(suit)][item] * game_state_data.card_data["rank"+str(rank)]["suit"+str(suit)][item]
		sum += self.spring * game_state_data.spring
		sum += self.summer_s * game_state_data.summer_s
		sum += self.summer_d * game_state_data.summer_d
		sum += self.summer_c * game_state_data.summer_c
		sum += self.summer_h * game_state_data.summer_h
		sum += self.fall * game_state_data.fall
		sum += self.winter * game_state_data.winter
		sum += self.broken * game_state_data.broken
		sum += self.frog * game_state_data.frog
		return sum
		
class Dna:
	def __init__(self):
		self.card_strands = {}
		for rank in range(1,11):
			for suit in range(4):
				self.card_strands[(rank,suit)] = Strand()
	def getScoreFor(self, card, current_game_state):
		return self.card_strands[card.asTuple()].getCalculatedWeight(current_game_state)

class Player:
	def __init__(self, next_player):
		self.dna = Dna()
		self.hand = set()
		self.hole = set()
		self.score = 0
		self.next_player = next_player
		self.game_state = GameStateMatrix()
	def __eq__(self, other):
		return False
	def addCardToHand(self, card):
		self.hand.add(card)
		game_state_card_array = self.game_state.card_data["rank"+str(card.rank)]["suit"+str(card.suit)]
		for item in ("hut", "hole", "lead", "follow", "swamp", "hidden"):
			game_state_card_array[item] = 0
		game_state_card_array["hand"] = 1
	def removeCardFromHand(self, card, where_to="hidden"):
		self.hand.remove(card)
		game_state_card_array = self.game_state.card_data["rank"+str(card.rank)]["suit"+str(card.suit)]
		for item in ("hut", "hole", "lead", "follow", "swamp", "hidden"):
			game_state_card_array[item] = 0
		game_state_card_array[where_to] = 1
	def putInHole(self, card, knowledge=True):
		self.hole.add(card)
		game_state_card_array = self.game_state.card_data["rank"+str(card.rank)]["suit"+str(card.suit)]
		if knowledge:
			for item in ("hand", "hut", "lead", "follow", "swamp", "hidden"):
				game_state_card_array[item] = 0
			game_state_card_array["hole"] = 1
		else:
			for item in ("hand", "hut", "hole", "lead", "follow", "swamp"):
				game_state_card_array[item] = 0
			game_state_card_array["hidden"] = 1
	def gainKnowledge(self, card, where):
		game_state_card_array = self.game_state.card_data["rank"+str(card.rank)]["suit"+str(card.suit)]
		for item in ("hand", "hut", "hole", "lead", "follow", "swamp", "hidden"):
			game_state_card_array[item] = 0
		game_state_card_array[where] = 1
	def forgetAbout(self, card):
		self.gainKnowledge(card, "hidden")
	def reset(self):
		self.game_state = GameStateMatrix()
		self.hole = set()
	def setSeason(self, new_season):
		self.game_state.spring = 1 if new_season=="spring" else 0
		self.game_state.summer_s = 1 if new_season=="summer_s" else 0
		self.game_state.summer_d = 1 if new_season=="summer_d" else 0
		self.game_state.summer_c = 1 if new_season=="summer_c" else 0
		self.game_state.summer_h = 1 if new_season=="summer_h" else 0
		self.game_state.fall = 1 if new_season=="fall" else 0
		self.game_state.winter = 1 if new_season=="winter" else 0
	def setFrogState(self, you_are_frog):
		self.game_state.frog = 1 if you_are_frog else 0
	def setTrumpBreakState(self, new_state=True):
		self.game_state.broken = new_state
	def whatToPlay(self, options):
		best_score = float('-inf')
		best_card = None
		for this_card in options:
			this_score = self.dna.getScoreFor(this_card, self.game_state)
			if this_score>best_score:
				best_score = this_score
				best_card = this_card
		return best_card
	def pointsInHole(self, comfort_number):
		ret = 0
		for card in self.hole:
			if card.rank==1 or card.rank==comfort_number:
				ret += 1
		return ret

def getLeadableCards(hand_of_cards, trump, is_trump_broken):
	if is_trump_broken:
		return hand_of_cards
	non_trump_cards = {card for card in hand_of_cards if card.suit != trump}
	if len(non_trump_cards)==0:
		return hand_of_cards
	return non_trump_cards
def getPlayableCards(hand_of_cards, lead_card_suit):
	in_suit_cards = {card for card in hand_of_cards if card.suit == lead_card_suit}
	if len(in_suit_cards) == 0:
		return hand_of_cards
	return in_suit_cards

player_three = Player(None)
player_two = Player(player_three)
player_one = Player(player_two)
player_three.next_player = player_one
all_players = (player_one, player_two, player_three)

elder = player_one
middle = player_two
youngest = player_three

for game in range(12): # three games per match # eh let's do 12
	for player in all_players:
		player.reset()
	elder, middle, youngest = middle, youngest, elder # cycle seats
	deck = [Card(r, s) for s in range(4) for r in range(1,11)]
	random.shuffle(deck)
	hut = deck.pop()
	water = [deck.pop(), deck.pop(), deck.pop()]
	for i in range(12):
		elder.addCardToHand(deck.pop())
	for i in range(12):
		middle.addCardToHand(deck.pop())
	for i in range(12):
		youngest.addCardToHand(deck.pop())
	# for now, we will just pick a random season and frog, we will train them on bidding once they can play well enough
	seasons = {"spring", "summer_s", "summer_d", "summer_c", "summer_h", "fall", "winter"}
	seasons.remove(("summer_s", "summer_d", "summer_c", "summer_h")[hut.suit])
	season = random.choice(list(seasons))
	# let's make winter a little more rare since it's not a common thing, I think
	#if season=="winter":
	#	season = random.choice(list(seasons))
	frog = "all"
	if season != "winter":
		frog = random.choice((elder, middle, youngest))
	if season != "winter":
		for card in water:
			frog.putInHole(card, season=="spring")
	for player in elder,middle,youngest:
		player.setSeason(season)
		player.setFrogState(player is frog or frog=="all")
	trump = hut.suit
	if season == "summer_s":
		trump = SPADES
	elif season == "summer_d":
		trump = DIAMONDS
	elif season == "summer_c":
		trump = CLUBS
	elif season == "summer_h":
		trump = HEARTS
	trump_broken = False
	who_has_lead = elder
	#print("playing a round of", season)
	#print("the hut is", hut)
	#input("...")
	for hand in range(12): # twelve hands per game
		second_player = who_has_lead.next_player
		third_player = second_player.next_player
		#print("elder's hand" + (" (lead)" if elder is who_has_lead else "") + (" (frog)" if elder is frog or frog=="all" else ""))
		#print(elder.hand)
		#print("middle's hand" + (" (lead)" if middle is who_has_lead else "") + (" (frog)" if middle is frog or frog=="all" else ""))
		#print(middle.hand)
		#print("youngest's hand" + (" (lead)" if youngest is who_has_lead else "") + (" (frog)" if youngest is frog or frog=="all" else ""))
		#print(youngest.hand)
		# lead
		leadable_cards = getLeadableCards(who_has_lead.hand, trump, trump_broken)
		lead_card = who_has_lead.whatToPlay(leadable_cards)
		#print(lead_card, "is the lead card" + ("                      !!!!!" if lead_card.rank==1 or lead_card.rank==hut.rank else ""))
		if not trump_broken and lead_card.suit==trump:
			trump_broken = True
			for player in all_players:
				player.setTrumpBreakState()
		who_has_lead.removeCardFromHand(lead_card, "lead")
		second_player.gainKnowledge(lead_card, "lead")
		third_player.gainKnowledge(lead_card, "lead")
		# follow
		playable_cards = getPlayableCards(second_player.hand, lead_card.suit)
		follow_card = second_player.whatToPlay(playable_cards)
		#print("followed by", str(follow_card) + ("                      !!!!!" if follow_card.rank==1 or follow_card.rank==hut.rank else ""))
		if not trump_broken and follow_card.suit==trump:
			trump_broken = True
			for player in all_players:
				player.setTrumpBreakState()
		second_player.removeCardFromHand(follow_card, "follow")
		third_player.gainKnowledge(follow_card, "follow")
		# last
		playable_cards = getPlayableCards(third_player.hand, lead_card.suit)
		last_card = third_player.whatToPlay(playable_cards)
		#print("lastly", str(last_card) + ("                      !!!!!" if last_card.rank==1 or last_card.rank==hut.rank else ""))
		if not trump_broken and last_card.suit==trump:
			trump_broken = True
			for player in all_players:
				player.setTrumpBreakState()
		third_player.removeCardFromHand(last_card, "follow")
		# put cards in hole or swamp based on winner
		winner_player = who_has_lead
		winner_name = "lead"
		winner_points = lead_card.getCardPoints(lead_card.suit, trump)
		follow_points = follow_card.getCardPoints(lead_card.suit, trump)
		if follow_points > winner_points:
			winner_points = follow_points
			winner_player = second_player
			winner_name = "second"
		last_points = last_card.getCardPoints(lead_card.suit, trump)
		if last_points > winner_points:
			winner_player = third_player
			winner_name = "third"
		#print(winner_name, "takes it")
		first_loser = winner_player.next_player
		second_loser = first_loser.next_player
		if frog=="all":
			#print("as it is winter, it goes into their hole")
			winner_player.putInHole(lead_card)
			winner_player.putInHole(follow_card)
			winner_player.putInHole(last_card)
			first_loser.gainKnowledge(lead_card, "swamp")
			first_loser.gainKnowledge(follow_card, "swamp")
			first_loser.gainKnowledge(last_card, "swamp")
			second_loser.gainKnowledge(lead_card, "swamp")
			second_loser.gainKnowledge(follow_card, "swamp")
			second_loser.gainKnowledge(last_card, "swamp")
		elif winner_player is frog:
			#print("as they are the frog, it goes into the hole")
			winner_player.putInHole(lead_card)
			winner_player.putInHole(follow_card)
			winner_player.putInHole(last_card)
			first_loser.gainKnowledge(lead_card, "hole")
			first_loser.gainKnowledge(follow_card, "hole")
			first_loser.gainKnowledge(last_card, "hole")
			second_loser.gainKnowledge(lead_card, "hole")
			second_loser.gainKnowledge(follow_card, "hole")
			second_loser.gainKnowledge(last_card, "hole")
		else:
			#print("as they are nature, it goes into the swamp")
			winner_player.gainKnowledge(lead_card, "swamp")
			winner_player.gainKnowledge(follow_card, "swamp")
			winner_player.gainKnowledge(last_card, "swamp")
			first_loser.gainKnowledge(lead_card, "swamp")
			first_loser.gainKnowledge(follow_card, "swamp")
			first_loser.gainKnowledge(last_card, "swamp")
			second_loser.gainKnowledge(lead_card, "swamp")
			second_loser.gainKnowledge(follow_card, "swamp")
			second_loser.gainKnowledge(last_card, "swamp")
		who_has_lead = winner_player
	#print("round over, here was the water:", water)
	if season=="winter":
		# compare each hole
		p1_pts = player_one.pointsInHole(hut.rank)
		p2_pts = player_two.pointsInHole(hut.rank)
		p3_pts = player_three.pointsInHole(hut.rank)
		#print("each player's hole:")
		#for player in ((player_one, "player_one:", p1_pts), (player_two, "player_two:", p2_pts), (player_three, "player_three:", p3_pts)):
		#	print(player[1], player[0].hole, player[2])
		if p1_pts==p2_pts==p3_pts: # no-fun result
			for player in all_players:
				player.score -= 1
		elif p1_pts==p2_pts:
			player_one.score += 1
			player_two.score += 1
			player_three.score -= 2
		elif p3_pts==p2_pts:
			player_one.score -= 2
			player_two.score += 1
			player_three.score += 1
		elif p1_pts==p3_pts:
			player_one.score += 1
			player_two.score -= 2
			player_three.score += 1
		elif p1_pts > p2_pts and p1_pts > p3_pts:
			player_one.score += 2
			player_two.score -= 1
			player_three.score -= 1
		elif p2_pts > p1_pts and p2_pts > p3_pts:
			player_one.score -= 1
			player_two.score += 2
			player_three.score -= 1
		else: # should imply if p3_pts > p2_pts and p3_pts > p3_pts:
			player_one.score -= 1
			player_two.score -= 1
			player_three.score += 2
	else:
		#print("and the final hole:", frog.hole)
		frog_points = frog.pointsInHole(hut.rank)
		#print("the frog has", frog_points, "points")
		if frog_points >= (2 if hut.rank==1 else 4):
			#print("so the frog wins!")
			frog.score += 3
		else:
			#print("so the frog loses!")
			for player in all_players:
				if player is not frog:
					player.score += {"spring": 1, "summer_s":2, "summer_d":2, "summer_c":2, "summer_h":2, "fall":3}[season]
	print("player 1's score: ", str(player_one.score) + (" (frog)" if player_one is frog or frog=="all" else ""))
	print("player 2's score:", str(player_two.score) + (" (frog)" if player_two is frog or frog=="all" else ""))
	print("player 3's score:", str(player_three.score) + (" (frog)" if player_three is frog or frog=="all" else ""))
	#input("...")