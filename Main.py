import discord
from discord.ext import commands
from discord.ext import tasks
import json
import os
import random
import asyncio
import datetime
import random

client = commands.Bot(command_prefix = '+')
bot = client

@client.event
async def on_ready():
        await client.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f'people use +help'))
        print('We have logged in as {0.user}'.format(client))

@client.command()
async def standings(ctx):
  await ctx.send('check <#1007035608675401748> to see the standings')

@client.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount : int):
  await ctx.channel.purge(limit=amount + 1)
  await ctx.send(f'cleared {amount} messages!')

@client.command()
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, user: discord.User, nick):
  await user.edit(nick=nick)
  await ctx.send(f"i have changed {user}'s nickname")

@client.command()
@commands.has_permissions(manage_messages=True)
async def poll(ctx, *, question):
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"{question}: \n✅ = Yes**\n**❎ = No")
    await message.add_reaction('✅')
    await message.add_reaction('❎')

@client.event
async def on_command_error(ctx,error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send('please use a command that exists')

@client.event
async def on_guild_channel_create(channel):
  await channel.send(f'Welcome to this brand new channel called {channel.name}')

@client.command()
async def repeat(ctx, *, message):
  await ctx.send(f'you said {message}')

@purge.error
async def clear_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send('please specify the amount of messages you want me to delete')


@client.command()
async def timer(ctx, days, hours, minutes, seconds):
    try:
        hoursint = int(hours)
        daysint = int(days)
        minutesint = int(minutes)
        secondint = int(seconds)
        if daysint < 0:
            await ctx.send("I dont think im allowed to do negatives")
            raise BaseException
        elif hoursint < 0:
            await ctx.send("I dont think im allowed to do negatives")
            raise BaseException
        elif minutesint < 0:
            await ctx.send("I dont think im allowed to do negatives")
            raise BaseException
        elif secondint < 0:
            await ctx.send("I dont think im allowed to do negatives")
            raise BaseException
        elif secondint <= 0 and hoursint <= 0 and daysint <= 0 and minutesint <= 0:
            await ctx.send("That's not a time dummy!")
            raise BaseException
        if secondint >= 60:
            secondint = secondint - 60
            minutesint += 1
        if minutesint >= 60:
            minutesint = minutesint - 60
            hoursint +=1
        if hoursint >= 24:
            hoursint = hoursint - 24
            daysint += 1
        message = await ctx.send("Timer: {seconds}")
        if daysint > 0 and hoursint == 0:
            hoursint = 23
            daysint -= 1
            minutesint = 60
            secondint = 60
        if hoursint > 0 and minutesint == 0:
            minutesint = 60
            secondint = 60
            hoursint -= 1
        if secondint == 0 and minutesint > 0:
            secondint = 60
            minutesint -= 1
        while True:
            if secondint > 0:
                secondint -= 1
            if secondint <= 0 and minutesint > 0:
                minutesint -=1
                secondint = 60
                if minutesint <= 0 and hoursint > 0:
                    hoursint -= 1
                    minutesint = 60
                    if hoursint <= 0 and daysint > 0:
                        daysint -= 1
                        hoursint = 24
            if secondint == 0 and minutesint == 0 and hoursint == 0 and daysint == 0:
                await message.edit(content="Ended!")
                break
            await message.edit(content=f"**Timer: {daysint}:{hoursint}:{minutesint}:{secondint}**")
            await asyncio.sleep(1)
        await ctx.send(f"{ctx.author.mention} Your countdown Has ended!")
    except ValueError:
        await ctx.send("Must be a number!")

@client.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode in this channel to {seconds} seconds!")

@client.command()
async def staff(ctx):
  await ctx.send('I see you want to see the staff. You can find our full staff list here <#1030554712212258896>')

@client.command()
@commands.has_permissions(manage_nicknames=True)
async def warn(ctx,user: discord.User,*,reason):
    await ctx.send(f"Succesfully warned {user.name} with reason {reason}")
    await user.send(f"You were warned in Electric Racing Society with reason {reason}")

@client.command()
@commands.has_permissions(manage_nicknames=True)
async def bam(ctx, user: discord.User, *, reason):
  await ctx.send(f'i have bammed {user} with reason {reason}.')

@client.command()
@commands.has_permissions(manage_roles=True)
async def userinfo(ctx, user: discord.User):
  await ctx.send(f'{user.mention} was created at {user.created_at}. Their ID is {user.id} and their discriminator is {user.discriminator}.')

@client.command()
@commands.has_permissions(manage_roles=True)
async def roleinfo(ctx, role: discord.Role):
  await ctx.send(f'{role} is this colour {role.colour} *look it up on hex colour codes*. It is currently {role.position} on the role list (the higher the number, the higher on the list)')

@client.command()
async def ping(ctx):
  await ctx.send(f':ping_pong: pong! My latency is {round(client.latency * 1000)}ms. GIVE ME BETTER RESPONSE TIME')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.User, *, reason):
    await user.ban(reason=reason)
    await ctx.send(f'sucessfully banned {user.mention} with reason {reason}')
    await user.send(f'you have been banned with reason {reason}')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.User, *, reason):
    await user.kick(reason=reason)
    await ctx.send(f'successfully kicked {user.mention} with reason {reason}')
    await user.send(f'you have been kicked with reason {reason}')

@client.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, user: discord.User, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f'added {role} to {user}')
    await user.send(f'you have been given the role {role}')

@client.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, user: discord.User, role: discord.Role):
    await user.remove_roles(role) 
    await ctx.send(f"{role} has been removed from {user}.")
    await user.send(f'you have been removed from the role {role}')

@client.command()
async def matti(ctx):
  await ctx.send('what are the chances that tommys gran is faster than matti?')

@client.command()
async def invite(ctx):
  await ctx.send('i cant be invited to anyones server but all of my code is open source! you can find it here: https://github.com/IdnigoFire/ERS-Bot-source-code')

client.run('TOKEN GOES HERE')
