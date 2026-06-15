import random
import os
os.system("")  # enables ansi escape characters in terminal

SPADES = 0
DIAMONDS = 1
CLUBS = 2
HEARTS = 3

BLACK = 30
RED = 31
# GREEN = 32
GREEN = 92
YELLOW = 33
BLUE = 34
PURPLE = 35
CYAN = 36
WHITE = 37

class Globals:
	pass

Globals.screen_data = [[" "]*32 for _ in range(7)]
round_letter = "A"
Globals.game_mode = "title screen"
Globals.help_status = -1
Globals.game_going = True
Globals.rounds_setting = "Ace Only"
Globals.suit_styles = "Red & Black"
Globals.current_seat = "Elder"

def blitText(row, col, text, text_color = WHITE):
	for i in range(len(text)):
		this_col = col + i
		if this_col >=0 and this_col < 32:
			if i==0:
				Globals.screen_data[row][this_col] = "\033[" + str(text_color) + ";100m" + text[i]
			else:
				Globals.screen_data[row][this_col] = text[i]
def blitTextCenter(row, col, text, text_color = WHITE):
	return blitText(row, col - (len(text)//2), text, text_color)
def blitTextRight(row, col, text, text_color = WHITE):
	return blitText(row, col - len(text), text, text_color)
def blitCard(row, col, rank, suit):
	card_color = [
		BLACK,
		RED if Globals.suit_styles == "Red & Black" else GREEN,
		BLACK if Globals.suit_styles == "Red & Black" else BLUE,
		RED,
	][suit]
	Globals.screen_data[row][col] = "\033[" + str(PURPLE if Globals.suit_styles == "Purple" else card_color) + ";100m" + str(round_letter if rank==1 else rank)
	Globals.screen_data[row][col + 1] = [
		"\u2660",
		"\u2666",
		"\u2663",
		"\u2665"
	][suit]
def cleanScreen(debug = False):
	if debug:
		print(Globals.screen_data)
	Globals.screen_data = [[" "]*32 for _ in range(7)]
	if debug:
		print(Globals.screen_data)
def blitParagraph(text):
	cleanScreen()
	next_line_number = 0
	cursor = 0
	while cursor < len(text):
		if text[cursor]==" ":
			cursor += 1
		remaining_text = text[cursor:]
		if len(remaining_text) <= 32:
			blitText(next_line_number, 0, remaining_text)
			break
		length_finder = 31
		while length_finder > 0 and remaining_text[length_finder + 1] != " ":
			length_finder -= 1
		if length_finder==0:
			length_finder = 32
		blitText(next_line_number, 0, remaining_text[:length_finder+1])
		cursor += length_finder + 1
		next_line_number += 1
		if next_line_number > 6:
			break

def updateScreen():
	print("\033[F"*7 + "\033[37;100m", end="")
	for text_row in Globals.screen_data:
		print("".join(text_row))

help_options = ("help", "h", "help me")
next_options = ("next", "n", "next page")
prev_options = ("prev", "p", "previous", "prev page", "previous page")
exit_options = ("exit", "e", "back", "go back", "b")
class Mode:
	@classmethod
	def progress(cls):
		pass
	@classmethod
	def ready(cls):
		pass
	@classmethod
	def progressGameLogic(cls, ink):
		if ink in help_options:
			Globals.help_status = 0
			return ">>> "
		elif Globals.help_status >= 0:
			if len(cls.help_pages) > (Globals.help_status + 1) and ink in next_options:
				Globals.help_status += 1
				return ">>> "
			if Globals.help_status > 0 and ink in prev_options:
				Globals.help_status -= 1
				return ">>> "
			if ink in exit_options:
				Globals.help_status = -1
				return ">>> "
			return "?>> "
		else:
			return cls.progress(ink)
	@classmethod
	def readyNextScreen(cls):
		if Globals.help_status >= 0:
			blitParagraph(cls.help_pages[Globals.help_status])
			if Globals.help_status > 0 and len(cls.help_pages) > (Globals.help_status + 1):
				blitText(6, 0, "<PREV         EXIT         NEXT>", YELLOW)
			elif len(cls.help_pages) > (Globals.help_status + 1):
				blitText(6, 0, "              EXIT         NEXT>", YELLOW)
			elif Globals.help_status > 0:
				blitText(6, 0, "<PREV         EXIT", YELLOW)
			else:
				blitText(6, 0, "              EXIT", YELLOW)
			return
		return cls.ready()
class TitleScreenMode(Mode):
	help_pages = [
		"You are currently on the title page. There is nothing to do but press enter so type in EXIT and press enter, and then press enter again to move on from the title page.",
	]
	@classmethod
	def progress(cls, ink):
		Globals.game_mode = "intro"
	@classmethod
	def ready(cls):
		loadTitleScreen()
class WelcomeMode(Mode):
	help_pages = [
		"From the welcome page, you need to type START to begin. HELP will bring you here. When you see things in yellow that's telling you what you can type in. Try typing in NEXT here.",
		"All help pages work the same way. You can type NEXT to read the next page, PREV to read the previous page or EXIT to go back to what you doing before.",
		"You can often abbriviate things you can type.  N, P and E will do the same as NEXT, PREV and EXIT here.",
		"Go ahead and EXIT. Once you are out, use START to get going."
	]
	@classmethod
	def progress(cls, ink):
		if ink in ("start", "s", "go"):
			Globals.game_mode = "setup"
			return ">>> "
		else:
			return "?>> "
	@classmethod
	def ready(cls):
		cleanScreen()
		blitText(0, 0, "Welcome:", PURPLE)
		blitText(1, 0, "The game works by typing things")
		blitText(2, 0, "in and then pressing ENTER.")
		blitText(3, 0, "You can type HELP if needed.", YELLOW)
		blitText(4, 0, "Caps or lowercase is always fine")
		blitText(5, 0, "You may want to zoom or increase", BLUE)
		blitText(6, 0, "font size of your terminal.", BLUE)
class SetupMode(Mode):
	help_pages = [
		"Haven't filled this out yet"
	]
	@classmethod
	def progress(cls, ink):
		if ink in ("rounds", "round", "r", "number", "n"):
			Globals.rounds_setting = "Royals (4)" if Globals.rounds_setting=="Ace Only" else "Ace Only"
		if ink in ("suit", "s", "style", "suits", "styles"):
			Globals.suit_styles = {"Red & Black": "Four Color", "Four Color": "Purple", "Purple": "Red & Black"}[Globals.suit_styles]
		if ink in ("begin", "b", "start", "play"):
			Globals.current_seat = random.choice(("Elder", "Middle", "Youngest"))
			Globals.game_mode = "seat reveal"
	@classmethod
	def ready(cls):
		cleanScreen()
		blitTextCenter(1, 15, "Game Setup", PURPLE)
		blitText(3, 1, "Number of")
		blitText(3, 11, "ROUNDS", YELLOW)
		blitText(3, 18, "- " + Globals.rounds_setting)
		blitText(4, 6, "SUIT", YELLOW)
		blitText(4, 11, "Styles - " + Globals.suit_styles)
		blitText(6, 8, "BEGIN", YELLOW)
		blitText(6, 14, "when ready")
class SeatMode(Mode):
	help_pages = [
		"Haven't filled this out yet"
	]
	@classmethod
	def progress(cls, ink):
		Globals.game_mode = "bidding"
	@classmethod
	def ready(cls):
		cleanScreen()
		blitTextCenter(1, 16, "For this round, your seat is", PURPLE)
		blitTextCenter(3, 16, Globals.current_seat, GREEN)
		blitTextCenter(5, 16, "Press ENTER to start", YELLOW)
class ModeTemplate(Mode):
	help_pages = [
		"Haven't filled this out yet"
	]
	@classmethod
	def progress(cls, ink):
		pass
	@classmethod
	def ready(cls):
		pass

Globals.modes = {
	"title screen": TitleScreenMode,
	"intro": WelcomeMode,
	"setup": SetupMode,
	"seat reveal": SeatMode,
}

# 00000000001111111111222222222233

print(" "*32)
print(" "*32)
print(" "*32)
print(" "*32)
print(" "*32)
print(" "*32)
print(" "*32)

def loadTitleScreen():
	cleanScreen()
	blitText(1, 6, "Swamp", GREEN)
	blitText(1, 12, "the Card Game")
	blitText(2, 9, "by")
	blitText(2, 12, "Joel Moss", GREEN)
	blitText(5, 6, "Press ENTER to start", YELLOW)
loadTitleScreen()

ink = ""
current_ink_style = "... "
while Globals.game_going:
	updateScreen()
	raw_ink = input("\033[37;40m" + current_ink_style)
	ink = raw_ink.casefold()
	length_of_ink_line = len(current_ink_style) + len(ink)
	print("\033[F" + " "*length_of_ink_line, end="")
	Globals.modes[Globals.game_mode].progressGameLogic(ink)
	Globals.modes[Globals.game_mode].readyNextScreen() # note that the game_mode may change during progressGameLogic