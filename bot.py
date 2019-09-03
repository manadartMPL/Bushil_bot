import os

import discord
import random
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='*')


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(
        f'{bot.user} has connected to the following guilds:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@bot.command(name='guessNumbers', help='Do a number guessing and find the number between 0 and 100')
async def number_guess(ctx):
    number = random.randint(0, 100)
    numberOfGuesses = 0
    await ctx.send('Guess a number in between 0 and 100. \nSay stop to end the game early.')

    while True:
        answer = await bot.wait_for('message')
        if not (answer.content.isdigit() or answer.content.lower() == "stop"):
            continue

        numberOfGuesses += 1

        if answer.content.lower() == "stop":
            await ctx.send('Looks like game ends now')
            return
        answer = int(answer.content)

        if answer == number:
            await ctx.send(f'Congrats you found the number in {numberOfGuesses} guesses')
            return

        if answer < number:
            await ctx.send(f'Your guess is too low. Try a higher number.')
            continue

        if answer > number:
            await ctx.send(f'Your guess is too high. Try a lower number.')
            continue


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


@bot.command(name='roll_dice',
             help='*roll_dice [number of dice] [number of sides] Roll up to 6 dice with up to 20 sides.')
async def dice_roll(ctx, number_of_dice: int = 1, number_of_sides: int = 6):
    if number_of_dice <= 0 or number_of_sides <= 0:
        await ctx.send('Not enough dice to roll')
        return

    if number_of_dice > 6:
        number_of_dice = 6

    if number_of_sides > 20:
        number_of_sides = 20

    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


bot.run(token)
