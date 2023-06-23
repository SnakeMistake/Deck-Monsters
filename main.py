# ---- YOUR APP STARTS HERE ----

# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
from classes import Player, Deck
from game import calc_backstab_odds, attack, backstab, magic

# -- Initialization section --
app = Flask(__name__)
player_one = Player("Default")
computer_player = Player("Computer Joe")
deck_one = Deck()
turn_count = 1
player_one_cards = []
computer_cards = []
    

# -- Routes section --

# INDEX
@app.route('/')
@app.route('/index')
def index():
  return render_template("index.html")

@app.route('/setup', methods=["GET", "SEND", "POST"])
def setup():
    global player_one
    player_one = Player(request.form['name'])
    deck_one.deal(player_one, computer_player)
    props = {
    "deck_one": deck_one,
    "name": request.form['name'],
    'player_one': player_one,
    'computer_player': computer_player,
    'player_one_cards': player_one_cards,
    'computer_cards': computer_cards,
    'turn_count': turn_count
    }
    if request.method == "GET":
      return "ERROR - go back to the homepage."
    else:
      return render_template('setup.html', props = props)

@app.route('/battle', methods=["GET," "SEND", "POST"])
def battle():
  try:
    player_one_cards.append(player_one.dealone())
  except:
    pass
  try: 
    computer_cards.append(computer_player.dealone())
  except:
    pass
  odds = calc_backstab_odds(player_one_cards[-1].dexterity)
  props = {
    'player_one': player_one,
    'computer_player': computer_player,
    'player_one_cards': player_one_cards,
    'one_len': len(player_one_cards),
    'two_len': len(computer_cards),
    'computer_cards': computer_cards,
    'turn_count': turn_count,
    'odds': odds
    }
  return render_template('battle.html', props = props)

@app.route('/war', methods = ["GET", "SEND", "POST"])
def war():
  odds = calc_backstab_odds(player_one_cards[-1].dexterity)
  props = {
    'player_one': player_one,
    'computer_player': computer_player,
    'player_one_cards': player_one_cards,
    'computer_cards': computer_cards,
    'turn_count': turn_count,
    'odds': odds
    }
  return render_template('war.html', props = props)

@app.route('/damage', methods=["GET", "SEND", "POST"])
def damage():
  global turn_count
  global player_one_cards
  global computer_cards
  if computer_cards[-1].strength > computer_cards[-1].dexterity and computer_cards[-1].strength > computer_cards[-1].intelligence:
    two_power = attack(computer_cards[-1].strength)
    two_attack = "Attack"
  elif computer_cards[-1].dexterity > computer_cards[-1].intelligence:
    two_power = backstab(computer_cards[-1].dexterity)
    two_attack = "Backstab"
  else:
    two_power = magic(computer_cards[-1].intelligence)
    two_attack = "Magic Strike"
  props = {
    "deck_one": deck_one,
    'player_one': player_one,
    'computer_player': computer_player,
    'player_one_cards': player_one_cards,
    'computer_cards': computer_cards,
    'one_len': len(player_one_cards),
    'two_len': len(computer_cards),
    'attack_type': request.form['attack_type'],
    "two_power": two_power,
    "two_attack": two_attack,
    "player_one_card": player_one_cards[-1],
    "player_two_card": computer_cards[-1],
    'turn_count': turn_count,
    }
  if request.form['attack_type'] == "Attack":
    player_power = attack(player_one_cards[-1].strength)
    props["player_power"] = player_power
  if request.form['attack_type'] == "Magic Strike":
    player_power = magic(player_one_cards[-1].intelligence)
    props["player_power"] = player_power
  if request.form['attack_type'] == "Backstab":
    player_power = backstab(player_one_cards[-1].dexterity)
    props["player_power"] = player_power
  if two_power > player_power:
    computer_cards[-1].level_up()
    computer_player.addcards(player_one_cards)
    computer_player.addcards(computer_cards)
    battle_result = "two_wins"
    player_one_cards = []
    computer_cards = []
  elif player_power > two_power:
    player_one_cards[-1].level_up()
    player_one.addcards(player_one_cards)
    player_one.addcards(computer_cards)
    battle_result = "one_wins"
    player_one_cards = []
    computer_cards = []
  else:
    battle_result = "tie"
    try:
      for i in range(4):
        player_one_cards.append(player_one.dealone())
        computer_cards.append(computer_player.dealone())
    except:
      pass
  props["battle_result"] = battle_result
  turn_count += 1
  return render_template('damage.html', props = props)

@app.route('/end', methods=["GET", "SEND", "POST"])
def end():
    props = {
    'player_one': player_one,
    'computer_player': computer_player,
    'player_one_cards': player_one_cards,
    'computer_cards': computer_cards,
    'one_len': len(player_one_cards),
    'two_len': len(computer_cards),
    'turn_count': turn_count
    }
  return render_template('end.html', props = props)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
