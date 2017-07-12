import sys
import random
import time
from itertools import groupby



#This has to be a list because it must be a mutable variable
autogunammo = [0]

weaponsDict = {}
armoursDict = {}
healthitemsDict = {}
ammoDict={}
ammotypeDict={}
pluralDict={}



adjectives = ['old', 'rusty', 'damaged']


attackverblist = ['shoot', 'hit', 'kill', 'destroy', 'blast', 'attack', 'smash', 'engage', 'conquer', 'wack', 'smite', 'smack', 'slash']


playing = True

class AutogunAmmo():
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def take(self):
        global autogunammo
        v = ammoDict[self.name]
        autogunammo[0]+=v.amount
        print('You now have ' + str(autogunammo[0]) + ' rounds of autogun ammunition')



class Health():
    def __init__(self, name, healing):
        self.name = name
        self.healing = healing
        healthitemsDict.update({self.name: self})


    def use(self, character):
        global maxhealth
        temp = character.health + self.healing
        if character == player:

            if temp > maxhealth:
                character.health = maxhealth
                print('You now have ' + str(character.health) + ' health.')
            else:
                character.health = temp
                print('You now have ' + str(character.health) + ' health.')
            character.equipment.remove(self)
        else:
            character.health = temp
            character.equipment.remove(self)

    def take(self, character):
        if character.equipment == None:
            charcter.equipment = []
        character.equipment.append(self)
        character.location.items.remove(self)

class Weapon():
    def __init__(self, name, damage, wrange, ammotype=None):
        self.name = name
        self.damage = damage
        self.wrange = wrange
        self.ammotype = ammotype
        weaponsDict.update({self.name: self})


class Armour():
    def __init__(self, name, damageresist):
        self.name = name
        self.damageresist = damageresist
        armoursDict.update({self.name: self})


autogunammocase = AutogunAmmo('a case of autogun ammunition', 50)
fists = Weapon('fists', 1, 0)
clothes = Armour('clothes', 0)
rusty_auto_gun = Weapon('rusty autogun', 45, 1, 'autogun')
old_flak_jacket = Armour('old flak jacket',10)
rusty_bolter = Weapon('rusty bolter', 100, 1, 'bolter')
knife = Weapon('knife', 20, 0)
axe = Weapon('axe', 30, 0)
battered_autopistol = Weapon('battered autopistol', 20, 1, 'autogun')
plasma_pistol = Weapon('plasma pistol', 300, 1, 'plasma')
Adepta_Sororitas_power_armour = Armour('Adepta Sororitas power armour', 100)
medpack = Health('medpack', 40)
rusty_metal_armour = Armour('Rusty metal armour', 15)
chainsword = Weapon('chainsword', 65, 0)





class DialogNode():
    def __init__(self, primary=None, playerresponse=None, children=None, nextnode=None):
        self.primary = primary
        self.playerresponse = playerresponse
        self.children = children
        self.nextnode = nextnode
    def responsed(self):
        if self.primary != None:
            print(self.primary)
        [print(response) for response in self.playerresponse]
        time.sleep(1.5)
        self.response = listener()
        #This will cause a crash if something has less than 4 options and too high a number is input.
        if self.response in ['1', '2', '3', '4']:
            print(self.playerresponse[int(self.response)-1])
            time.sleep(1.5)
            if self.children != None:
                print(self.children[int(self.response)-1])
                time.sleep(1.5)
        else:
            print('Invalid commmand')
            self.responsed()
    def nextnode_M(self):
        return self.nextnode[int(self.response)-1]
    def getresponse(self):
        return int(self.response)



RescueTree4 = DialogNode(primary=""" "You're back...but where..where is my son?" """, playerresponse=[""" 1. " I'm sorry, I was too late. If it is any comfort, I killed those responsible." """, """ 2. "He had been tainted by chaos, its foul taint must be purged wherever it is found." """], children=[""" The merchant's face crumples, but then he takes a deep breath and collects himself. "He is with the Emperor, and I can take comfort in knowing that he will be the last person killed by those monsters." """, """ "What...? What!" The merchant suddenly seems to find his courage and draws his pistol. """])
RescueTree5 = DialogNode(primary= """ "You found him! Thank the Emperor!" """, playerresponse=["""1. "It is always a pleasure to be of service." """, """2. "Yeah yeah, are you going to pay me or what?" """])
RescueTree3 = DialogNode(primary='You finish off the heretic leader and quicky move towards the pedestal', playerresponse=['1. Free the young man and take him back to his father.', '2. He has been tainted by chaos and must be purged!'], children=['You are able to free the young man and free him from the circle, you carry him back through the heretic lair. The merchant has worked his way down to the bottom of the ramp.', "You raise your weapon and grant him the Emperor's peace. You trudge back through the heretic lair. The merchant is waiting for you at the bottom of the ramp."], nextnode=[RescueTree5, RescueTree4])
RescueTree2 = DialogNode(playerresponse=[""" 1. "I'll see what I can do." """, """ 2. "I don't have time for this" """], children=[""" "Thank you, thank you so much!" """, """ "But..but.." """])
RescueTree1 = DialogNode(primary='"Please, you look like someone who can fight, you must help me."', playerresponse=[""" 1. "What's wrong?" """, """ 2. "Get off me!" """], children=['"Its my son has been taken, please help me"', """ "I'm sorry, I'm sorry. But my son, hes been kidnapped." """], nextnode=[RescueTree2, RescueTree2])


class Quest():
    def __init__(self, stage=0):
        self.stage = stage


rescue = Quest()


def conversation(tree):
    print(tree.primary)
    tree.responsed()
    #while tree.nextnode != Null:
    tree.nextnode_M().responsed()



def rescue_stage1part1():
    print('A crazed looking merchant suddenly lurches up beside you and grabs your arm.')
    conversation(RescueTree1)
    if RescueTree2.getresponse() == 1:
        print(""" "The merchant almost drags you across the room to a door on the west side. He opens it and then jumps to the side. "I saw them go do there." A ramp slopes away into the dark, at the end you can spot a door. """)
        player.location = ramproom
    rescue.stage = 1

def rescue_endstage():
    if RescueTree3.getresponse() == 1:
        print(""" "Of course, I don't have much, but maybe I have something that can help you." """)
        time.sleep(1.5)
        print('The merchant takes you back to the main hall, he ducks behind one of the stalls and then rises up holding a sword of dull grey metal, with wicked looking teath running down one side of the blade.')
        time.sleep(1.5)
        player.equip_weapon(chainsword)
        player.location = merchantroom
        merchantroom.allies.remove(desperate_merchant)
        rescue.stage = 5
    else:
        player.location.enemies = []
        player.location.enemies.append(desperate_merchant)
        for enemy in player.location.enemies:
            AIcombat(enemy, player)
            time.sleep(1.5)
        merchantroom.allies.remove(desperate_merchant)
        rescue.stage = 5


def check_quests():
    if player.location == merchantroom and rescue.stage == 0:
        rescue_stage1part1()
    if player.location == sacrifcialchamber and rescue.stage == 1:
        print('On top of the pedestal is an upright circle of twisted dark metal. Spikes jut from the sides, and just looking at it makes your gut churn. A young man is chained to the front, he is unconsious and bleeding from several deep cuts, but is still alive.')
        rescue.stage = 2
    if player.location == sacrifcialchamber and sacrifcialchamber.enemies == [] and rescue.stage == 2:
        print('The heretic falls, but you barely have a chance to celebrate before there is crash and the eastern door is nearly torn off its hinges as a massive heretic leader in rusty armour covered with strange runes steps forward and grins.')
        sacrifcialchamber.enemies.append(heretic_leader)
        rescue.stage = 3
    if player.location == sacrifcialchamber and sacrifcialchamber.enemies == [] and rescue.stage == 3:
        conversation(RescueTree3)
        player.location = ramproom
        rescue.stage = 4
    if rescue.stage == 4:
        rescue_endstage()



class Actor():
    def __init__(self, name, health=100, maxhealth=100, weapon=fists, armour=clothes, equipment=None, location=None, rangetotarget=1, strength=1, dexterity=1, xpreward=0):
        self.name = name
        self.health = health
        self.weapon = weapon
        self.armour = armour
        self.equipment = equipment
        self.location = location
        self.rangetotarget = rangetotarget
        self.maxhealth = health
        self.strength = strength
        self.dexterity = dexterity
        self.xpreward = xpreward
    #you need to pass this a name (string), because when you parse it you have to search the dicts by string because that is what the key is
    def equip_weapon(self, weapon):
        if self.location.items == None:
            self.location.items = []
        if self.weapon != fists:
            self.equipment.append(self.weapon)
            print('You have moved the ' + self.weapon.name + ' to your inventory.')
        self.weapon = weaponsDict[weapon]
        if weaponsDict[weapon] in self.location.items:
            self.location.items.remove(weaponsDict[weapon])
        print('You have equipped the ' + self.weapon.name)

    def equip_armour(self, armour):
        if self.location.items == None:
            self.location.items = []
        if self.armour != clothes:
            self.equipment.append(self.armour)
            print('You have moved the ' + self.armour.name + ' to your inventory.')
        self.armour = armoursDict[armour]
        if armoursDict[armour] in self.location.items:
            self.location.items.remove(armoursDict[armour])
        print('You have equipped the ' + self.armour.name)

    def __repr__(self):
        return ', '.join([self.name, str(self.health), str(self.weapon.name), str(self.armour), str(self.equipment)])

    def searchRoom(self, room):
        print('You look around and find ' + room.get_items())

    def enterRoom(self, roomtoenter):
        global prior_room


        if (self.location.enemies != None and self.location.enemies != []):
            if roomtoenter == prior_room:
                self.rangetotarget == 1
                prior_room = self.location
                self.location = roomtoenter
                print('You are in ' + roomtoenter.desc)

            else:
                print('Enemies block your path!')

        else:
            if roomtoenter != None:
                prior_room = self.location
                self.location = roomtoenter
                print('You are in ' + roomtoenter.desc)

                if (self.location.enemies != None and self.location.enemies != []):
                    createalertstring(self.location.enemies)
                if (self.location.allies != None and self.location.allies != []):
                    createalliesstring(self.location.allies)

            else:
                print("You can't go that way")

    def attack(self, target):
        damage(self, target)


    def dies(self):
        global nextlevel
        global playerXP
        if self != player:
            #This might be a stupid hack. Will anything need to die not in a room with the player?
            #wait, can I not do self.location? Test if needed
            player.location.enemies.remove(self)
            print(self.name + ' has died')
            self.health = self.maxhealth
            playerXP = playerXP + self.xpreward
            print('You gain ' + str(self.xpreward) + ' experience!')
            if playerXP >= nextlevel:
                level_up(player)
                nextlevel+=100
        else:
            print('You have died!')
            exit()
    def addtodict(self):
        enemiesDict.update({self.name: self})

    def charge(self):
        self.rangetotarget -= 1





class Room():
    def __init__(self, name, desc='A dimly lit room with nothing remarkable', enemies=None, allies=None, items=None, North=None, East=None, South=None, West=None, ammo=None):
        self.name = name
        self.desc = desc
        self.enemies = enemies
        self.items = items
        self.North = North
        self.East = East
        self.South = South
        self.West = West
        self.allies = allies
        self.ammo = ammo

    def get_items(self):
        if self.items == None:
            self.items = []
        if self.ammo == None:
            self.ammo = []
        joined = self.items + self.ammo
        if (joined != None and len(joined) > 0):
            if len(joined) > 1:
                t3 = ', '.join([item.name for item in joined[:-1]])
                return t3 + ', and ' + joined[-1].name
            else:
                return joined[0].name



        else:
            return 'nothing'
    def __repr__(self):
        return ', '.join([self.name, self.desc, str(self.enemies), str(self.items), str(self.North), str(self.East), str(self.South), str(self.West)])






def createalertstring(givenlist):
    print('There are enemies in the room!')
    print('You spot ', end='')
    if len(givenlist) > 1:
        genlist(givenlist)
    else:
        print('a ' + givenlist[0].name)

def createalliesstring(givenlist):
    print('There are people in the room')
    print('You see ', end='')
    if len(givenlist) > 1:
        genlist(givenlist)
    else:
        print('a ' + givenlist[0].name)


def genlist(givenlist):
    #stupid english plurals
    temp = [list(group) for _, group in groupby(sorted([x.name for x in givenlist]))]
    l = []
    for x in temp:
        if len(x) != 1:
            l.append(str(len(x)) + ' ' + pluralDict[x[0]])
        else:
            l.append(str(len(x)) + ' ' + x[0])
    l2 = ', '.join([item for item in l[:-1]])
    print(l2 + ', and ' + l[-1])



def createchargestring(name, weapon):
    options = ['The ' + name + ' roars and charges you', 'The ' + name + ' raises their ' + weapon + ' above their head and races towards you!']
    return(options[random.randrange(0, len(options))])

def createbulletshooting(name, weapon, target):
    options = ['The ' + name + ' raises their ' + weapon + ' to their shoulder and releases a hail of gunfire into ' + target + '!']
    return(options[random.randrange(0, len(options))])

def meleeattack(name, weapon, target):
    options = ['The ' + name + ' slashes ' + target + ' with their ' + weapon + '!']
    return(options[random.randrange(0, len(options))])

def createbulletshooting_player(name, weapon, target):
    options = ['You raise your ' + weapon + ' to your shoulder and release a hail of gunfire into ' + target+ '!']
    return(options[random.randrange(0, len(options))])

def meleeattack_player(name, weapon, target):
    options = ['You slash ' + target + ' with your ' + weapon + '!']
    return(options[random.randrange(0, len(options))])





def move_north(character):
    character.enterRoom(character.location.North)
def move_east(character):
    character.enterRoom(character.location.East)
def move_south(character):
    character.enterRoom(character.location.South)
def move_west(character):
    character.enterRoom(character.location.West)

def level_up(character):
    print('Pick a stat to increase: strength, dexterity, or health')
    global maxhealth
    command = listener()
    if command in ['strength', 's', 'str']:
        character.strength = character.strength + 1
    elif command in ['dexterity', 'd', 'dex']:
        character.dexterity = character.dexterity + 1
    elif command in ['health', 'h', 'hp']:
        maxhealth = maxhealth + 40
        character.health = character.health + 40
    else:
        print('Invalid selection')
        level_up(character)


def lookatitems(character):
    print('You have ' + character.weapon.name + ' in your weapon slot, it does ' + str(character.weapon.damage) + ' damage')
    print('You have ' + character.armour.name + ' in your armour slot, it has ' + str(character.armour.damageresist) + ' damage resist')
    for x in character.equipment:
        print(x.name)

    print('You have ' + str(autogunammo[0]) + ' rounds of autogun ammo')


def damage(attacker, target):

    d20 = random.randrange(3 , 13)
    d20 = d20 / (random.randrange(20, 25))

    if attacker.weapon.wrange == 0:
        d = (((d20 + (attacker.strength)/1.5) * attacker.weapon.damage) - target.armour.damageresist) / 1.5
    if attacker.weapon.wrange == 1:
        d = (((d20 + (attacker.dexterity)/1.5) * attacker.weapon.damage) - target.armour.damageresist) / 1.5

    if d <= 0:
        if target == player:
            print('Your ' + target.armour.name + ' completely absorbs the blow!')
        else:
            print(target.name + "'s " + target.armour.name + ' completely absorbs the blow!')
    else:
        target.health = target.health - d
        if target.name == 'you':
            print('You take ' + str(d) + ' damage!')
            time.sleep(1.5)
            print('You have ' + str(target.health) + ' health remaining!')

        else:
            print(target.name + ' takes ' + str(d) + ' damage!')
            time.sleep(1.5)
            print(target.name + ' has ' + str(target.health) + ' health remaining!')

        if target.health <= 0:
            target.dies()

def AIcombat(attacker, target):
    if attacker.rangetotarget > attacker.weapon.wrange:
        attacker.charge()
        print(createchargestring(attacker.name, attacker.weapon.name))
    else:

        if attacker.weapon.wrange == 0:
            print(meleeattack(attacker.name, attacker.weapon.name, target.name))
            time.sleep(1.5)
            damage(attacker, target)
        else:
            print(createbulletshooting(attacker.name, attacker.weapon.name, target.name))
            time.sleep(1.5)
            damage(attacker, target)
        if target.health <= 0:
            target.dies()

def playercombat(enemy_object):
    global autogunammo
    if(player.rangetotarget > player.weapon.wrange):
        print("You aren't close enough to use your weapon; charge the enemy!")
        interpreter(player, listener())
    else:
        if player.weapon.wrange > 0:
            print(createbulletshooting_player(player.name, player.weapon.name, enemy_object.name))
            temp = ammotypeDict[player.weapon.ammotype][0] - 5
            if temp < 0:
                print("You don't have enough ammo! Switch weapons... or run away.")
                interpreter(player, listener())
            else:
                autogunammo[0] = temp
                damage(player, enemy_object)
                time.sleep(1.5)
        else:
            print(meleeattack_player(player.name, player.weapon.name, enemy_object.name))
            damage(player, enemy_object)
            time.sleep(1.5)
    if player.location.enemies != None and player.location.enemies != []:
        for enemy in player.location.enemies:
            AIcombat(enemy, player)
            time.sleep(1.5)



def interpreter(character, command):
    set_enemynames = []
    set_allynames = []
    #Lower is problemematic because of items with capital letters
    #listofwordsincommand = [x.lower() for x in command.split()]
    listofwordsincommand = command.split()
    set_listofwordsincommand = set(listofwordsincommand)
    if character.location.enemies != None:
        set_enemynames = set([x.name for x in character.location.enemies])
    if character.location.allies != None:
        set_allynames = set([x.name for x in character.location.allies])
    if character.equipment == None:
        character.equipment = []
    equipment = [x.name for x in character.equipment]
    parsed_weaponsinroom = []
    parsed_armoursinroom = []
    parsed_healingsinroom = []
    if character.location.items != None:
        temp = [x.name for x in character.location.items]
        set_weaponsinroom = set(weaponsDict.keys()).intersection(set(temp))
        set_armoursinroom = set(armoursDict.keys()).intersection(set(temp))
        set_healingsinroom = set(healthitemsDict.keys()).intersection(set(temp))
        weaponsinroom = list(set_weaponsinroom)
        armoursinroom = list(set_armoursinroom)
        healingsinroom = list(set_healingsinroom)

        parsed_armoursinroom = [x.split() for x in armoursinroom]
        parsed_armoursinroom = [item for sublist in parsed_armoursinroom for item in sublist]

        parsed_weaponsinroom = [x.split() for x in weaponsinroom]
        parsed_weaponsinroom = [item for sublist in parsed_weaponsinroom for item in sublist]

        parsed_healingsinroom = [x.split() for x in healingsinroom]
        parsed_healingsinroom = [item for sublist in parsed_healingsinroom for item in sublist]






    if command in ['examine inventory', 'inventory', 'items']:
        lookatitems(character)
    elif set_listofwordsincommand.intersection({'description', 'desc'}):
        print(character.location.desc)

    elif set_listofwordsincommand.intersection(set(attackverblist)):
        nameofenemy = command.split(' ', 1)
        verb = nameofenemy[0]
        if len(nameofenemy) > 1:
            nameofenemy = nameofenemy[1]
            if character.location.enemies != None:
                if nameofenemy in [x.name for x in character.location.enemies]:
                    possible = [o for o in character.location.enemies if o.name == nameofenemy]
                    enemy_object = possible[0]
                    playercombat(enemy_object)


            elif character.location.allies != None:
                if nameofenemy in [x.name for x in character.location.allies]:
                    print(nameofenemy + ' is currently not hostile, attacking them may change that, are you sure you want to proceed?')
                    yesorno = sys.stdin.readline().strip()
                    if yesorno in ['Yes', 'yes', 'y']:
                        possible2 = [o for o in character.location.allies if o.name == nameofenemy]
                        enemy_object = possible2[0]
                        character.location.allies.remove(enemy_object)
                        if character.location.enemies == None:
                            character.location.enemies = []
                        character.location.enemies.append(enemy_object)
                        playercombat(enemy_object)

                    elif yesorno in ['No', 'no', 'n']:
                        interpreter(player, listener())
                    else:
                        print('Invalid command')


                else:
                    print(verb + ' what?')
            else:
                print(verb + ' what?')
        else:
            print(verb + ' what?')




    elif set_listofwordsincommand.intersection(set(parsed_weaponsinroom)):
        x = 0
        specific = False
        while(x < len(weaponsinroom)):
            wow = set_listofwordsincommand.intersection(set(weaponsinroom[x].split()))

            if wow:
                if wow.issubset(set(adjectives)):
                    specific = True

                else:
                    specific = False
                    player.equip_weapon(weaponsinroom[x])
                    x = 100
            x+=1
        if specific:
            print('Please be more specific')

    elif set_listofwordsincommand.intersection(set(parsed_healingsinroom)):
        x = 0
        while(x < len(healingsinroom)):
            wow = set_listofwordsincommand.intersection(set(healingsinroom[x].split()))
            t = healthitemsDict[healingsinroom[x]]
            character.equipment.append(t)
            character.location.items.remove(t)
            print('You take the medpack')
            x+=1



    elif set_listofwordsincommand.intersection({'medpack'}):
        if set_listofwordsincommand.intersection({'take'}):
            print('There are no medpacks to take')

        else:
            if set(equipment).intersection({'medpack'}):
                healthitemsDict['medpack'].use(character)
            else:
                print("You don't have any medpacks to use.")

    elif set_listofwordsincommand.intersection({'ammo', 'ammunition', 'case', 'autogun ammo', 'autogun ammunition'}):
        if character.location.ammo == None:
            print('There is no ammunition to take.')
        else:
            while (character.location.ammo !=[]):
                for item in character.location.ammo:
                    if item.name in ammoDict.keys():
                        ammoDict[item.name].take()
                        character.location.ammo.remove(item)






    elif set_listofwordsincommand.intersection(set(parsed_armoursinroom)):
        x = 0
        specific = False
        while(x < len(armoursinroom)):
            wow = set_listofwordsincommand.intersection(set(armoursinroom[x].split()))

            if wow:
                if wow.issubset(set(adjectives)):
                    specific = True

                else:
                    specific = False
                    player.equip_armour(armoursinroom[x])
                    x = 100
            x+=1
        if specific:
            print('Please be more specific')
    elif set_listofwordsincommand.intersection({'charge', 'run at', 'run towards'}):
        if (character.location.enemies != None and character.location.enemies != []):
            print('You raise your weapon up and race towards your foes')
            character.charge()
            for enemy in character.location.enemies:
                AIcombat(enemy, character)
                time.sleep(1.5)
        else:
            print('There is nothing to charge!')



    elif set_listofwordsincommand.intersection({'north', 'n', 'northwards', 'North', 'N'}):
        move_north(character)
    elif set_listofwordsincommand.intersection({'east', 'e', 'eastwards', 'East', 'E'}):
        move_east(character)
    elif set_listofwordsincommand.intersection({'south', 's', 'southwards', 'South', 'S'}):
        move_south(character)
    elif set_listofwordsincommand.intersection({'west', 'w', 'westwards', 'West', 'W'}):
        move_west(character)
    elif set_listofwordsincommand.intersection({'search', 'examine', 'look', 'look around'}):
        character.searchRoom(character.location)
    elif command in ['take all', 'take everything']:
        if (character.location.items == None and character.location.ammo == None):
            print('Nothing found')
        x = 0
        while character.location.items != []:

            for item in character.location.items:
                if item.name in weaponsDict.keys():
                    character.equip_weapon(item.name)
                if item.name in armoursDict.keys():
                    character.equip_armour(item.name)
                if item.name in healthitemsDict.keys():
                    character.equipment.append(item)
                    character.location.items.remove(item)
                    print('You take the medpack')
        while character.location.ammo !=[] and character.location.ammo != None:
            for item in character.location.ammo:
                if item.name in ammoDict.keys():
                    ammoDict[item.name].take()
                    character.location.ammo.remove(item)




    elif set_listofwordsincommand.intersection({'sneak', 'slip', 'around'}):
        print('You are caught!')
        for enemy in character.location.enemies:
            AIcombat(enemy, character)
            time.sleep(1.5)

    elif set_listofwordsincommand.intersection({'equip', 'use'}):
        equipcmd = command.split(' ', 1)
        equipcmd = equipcmd[1]
        if equipcmd in armoursDict.keys():
            if armoursDict[equipcmd] in character.equipment:
                character.equip_armour(equipcmd)
            else:
                print('Equip what?')
        elif equipcmd in weaponsDict.keys():
            if weaponsDict[equipcmd] in character.equipment:
                character.equip_weapon(equipcmd)
            else:
                print('Equip what?')
        else:
            print('Equip what?')


    elif command in ['enemies', 'get enemies']:
        if (character.location.enemies != None and character.location.enemies != []):
            if len(character.location.enemies) > 1:
                t3 = ', '.join([enemy.name for enemy in character.location.enemies[:-1]])
                print(t3 + ', and ' + character.location.enemies[-1].name)
            else:
                print(character.location.enemies[0].name)
        else:
            print('No enemies')


    elif set_listofwordsincommand.intersection(set_enemynames):
        print('You make it mad!')
        for enemy in character.location.enemies:
            AIcombat(enemy, character)
            time.sleep(1.5)


    else:
        print('Invalid Command')


def listener():
    playerchoice = sys.stdin.readline().strip()
    return playerchoice


#defaults = health=100, maxhealth=100, weapon=fists, armour=clothes, equipment=None, location=None, rangetotarget=1, strength=1, dexterity=1, xpreward=0
big_gretchin = Actor(name='big gretchin', weapon=axe, strength=2, xpreward=40)
gretchin = Actor(name='gretchin', health=50, weapon=battered_autopistol, xpreward=30)
gretchin2 = Actor(name='gretchin', health=50, weapon=battered_autopistol, xpreward=30)
heretic = Actor(name = 'heretic', weapon=battered_autopistol, armour=old_flak_jacket, dexterity=2, xpreward=50)
merchant = Actor(name = 'merchant', weapon=battered_autopistol)
man = Actor(name = 'man', health = 50)
woman = Actor(name = 'woman', health = 50)

desperate_merchant = Actor(name = 'desperate merchant', weapon=battered_autopistol)
heretic_leader = Actor(name='heretic leader', weapon=rusty_auto_gun, armour=rusty_metal_armour, dexterity=2, xpreward=60)

player = Actor(name='you', weapon=fists, armour=clothes, rangetotarget=1)


startRoom = Room('Start', desc='a small grimy room with a door on the north wall', items=[rusty_auto_gun, old_flak_jacket, medpack, axe], ammo=[autogunammocase])
secondRoom = Room('hallway1', desc='a long dark hallway running past the door of the room to the east and west. There are other doors lining the hall, but they are locked, bared, or otherwise impassable', enemies=[gretchin, big_gretchin], South=startRoom)
lookout = Room('lookout', desc='a room with a smashed row of windows lining one wall. Outside you can see Grybith hive, from your position partway up the spire you can see the damaged city spread out towards the horizon. In the distance you can see the ruins of the massive walls that once surrounded Grybith.', items=[medpack], East=secondRoom)
anteroom = Room('anteroom', desc='a small anteroom. To the north a door is ajar; light and voices spill from the other side.', West=secondRoom)
merchantroom = Room('merchantroom', desc='a large rectangular room with high ceilings. A second story gallery once stretched along several of the walls, but it has collapsed. The rubble has been pushed into the corners to make room for several stalls. There are exits in every direction.', allies=[man, man, man, woman, merchant, desperate_merchant], South=anteroom)
ramproom = Room('ramproom', desc=' a room with a long ramp sloping downwards into the dark, there is a door at the end of it.', East=merchantroom)
bloodyroom = Room('bloodyroom', desc='a room with long blood stains down the sides of the walls, almost as if the ceiling was bleeding.', items=[medpack, knife])
sacrifcialchamber = Room('sacrifcialchamber', desc='a large circular room with a pedestal in the middle. There is a door on the eastern wall', enemies=[heretic])
Hereticstorage = Room('Hereticstorage', desc='a small room with a few boxes. You poke around but find nothing interesting.', West=sacrifcialchamber)


deadwomanRoom = Room('noblewoman house', desc='a fancy house with plates that gleam like a thousand moons. A stench hits you as you look around a table and see a woman on her back wearing an expensive gown for a noblewoman that used to be white, but now is soaked with her blood. You notice a deep knife wound that appears to have been her demise. Politics in the hives are always messy. Exits lie to the north and east.',West=secondRoom)

gretchin_nest = Room('gretchin nest', desc='a dank room that smells as if something foul had been living there for some time. There are exits to the south and east.', enemies=[big_gretchin], West=deadwomanRoom)
oldstoreroom = Room('storeroom', desc='a room filled with unopenable boxes. Something glints in the shadows in the corner of your eye as the light from the room behind you enters. There are no new exits', items=[knife], South=deadwomanRoom)
guardroom = Room('guardroom1', desc='a disorganized room with a shivering man that does not respond to your calls. You see that he is wearing PDF uniform and realize he must have been here when the invasion happened. He is obviously insane and you decide to leave him alone. There are no new exits.', allies=[man], North=gretchin_nest)
armory = Room('armory', desc='a wreck of a room where weapons lay broken and tossed around. Hopefully there is still something useful here. There is an open doorway to the north', enemies=[big_gretchin], South=bloodyroom)
guards_quarters= Room('guards quaters', desc='a small room where beds lay in ruins and slime runs down the wall. There are exits to the north and west.', enemies=[big_gretchin, gretchin], South=armory)




def stupidhack():
    global nextlevel
    global prior_room
    global playerXP
    global maxhealth
    global autogunammo
    ammoDict.update({'a case of autogun ammunition': autogunammocase})
    ammotypeDict.update({'autogun': autogunammo})
    pluralDict.update({'man': 'men'})
    pluralDict.update({'woman': 'women'})
    pluralDict.update({'heretic': 'heretics'})
    pluralDict.update({'gretchin': 'gretchin'})
    pluralDict.update({'big gretchin': 'gretchin'})
    pluralDict.update({'ork boy': 'ork boyz'})

    playerXP = 0
    nextlevel = 50
    maxhealth = 100
    startRoom.North = secondRoom
    secondRoom.West = lookout
    secondRoom.East = anteroom
    anteroom.North = merchantroom
    deadwomanRoom.North = oldstoreroom
    deadwomanRoom.East = gretchin_nest
    gretchin_nest.East = bloodyroom
    gretchin_nest.South = guardroom
    #bloodyroom.North = armory
    armory.North = guards_quarters
    prior_room = startRoom
    player.location = startRoom
    anteroom.North = merchantroom
    merchantroom.West = ramproom
    ramproom.West = bloodyroom
    bloodyroom.South = sacrifcialchamber
    sacrifcialchamber.North = bloodyroom
    bloodyroom.East = ramproom
    sacrifcialchamber.West = Hereticstorage


def main_Control_Loop():
    print('Initial stats:')
    print('Strength increases your damage with melee weapons.')
    print('Dexterity increases your damage with ranged weapons.')
    print('Health increases your maximum health')
    level_up(player)
    level_up(player)
    print('You are in ' + startRoom.desc)
    while playing:
        check_quests()
        interpreter(player, listener())







if __name__ == '__main__':
    print('Welcome')
    print('Hint: remember to search rooms for items before you leave')
    #print("Enter your character's name")
    #playername = sys.stdin.readline().strip()
    #player.name = playername
    stupidhack()
    main_Control_Loop()
