# imports
from cogs.utils.paginator import *
from cogs.summacog import *

from discord.ext import commands
import wikipedia
from googleapiclient.discovery import build

from safety import API_KEY, CSE_ID

api_key = API_KEY
cse_id = CSE_ID

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def is_citation(arr, k):
        '''checks if arr[k] is part of a citation.'''

        if arr[k] == "[" or arr[k] == "]":
            return True

        if arr[k - 1] == "[" and arr[k + 1] == "]":
            return True

        if arr[k -2] == "[" and arr[k + 1] == "]":
            return True

        if arr[k - 1] == "[" and arr[k + 2] == "]":
            return True

        if arr[k - 2] == "[" and arr[k + 2] == "]":
            return True

        return False

    @commands.command()
    async def wiki(self, ctx, *, query: str):
        '''Searches for the Wikipedia article using the query.'''

        # search
        new_query = "wikipedia " + query
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=new_query, cx=cse_id).execute()
        print(res)
        url = res['items'][0]['link']

        # parse
        html = await Summa(self.bot).simple_get_url(url)

        # get the text
        result = html.select('.mw-parser-output > p, .mw-parser-output > ul')

        # find content (edited)
        paragraphs = []

        for i in result:
            if i.name == 'p':
                # if the next item is a paragraph, add it to the list
                if i.text.strip() != "":
                    chars = []
                    for c in i.text.strip():
                        if c != "\n":
                            chars.append(c)

                    # remove citations
                    good_chars = []
                    for j in range(len(chars)):
                        if not self.is_citation(chars, j):
                            good_chars.append(chars[j])

                    paragraphs.append(''.join(good_chars))

            elif i.name == 'ul':
                # if the next item is a list, add it to the previous paragraph
                list_text = []
                list_items = i.find_all('li')

                for list_item in list_items:
                    list_text.append("- " + list_item.text)

                new_list = '\n'.join(list_text)
                paragraphs[len(paragraphs) - 1] = paragraphs[len(paragraphs) - 1] \
                        + '\n' + new_list

        # find article title
        title = html.find("h1", {"class": "firstHeading"}).text
        article_title = "Wikipedia: " + title

        pages = Pages(ctx, entries=paragraphs, per_page=1, title=article_title)
        await pages.paginate()

    @commands.command()
    async def yt(self, ctx, *, query: str):
        '''Searches for a YouTube video using the query.'''
        youtube = build('youtube', 'v3', developerKey=api_key)
        req = youtube.search().list(part="snippet", q=query, type="video")
        res = req.execute()
        url = 'https://www.youtube.com/watch?v=' \
            + str(res['items'][0]['id']['videoId'])
        await ctx.send(url)

    @commands.command()
    async def xkcd(self, ctx, *, query: str):
        '''Searches for an xkcd comic with the given query. Enter "random" as the query for a random comic.'''

        # search
        new_query = "xkcd " + query
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=new_query, cx=cse_id).execute()
        url = res['items'][0]['link']

        if query.lower() == "random":
            url = "https://c.xkcd.com/random/comic/"
            html = await Summa(self.bot).simple_get_url(url)

            m = html.find('meta', {'property': 'og:url'})
            url = m.get('content')
        
        await ctx.send(url)


def setup(bot):
    bot.add_cog(Fun(bot))

