import discord
from latest.ftp_adapter import get_last_file_url, HTTP_HOST
from discord.ext import commands


class Latest:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def latest(self, ctx, subdir=None):
        """Sends a PM with the newest release's download URL.
        You can write the subdir desired"""
        # Get the latest file
        file = get_last_file_url(subdir)

        # Check connection to FTP server
        if file is None:
            await self.bot.send_message(ctx.message.author, 'Unable to connect to the FTP server')
            return
        # Check error file
        if file.date == 0:
            await self.bot.send_message(ctx.message.author, file.name)
            return

        # Building route
        route = HTTP_HOST
        if subdir is not None:
            route += subdir + '/'
        route += file.name

        # PM Embed message
        embed = discord.Embed(title='Download Link')
        embed.add_field(name='HTTP', value=route, inline=False)
        await self.bot.send_message(ctx.message.author, embed=embed)


def setup(bot):
    bot.add_cog(Latest(bot))
