# Import some necessary libraries.
import math
import time
import random
import re
import socket
 
# Some basic variables used to configure the bot        
server = "irc.ircworld.org" # Server
channel = "#balt" # Channel
botnick = "Legatobot" # Your bot's nick
 
# User stats object, makes the stats recallable
userStats = {}
 
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ircsock.connect((server, 6667)) # Here we connect to the server using the port 6667
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :http://lemonparty.org.\n") # user authentication
ircsock.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot
 
# All the functions
def commands(nick,channel,message):
  if message.find('!shellium')!=-1:
    ircsock.send('PRIVMSG %s :%s: Shellium is dead!\r\n' % (channel,nick))
  elif message.find('!help')!=-1:
    ircsock.send('PRIVMSG %s :%s: #XdY to roll X Y-sided die' % (channel,nick))
 
def ping(): # This is our first function! It will respond to server Pings.
  ircsock.send("PONG :pingis\n")
 
def sendmsg(chan , msg): # This is the send message function, it simply sends messages to the channel.
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n")
 
def joinchan(chan): # This function is used to join channels.
  ircsock.send("JOIN "+ chan +"\n")
 
def rollDie(numberOfDice, typeOfDie, usernick): # Dice rolling function
  if typeOfDie == "0":
    ircsock.send("PRIVMSG " + channel + " :" + ":^)\n")
    return
 
  if numberOfDice == "":
    numberOfDice = "1"
  elif numberOfDice == "0":
    ircsock.send("PRIVMSG " + channel + " :" + ":^)\n")
    return
 
  dieResults = []
  for i in range(int(numberOfDice)):
    dieResults.append(random.randint(1, int(typeOfDie)))
 
  ircsock.send("PRIVMSG " + channel + " :" + usernick + " rolls " + numberOfDice + "d" + typeOfDie + " = " + str(sum(dieResults)) + " (" + " + ".join(str(x) for x in dieResults) + ")\n")
 
def rollStats(usernick): # Stat rolling function
  def modPipe(dieScore): # Stat modifier function
    # Minus 10, divide by 2 and floor it then make it into an integer
    modValue = int(math.floor((dieScore - 10) / 2 ))
   
    # Adds a + if the modifier is more than or equal to 0
    if modValue < 0:
      modValue = "" + str(modValue)
    elif modValue >= 0:
      modValue = "+" + str(modValue)
     
    return modValue
   
  if usernick in userStats:
    ircsock.send("PRIVMSG " + channel + " :" + usernick + " rolled: \n")
    for stat in userStats[usernick]:
      ircsock.send("PRIVMSG " + channel + " :" + stat + ": " + str(userStats[usernick].get(stat)) + " (" +modPipe(userStats[usernick].get(stat)) + ")\n")
    return
 
  stats = ["Str", "Dex", "Con", "Int", "Wis", "Cha"]
  statObj = {}
 
  ircsock.send("PRIVMSG " + channel + " :" + usernick + " rolled: \n")
 
  for stat in stats:
    dieScoreResults = []
    for i in range(0, 4):
      dieScoreResults.append(random.randint(1, 6))
    dieScoreResults.remove(min(dieScoreResults))
   
    statObj[stat] = sum(dieScoreResults)
   
    ircsock.send("PRIVMSG " + channel + " :" + stat + ": " + str(sum(dieScoreResults)) + " (" + modPipe(sum(dieScoreResults)) + ")\n")
 
  userStats[usernick] = statObj
 
def clearStats(usernick): # Clears stored stats for user
  if usernick in userStats:
    del userStats[usernick]
    ircsock.send("PRIVMSG " + channel + " :" + "Stats cleared for " + usernick + "\n")
 
# End of functions
 
joinchan(channel) # Joins the channel using the functions we previously defined
 
while 1: # Be careful with these! it might send you to an infinite loop
  ircmsg = ircsock.recv(2048) # receive data from the server
  ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
  usernick = ircmsg.split('!')[0][1:]
  print(ircmsg) # Here we print what's coming from the server
  if ircmsg.find(' PRIVMSG ')!=-1:
    nick=ircmsg.split('!')[0][1:]
    channel=ircmsg.split(' PRIVMSG ')[-1].split(' :')[0]
    commands(nick,channel,ircmsg)
 
  if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
    ping()
 
  # If anonkun joins, bot says hi :3
  if ircmsg.find("JOIN") != -1 and ircmsg.lower().find("anonkun") != -1:
    ircsock.send("PRIVMSG " + channel + " :" + "hello " + usernick + " :3\n")
 
  # If someone says bye, bot says bye to them
  if ircmsg.lower().find("bye") != -1:
    ircsock.send("PRIVMSG " + channel + " :" + "Bye " + usernick + "!\n")
 
  # Array for funny naughty words
  curses = ["homo", "dildo", "scrub", "penishole", "fag",
  "vagina", "refugee", "immigrant", "nigger", "shitskin",
  "scrotum", "banaan", "madman", "equine vaginal cavity"]
 
  # Funny reply
  for curse in curses:
    if ircmsg.lower().find(curse) != -1 and ircmsg.lower().find("you") != -1:
      if ircmsg.lower().find("fuck") != -1: # If it has fuck, add some fucking
        ircsock.send("PRIVMSG " + channel + " :" + "yeah you fucking " + curse + "\n")
        break
      else:
        ircsock.send("PRIVMSG " + channel + " :" + "yeah you " + curse + "\n")
        break
 
  # Splits message into words
  if re.search(r'#\d[dD]\d', ircmsg):
    splitMessage = ircmsg.split(" ")
   
    # Gives all the words a number
    def indexOfRoll(the_list, substring):
      for i, s in enumerate(the_list):
        if re.search(r'#\d[dD]\d', s):
          return i
      return -1
   
    # Creates dieRoll variables
    dieRoll = re.split(r'[dD]', splitMessage[indexOfRoll(splitMessage, "#")])
   
    # Rolls the die somehow???
    rollDie(re.sub('[^0-9]','', dieRoll[0]), re.sub('[^0-9]','', dieRoll[1]), usernick)
 
  if ircmsg.find("#stats") != -1:
    rollStats(usernick)
 
  if ircmsg.find("#clearstats") != -1: # Calls clearStats if someone wants to clear their stats
    clearStats(usernick)