import discord
from discord.ext import commands

class Accounts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Command group
        accounts = bot.create_group("accounts", "Account-related commands")

        # /account create
        @accounts.command(name= "create", description= "Create your account")
        async def create(ctx: discord.ApplicationContext):
            await ctx.respond("code")
        
        # /account overview
        @accounts.command(name= "overview", description= "Your account at a glimpse")
        async def overview(ctx: discord.ApplicationContext):
            await ctx.respond("code")
        
        # /account switch

        # /account reset

        # /account delete


def setup(bot):
    bot.add_cog(Accounts(bot))
