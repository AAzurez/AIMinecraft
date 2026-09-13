from fastmcp import FastMCP
from javascript import require, On
mineflayer = require('mineflayer')
pathfinder = require('mineflayer-pathfinder')
from tools.chat import chat

import anthropic 

client = anthropic.Anthropic(api_key="")

mcp = FastMCP("Jerry")

@mcp.tool()
def chat_tool(sender: str, message: str) -> str:
    """Send a chat message as the bot."""
    chat(sender, message)
    return f"Sent message from {sender}: {message}"

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
                {"role": "user", "content": "You are a helpful assistant that responds to Minecraft chat messages. NO EXTRA TEXT. Just respond with a short message."},
            ],
            max_tokens=50,
        )
        reply = response.content[0].text
        bot.chat(reply)

if __name__ == "__main__":
    mcp.run()