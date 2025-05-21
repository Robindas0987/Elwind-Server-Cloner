import discord
from colorama import Fore, init, Style

init(autoreset=True)  # Ensure color resets after each print


def print_add(message):
    print(f'{Fore.GREEN}[+]{Style.RESET_ALL} {message}')


def print_delete(message):
    print(f'{Fore.RED}[-]{Style.RESET_ALL} {message}')


def print_warning(message):
    print(f'{Fore.YELLOW}[WARNING]{Style.RESET_ALL} {message}')


def print_error(message):
    print(f'{Fore.RED}[ERROR]{Style.RESET_ALL} {message}')


class Clone:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
        for role in guild_to.roles:
            try:
                if role.name != "@everyone":
                    await role.delete()
                    print_delete(f"Deleted Role: {role.name}")
            except discord.Forbidden:
                print_error(f"Permission error deleting role: {role.name}")
            except discord.HTTPException:
                print_error(f"HTTP error deleting role: {role.name}")

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = [r for r in reversed(guild_from.roles) if r.name != "@everyone"]
        for role in roles:
            try:
                await guild_to.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    colour=role.colour,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                print_add(f"Created Role: {role.name}")
            except discord.Forbidden:
                print_error(f"Permission error creating role: {role.name}")
            except discord.HTTPException:
                print_error(f"HTTP error creating role: {role.name}")

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print_delete(f"Deleted Channel: {channel.name}")
            except discord.Forbidden:
                print_error(f"Permission error deleting channel: {channel.name}")
            except discord.HTTPException:
                print_error(f"HTTP error deleting channel: {channel.name}")

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for category in guild_from.categories:
            try:
                overwrites_to = {
                    discord.utils.get(guild_to.roles, name=role.name): perms
                    for role, perms in category.overwrites.items()
                    if discord.utils.get(guild_to.roles, name=role.name)
                }
                new_category = await guild_to.create_category(
                    name=category.name,
                    overwrites=overwrites_to
                )
                await new_category.edit(position=category.position)
                print_add(f"Created Category: {category.name}")
            except discord.Forbidden:
                print_error(f"Permission error creating category: {category.name}")
            except discord.HTTPException:
                print_error(f"HTTP error creating category: {category.name}")

    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
        # Text channels
        for channel in guild_from.text_channels:
            try:
                category = None
                if channel.category:
                    category = discord.utils.get(guild_to.categories, name=channel.category.name)

                overwrites_to = {
                    discord.utils.get(guild_to.roles, name=role.name): perms
                    for role, perms in channel.overwrites.items()
                    if discord.utils.get(guild_to.roles, name=role.name)
                }

                kwargs = {
                    'name': channel.name,
                    'overwrites': overwrites_to,
                    'position': channel.position,
                    'topic': channel.topic,
                    'slowmode_delay': channel.slowmode_delay,
                    'nsfw': channel.nsfw
                }

                new_channel = await guild_to.create_text_channel(**kwargs)
                if category:
                    await new_channel.edit(category=category)
                print_add(f"Created Text Channel: {channel.name}")
            except Exception as e:
                print_error(f"Error creating text channel '{channel.name}': {e}")

        # Voice channels
        for channel in guild_from.voice_channels:
            try:
                category = None
                if channel.category:
                    category = discord.utils.get(guild_to.categories, name=channel.category.name)

                overwrites_to = {
                    discord.utils.get(guild_to.roles, name=role.name): perms
                    for role, perms in channel.overwrites.items()
                    if discord.utils.get(guild_to.roles, name=role.name)
                }

                kwargs = {
                    'name': channel.name,
                    'overwrites': overwrites_to,
                    'position': channel.position,
                    'bitrate': channel.bitrate,
                    'user_limit': channel.user_limit
                }

                new_channel = await guild_to.create_voice_channel(**kwargs)
                if category:
                    await new_channel.edit(category=category)
                print_add(f"Created Voice Channel: {channel.name}")
            except Exception as e:
                print_error(f"Error creating voice channel '{channel.name}': {e}")

    @staticmethod
    async def emojis_delete(guild_to: discord.Guild):
        for emoji in guild_to.emojis:
            try:
                await emoji.delete()
                print_delete(f"Deleted Emoji: {emoji.name}")
            except discord.Forbidden:
                print_error(f"Permission error deleting emoji: {emoji.name}")
            except discord.HTTPException:
                print_error(f"HTTP error deleting emoji: {emoji.name}")

    @staticmethod
    async def emojis_create(guild_to: discord.Guild, guild_from: discord.Guild):
        for emoji in guild_from.emojis:
            try:
                image_data = await emoji.read()  # Correct for modern discord.py
                await guild_to.create_custom_emoji(name=emoji.name, image=image_data)
                print_add(f"Created Emoji: {emoji.name}")
            except discord.Forbidden:
                print_error(f"Permission error creating emoji: {emoji.name}")
            except discord.HTTPException:
                print_error(f"HTTP error creating emoji: {emoji.name}")
            except Exception as e:
                print_error(f"General error creating emoji {emoji.name}: {e}")

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        try:
            icon_data = None
            try:
                icon_data = await guild_from.icon.read()
            except discord.DiscordException:
                print_error(f"Failed to read icon from {guild_from.name}")

            await guild_to.edit(name=guild_from.name)
            if icon_data:
                try:
                    await guild_to.edit(icon=icon_data)
                    print_add(f"Changed Guild Icon: {guild_to.name}")
                except Exception as e:
                    print_error(f"Error setting icon: {e}")
        except discord.Forbidden:
            print_error(f"Permission error editing guild: {guild_to.name}")
