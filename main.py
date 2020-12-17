import json
import discord
from discord.ext import commands
from vote import Vote
from time import sleep

with open('secrets.json') as file:
    data = json.load(file)

TOKEN = data['bot_token']

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)
# bot = commands.Bot(command_prefix='!')
vote = Vote(None, None)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name='mutenicko')
async def mutenicko(ctx):
    response = "mute nicko :^)"
    await ctx.send(response)


@bot.command(name='mute')
# @commands.has_permissions(mute_members=True)
async def mute_user(ctx, user: discord.Member):
    await user.edit(mute=True)

    response = f"User {user.display_name} has been muted."
    await ctx.send(response)


def get_voters(guild):
    vchannel = discord.utils.get(guild.voice_channels, name="General", type=discord.ChannelType.voice)

    voters = []
    for member in vchannel.members:
        # only want undeafened and unmuted users
        vs = member.voice  # member voice state
        if not vs.deaf and not vs.mute and not vs.self_mute and not vs.self_deaf:
            voters.append(member)

    return voters


@bot.command(name='votemute')
async def vote_mute_user(ctx, user: discord.Member):
    # check if there is already a vote in progress
    global vote
    if vote.active:
        response = f"Sorry {ctx.message.author.mention}, a vote is already in progress."
    else:
        voters = get_voters(ctx.guild)
        vote = Vote(voters, user)
        vote.activate()  # start vote
        response = f"{ctx.message.author.nick} has started a vote to server mute {user.display_name}. The current " \
                   f"voters are:\n"

        response += "\n".join(v.display_name for v in voters)
    await ctx.send(response)


@bot.command(name='yes')
async def confirm_mute(ctx):
    if not vote.active:
        response = f"There is no vote in progress, {ctx.message.author.mention}"
        await ctx.send(response)
    else:
        response = vote.confirm(ctx.message.author)
        await ctx.send(response)

        # check if vote is done
        if vote.is_majority():
            response = f"It is decided! {vote.mutee.mention} shall be muted!"
            await ctx.send(response)

            await vote.mutee.edit(mute=True)


bot.run(TOKEN)
