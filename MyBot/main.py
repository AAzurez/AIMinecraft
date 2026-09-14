from fastmcp import FastMCP
from javascript import require, On
from tools.chat import chat
from tools.attack import attackEntity
from tools.destroy import destroy
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

mineflayer = require('mineflayer')

import anthropic 

client = anthropic.Anthropic(api_key = os.getenv("API_KEY"))

mcp = FastMCP("Server")

BOT_USERNAME = 'Jerry'

bot = mineflayer.createBot({
    'host': '127.0.0.1',
    'port': 25565,
    'username': BOT_USERNAME
    })

@mcp.tool()
def attack_tool(bot):
    attackEntity(bot)

@mcp.tool()
def chat_tool(sender, message):
    print(chat(sender, message))

@mcp.tool()
def destroy_tool(bot):
    print(destroy(bot))

tools = [
    {
        "name": "attack",
        "description": "Attack the nearest entity",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "chat",
        "description": "Send a message in the chat",
        "input_schema": {
            "type": "object",
            "properties": {
                "sender": {"type": "string"},
                "message": {"type": "string"}
            }
        }
    },
    {
        "name": "destroy",
        "description": "Destroy the nearest block",
        "input_schema": {
            "type": "object",
            "properties": {}
        }
    }
]

@On(bot, "login")
def login(*args):
    bot.chat("Hi everyone!")

@On(bot, 'chat')
def handleMsg( sender, message, *args):
    if sender != BOT_USERNAME:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            messages=[
                {"role": "user", "content": 
                 
                 "Goal: Beat the Ender Dragon. The General Timeline is to get wood first and then get stone."
                 "If I need to get wood -> I need to break wood"
                 "If I need to get stone -> I need to break stone"

                },
            ],
            max_tokens=100,
            tools = tools,
        )

        for block in response.content:
            print(block)
            if block.type == "tool_use" and block.name == "attack":
                attack_tool()
            elif block.type == "tool_use" and block.name == "chat":
                msg = block.input.get('message')
                bot.chat(msg)
            elif block.type == "tool_use" and block.name == "destroy":
                destroy_tool()

if __name__ == "__main__":
    mcp.run()