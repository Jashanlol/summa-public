import discord

from discord.ext import commands

from cogs.utils.paginator import PaginatedHelpCommand


class Meta(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.old_help_command = bot.help_command
        bot.help_command = PaginatedHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self.old_help_command

    @commands.command()
    async def invite(self, ctx):
        """Invite the bot to your server.

        You must have Manage Server permissions in the
        server you wish to invite the bot.
        """
        perms = discord.Permissions.none()
        perms.add_reactions = True
        perms.send_messages = True
        perms.embed_links = True
        perms.external_emojis = True
        perms.attach_files = True
        perms.read_messages = True
        perms.read_message_history = True

        await ctx.send(f"<{discord.utils.oauth_url(self.bot.user.id, perms)}>")

    @commands.command()
    async def uptime(self, ctx):
        """Tells you how long the bot has been up for."""
        await ctx.send(self.bot.uptime())


def setup(bot):
    bot.add_cog(Meta(bot))