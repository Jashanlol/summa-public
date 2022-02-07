import asyncio

import discord
from discord.ext import commands


class Context(commands.Context):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def session(self):
        return self.bot.session

    @property
    def db(self):
        return self.bot.db

    async def prompt(self, message, *, timeout=60.0, delete_after=True, author_id=None):

        if not self.channel.permissions_for(self.me).add_reactions:
            raise RuntimeError('Bot does not have Add Reactions permission.')

        reactions = ["<:tickGreen:560141334367698989>", "<:tickRed:560141344694075423>"]

        fmt = f'{message}\n\nReact with {reactions[0]} to confirm or {reactions[1]} to deny.'

        author_id = author_id or self.author.id
        msg = await self.send(fmt)

        confirm = None

        def check(payload):
            nonlocal confirm

            if payload.message_id != msg.id or payload.user_id != author_id:
                return False

            codepoint = str(payload.emoji)

            if codepoint == reactions[0]:
                confirm = True
                return True
            elif codepoint == reactions[1]:
                confirm = False
                return True

            return False

        for emoji in reactions:
            await msg.add_reaction(emoji[1:-1])

        try:
            await self.bot.wait_for('raw_reaction_add', check=check, timeout=timeout)
        except asyncio.TimeoutError:
            confirm = False

        try:
            if delete_after:
                await msg.delete()
        finally:
            return confirm

    def tick(self, opt, label=None):
        emoji = "<:tickGreen:560141334367698989>" if opt else "<:tickRed:560141344694075423>"
        if label:
            return f"{emoji}: {label}"
        return emoji

    async def kwargs_embed(self, title=None, description=None, author=None, footer=None, timestamp=None,
                           thumbnail=None, image=None, author_url=None, footer_url=None, **kwargs):

        e = discord.Embed(title=title, description=description, color=0x36393E)

        for key in kwargs.keys():
            e.add_field(name=key.replace("_", " "), value=kwargs[key])

        if author and author_url:
            e.set_author(name=author, icon_url=author_url)
        else:
            e.set_author(name=author) if author else ""

        if thumbnail:
            e.set_thumbnail(url=thumbnail)

        if image:
            e.set_image(url=image)

        if timestamp:
            e.timestamp = timestamp

        if footer and footer_url:
            e.set_footer(text=footer, icon_url=footer_url)
        else:
            e.set_footer(text=footer) if footer else ""

        await Context.send(self, embed=e)

    async def show_help(self, command=None):
        cmd = self.bot.get_command('help')
        command = command or self.command.qualified_name
        await self.invoke(cmd, command=command)
