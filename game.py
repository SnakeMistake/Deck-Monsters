from classes import Player, Deck
from random import randint


#Attack option - swings on a range between 50% and 150% of the original damage
def magic(intelligence):
  return (randint(5,15)/(10))*intelligence

#The most straightforward attack option - returns the strength as an attack
def attack(strength):
  return strength 
  
#Risky attack choice - Either returns 100 or 0, depending on dexterity and luck
def backstab(dexterity):
  if dexterity*(randint(0,10)) > 100:
    return 100
  else:
    return 0

def calc_backstab_odds(dexterity):
  odds = 0
  for i in range(0,11):
    if dexterity*i > 100:
      odds += 10
    else:
      pass
  return f"{odds}%"

#This provides some data on attack choices and allows the player to choose an attack option.  It returns the attack damage from the chosen attack.
def attack_choice(strength, intelligence, dexterity):
  print(f"1. ATTACK -- damage: {strength}")
  print(f"2. MAGIC STRIKE -- damage: between 0 and {intelligence*2}")
  odds = 0
  for i in range(0,11):
    if dexterity*i > 100:
      odds += 10
    else:
      pass    
  print(f"3. BACKSTAB -- 100 damage, chance of success: {odds}%")
  try:
    choice = input("Choose an attack (1, 2 or 3): ")
    if choice == "1":
      return attack(strength)
    if choice == "2":
      return magic(intelligence)
    if choice == "3":
      return backstab(dexterity)
  except:
    print("That didn't work. Try entering a number - 1, 2, or 3.")


