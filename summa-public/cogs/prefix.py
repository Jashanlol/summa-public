import os

import discord
from discord.ext import commands

from .utils.dataIO import dataIO


class _Prefix(commands.Converter):
    async def convert(self, ctx, argument):
        if argument in ["<@554530480117252125>", "<@!554530480117252125>"]:
            raise commands.BadArgument("That is a reserved prefix already in use.")

        if str(ctx.guild.id) not in dataIO.load_json("data/prefixes.json"):
            return argument

        if len(argument) > 20:
            raise commands.BadArgument(f"Prefix length too large ({len(argument)}/20)")

        return argument


class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefixes = dataIO.load_json("data/prefixes.json")

    def cog_check(self, ctx):
        return ctx.guild is not None

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx):
        """Shows the server's prefix list."""
        if str(ctx.guild.id) not in self.prefixes:
            _list = [f"<@{ctx.me.id}>", "?"]
        else:
            _list = [f"<@{ctx.me.id}>"]
            [_list.append(p) for p in sorted(self.prefixes[str(ctx.guild.id)])]

        enumerated_list = [f"{a}. {b}" for a, b in enumerate(_list, 1)]

        e = discord.Embed(title="Prefixes", description='\n'.join(enumerated_list), color=discord.Color(0x36393E))
        e.set_footer(text=f"{len(_list)} prefixes")
        await ctx.send(embed=e)

    @prefix.command()
    async def add(self, ctx, prefix: _Prefix):
        """Appends a prefix to the list of custom prefixes.

        Previously set prefixes are not overridden.

        To have a word prefix, you should quote it and end it with
        a space, e.g. "hello " to set the prefix to "hello ". This
        is because Discord removes spaces when sending messages so
        the spaces are not preserved.

        Multi-word prefixes must be quoted also.

        You must have Manage Server permission to use this command."""
        if str(ctx.guild.id) in self.prefixes and prefix in self.prefixes[str(ctx.guild.id)]:
            raise commands.BadArgument("Prefix is already in use.")

        if str(ctx.guild.id) in self.prefixes:
            self.prefixes[str(ctx.guild.id)].append(prefix)
        else:
            self.prefixes[str(ctx.guild.id)] = [prefix, "?"]

        dataIO.save_json("data/prefixes.json", self.prefixes)
        self.bot.prefixes = self.prefixes
        await ctx.send(ctx.tick(True))

    @prefix.command()
    async def remove(self, ctx, prefix: _Prefix):
        """Removes a prefix from the list of custom prefixes.

        This is the inverse of the 'prefix add' command. You can
        use this to remove prefixes from the default set as well.

        You must have Manage Server permission to use this command."""
        if str(ctx.guild.id) not in self.prefixes or prefix not in self.prefixes[str(ctx.guild.id)]:
            return await ctx.send("Error removing prefix...Make sure 1) you had one in the first place 2) "
                                  "the validity of the prefix.")

        else:
            self.prefixes[str(ctx.guild.id)].remove(prefix)
            if len(self.prefixes[str(ctx.guild.id)]) == 0 or self.prefixes[str(ctx.guild.id)] == ["?"]:
                self.prefixes.pop(str(ctx.guild.id))

        dataIO.save_json("data/prefixes.json", self.prefixes)
        self.bot.prefixes = self.prefixes
        await ctx.send(ctx.tick(True))

    @prefix.command()
    async def reset(self, ctx):
        """Removes all custom prefixes.

        After this, the bot will listen to only mention prefixes
        and the default prefix.

        You must have Manage Server permission to use this command.
        """
        self.prefixes.pop(str(ctx.guild.id))

        dataIO.save_json("data/prefixes.json", self.prefixes)
        self.bot.prefixes = self.prefixes
        await ctx.send(ctx.tick(True))


def check_files():
    if not os.path.exists("data/prefixes.json"):
        print("Creating prefixes json!")
        dataIO.save_json("data/prefixes.json", {})


def setup(bot):
    check_files()
    bot.add_cog(Prefix(bot))
