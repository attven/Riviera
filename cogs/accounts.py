import discord, sqlite3, json
from discord.ext import commands

with open("./config.json", "r") as f:
    config = json.load(f)

def account_create(user_id: int):
    with sqlite3.connect(config["db"]["accounts"]) as conn:
        with conn:
            conn.execute("")

class Accounts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # Create database
        with sqlite3.connect(config["db"]["accounts"]) as conn:
            with conn:
                conn.execute("CREATE TABLE IF NOT EXISTS users (user INTEGER PRIMARY KEY, balance FLOAT, score INTEGER)")
                conn.execute("CREATE TABLE IF NOT EXISTS ")

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
