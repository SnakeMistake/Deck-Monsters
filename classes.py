from requests import get
import random

#This pulls a list of all the monster names from the Dungeons and Dragons API.  It also saves the URLs for each name in a monster_urls dictionary so that those URLs can be looked up at random by the following function.
monster_names = []
def monster_list():
  monster_list = get ("https://www.dnd5eapi.co/api/monsters").json()
  monster_urls = {}
  for monster in monster_list["results"]:
    monster_urls[monster["name"]] = monster['url']
    monster_names.append(monster["name"])
  return monster_urls

monster_urls = monster_list()

#This creates a single monster by shuffling the monster names deck and going to the url for that specific monster.  It returns the full json as "monster info" which is used to make the monster class in the classes.py file
def create_monster():
  random.shuffle(monster_names)
  name = monster_names[0]
  url = monster_urls[name]
  monster_info = get(f'https://www.dnd5eapi.co{url}').json()
  return monster_info
  
#Creates the individual monster cards.  Each has 3 stats and the ability to level up - which increases each by 20 percent.  The string returns a synopsis of the monster.
class Monster:
  def __init__(self, name, strength, dexterity, intelligence, level=1):
    self.name = name
    self.strength = strength
    self.dexterity = dexterity
    self.intelligence = intelligence
    self.level = level
  def level_up(self):
    self.level += 1
    self.strength = int(self.strength*1.2)
    self.dexterity = int(self.dexterity*1.2)
    self.intelligence = int(self.intelligence*1.2)
  def __str__(self):
    return f'{self.name}'

#This creates a deck of 52 monster cards using the create_moster() function from the monsters.py file.  This pulls from the Dungeons and Dragons API to make random cards from a list of 300+ on the site.  Cards have a funciton to deal themselves out using the pop method.
class Deck:
  def __init__(self):
    self.allmonsters = []
    for i in range(52):
      monster_data1 = create_monster()
      monster_one = Monster(name = monster_data1['name'], strength = monster_data1['strength'], dexterity = monster_data1['dexterity'], intelligence = monster_data1['intelligence'])
      self.allmonsters.append(monster_one)
      
  def deal_card(self):
    return self.allmonsters.pop(0)
  
  def deal(self, player_one, player_two):
    for i in range(26):
      player_one.deck.append(self.deal_card())
      player_two.deck.append(self.deal_card())
      
  def __str__(self):
    return str(self.allmonsters)
    
#The player class includes a name and a deck of cards.  The dealone function happens at the start of each round when the players play a card from the top of the deck.  The addcards function puts any cards that have been won on the bottom of the deck.
class Player:
  def __init__(self, name):
    self.name = name
    self.deck = []
  def dealone(self):
    return self.deck.pop(0)
  def addcards(self, new_cards):
    if type(new_cards) == type([]):
      self.deck.extend(new_cards)
    else:
      self.deck.append(new_cards)
  def __str__(self):
    return(f'{self.name} has {len(self.deck)} cards in their hand.')
  