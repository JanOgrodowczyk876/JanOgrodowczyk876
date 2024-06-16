#imports all modules
import discord
from discord.ext import commands
from random import randint
import aiohttp
import os
import datetime
import sys


#sets basic settings
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)
version = "pre-alpha"

@bot.command(name="shutdown")
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("@everyone ⚠️Warning: Shutting down...")
    await bot.close()
    sys.exit(0)

@shutdown.error
async def owner_only_error(cxt, error):
    if isinstance(error, commands.NotOwner):
        await cxt.send(f"🚫Error: Access denied.")

@bot.event
async def on_ready():
    print(f"Bot: {bot.user} is Online")
    
@bot.command(name="ping")
async def when_pinged(ctx):
    try:
        latency = bot.latency
        await ctx.send(f"Pong! Latency: {latency:.4f} s")
    except Exception as e:
        await ctx.send(f"⚠️An error occurred: {str(e)}")

@bot.command(name='clear')
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    try:
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'Deleted {amount} messages.', delete_after=5)
    except Exception as e:
        await ctx.send(f"⚠️An error occurred: {str(e)}")

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("⚠️Error: You do not have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify the number of messages to delete.")
    else:
        await ctx.send(f"⚠️An error occurred: {str(error)}")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    try:
        await member.kick(reason=reason)
        await ctx.send(f'Member {member.mention} was kicked. Reason: {reason}')
    except Exception as e:
        await ctx.send(f"⚠️An error occurred: {str(e)}")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("⚠️Error: You do not have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify a member to kick.")
    else:
        await ctx.send(f"⚠️An error occurred: {str(error)}")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    try:
        await member.ban(reason=reason)
        await ctx.send(f'Member {member.mention} was banned. Reason: {reason}')
    except Exception as e:
        await ctx.send("⚠️An error occurred: {str(e)}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("⚠️Error: You do not have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify a member to ban.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")

@bot.command(name="mute")
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    try:
        # Check if the "Muted" role already exists
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        # If the "Muted" role does not exist, create it
        if not muted_role:
            muted_role = await ctx.guild.create_role(name="Muted")
            
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False, read_message_history=True, read_messages=True)

        # Assign the "Muted" role to the user
        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"User {member.mention} has been muted for: {reason}")
    except Exception as e:
        await ctx.send(f"⚠️An error occurred: {str(e)}")

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("⚠️Error: You do not have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please specify a member to mute.")
    else:
        await ctx.send(f"⚠️An error occurred: {str(error)}")
        
@bot.command(name="unmute")
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member: discord.Member):
    try:
        # Check if the "Muted" role exists
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if muted_role:
            # Remove the "Muted" role from the member
            await member.remove_roles(muted_role)
            await ctx.send(f"User {member.mention} has been unmuted.")
        else:
            await ctx.send("⚠️Error: The 'Muted' role does not exist.")
    except Exception as e:
        await ctx.send(f"⚠️An error occurred: {str(e)}")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(channel.guild.text_channels)  # Znajdź kanał tekstowy o nazwie 'general'
    if channel:
        await channel.send(f'{member.mention} finnaly got here! Remember to say Hi!')

@bot.command(name="Help")
async def help_command(ctx):
    help_message = """
    **List of commands:**
    - `?mute <User> [reason]`: Mute the member with entered reason.
    - `?ping`: pings the bot.
    - `?kick <Member> [reason]`: Kick the member with entered reason. (Admins only)
    - `?ban <Member> [reason]`: Bans the member with entered reason. (Admins only)
    - `?clear`: Removes number of messages entered to the command. (Admins only)
    - `?serverinfo`: Displays information about the server.
    - `?userinfo <Member>`: Displays information about a user.
    - `?say <message>`: The bot repeats whatever message you provide.
    - `?meme`: Fetches a random meme from the internet.
    - `?weather <city>`: Provides the current weather for a specified location.
    -  `?shutdown: Shutdown the bot (Owner only).
    """
    try:
        await ctx.author.send(help_message)
        await ctx.send(f"{ctx.author.mention}, I sent you a private message with all avaitable commands.")
    except discord.Forbidden:
        await ctx.send(f"⚠️Error: Can't send the message to: {ctx.author.mention}")

@bot.command(name="roll")
async def roll(ctx):
    number = randint(0, 10)
    await ctx.send(f"{number}")

@bot.command(name="serverinfo")
async def serverinfo(ctx):
    server = ctx.guild
    number_of_channels = len(server.channels)
    number_of_members = server.member_count
    server_name = server.name

    embed = discord.Embed(title=f"Server info for {server_name}", description="", color=discord.Color.blue())
    embed.add_field(name="Number of channels", value=number_of_channels, inline=False)
    embed.add_field(name="Number of members", value=number_of_members, inline=False)

    await ctx.author.send(embed=embed)

@bot.command(name="userinfo")
async def userinfo(ctx, member: discord.Member):
    embed = discord.Embed(title=f"User info for {member.name}", description="", color=discord.Color.green())
    embed.add_field(name="ID", value=member.id, inline=False)
    embed.add_field(name="Name", value=member.display_name, inline=False)
    embed.add_field(name="Status", value=member.web_status, inline=False)
    embed.add_field(name="Top role", value=member.top_role, inline=False)
    embed.add_field(name="Joined at", value=member.joined_at, inline=False)

    await ctx.author.send(embed=embed)

@bot.command(name="say")
async def say(ctx, *, message):
    await ctx.send(message)

@bot.command(name="meme")
async def meme(ctx):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.reddit.com/r/memes/random/.json") as response:
                if response.status == 200:
                    data = await response.json()
                    post = data[0]['data']['children'][0]['data']
                    meme_url = post['url']
                    title = post['title']
                    await ctx.send(f"**{title}**\n{meme_url}")
                else:
                    await ctx.send("Could not fetch a meme at this time. Please try again later.")
    except Exception as e:
        await ctx.send(f"⚠️An error occurred: {str(e)}")
        
@bot.command(name="setstatus")
@commands.is_owner()
async def setstatus(ctx, status: str):
    try:
        status = status.lower()
        if status == 'online':
            await bot.change_presence(status=discord.Status.online)
        elif status == 'offline':
            await bot.change_presence(status=discord.Status.offline)
        elif status == 'dnd':
            await bot.change_presence(status=discord.Status.dnd)
        elif status == 'brb':
            await bot.change_presence(status=discord.Status.idle)
        else:
            await ctx.send("""*Please choose a status from here*:
            - `online`
            - `offline`
            - `dnd`
            - `brb`""")
            return
        await ctx.send(f"Status was successfully set to: {status}")
    except Exception as e:
        await ctx.send(f"⚠️An error occurred: {str(e)}")

@bot.command(name="botinfo")
async def botinfo(ctx):
    try:
        embed = discord.Embed(title="Bot Information", color=discord.Color.purple())
        embed.add_field(name="Name", value=bot.user.name, inline=True)
        embed.add_field(name="ID", value=bot.user.id, inline=True)
        embed.add_field(name="Servers", value=f"{len(bot.guilds)}", inline=True)
        embed.add_field(name="Version", value=f"{version}")
        embed.set_thumbnail(url=bot.user.avatar.url)

        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"⚠️An error occurred: {str(e)}")

@setstatus.error
async def setstatus_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("⚠️Error: You do not have permission to use this command.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("""*Please choose a status from here*:
        - `online`
        - `offline`
        - `dnd`
        - `brb`""")
    else:
        await ctx.send("🚫Error: Access denied.")

@bot.command(name="weather")
async def weather(ctx, *, city: str):
    api_key = 'e81425a50f9ccc087a5d5b271f38dc35'
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url) as r:
            if r.status == 200:
                data = await r.json()
                weather_description = data['weather'][0]['description']
                temp = data['main']['temp']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']

                embed = discord.Embed(title=f"Weather in {city}", description="", color=discord.Color.green())
                embed.add_field(name="Description", value=weather_description, inline=False)
                embed.add_field(name="Temperature", value=f"{temp}°C", inline=False)
                embed.add_field(name="Feels like", value=f"{feels_like}°C", inline=False)
                embed.add_field(name="Humidity", value=f"{humidity}%", inline=False)

                await ctx.send(embed=embed)
            else:
                await ctx.send(f"⚠️Error: Could not retrieve weather data for {city}")

@bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='general')
    if channel:
        await channel.send(f'{member.mention} finally got here! Remember to say Hi!')


bot.run("<YOUR-DISCORD-TOKEN")
