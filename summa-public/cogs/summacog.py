# imports
import re
from cogs.utils.paginator import *
from cogs.utils.summautil import *

from discord.ext import commands


class Summa(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def simple_get_url(self, url):
        """
        Gets the url by opening a sesssion in the bot.
        """
        async with self.bot.session.get(url) as response:
            resp = await response.text()
            html = BeautifulSoup(resp, 'html.parser')

        return html

    @commands.command()
    async def st(self, ctx, *, search: str):
        """
        Searches the Summa Theologiae for an article. The search should be in the format pXqYaZ (e.g. p1q2a3).
        """

        my_reg = re.findall(r"[p|q|a]\d{1,3}", search)

        # get the part, question, and article i need
        p, q, a = None, None, None
        try:
            p = int(my_reg[0][1:])
            q = int(my_reg[1][1:])
            a = int(my_reg[2][1:])
        except IndexError:
            await ctx.send(f"Invalid search provided. Use the format `{ctx.prefix}{ctx.command.name}p#q#a#`")

        # convert the query to a string to be used for url
        query = st_int_to_str(p, q, a)
        url = "http://summa-theologiae.org/question/" + query + ".htm"

        soup = await self.simple_get_url(url)

        summa_content = soup.findAll('td', {"class": "textarea"})

        try:
            summa_text = summa_content[0].p.text.split('\n\n\n')
            summa_text = [text for text in summa_text if text != ""]

            # separate paragraphs that are too long
            for i in range(len(summa_text)):
                while len(summa_text[i]) > 2048:
                    # divide the paragraph into lines
                    p_list = summa_text[i].split('\n')

                    # divide the lines into two parts
                    mid = int(len(p_list) / 2)
                    former = p_list[:mid]
                    latter = p_list[mid:]

                    # splits the paragraphs into two
                    summa_text[i] = '\n'.join(former)
                    summa_text.insert(i + 1, '\n'.join(latter))

            # separate the article name and the opening paragraph
            summa_intro = summa_text[0].split('\n\n')

            # get the opening paragraph
            summa_text[0] = summa_intro[1]

            # get the article name
            article_name = (summa_intro[0].split("\n"))[2]

            # format the sentences into a paragraph
            for i in range(len(summa_text)):
                i_split = summa_text[i].split('\n')
                summa_text[i] = ' '.join(i_split[1:])
        except IndexError:
            await ctx.send("Not a valid article.")
        else:
            pages = Pages(ctx, entries=summa_text, per_page=1, title=article_name)
            await pages.paginate()


def setup(bot):
    bot.add_cog(Summa(bot))
