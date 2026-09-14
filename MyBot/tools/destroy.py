def destroy(bot, block_name):
    print("Destroy tool is running")\
    
    block = bot.findBlock({
    'matching': bot.registry.blocksByName[block_name].id,
    'maxDistance': 32
    })

    if block is None:
        bot.chat(f"No {block_name} found nearby.")
        return

    bot.dig(block)
         
"""
Movement needed
"""