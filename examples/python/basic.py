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

@On(bot, "end")
def handle(*args):
  print("Bot ended!", args)

@On(bot, "login")
def login(*args):
    bot.chat("Hi everyone!")

@On(bot, "entityHurt")
def entityHurt(this, entity):
    if entity == None:
       return
    print(' ', entity)
    if entity.type == "hostile":
        bot.chat(f"Haha! The {entity.displayName} got hurt!")
    elif entity.type == "player":
        if entity.username in bot.players:
            ping = bot.players[entity.username].ping
            bot.chat(f"Aww, poor {entity.username} got hurt. Maybe you shouldn't have a ping of {ping}")

@On(bot, "health")
def health(*args):
    bot.chat(f"I have {bot.health} health and {bot.food} food")
@On(bot, "death")
def death(*args):
    bot.chat("I died x.x")