# imports
from cogs.summacog import *
from cogs.utils.cccutil import *

class Catechism(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ccc(self, ctx, *, search:str):
        """
        Searches the Catechism of the Catholic Church by paragraph.
        """

        tsearch = []
        try:
            isearch = int(search)
        except ValueError:
            my_reg = re.search(r"([0-9]{1,4})-([0-9]{1,4})", search)
            try:
                for i in my_reg.groups():
                    tsearch.append(int(i))
            except AttributeError:
                await ctx.send("Invalid query.")
                return

        if len(tsearch) < 2:
            url = ccc_get_url(search)
            soup = await Summa(self.bot).simple_get_url(url)

            result = soup.find('td', {"class": 'text'})
            try:
                p = ' '.join((result.text.split())[1:])
                t = f"*Catechism of the Catholic Church*, Paragraph {search}"
                e = discord.Embed(title=t, description=p, colour=discord.Color(0x36393E))
                await ctx.send(embed=e)
            except AttributeError:
                await ctx.send("Invalid paragraph.")
        else:
            # error checking
            if tsearch[0] > tsearch[1]:
                await ctx.send("Invalid query.")
                return
            if tsearch[1] - tsearch[0] > 20:
                await ctx.send("Query is too long.")
                return
            
            # initialize
            paragraphs = []
            
            for i in range(tsearch[0], tsearch[1] + 1):
                url = ccc_get_url(i)
                soup = await Summa(self.bot).simple_get_url(url)

                result = soup.find('td', {"class": 'text'})
                try:
                    p = ' '.join((result.text.split())[1:])
                    paragraphs.append(p)
                except AttributeError:
                    await ctx.send("Invalid paragraph.")
                    return

            t = f"*Catechism of the Catholic Church*, Paragraphs {search}"
            pages = Pages(ctx, entries=paragraphs, per_page=1, title=t)
            await pages.paginate()

            


def setup(bot):
    bot.add_cog(Catechism(bot))
