import sys
import traceback

from discord.ext import commands


class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            clean_content = await commands.clean_content().convert(ctx, str(error))
            await ctx.send(clean_content)

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(error)

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(error)

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(error)

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"```\n{ctx.prefix}{ctx.command.name} {ctx.command.signature}\n\n"
                           f"{str(error.param).split(':')[0]} is a required argument that is missing.```")

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)

            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
