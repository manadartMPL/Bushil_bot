import os

import discord
import random
from dotenv import load_dotenv

from discord.ext import commands

# .env file can be created for own use. Just need a discord account

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Setting prefix needed to execute commands, could be almost anything
# Change prefix in code if want to.
bot = commands.Bot(command_prefix='b!')


# Something to just see the bot has connected to channels its been added to and
# wanted to list members as little test on bot.
@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} has connected to the following guilds:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


# Simple number guessing, the people in channel game was started in can guess which
# number bot has between 0 and 100. The guessing game will end early if a player says stop
# casing does not matter but the message has to be only the word.
# After each guess the bot will give a hint if the guess is not correct. If correct
# bot will say how many guesses it took and who said it.
@bot.command(name='guessNumbers', help='Do a number guessing and find the number between 0 and 100')
async def number_guess(ctx):
    number = random.randint(0, 100)
    number_of_guesses = 0
    await ctx.send('Guess a number in between 0 and 100. \nSay stop to end the game early.')

    while True:
        answer = await bot.wait_for('message')
        if answer.channel != ctx.channel:
            continue

        if not (answer.content.isdigit() or answer.content.lower() == "stop") and answer.author == bot.user:
            continue

        number_of_guesses += 1

        if answer.content.lower() == "stop":
            await ctx.send('Looks like game ends now')
            return
        sender = answer.author.display_name
        answer = int(answer.content)

        if answer == number:
            await ctx.send(
                f'Congrats {sender} found the number. It took {number_of_guesses} guesses to find the number')
            return

        if answer < number:
            await ctx.send(f'Your guess is too low. Try a higher number.')
            continue

        if answer > number:
            await ctx.send(f'Your guess is too high. Try a lower number.')
            continue


# Just a test on seeing on how embedded messages work on discord
@bot.command(name='mro', help='Spawns a random monster ranch monster')
async def monster_spawn(ctx):
    monster_names = ['Drezo', 'Zenchen']
    monster_pics = [
        'https://vignette.wikia.nocookie.net/mro/images/e/e9/Dpmfa822.png/revision/latest?cb=20120514202103',
        'https://vignette.wikia.nocookie.net/mro/images/f/fe/Dpmfa599-1-.png/revision/latest?cb=20110414141712'
    ]
    choice = random.randrange(2)
    response = discord.Embed(title=monster_names[choice])
    response.set_image(url=monster_pics[choice])
    await ctx.send(embed=response)


# A dice rolling command that'll give user random number(s).
# User can specify how many dice and how many sides the dice has. If they try to use negative numbers for either option
# then bot will give error message. If no additional options given then bot pick number form random 1-6.
@bot.command(name='roll_dice',
             help='*roll_dice [number of dice] [number of sides] Roll up to 6 dice with up to 20 sides.')
async def dice_roll(ctx, number_of_dice: int = 1, number_of_sides: int = 6):
    if number_of_dice <= 0 or number_of_sides <= 0:
        await ctx.send(f'Not enough dice to roll {ctx.author.display_name}')
        return

    if number_of_dice > 6:
        number_of_dice = 6

    if number_of_sides > 20:
        number_of_sides = 20

    dice = []
    for _ in range(number_of_dice):
        dice.append(str(random.choice(range(1, number_of_sides + 1))))
    await ctx.send(f'{ctx.author.display_name} rolled ' + ', '.join(dice))


# Coin toss command
# Command to simulate coin tosses. Bot will flip 1-20 coins.
# Any number less than 1 will be rejected and any number higher than 20 is turned down to 20.
@bot.command(name='coin_toss',
             help='*coin_toss [number of coins] Flip up to 20 coins with 1 being the minimum.')
async def coin_toss(ctx, number_of_coins: int = 1):
    if number_of_coins <= 0:
        await ctx.send(f'Not enough coins to flip {ctx.author.display_name}')
        return

    print(f'{number_of_coins}')
    if number_of_coins > 20:
        number_of_coins = 20

    coins = []
    for _ in range(number_of_coins):
        flip = random.randrange(2)
        if flip == 0:
            coins.append('heads')
        else:
            coins.append('tails')
    await ctx.send(f'{ctx.author.display_name} flipped ' + ', '.join(coins))


# A command that lets users make the bot say anything given to the bot.
# Bot will quickly delete the message of the member commanding the bot to saying the message
@bot.command(name='say',
             help='Make the bot say and hide the message commanding the bot.')
async def say(ctx):
    msg = ctx.message.content.split(' ', 1)
    await ctx.message.delete()
    await ctx.send(msg[1])

# A guessing game that uses the display names of people in the text channel the command was used in.
# Players will try to guess the name that bot has. The bot will can end the game early or give hints if told to.
# When the chosen name has been guess the bot will how many guesses and hints it took to find the name.
@bot.command(name='guessWho')
async def guess_who(ctx):
    membersList = ctx.message.channel.members
    members = []
    number_of_guesses = 0
    number_of_hints = 0
    for person in membersList:
        members.append(person.display_name)
    chosen = random.choice(members)
    await ctx.send(f'I have chosen a name of a person in this room. Can you guess who it is? \n '
                   f'Say bushil stop to end the game early or hint if you need one.')
    while True:
        answer = await bot.wait_for('message')
        if answer.channel != ctx.channel or answer.author == bot.user:
            continue

        if answer.content.lower() == "bushil stop" and not answer.author == bot.user:
            await ctx.send('Looks like game ends now')
            return

        if answer.content.lower() == "hint" and not chosen == 'hint':
            number_of_hints += 1
        else:
            number_of_guesses += 1
        sender = answer.author.display_name

        if answer.content.lower() == chosen.lower():
            await ctx.send(f'{sender} guessed correctly. It only took {number_of_guesses} guesses to find '
                           f' the answer and {number_of_hints} hints')
            return

        if answer.content.lower() == 'hint':
            hintList = random.randint(0, 2)
            if hintList == 0:
                await ctx.send(f'The name starts with {chosen[0]}')
                continue
            elif hintList == 1:
                await ctx.send(f'The name ends with {chosen[len(chosen)-1]}')
                continue
            else:
                await ctx.send(f'The name is {len(chosen)} characters long.')
                continue
        await ctx.send('Nope that is not the person i was thinking of.')


# Command that will get the bot to delete an number of messages in a text channel.
# User has option to delete the newest message (default) or oldest messages first
@bot.command(name='purge',
             help='b!purge [number of messages] [(optional) delete oldest or newest (true or false)]')
async def purge(ctx, messages: int, oldest: bool = False):
    loops = 1
    extramsgs = 0

    if not ctx.message.author.permissions_in(ctx.channel).manage_messages:
        await ctx.send('You do not have the permissions to delete messages in here.')
        return

    if messages <= 0:
        await ctx.send('Can only delete a positive number amount of messages')
        return
    if messages > 100:
        loops = round(messages / 100)
        extramsgs = messages - 100
        messages = 100

    for _ in range(loops):
        await ctx.message.channel.purge(limit=messages + 1, oldest_first=oldest)
        messages = extramsgs
        if extramsgs > 100:
            extramsgs -= 100
    await ctx.send(f'Bushil chomped on the messages that needed to go')


# Just some random auto responses the both will throw out if it sees specific words said by someone
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if 'good night' in message.content:
        await message.channel.send(f'Good night {message.author.display_name}')
    if 'good morning' in message.content:
        await message.channel.send(f'Good morning {message.author.display_name}')
    if 'happy birthday' in message.content:
        await message.channel.send(f'Happy Birthday!')

    await bot.process_commands(message)

bot.run(token)
