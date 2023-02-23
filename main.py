from keepalive import keep_alive
import discord
import pickle
import os
from gpt_index import GPTSimpleVectorIndex

os.environ["OPENAI_API_KEY"] = os.getenv('openai_token')

MAX_REQUESTS = 10

# Load the request counts from a file, if it exists
try:
    with open('request_counts.pkl', 'rb') as f:
        request_counts = pickle.load(f)
except FileNotFoundError:
    request_counts = {}

intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)

def print_request_counts():
    for user_id, request_count in request_counts.items():
        print(f'The user with ID {user_id} has made {request_count} requests.')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = message.author.id
    user_name = str(message.author)

    if user_id not in request_counts:
        request_counts[user_id] = {'name': user_name, 'count': 0}

    if request_counts[user_id]['count'] >= MAX_REQUESTS:
        await message.channel.send('Sorry, you have reached the maximum number of requests.')
        return
      
    if message.content == '/search':
        await message.channel.send(f'Hello {user_name}!')

    try:
      if message.content.startswith('$search'):
        request_counts[user_id]['count'] += 1
        await message.channel.send('Hello!')
        index = GPTSimpleVectorIndex.load_from_disk('archichatso_high_train.json')
        query = message.content[8:]  # extract the query from the message content
        response = index.query(query, response_mode="compact")
        await message.channel.send(f"Bot says: {response.response}")  # send the response to the user

    except:
        await message.channel.send(f'Something Error Has Occured.')

    

    # Print the request counts after processing each message
    print_request_counts()

    # Save the updated request counts to a file
    with open('request_counts.pkl', 'wb') as f:
        pickle.dump(request_counts, f)

keep_alive()
Token = os.getenv('discord_token')
client.run(Token)


# import discord
# import pickle
# import os
# from discord.ext import commands
# from discord import app_commands

# MAX_REQUESTS = 5

# # Load the request counts from a file, if it exists
# try:
#     with open('request_counts.pkl', 'rb') as f:
#         request_counts = pickle.load(f)
# except FileNotFoundError:
#     request_counts = {}

# intents = discord.Intents.all()
# client = commands.Bot(command_prefix='/', intents=intents)

# def print_request_counts():
#     for user_id, request_count in request_counts.items():
#         print(f'The user with ID {user_id} has made {request_count} requests.')


# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))



# @client.tree.command(name="search", description="Have a chat with nbc")
# async def chat(ctx):
#     user_id = ctx.author.id
#     user_name = str(ctx.author)

#     if user_id not in request_counts:
#         request_counts[user_id] = {'name': user_name, 'count': 0}

#     if request_counts[user_id]['count'] >= MAX_REQUESTS:
#         await ctx.send('Sorry, you have reached the maximum number of requests.')
#         return

#     await ctx.send('Hello!')
#     request_counts[user_id]['count'] += 1

#     # Print the request counts after processing each message
#     print_request_counts()

#     # Save the updated request counts to a file
#     with open('request_counts.pkl', 'wb') as f:
#         pickle.dump(request_counts, f)
# Token = os.getenv('discord_token')
# client.run(Token)


# Not working version but was similar to my chatgpt
# import discord
# import pickle
# from discord.ext import commands
# from discord_slash.context import SlashContext
# from discord_slash import SlashCommand



# MAX_REQUESTS = 5

# # Load the request counts from a file, if it exists
# try:
#     with open('request_counts.pkl', 'rb') as f:
#         request_counts = pickle.load(f)
# except FileNotFoundError:
#     request_counts = {}

# intents = discord.Intents.all()
# client = commands.Bot(command_prefix='/', intents=intents)
# slash = SlashCommand(client, sync_commands=True)

# def print_request_counts():
#     for user_id, request_count in request_counts.items():
#         print(f'The user with ID {user_id} has made {request_count} requests.')


# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))
#     guild_ids = [guild.id for guild in client.guilds]
#     await slash.sync_all_commands(guild_ids)


# @slash.slash(name="search", description="Have a chat with nbc")
# async def chat(ctx: SlashContext):
#     user_id = ctx.author.id
#     user_name = str(ctx.author)

#     if user_id not in request_counts:
#         request_counts[user_id] = {'name': user_name, 'count': 0}

#     if request_counts[user_id]['count'] >= MAX_REQUESTS:
#         await ctx.send('Sorry, you have reached the maximum number of requests.')
#         return

#     await ctx.send('Hello!')
#     request_counts[user_id]['count'] += 1

#     # Print the request counts after processing each message
#     print_request_counts()

#     # Save the updated request counts to a file
#     with open('request_counts.pkl', 'wb') as f:
#         pickle.dump(request_counts, f)

# client.run('MTA3NzQxNzQ4MzUyNDM4NjgzNg.G06qjv.80DVaUSNqMmtCiDpMMYTd3Y_9kOEoouHXUpZts')
