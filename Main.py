import discord
from discord.ext import commands
import os
from os import system
import asyncio
from keep_alive import keep_alive

client = commands.Bot(command_prefix = '+')


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def standings(ctx):
  await ctx.send('check <#1007035608675401748> to see the standings')

@client.command()
@commands.has_permissions(ban_members=True)
async def bam(ctx, user: discord.User):
  await ctx.send(f'i have bammed {user.mention}.')


@client.command()
async def pingowners(ctx):
  await ctx.send('bro. Did you ask me to ruin the owners day by pinging them?')


@client.command()
@commands.has_permissions(manage_roles=True)
async def userinfo(ctx, user: discord.User):
  await ctx.send(f'{user.mention} was created at {user.created_at}. Their ID is {user.id} and their discriminator is {user.discriminator}')

@client.command()
@commands.has_permissions(manage_roles=True)
async def roleinfo(ctx, role: discord.Role):
  await ctx.send(f'{role} is this colour {role.colour} *look it up on hex colour codes*. It is currently {role.position} on the role list (the higher the number, the higher on the list)')

@client.command()
async def ping(ctx):
  await ctx.send(f':ping_pong: pong! My latency is {round(client.latency * 1000)}ms. GIVE ME BETTER RESPONSE TIME')


@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, user: discord.User, *, reason):
    await user.ban(reason=reason)
    await ctx.send(f'sucessfully banned {user.mention}')

@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, user: discord.User, *, reason):
    await user.kick(reason=reason)
    await ctx.send(f'successfully kicked {user.mention}')

@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, user: discord.User):
    banned_users = await ctx.guild.bans()
    user_name, user_discriminator = user.split('#')
    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (user_name, user_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'successfully unbanned {user}')

sent_users = []


@client.command()
async def matti(ctx):
  await ctx.send('what are the chances that tommys gran is faster than matti?')

@client.command()
async def invite(ctx):

    await ctx.send('bro i cant be invited to anyones server')

keep_alive()
try:
    client.run(os.getenv('TOKEN'))
except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    system("python restarter.py")
    system('kill 1')
