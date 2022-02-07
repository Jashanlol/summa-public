import copy
import datetime
import difflib
import os
import discord
import traceback

import aiohttp
from discord.ext import commands
from cogs.utils.dataIO import dataIO

from cogs.utils import context
from safety import TOKEN

intents = discord.Intents.all()


def _prefix(bot, msg):
    user_id = bot.user.id
    base = [f'<@!{user_id}> ', f'<@{user_id}> ']
    default = ['test ']
    if msg.guild is None:
        base.extend(default)
    else:
        base.extend(bot.prefixes.get(str(msg.guild.id), default))
    return base


initial_extensions = []
for i in os.listdir('cogs'):
    if '.py' in i:
        i = i.split('.py', 1)[0]
        initial_extensions.append(f'cogs.{i}')


class BotClient(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(description="Summa Bot", command_prefix=_prefix, intents=intents)

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
                print(f'Loaded extension {extension}')
            except Exception as e:
                print(f'{e.__class__.__name__}: {e}')
                traceback.print_exc()

        self.prefixes = dataIO.load_json("data/prefixes.json")
        self._commands = 0
        self.owners = None

    def timenow(self, utc=True, sqlTs=False):
        ts = datetime.datetime.now()
        if utc:
            ts = datetime.datetime.utcnow()
        if sqlTs:
            f = '%Y-%m-%d %H:%M:%S'
            ts = ts.strftime(f)
        return (ts)

    def uptime(self):
        delta = bot.timenow(utc=True) - bot.uptime_
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        values = [f'{days}d', f'{hours}h', f'{minutes}m', f'{seconds}s']
        return ', '.join(v for v in values if str(v)[0] != '0')

    async def on_ready(self):
        if not hasattr(self, 'uptime_'):
            self.uptime_ = datetime.datetime.utcnow()

        print(f'Ready: {self.user} (ID: {self.user.id})')
        self.owners = [m.id for m in (await self.application_info()).team.members]

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=context.Context)

        if ctx.command is None:

            if ctx.prefix is None:
                return

            woprefix = message.content.split(ctx.prefix)
            typo = woprefix[1].split(" ")[0]

            bot_cmds = [command.name for command in bot.commands]

            try:
                match = difflib.get_close_matches(typo, bot_cmds, cutoff=0.8)[0]
            except IndexError:
                return

            msg = copy.copy(ctx.message)
            content = message.content.replace(typo, match)
            prompt = await ctx.prompt(f"Seems like there was an error in calling a command? Did you mean `{content}`")

            if not prompt:
                return

            msg.content = content
            new_ctx = await self.get_context(msg, cls=context.Context)
            await self.invoke(new_ctx)

        else:
            await self.invoke(ctx)

        self._commands += 1

    async def on_message(self, message):
        if message.author.bot:
            return

        await self.process_commands(message)

    async def close(self):
        await super().close()

    def run(self):
        super().run(TOKEN, reconnect=True)


bot = BotClient()
bot.session = aiohttp.ClientSession(loop=bot.loop)
bot.run()
