import discord
from discord.ext import commands
from main import footer_text

from scripts import embeds

class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        info = bot.create_group("info", "Information commands")

        # /info ping
        @info.command(name= "ping", description= "Check if bot is alive?")
        async def ping(self, ctx: discord.ApplicationContext):
            embed = discord.Embed(
                title= ":ping_pong: Pong!",
                description= "This bot is alive and well, thanks for checking in."
            )
            embed.add_field(name= "Latency:", value= f"{round(self.bot.latency * 1000)}ms")

            embed.set_footer(text= footer_text, icon_url= self.bot.user.avatar.url)
            await ctx.respond(embed= embed)
        
        # /info bot
        @info.command(name= "bot", description= "General bot information")
        async def bot_info(self, ctx: discord.ApplicationContext):
            embed = discord.Embed(
                title= "Riviera",
                description= "Community economics, currency and analytics."
            )

            embed.set_footer(text= footer_text, icon_url= self.bot.user.avatar.url)
            await ctx.respond(embed= embed)
        
        # /info server

def setup(bot):
    bot.add_cog(Bot(bot))