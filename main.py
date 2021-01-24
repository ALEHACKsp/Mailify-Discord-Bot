import discord 
import asyncio
import requests
import smtplib
from discord.ext import commands
from threading import Thread

class Mailify:

    async def Send(target, message):
        count = 0
        with open('Storage/Accounts.txt', 'r', encoding='UTF-8') as f:
            for line in f:
                count += 1
                combo = line.replace('\n', '')
                username = combo.split(':')[0]
                password = combo.split(':')[1]
                Thread(target=Mailify.Mail, args=(username, password, target, message,)).start()
        return count

    def Mail(username, password, target, message):
        _smpt = smtplib.SMTP('smtp.gmail.com', 587)
        _smpt.starttls()
        try:
            _smpt.login(username, password)
            _smpt.sendmail(username, target, message)
            return True
        except:
            return False

client = discord.Client()
client = commands.Bot (command_prefix='m!')
client.remove_command('help')

@client.event
async def on_ready():
    print(discord.__version__)
    print('logged in as')
    print(client.user.name)

@client.command()
async def spam(ctx, target = None, message = None):
    if target or message == None:
        await ctx.send("Invalid Arguments...")

    await ctx.send(f"Sending Emails To {target}... Please Wait!")
    send = await Mailify.Send(target, message)
    await ctx.send(f"Sent {send} Mails To {target}!")

client.run('Token Here')