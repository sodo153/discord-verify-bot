import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.reactions = True
intents.members = True  # Needed to assign roles

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.environ["TOKEN"]
GUILD_ID = int(os.environ["GUILD_ID"])
VERIFY_CHANNEL_ID = int(os.environ["VERIFY_CHANNEL_ID"])
ROLE_ID = int(os.environ["ROLE_ID"])

verify_message_id = None

@bot.event
async def on_ready():
    global verify_message_id
    print(f"Logged in as {bot.user}")

    guild = bot.get_guild(GUILD_ID)
    channel = guild.get_channel(VERIFY_CHANNEL_ID)

    # Check if message already exists
    async for message in channel.history(limit=50):
        if message.author == bot.user and "תסמנו וי" in message.content:
            verify_message_id = message.id
            print("✅ Verify message already exists.")
            break

    # If not, send it
    if verify_message_id is None:
        msg = await channel.send("תסמנו וי בשביל לקבל רול מאומת")
        await msg.add_reaction("✅")
        verify_message_id = msg.id
        print("✅ Verify message sent and reaction added.")

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != verify_message_id:
        return
    if str(payload.emoji) != "✅":
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    role = guild.get_role(ROLE_ID)
    if role not in member.roles:
        await member.add_roles(role)
        print(f"✅ Gave role to {member.name}")

@bot.event
async def on_raw_reaction_remove(payload):
    if payload.message_id != verify_message_id:
        return
    if str(payload.emoji) != "✅":
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    role = guild.get_role(ROLE_ID)
    if role in member.roles:
        await member.remove_roles(role)
        print(f"❌ Removed role from {member.name}")

bot.run(TOKEN)
