from fastmcp import FastMCP
from javascript import require, On
from tools.chat import chat
from tools.attack import attackEntity
from tools.destroy import destroy

mineflayer = require('mineflayer')

import anthropic 

client = anthropic.Anthropic()

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
def chat_tool():
    print(chat())

@mcp.tool()
def destroy_tool():
    print(destroy())

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
                 
                 "From any message, USE THE attack TOOL. NO EXTRA TEXT. Just respond with a short message."

                },
            ],
            max_tokens=50,
            tools = tools,
        )

        for block in response.content:
            print(block)
            if block.type == "tool_use" and block.name == "attack":
                attack_tool(bot)
            elif block.type == "tool_use" and block.name == "chat":
                chat_tool()
            elif block.type == "tool_use" and block.name == "destroy":
                destroy_tool()

"""        reply = response.content[0].text
        bot.chat(reply)"""

if __name__ == "__main__":
    mcp.run()