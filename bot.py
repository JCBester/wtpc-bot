from discord.ext import commands, tasks
import configparser
from datetime import datetime
from discord import Embed


config = configparser.ConfigParser()
config.read("wtpc-config.ini")
token = config["secrets"]["token"]
channelID = int(config["discord"]["channelID"])
bot_prefix = config["discord"]["bot_prefix"]

bot = commands.Bot(command_prefix = bot_prefix)
client = commands.Bot(command_prefix= bot_prefix)

#To be used later
trackers = {
    "rsvp": [],
}


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} - {bot.user.id}")


@bot.command()
async def ping(ctx):
    await ctx.message.channel.send("I'm alive!")


async def send_reminder():
    channel = await bot.fetch_channel(channelID)
    await channel.send(
        embed=Embed().from_dict(
            {
                "fields": [
                    {
                        "name": "Meeting this Friday at 7pm",
                        "value": "React with 👍 to RSVP",
                    }
                    
                ]
            }
        )
    )
    


#Days are 0-6 where mon = 0 sun=6
#strftime returns the 24 hour time in string format
@tasks.loop(minutes=1)
async def weekly_reminder():
    await bot.wait_until_ready()
    today = datetime.now().weekday()
    hour = int(datetime.now().strftime("%H"))
    min = int(datetime.now().strftime("%M"))
    if today == 3 and hour == 12 and min == 1:
        await send_reminder()
        

#Run wtpc-bot, Run!
weekly_reminder.start()
bot.run(token)

