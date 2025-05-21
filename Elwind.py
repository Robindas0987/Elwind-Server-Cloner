from os import system
import psutil
import time
import sys
import platform
import asyncio
import discord
from colorama import Fore, init, Style
from serverclone import Clone

init(autoreset=True)

# Set terminal title
mytitle = "Made by horsewithnoname#6743 | @onurrzy"
if platform.system() == "Windows":
    system(f"title {mytitle}")
    system("cls")
else:
    system("clear")

# Display banner
print(f"""{Fore.WHITE}
███████╗██╗     ██╗    ██╗██╗███╗   ██╗██████╗ 
██╔════╝██║     ██║    ██║██║████╗  ██║██╔══██╗
█████╗  ██║     ██║ █╗ ██║██║██╔██╗ ██║██║  ██║
██╔══╝  ██║     ██║███╗██║██║██║╚██╗██║██║  ██║
███████╗███████╗╚███╔███╔╝██║██║ ╚████║██████╔╝
╚══════╝╚══════╝ ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═════╝ 
{Style.RESET_ALL}              
""")

# Input
guild_from_id = input('\n[>] Server to Copy (Source Guild ID): ')
guild_to_id = input('\n[>] Target Server (Your Guild ID): ')
token = input('\n[>] Bot Token: ').strip()

# Discord client
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{Fore.GREEN}[+] Logged in as: {client.user} ({client.user.id}){Style.RESET_ALL}")
    guild_from = client.get_guild(int(guild_from_id))
    guild_to = client.get_guild(int(guild_to_id))

    if not guild_from or not guild_to:
        print(f"{Fore.RED}[ERROR] Could not find one or both guilds. Make sure the bot is in both servers.{Style.RESET_ALL}")
        await client.close()
        return

    print(f"{Fore.YELLOW}[!] Starting server cloning process...{Style.RESET_ALL}")

    await Clone.guild_edit(guild_to, guild_from)
    await Clone.roles_delete(guild_to)
    await Clone.channels_delete(guild_to)
    await Clone.roles_create(guild_to, guild_from)
    await Clone.categories_create(guild_to, guild_from)
    await Clone.channels_create(guild_to, guild_from)

    print(f"""{Fore.GREEN}
███████╗██╗███╗   ██╗██╗███████╗██╗  ██╗    ██╗  ██╗██████╗ 
██╔════╝██║████╗  ██║██║██╔════╝██║  ██║    ╚██╗██╔╝██╔══██╗
█████╗  ██║██╔██╗ ██║██║███████╗███████║     ╚███╔╝ ██║  ██║
██╔══╝  ██║██║╚██╗██║██║╚════██║██╔══██║     ██╔██╗ ██║  ██║
██║     ██║██║ ╚████║██║███████║██║  ██║    ██╔╝ ██╗██████╔╝
╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═════╝ 
{Style.RESET_ALL}
    """)
    await asyncio.sleep(5)
    await client.close()

client.run(token)
