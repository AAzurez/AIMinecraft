from fastmcp import FastMCP
from javascript import require, On
mineflayer = require('mineflayer')
from tools.chat import attack

import anthropic 

client = anthropic.Anthropic(api_key="")

mcp = FastMCP("Jerry")

@mcp.tool()
def attack_tool():
    print(attack())

tools = [
    {
        "name": "attack",
        "description": "Attack the nearest entity",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    }
]

RANGE_GOAL = 1
BOT_USERNAME = 'Jerry'

bot = mineflayer.createBot({
    'host': '127.0.0.1',
    'port': 25565,
    'username': BOT_USERNAME
    })

@On(bot, "login")
def login(*args):
    bot.chat("Hi everyone!")

@On(bot, 'chat')
def handleMsg( sender, message, *args):
    if sender != BOT_USERNAME:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            messages=[
                {"role": "user", "content": "From any message, Use the attack tool. NO EXTRA TEXT. Just respond with a short message."},
            ],
            max_tokens=50,
            tools = tools,
        )

        for block in response.content:
            if block.type == "tool_use" and block.name == "attack":
                attack_tool()

        reply = response.content[0].text
        bot.chat(reply)

if __name__ == "__main__":
    mcp.run()