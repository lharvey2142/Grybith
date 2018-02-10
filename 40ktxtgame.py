import sys
import random
import time
#import tkinter as tk
from itertools import groupby



#This has to be a list because it must be a mutable variable
#why can't it be an int? 2/7/18
autogunammo = [0]
lasgunammo = [0]
bolterammo = [0]

examineDict = {}
weaponsDict = {}
armoursDict = {}
healthitemsDict = {}
ammoDict={}
ammotypeDict={}
pluralDict={}

def myhelp():
    print(""" Grybith is a text based rpg / exploration game set in the Warhammer 40k universe. The game is still under development and you may encounter bugs.   bbbbbbbbbbbbbbbbbbbnnb
    Commands:
    Movement:
    The game was designed to be flexible with its commands, for example if the player wants to go north, they
    can type something as simple as "n", or they can type something as complex as "I run quickly northwards,
    my heart pounding in my chest." The commands given in this document aren't comprehensive, often times there are more ways
    to do something than are given here.
    Items:
    Items can be found within the game by using a command with "search", "look", "examine", or "look around."
    Take items using "take + item" Note that you don't have to type the full name of the item if it is on the ground.
    For example, if you find "Adepta Sororitas power armour", typing "take power armour", or "take armour" will work.
    Taking an item will automatically equip it into its proper spot. However, if you want to use a different piece of equipment
    the "use + item" or "equip + item" command will move the current weapon or armour to your inventory, and equip the one
    you specified.
    Healing items, such as medpacks, will increase your current health, up to your maximum health. They can be taken the same as
    any item, and then used with any command with "medpack" in it.
    Ammo can be taken with a fairly wide variety of commands, the simplest is "take ammo"
    And, of course, you can take all items in a room with a command like "take all" Note: Make sure that the weapon and armour
    you want to use is equipped after using this command.
    General:
    You can see your items using "inventory" / "items"
    You can print out the enemies in a room with "enemies"
    You can print the room's description with "desc"
    Combat:
    Combat commands are very straight forward
    You can attack using a wide variety of verbs followed by what you want to attack. For example: "Shoot gretchin"
    Melee weapons can't be used unless you get into range first. You can do this with the "charge" command.
    You can switch weapons or armours in the middle of a fight, you can also use healing items.
    Strategy:
    None of the quests / objectives in this game are time limited, if something seems to hard for you, come back later
    when you are better equipped.
    Melee weapons leave you vulnerable for the first turn, and using one generally means you will take some damage while you
    charge. However, they don't use any ammunition
    You can always retreat from a fight by going back the way you came. Though, you won't be able to proceed through a room
    until you have neutralized all the enemies within it.""")

def printdelay(seconds=1.5):
    time.sleep(seconds)

adjectives = ['old', 'rusty', 'damaged', 'battered']


attackverblist = ['shoot', 'hit', 'kill', 'destroy', 'blast', 'attack', 'smash', 'engage', 'conquer', 'wack', 'smite', 'smack', 'slash', 'fight']


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

class Lasgunammo():
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def take(self):
        global lasgunammo
        v = ammoDict[self.name]
        lasgunammo[0]+=v.amount
        print('You now have ' + str(lasgunammo[0]) + ' las shots')

class Bolterammo():
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def take(self):
        global bolterammo
        v = ammoDict[self.name]
        bolterammo[0]+=v.amount
        print('You now have ' + str(bolterammo[0]) + ' bolter shells')



class Health():
    def __init__(self, name, healing):
        self.name = name
        self.healing = healing
        healthitemsDict.update({self.name: self})

    def use(self, character):
        global maxhealth
        temp = character.health + self.healing
        if character == player:
            character.health = maxhealth if temp > maxhealth else temp
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

class ToExamine():
    def __init__(self, name, onexamine, quest=None, queststage=0, hasexamined=False, willcall=None):
        self.name = name
        self.onexamine = onexamine
        self.quest = quest
        self.queststage = queststage
        self.hasexamined = hasexamined
        self.willcall = willcall
        examineDict.update({self.name: self})

    def examine(self):
        print(self.onexamine)
        if self.quest != None:
            self.quest.stage = self.queststage
        self.haveexamined = True
        if self.willcall != None:
            self.willcall()


def utility():
    print('A screen on the door blinks slowly: Enter Access Code')
    doorcmd = sys.stdin.readline().strip()
    if doorcmd == '41281':
        print('...Access Granted')
        print('You push open the door and slide carefully inside.')
        player.location = utilityroom

    else:
        print('...Access Denied')


lasgunammocase = Lasgunammo('several lasgun packs', 30)
autogunammocase = AutogunAmmo('a case of autogun ammunition', 50)
bolterammocase = Bolterammo('a container of bolter shells', 25)

fists = Weapon('fists', 1, 0)
clothes = Armour('clothes', 0)
rusty_auto_gun = Weapon('rusty autogun', 40, 1, 'autogun')
old_flak_jacket = Armour('old flak jacket',10)
rusty_bolter = Weapon('rusty bolter', 100, 1, 'bolter')
knife = Weapon('knife', 20, 0)
axe = Weapon('axe', 30, 0)
battered_autopistol = Weapon('battered autopistol', 20, 1, 'autogun')
plasma_pistol = Weapon('plasma pistol', 120, 1, 'plasma')
Adepta_Sororitas_power_armour = Armour('Adepta Sororitas power armour', 100)
medpack = Health('medpack', 40)
rusty_metal_armour = Armour('Rusty metal armour', 15)
chainsword = Weapon('chainsword', 65, 0)
bolt_pistol = Weapon('bolt pistol', 75, 1, 'bolter')
battered_lasgun = Weapon('battered lasgun', 50, 1, 'lasgun')
autopistol = Weapon('autopistol', 25, 1, 'autogun')







class DialogNode():
    def __init__(self, primary=None, playerresponse=None, children=None, nextnode=None):
        self.primary = primary
        self.playerresponse = playerresponse
        self.children = children
        self.nextnode = nextnode
        self.response = None
    def responsed(self):
        if self.primary != None:
            print(self.primary)
        [print(response) for response in self.playerresponse]
        printdelay()
        self.response = listener()
        #This will cause a crash if something has less than 4 options and the delta between the options and 4 is input
        if self.response in ['1', '2', '3', '4']:
            print(self.playerresponse[int(self.response)-1])
            printdelay()
            if self.children != None:
                print(self.children[int(self.response)-1])
                printdelay()
        else:
            print('Invalid commmand')
            self.responsed()
    def nextnode_M(self):
        return self.nextnode[int(self.response)-1]
    def getresponse(self):
        return int(self.response)



RescueTree4 = DialogNode(primary=""" "You're back...but where..where is my son?" """, playerresponse=[""" 1. " I'm sorry, I was too late. If it is any comfort, I killed those responsible." """, """ 2. "He had been tainted by chaos, its foul taint must be purged wherever it is found." """], children=[""" The merchant's face crumples, but then he takes a deep breath and collects himself. "He is with the Emperor, and I can take comfort in knowing that he will be the last person killed by those unholy things." """, """ "What...? What!" The merchant suddenly seems to find his courage and draws his pistol. """])
RescueTree5 = DialogNode(primary= """ "You found him! Thank the Emperor!" """, playerresponse=["""1. "It is always a pleasure to be of service." """, """2. "Yeah yeah, are you going to pay me or what?" """])
RescueTree3 = DialogNode(primary='You finish off the heretic leader and quicky move towards the pedestal', playerresponse=['1. Free the young man and take him back to his father.', '2. He has been tainted by chaos and must be purged!'], children=['You are able to free the young man and free him from the circle, you carry him back through the heretic lair. The merchant has worked his way down to the bottom of the ramp.', "You raise your weapon and grant him the Emperor's peace. You trudge back through the heretic lair. The merchant is waiting for you at the bottom of the ramp."], nextnode=[RescueTree5, RescueTree4])
RescueTree2 = DialogNode(playerresponse=[""" 1. "I'll see what I can do." """, """ 2. "I don't have time for this" """], children=[""" "Thank you, thank you so much!" """, """ "But..but.." You push the merchant roughly aside and continue onwards. """])
RescueTree1 = DialogNode(primary='"Please, you look like someone who can fight, you must help me."', playerresponse=[""" 1. "What's wrong?" """, """ 2. "Get off me!" """], children=['"Its my son has been taken, please help me"', """ "I'm sorry, I'm sorry. But my son, hes been kidnapped." """], nextnode=[RescueTree2, RescueTree2])


class Quest():
    def __init__(self, stage=0):
        self.stage = stage


rescue = Quest()
Genestealers = Quest()



def conversation(tree):
    tree.responsed()
    #while tree.nextnode != Null:
    tree.nextnode_M().responsed()



def rescue_stage1part1():
    print('A crazed looking merchant suddenly lurches up beside you and grabs your arm.')
    conversation(RescueTree1)
    if RescueTree2.getresponse() == 1:
        print(""" "The merchant almost drags you across the room to a door on the west side. He opens it and then jumps to the side. "I saw them go down there." A ramp slopes down and west into the dark, at the end you can spot a door. """)
        player.location = ramproom
    rescue.stage = 1

def rescue_endstage():
    if RescueTree5.getresponse != None:
        print(""" "I don't have much, but maybe I have something that can help you." """)
        printdelay()
        print('The merchant takes you back to the main hall, he ducks behind one of the stalls and then rises up holding a sword of dull grey metal, with wicked looking teath running down one side of the blade.')
        printdelay()
        player.equipment.append(chainsword)
        print('You take the chainsword')
        player.location = merchantroom
        merchantroom.allies.remove(desperate_merchant)


    elif RescueTree4.getresponse() == 1:
        print(""" "You did your best, and for that I owe you. I don't have much, but I may have something that you can use." """)
        printdelay()
        print('The merchant takes you back to the main hall, he ducks behind one of the stalls and then rises up holding a sword of dull grey metal, with wicked looking teath running down one side of the blade.')
        printdelay()
        player.equipment.append(chainsword)
        print('You take the chainsword')
        player.location = merchantroom
        merchantroom.allies.remove(desperate_merchant)

    else:
        player.location.enemies = []
        player.location.enemies.append(desperate_merchant)
        for enemy in player.location.enemies:
            AIcombat(enemy, player)
            printdelay()
        merchantroom.allies.remove(desperate_merchant)


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
        rescue.stage = 5
        print('Quest Complete!')

    if crack.hasexamined == True and shuttle.hasexamined == True and player.location == landingpad:
        Genestealers.stage == 1
        print("You glance down at the bodies of the gretchin. They are holding tools, seemingly in the middle of repairs. Something doesn't add up. The people in the slums were clearly scared of something down here, and someone had tried hard to collapse both enterances to the main tunnel. But the orks hadn't been very long at all. You walk over to the edge of the platform. Below is the massive docking mechanism that must be on the other side of the collapsed wall. Its too far to jump, and the sheer walls of the shaft would be an impossible climb for any human or ork. And yet, something has dug a line of chunks up the wall from the docking mechanism to the landing pad. Whatever is going on down here, the answers likely lie beyond the destroyed tunnel.")
    if player.location == warren4 and Genestealers.stage == 1:
        print('You examine the pile of broken and smashed ferrocrete more carefully. Whoever did this had no shortage of explosives, and was happy to use them. In fact, attempting to blow your way through would likely bring even more of the tunnel down. You will have to find something that lets you carefully dig your way through.')



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
                whichdesc(roomtoenter)

            else:
                print('Enemies block your path!')

        else:
            if roomtoenter != None:
                prior_room = self.location
                self.location = roomtoenter
                self.rangetotarget == 1
                whichdesc(roomtoenter)
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
            self.rangetotarget = 1
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



def whichdesc(roomtoenter):
    if (roomtoenter.firsttime == False and roomtoenter.shortdesc != None):
        print(shortdesc)
    else:
        print('You are ' + roomtoenter.desc + '\n')
        roomtoenter.firsttime = False

def pickone(endnumber, listofoptions):
    if random.randrange(0, endnumber) == 0:
        return listofoptions[random.randrange(0, len(listofoptions))]
#how do get in and out of generated areas??


# def generateHabBlock():
#     for x in range(0, 10):
#         generateRoom([gretchin], [medpack], ["You are in a series of rooms that used to hold a family", "You are in the center of several damaged apartments", [], [autogunammo])

#EnterHab1 = Room(North = )

# def generateRoom(possibleEnemies = [], possibleItems = [], possibleDesc = [], possibleAllies = [], possibleAmmo = [], North, South, East, West):
#     randomRoom = Room(desc = pickone(0, possibleDesc), enemies = pickone(2, possibleEnemies), ammo = pickone(4, possibleAmmo))
#     return randomRoom


    

#leaving commented out code for record of work for now
def linker(roomtolink, roomtolinkto):
    #not setting variable
    # call a method within rooom
    CardDir = {'North' : [roomtolinkto.North, 'South'], 'East' : [roomtolinkto.East, 'West'], 'South' : [roomtolinkto.South, 'North'], 'West' : [roomtolinkto.West,'East']}
    cardinaldirections = ['North', 'East', 'South', 'West']
    for cardinaldirection in cardinaldirections: 
        if CardDir[cardinaldirection][0] != None:
            print('Trying to link ' + roomtolink.name + ' to ' + roomtolinkto.name)


            #roomtolink.North = roomtolinkto
            #CardDir[cardinaldirection][1] = roomtolinkto
            roomtolink.changelink(CardDir[cardinaldirection][1], roomtolinkto)


            #CardDir[cardinaldirection][1] = roomtolinkto
            #roomtolink.North = roomtolinkto

            #roomtolink.changelink(cardinaldirection, roomtolinkto)
            #CardDir[cardinaldirection][0] = roomtolinkto
            #print(str(CardDir[cardinaldirection][1]) + ' linked to ' + str(roomtolinkto))
            #print(CardDir[cardinaldirection][1].name + ' linked to ' + roomtolinkto.name)

class Room():
    def __init__(self, name, desc='A dimly lit room with nothing remarkable', shortdesc=None, enemies=None, allies=None, items=None, ammo=None, canexamine=None, North=None, East=None, South=None, West=None, firsttime=False):
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
        self.shortdesc = shortdesc
        self.canexamine = canexamine
        self.firsttime = firsttime

        cardinals = [North, East, South, West]
        for cardinal in cardinals:
            if cardinal != None:
                linker(cardinal, self)

    def changelink(self, direction, new):
        if direction == 'North':
            self.North = new
        elif direction == 'East':
            self.East = new
        elif direction == 'South':
            self.South = new
        else:
            self.West = new
  
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
    print('There are enemies here!')
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

    if len(l2) > 1:
        print(l2 + ', and ' + l[-1])
    else:
        print(l[-1])



def createchargestring(name, weapon):
    options = ['The ' + name + ' roars and charges you', 'The ' + name + ' raises their ' + weapon + ' above their head and races towards you!']
    return(options[random.randrange(0, len(options))])

def createbulletshooting(name, weapon, target):
    options = ['The ' + name + ' raises their ' + weapon + ' to their shoulder and releases a hail of gunfire into ' + target + '!']
    return(options[random.randrange(0, len(options))])

def createenergyshooting(name, weapon, target):
    options = ['The ' + name + ' aims their ' + weapon + ' at ' + target + ' and unleashes a searing stream of energy!']
    return(options[random.randrange(0, len(options))])

def meleeattack(name, weapon, target):
    options = ['The ' + name + ' slashes ' + target + ' with their ' + weapon + '!']
    return(options[random.randrange(0, len(options))])

def createbulletshooting_player(name, weapon, target):
    options = ['You raise your ' + weapon + ' to your shoulder and release a hail of gunfire into ' + target+ '!']
    return(options[random.randrange(0, len(options))])

def createenergyshooting_player(name, weapon, target):
    options = ['You aim your ' + weapon + ' at ' + target + ' and unleash a searing stream of energy!']
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
        print('You now have ' + str(character.strength) + ' strength')
    elif command in ['dexterity', 'd', 'dex']:
        character.dexterity = character.dexterity + 1
        print('You now have ' + str(character.dexterity) + ' dexterity')
    elif command in ['health', 'h', 'hp']:
        maxhealth = maxhealth + 40
        character.health = character.health + 40
        print('You now have ' + str(character.health) + ' / ' + str(maxhealth) + ' health')
    else:
        print('Invalid selection')
        level_up(character)


def lookatitems(character):
    print('You have ' + character.weapon.name + ' in your weapon slot, it does ' + str(character.weapon.damage) + ' damage')
    print('You have ' + character.armour.name + ' in your armour slot, it has ' + str(character.armour.damageresist) + ' damage resist')
    for x in character.equipment:
        print(x.name)

    if autogunammo[0] > 0:
        print('You have ' + str(autogunammo[0]) + ' rounds of autogun ammo')
    if lasgunammo[0] > 0:
        print('You have ' + str(lasgunammo[0]) + ' las shots')
    if bolterammo[0] > 0:
        print('You have ' + str(lasgunammo[0]) + ' bolter shells')


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
            printdelay()
            print('You have ' + str(target.health) + ' health remaining!')

        else:
            print(target.name + ' takes ' + str(d) + ' damage!')
            printdelay()
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
            printdelay()
            damage(attacker, target)
        else:
            if attacker.weapon.ammotype == 'autogun':
                print(createbulletshooting(attacker.name, attacker.weapon.name, target.name))
            elif attacker.weapon.ammotype == 'plasma':
                print(createenergyshooting(attacker.name, attacker.weapon.name, target.name))
            else:
                print('The ' + attacker.name + ' shoots ' + target.name + ' with their ' + attacker.weapon.name)
            printdelay()
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
            temp = ammotypeDict[player.weapon.ammotype][0] - 5
            if temp < 0:
                print("You don't have enough ammo! Switch weapons... or run away.")
                interpreter(player, listener())

            else:
                if player.weapon.ammotype == 'plasma':
                    print(createenergyshooting_player(player.name, player.weapon.name, enemy_object.name))

                elif player.weapon.ammotype == 'autogun':
                    print(createbulletshooting_player(player.name, player.weapon.name, enemy_object.name))

                else:
                    print('You shoot the ' + enemy_object.name + ' with your ' + player.weapon.name)
                autogunammo[0] = temp
                damage(player, enemy_object)
                printdelay()
        else:
            print(meleeattack_player(player.name, player.weapon.name, enemy_object.name))
            damage(player, enemy_object)
            printdelay()
    if player.location.enemies != None and player.location.enemies != []:
        for enemy in player.location.enemies:
            AIcombat(enemy, player)
            printdelay()

#big gretchin didn't attack in the hallway, also passing function doesn't seem to work, also 'attack what', isn't working

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
    parsed_examinablesinroom = []
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

    if character.location.canexamine !=None:
        temp = [x.name for x in character.location.canexamine]
        set_examinablesinroom = set(examineDict.keys()).intersection(set(temp))
        examinablesinroom = list(set_examinablesinroom)
        parsed_examinablesinroom = [x.split() for x in examinablesinroom]
        parsed_examinablesinroom = [item for sublist in parsed_examinablesinroom for item in sublist]





    if command in ['examine inventory', 'inventory', 'items', 'inv']:
        lookatitems(character)
    elif command == "help":
        myhelp()
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
                else:
                    print(verb + ' what?') 


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

    elif set_listofwordsincommand.intersection({'ammo', 'ammunition', 'case', 'packs'}):
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

    elif set_listofwordsincommand.intersection(set(parsed_examinablesinroom)):
        x = 0
        specific = False
        while(x < len(examinablesinroom)):
            wow = set_listofwordsincommand.intersection(set(examinablesinroom[x].split()))

            if wow:

                specific = False
                examineDict[examinablesinroom[x]].examine()
                x = 100
            x+=1

    elif set_listofwordsincommand.intersection({'charge', 'run at', 'run towards'}):
        if (character.location.enemies != None and character.location.enemies != []):
            print('You raise your weapon up and race towards your foes')
            character.charge()
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
        if character.location.enemies != None and character.location.enemies != []:
            print("There are enemies in the room, better deal with them before looking around!")
        else:
            character.searchRoom(character.location)
    elif command in ['take all', 'take everything']:
        if character.location.enemies != None and character.location.enemies != []:
            print("There are enemies in the room, better deal with them before taking things!")

        else:
            if (character.location.items == None and character.location.ammo == None):
                print('Nothing found')
            x = 0
            while character.location.items != [] and character.location.items != None:

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



    elif set_listofwordsincommand.intersection({'door'}):
        print("You don't need to open doors, unless specified they will be openable. To move throughout the world, type a command containing the cardinal direction you want to move.")
        interpreter(player, listener())
    elif set_listofwordsincommand.intersection({'sneak', 'slip', 'around'}):
        print('You are caught!')
        for enemy in character.location.enemies:
            AIcombat(enemy, character)
            printdelay()

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
            printdelay()

    elif set_listofwordsincommand.intersection({'take', 'pick up', 'grab'}):
        print('Take what?')
    else:
        print('Invalid Command')
        interpreter(player, listener())


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
OrkBoy = Actor(name = 'ork boy', health = 150, weapon = bolt_pistol, armour=rusty_metal_armour, strength=3, dexterity=2, xpreward=70)
hiveganger = Actor(name = 'hive ganger', health = 100, weapon = axe, armour=old_flak_jacket, strength=2, xpreward=40)
hiveganger2 = Actor(name = 'hive ganger', health = 100, weapon = autopistol, armour=old_flak_jacket, dexterity=2, xpreward=40)

desperate_merchant = Actor(name = 'desperate merchant', weapon=autopistol, xpreward=30)
heretic_leader = Actor(name='heretic leader', weapon=rusty_auto_gun, armour=rusty_metal_armour, dexterity=2, xpreward=60)

player = Actor(name='you', weapon=fists, armour=clothes, rangetotarget=1)


#   def __init__(self, name, onexamine, quest=None, queststage=0, hasexamined=False, willcall=None):

mirror1 = ToExamine(name='cracked mirror', onexamine='Your reflection stares back sullenly.')
window1 = ToExamine('window', 'The windows are sealed tight.')
merchantstall = ToExamine('merchant stall', 'You quickly glance over the items on display, but none of them are any use to you.')
pedestal = ToExamine('pedestal', 'An evil looking structure of twisted metal and rusty spikes')
shuttle1 = ToExamine('ork shuttle', 'The shuttle is smoking slightly and does not seem to have been on the pad long.')
crack = ToExamine('crack in ceiling', 'You stand up on a desk to get a better look, and an icy hand seems to grip your gut. A line of explosives is wedged into the crack. After regaining your balance you take a closer look, most of the wires are frayed, several of the explosive packs are missing, and you can see no sign of any form of detonator. There does not seem to be an immidiate danger, but best to leave the weapons alone.')
utilitydoor = ToExamine('utility door', 'You attempt to open the door, but it is locked shut', willcall=utility)
roofcollapse = ToExamine('collapse of rubble', 'You start to move a few of the smaller pieces of debris when you notice what is unmistakably a human arm. You has you move more rubble you uncover more of the unfortunate person dressed in a workers uniform. You find a small card in one pocket that just has the numbers 41281 written on it.')



#I need to figure out if the pythonanywhere gist can take multiple files. All this text is a pain
startRoom = Room('Start', desc='in a small grimy room with a door on the north wall. A mirror is propped against a wall.', items=[rusty_auto_gun, old_flak_jacket, medpack, axe], canexamine=[mirror1], ammo=[autogunammocase])
secondRoom = Room('hallway1', desc='in a long dark hallway that runs east to west. There are other doors lining the hall, but they are locked, barred, or otherwise impassable', enemies=[gretchin], South=startRoom)
lookout = Room('lookout', desc='in a room with a smashed row of windows lining one wall. Outside you can see Grybith hive, from your position partway up the spire you can see the damaged city spread out towards the horizon. In the distance you can see the ruins of the massive walls that once surrounded Grybith.', items=[medpack], canexamine=[window1], East=secondRoom)
anteroom = Room('anteroom', desc='in a small anteroom. To the north a door is ajar; light and voices spill from the other side.', West=secondRoom)
merchantroom = Room('merchantroom', desc='in a large rectangular room with high ceilings. A second story gallery once stretched along several of the walls, but it has collapsed. The rubble has been pushed into the corners to make room for several stalls. There are exits in every direction.', allies=[man, man, man, woman, merchant, desperate_merchant], canexamine=[merchantstall], South=anteroom)
ramproom = Room('ramproom', desc='in  a room with a long ramp sloping down and to the west into the dark, there is a door at the end of it.', East=merchantroom)
bloodyroom = Room('bloodyroom', desc='in a room with long blood stains down the sides of the walls, almost as if the ceiling was bleeding. There is a an archway to the south covered in a black cloth', items=[medpack, knife])
sacrifcialchamber = Room('sacrifcialchamber', desc='in a large circular room with a pedestal in the middle. There is a door on the eastern wall', enemies=[heretic], canexamine=[pedestal])
Hereticstorage = Room('Hereticstorage', desc='in a small room with a few boxes.', West=sacrifcialchamber, ammo=[autogunammocase])
warren = Room('warren', desc='in a filthy warren of rooms that spread out in a nonsensical fashion. Some of the "walls" are nothing more than tarps. It takes you a moment to notice that some of piles you mistook for rags are actually people, they shy away from you, refusing to meet your eye, some scramble up meager possessions and flee. The maze continues down and to the east.', West=merchantroom)
warren2 = Room('a continuation of the warrens', desc='in the wild tangle of rooms continues. More people, more makeshift homes, more hopelessness. You are somewhat turned around, but notice a wide corridor leading south. Somewhere to the west behind you, you know there is a way back towards the enterance.', West=warren)
warren3 = Room('corridor', desc='in a long wide corridor. At the northern end, there is the enterance to the filthy slums. Indeed, there are tents, beds, and people crowding near the entrence and spreading down the corridor. However, farther south the human sprawl lessens and eventually disapears. You frown and glance at the people crowded far to close for comfort at the north end. A young girl, covered in grime catchs your eye. She points down the tunnel, and shakes her head; eyes wide with fear.', shortdesc='You are in the long corridor, exits to the north and south.', North=warren2)
warren4 = Room('2nd corridor', desc="in a corridor running north to south. You can't make much out to the north due to poor lighting. The south is completely blocked by a massive collapse. A brief examination shows that the destruction was too targeted to be an accident, this tunnel was collapsed on purpose. There is a door near the collapse on the western wall of the tunnel.", enemies=[big_gretchin], North=warren3)
security = Room('Security', desc='in a small room that runs paralell to the main tunnel, it seems to be a security room of some kind. To the south you can see a thick blast door leading outside.', enemies=[gretchin], canexamine=[crack], East=warren4)
landingpad = Room('landing pad', desc="on a thin platform leading out to landing pad. You step outside and can barely contain a gasp, stretching out before you is a verticle shaft so large a frigate could fly down it with room to spare. Above you there is a bright circle of light that marks the entrance. However, the light does not penetrate far, as you can't make out the bottom. An extremely makeshift shuttle sits on the pad to the south.", shortdesc='You are on the landing platform', enemies=[gretchin, gretchin2], ammo=[autogunammocase], canexamine=[shuttle1], North=security)
ship = Room('shuttle', desc='in the tiny stinking confines of what appears to be a small broken ork shuttlcraft', enemies=[OrkBoy], items=[battered_lasgun], ammo=[lasgunammocase], North=landingpad)
stairs = Room('nmerchant', desc='on a wide set of stairs desending northwards, in happier times thousands of people would have climbed these every day, now they lie broken and empty. There is a small utility door on one side of the staircase.', canexamine=[utilitydoor], South=merchantroom)
utilityroom = Room('uroom', desc='in a utility room with a door on the east wall. There is a considerable amount of stuff in the room, most of it useless, but you may find something of interest if you look around.', items=[medpack, medpack], ammo=[bolterammocase, lasgunammocase, autogunammocase], East=stairs)
promonade = Room('prom', desc='on a wide promonade runs east and west, stretching away into the gloom. Broken decorations, adverstisements, and other trash litter the avenue. To the south the massive stairway heads up and down, but the downward flight has been blocked by the ruined wrechage of several Imperial Guard Chimeras. How they got there is a mystery.', South=stairs)
promw1 = Room('promw1', desc='on a promonade that runs east to west, there is a wide archway to the north.', East=promonade)
npromw1 = Room('npromw1', desc='on a short wide walkway that opens onto a square surrounded by the ruins of what look like apartements. This section of the hive appears to have been hit by a barrage of artillery shells. The outer shell of the hive took the majority of the beating, but several shells pieced through into this complex.', enemies=[hiveganger, hiveganger2],ammo=[autogunammocase], South=promw1)
promw2 = Room('promw2', desc='on a promonade that runs east to west, there is an observation deck to your north, but the massive windows are covered by blast doors.', East=promw1)
promw3 = Room('promw3', desc='on a promonade that runs east to west, this section has a noticable curve along the contour of the hive. One section of the wall has collapsed into a heap of rubble.', canexamine=[roofcollapse], East=promw2)

deadwomanRoom = Room('noblewoman house', desc='a fancy house with plates that gleam like a thousand moons. A stench hits you as you look around a table and see a woman on her back wearing an expensive gown for a noblewoman that used to be white, but now is soaked with her blood. You notice a deep knife wound that appears to have been her demise. Politics in the hives are always messy. Exits lie to the north and east.',West=secondRoom)
gretchin_nest = Room('gretchin nest', desc='a dank room that smells as if something foul had been living there for some time. There are exits to the south and east.', enemies=[big_gretchin], West=deadwomanRoom)
oldstoreroom = Room('storeroom', desc='a room filled with unopenable boxes. Something glints in the shadows in the corner of your eye as the light from the room behind you enters. There are no new exits', items=[knife], South=deadwomanRoom)
guardroom = Room('guardroom1', desc='a disorganized room with a shivering man that does not respond to your calls. You see that he is wearing PDF uniform and realize he must have been here when the invasion happened. He is obviously insane and you decide to leave him alone. There are no new exits.', allies=[man], North=gretchin_nest)
armory = Room('armory', desc='a wreck of a room where weapons lay broken and tossed around. Hopefully there is still something useful here. There is an open doorway to the north', enemies=[big_gretchin], South=bloodyroom)
guards_quarters= Room('guards quaters', desc='a small room where beds lay in ruins and slime runs down the wall. There are exits to the north and west.', enemies=[big_gretchin, gretchin], South=armory)




def loading():



    global nextlevel
    global prior_room
    global playerXP
    global maxhealth
    global autogunammo
    ammoDict.update({'a case of autogun ammunition': autogunammocase})
    ammoDict.update({'several lasgun packs': lasgunammocase})
    ammotypeDict.update({'autogun': autogunammo})
    ammotypeDict.update({'lasgun': lasgunammo})
    pluralDict.update({'man': 'men'})
    pluralDict.update({'woman': 'women'})
    pluralDict.update({'heretic': 'heretics'})
    pluralDict.update({'gretchin': 'gretchin'})
    pluralDict.update({'big gretchin': 'big gretchin'})
    pluralDict.update({'ork boy': 'ork boyz'})
    pluralDict.update({'hive ganger': 'hive gangers'})
    playerXP = 0
    nextlevel = 50
    maxhealth = 100

    #There has got to be a better way to do this.
    #coordinate based matrices is one option
    #a messenger method in the room class that was sent to A when B is called. This would create the doublelinked list 
    #startRoom.North = secondRoom
    #A linker has been added, need to test, this can be removed (after testing), thank the gods
    secondRoom.West = lookout
    secondRoom.East = anteroom
    anteroom.North = merchantroom
    deadwomanRoom.North = oldstoreroom
    deadwomanRoom.East = gretchin_nest
    gretchin_nest.East = bloodyroom
    gretchin_nest.South = guardroom
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
    merchantroom.East = warren
    warren.East = warren2
    warren2.South=warren3
    warren3.South=warren4
    warren4.West=security
    security.South=landingpad
    landingpad.South=ship
    merchantroom.North=stairs
    stairs.North = promonade
    promonade.West = promw1
    promw1.North = npromw1
    promw1.West = promw2
    promw2.West = promw3



def main_Control_Loop():
    print('Initial stats:')
    print('Strength increases your damage with melee weapons.')
    print('Dexterity increases your damage with ranged weapons.')
    print('Health increases your maximum health')
    print('Select starting stats: 1/2')
    level_up(player)
    print('Select starting stats: 2/2')
    level_up(player)
    print('You are ' + startRoom.desc)
    print('Type help for help')
    while playing:
        check_quests()
        interpreter(player, listener())







if __name__ == '__main__':

    print('Welcome')
    print('Hint: remember to search rooms for items before you leave')
    #print("Enter your character's name")
    #playername = sys.stdin.readline().strip()
    #player.name = playername

    loading()
    main_Control_Loop()
