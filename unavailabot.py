import discord
from discord.ext import commands
"""This is a one-shot bot for tracking when bots (or people) go offline.
    Currently it's designed for 2 people for 1 server, but is easily extendible, and might be updated.
    Feel free to suggest changes.
"""

token = "1234321puttokenhere9876789"
log_channel = 'fix-the-bot'         # name of the channel you want it to ping in
person_one = 123456789876543210     # ID of the first person to ping
bot_one = 311283840516274809        # ID of the first bot to watch
person_two = 311283840516274809     # ID of the second person to ping
bot_two = 918273645463728190        # ID of the second bot to watch

bot = commands.Bot(
    command_prefix='off',
    description='Watching for offline bois.'
)

# console write when bot starts
@bot.event
async def on_ready():
    print(
        f'\n\nLogged in: {bot.user.name} ID: {bot.user.id}\nVersion: {discord.__version__}\n'
    )

    await bot.change_presence(
        activity=discord.Activity(
            name='the little green dot',
            type=3
        )
    )


@bot.event
async def on_member_update(before, after):
    channel = discord.utils.get(  # find the channel
        before.guild.channels,
        name=log_channel
    )

    if str(after.status) == "offline":
        # check if the user is the bot you're watching, then message related person
        if before.id == bot_one:
            await channel.send(f"<@{person_one}>, {after.name} has gone {after.status}.")
        elif before.id == bot_two:
            await channel.send(f"<@{person_two}>, {after.name} has gone {after.status}.")


# check ping
@bot.command()
async def ping(ctx):
    """checks the latency to Discord."""
    e = discord.Embed(
        color=discord.Color.green(),
        title="Pong!",
        description=f'{round(bot.latency * 1000, 2)} ms'
    )
    await ctx.send(embed=e)


@bot.command(name='logout')
@commands.is_owner()
async def log_out(ctx):
    """closes down the bot and goes offline."""
    print('Logging out...')
    await bot.logout()


bot.run(token, bot=True, reconnect=True)
