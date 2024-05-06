import discord
from discord.ext import commands
import asyncio
import requests
import random
import os
from dotenv import load_dotenv
from datetime import datetime
from tabulate import tabulate
from online24h import revive

intents = discord.Intents.all()
client = commands.Bot(command_prefix='/', intents=intents)
client.remove_command('help')
load_dotenv()


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("/help"))


@client.command(name='help')
async def help_command(message, arg=None):
    if arg is None:
        # Display general help message
        help_msg = {
            "title": "🤖 Main Menu:",
            "description": (
                "Type `/help command` for more info on a command.\n\n"
                "**Commands:**\n"
                ":blue_circle: `/help` - Shows this message\n"
                ":orange_circle: `/fact` - Get a random fun-fact\n"
                ":green_circle: `/say text` - Make the bot say something\n"
                ":purple_circle: `/prayer country city` - Today's prayer times for given country and city\n"
                ":red_circle: `/delete number` - Delete a specified number of messages"
            )
        }

        await message.channel.send(embed=discord.Embed.from_dict(help_msg))

    else:
        if arg.lower() == 'help':

            help_embed = discord.Embed(
                title="🤖 /help",
                description="Shows the list of all available commands",
                color=discord.Color.blue()
            )
            await message.channel.send(embed=help_embed)

        elif arg.lower() == 'fact':
            help_embed = discord.Embed(
                title="📚 /fact",
                description="Get a random fun-fact",
                color=discord.Color.orange(),
            )
            file = discord.File("images/fact.png", filename="image.png")
            help_embed.set_image(url="attachment://image.png")
            await message.channel.send(embed=help_embed, file=file)

        elif arg.lower() == 'say':
            help_embed = discord.Embed(
                title="💬 /say",
                description="Make the bot say something",
                color=discord.Color.green()
            )
            file = discord.File("images/say.png", filename="image.png")
            help_embed.set_image(url="attachment://image.png")
            await message.channel.send(embed=help_embed, file=file)

        elif arg.lower() == 'prayer':
            help_embed = discord.Embed(
                title="🕌 /prayer",
                description="Get today's prayer times for the specified country and city",
                color=discord.Color.purple()
            )
            file = discord.File("images/prayer.png", filename="image.png")
            help_embed.set_image(url="attachment://image.png")
            await message.channel.send(embed=help_embed, file=file)

        elif arg.lower() == 'delete':
            help_embed = discord.Embed(
                title="🗑️ /delete",
                description="Delete the specified number of messages",
                color=discord.Color.red()
            )
            file = discord.File("images/delete.png", filename="image.png")
            help_embed.set_image(url="attachment://image.png")
            await message.channel.send(embed=help_embed, file=file)

        else:
            help_embed = discord.Embed(
                title="❌ Unknown command",
                description="Type `/help` to see available commands.",
                color=discord.Color.dark_red()
            )
            await message.channel.send(embed=help_embed)


@client.command()
async def fact(message):
    api_url = 'https://api.api-ninjas.com/v1/facts'
    response = requests.get(api_url, headers={'X-Api-Key': os.environ['NINJA_API_TOKEN']})

    funfact_emojis = [":raised_hands:", ":point_down:", ":performing_arts:", ":ghost:", ":shushing_face:"]

    if response.status_code == requests.codes.ok:
        embed = discord.Embed(title="", description="", color=discord.Color.orange())
        embed.add_field(name=f'Fun fact {random.choice(funfact_emojis)}', value=response.text[11:-3])
        await message.channel.send(embed=embed)


@client.command()
async def say(message, *, arg):
    refusal = ["Nope", "Mind yourself", "Not today"]

    if random.random() < 0.3:
        await message.channel.send(random.choice(refusal))
    else:
        await message.channel.purge(limit=1)
        await message.channel.send(arg)


@client.command()
async def delete(message, arg: int):
    if message.author.guild_permissions.administrator:
        await message.channel.purge(limit=arg + 1)  # +1 to include the command

        embed = discord.Embed(
            title="",
            description=f'{arg} message{"s" if arg > 1 else ""} deleted by {message.author.mention}',
            color=discord.Color.red()
        )
        await message.channel.send(embed=embed)
    else:
        await message.channel.send("```Error: Missing admin permissions```")


@client.command()
async def prayer(message, country: str, *, city: str):
    api_url = f"http://api.aladhan.com/v1/timingsByCity?city={city}&country={country}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()

        required_timings = [
            ["Fajr", data["data"]["timings"]["Fajr"]],
            ["Sunrise", data["data"]["timings"]["Sunrise"]],
            ["Dhuhr", data["data"]["timings"]["Dhuhr"]],
            ["Asr", data["data"]["timings"]["Asr"]],
            ["Maghrib", data["data"]["timings"]["Maghrib"]],
            ["Isha", data["data"]["timings"]["Isha"]]
        ]

        today_date = datetime.now().strftime("%d-%m-%Y")
        prayer_times = tabulate(required_timings, headers=["Prayer", "Time"])
        await message.channel.send(f"```{today_date} | {country.upper()} - {city.upper()}```")
        await message.channel.send(f"```{prayer_times}```")
    else:
        await message.channel.send(f"```Error: {response.status_code}```")


@client.event
async def on_message(message):
    await client.process_commands(message)
    if message.author == client.user:
        return

    # GREETINGS
    user_greetings = ["hi", "hello", "wassup", "sup", 'hey', 'yo']
    bot_greetings = ["What's up", "Yooo", "How's it going?", "Hey", "Hello there"]
    greetings_emojis = [":wave:", ":eyes:", ":slight_smile:", ":upside_down:", ":smirk:", ]

    if any(message.content.lower().startswith(greeting) for greeting in user_greetings):
        async with message.channel.typing():
            await asyncio.sleep(2)
        await message.channel.send(f'{random.choice(bot_greetings)} {random.choice(greetings_emojis)}')

    # RANDOM MESSAGE REACTIONS
    reactions = ['👀', '👾', '🥸', '🤌', '👍', '👎']
    if random.random() < 0.1:
        await message.add_reaction(random.choice(reactions))

revive()
client.run(os.environ['STRADA_TOKEN'])
