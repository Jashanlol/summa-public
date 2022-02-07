# imports
from cogs.summacog import *


class SCG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def scg(self, ctx, *, search:str):
        """
        Searches the Summa Contra Gentiles for an article. The search should be in the format pXqY (e.g. p1q13).
        """

        # parse query
        my_reg = re.findall(r"[p|q]\d{1,3}", search)

        # get the part and question
        p, q = None, None
        try:
            p = int(my_reg[0][1:])
            q = int(my_reg[1][1:])
        except IndexError:
            await ctx.send(f"Invalid search provided. Use the format `{ctx.prefix}{ctx.command.name}p#q#`")

        # account for the split in part 3
        if p == 3:
            if q >= 84:
                p = "3b"
            else:
                p = "3a"

        url = "cogs/utils/SCGfiles/scg" + str(p) + ".html"
        foo = open(url, 'rb')
        soup = BeautifulSoup(foo.read(), 'html.parser')

        try:
            result = soup.find('a', {"id": q}).text
            proto_paragraphs = result.split('\n')
            new_paragraphs = [text for text in proto_paragraphs if len(text) > 5]

            title_text = new_paragraphs[1]
            content_paragraphs = new_paragraphs[2:]
        except IndexError:
            await ctx.send("Not a valid article.")
        else:
            pages = Pages(ctx, entries=content_paragraphs, per_page=1, title=title_text)
            await pages.paginate()


def setup(bot):
    bot.add_cog(SCG(bot))

