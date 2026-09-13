from javascript import require, On
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')

RANGE_GOAL = 1
BOT_USERNAME = 'Jerry'

bot = mineflayer.createBot({
  'host': '127.0.0.1',
  'port': 25565,
  'username': BOT_USERNAME
})

bot.loadPlugin(pathfinder.pathfinder)
print("Started mineflayer")

@On(bot, 'spawn')
def handle(*args):
  print("I spawned 👋")
  movements = pathfinder.Movements(bot)

  @On(bot, 'chat')
  def handleMsg( sender, message, *args):
    print("Got message", sender, message)
    if sender != BOT_USERNAME:
      bot.chat(f'Hi, you said "{message}"')
      if 'go beat the game' in message:
        bot.chat("Ok, I will go beat the game!")
      if 'come' in message:
        player = bot.players[sender]
        print("Target", player)
        target = player.entity
        if not target:
          bot.chat("I don't see you !")
          return
        pos = target.position
        bot.pathfinder.setMovements(movements)
        bot.pathfinder.setGoal(pathfinder.goals.GoalNear(pos.x, pos.y, pos.z, RANGE_GOAL))
      

@On(bot, "login")
def login(*args):
    bot.chat("Hi everyone!")

@On(bot, "end")
def handle(*args):
  print("Bot ended!", args)