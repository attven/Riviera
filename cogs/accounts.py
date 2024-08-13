import discord, sqlite3, json
from discord.ext import commands
from main import footer_text

from scripts.tracker import StatisticsTracker
stats = StatisticsTracker()

with open("./config.json", "r") as f:
    config = json.load(f)

def account_exists(type, id: int):
    with sqlite3.connect(config["db"]["accounts"][type]) as conn:
        with conn:
            cursor = conn.execute("SELECT * FROM accounts WHERE id = ?", (id,))
            if cursor.fetchone() is None:
                account_create(type, id)
                return False
            else:
                return True

def account_create(type, id: int):
    # Add to accounts database
    with sqlite3.connect(config["db"]["accounts"][type]) as conn:
        with conn:
            conn.execute("INSERT INTO accounts (id, balance, score) VALUES (?, ?, ?)", (id, 0, 0))

    # Set profile to personal
    with sqlite3.connect(config["db"]["profiles"]) as conn:
        with conn:
            conn.execute("INSERT INTO profiles (id, profile_type, profile_id) VALUES (?, ?, ?)", (id, type, id))
    stats.track_events("account created", f"type: {type}, id: {id}")

def account_balance(type, id: int):
    with sqlite3.connect(config["db"]["accounts"][type]) as conn:
        with conn:
            cursor = conn.execute("SELECT balance FROM accounts WHERE id = ?", (id,))
            return cursor.fetchone()[0]
        
def account_score(type, id: int):
    with sqlite3.connect(config["db"]["accounts"][type]) as conn:
        with conn:
            cursor = conn.execute("SELECT score FROM accounts WHERE id = ?", (id,))
            return cursor.fetchone()[0]

def account_profile():
    with sqlite3.connect(config["db"]["profiles"]) as conn:
        with conn:
            cursor = conn.execute("SELECT profile_type, profile_id FROM profiles WHERE id = ?", (id,))
            return cursor.fetchone()

class Accounts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # User database
        with sqlite3.connect(config["db"]["accounts"]["users"]) as conn:
            with conn:
                conn.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY, balance FLOAT, score INTEGER)")
                conn.execute("CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY, setting TEXT)")
        
        # Profile database
        with sqlite3.connect(config["db"]["profiles"]) as conn:
            with conn:
                conn.execute("CREATE TABLE IF NOT EXISTS profiles (id INTEGER PRIMARY KEY, profile_type TEXT, profile_id INTEGER)")

        # Command group
        accounts = bot.create_group("accounts", "Account-related commands")

        # /account create
        @accounts.command(name= "create", description= "Create your account")
        async def create(ctx: discord.ApplicationContext):
            if account_exists("users", ctx.author.id):
                embed = discord.Embed(
                    title= "Account already exists",
                    description= "You are already inside the Riviera database."
                )

                embed.set_footer(text= footer_text)
                await ctx.respond(embed= embed)
            else:
                embed = discord.Embed(
                    title= "Account created",
                    description= f"Welcome to Riviera, {ctx.author.mention}!"
                )
                
                embed.set_footer(text= footer_text)
                await ctx.respond(embed= embed)
                stats.track_commands(ctx)
        
        # /account overview
        @accounts.command(name= "overview", description= "Your account at a glimpse")
        async def overview(ctx: discord.ApplicationContext):
            await ctx.respond("wip")
            stats.track_commands(ctx)
        
        # /account switch

        # /account reset

        # /account delete

def setup(bot):
    bot.add_cog(Accounts(bot))
    # Add functions to bot object
    bot.account_exists = account_exists
    bot.account_create = account_create
    bot.account_balance = account_balance
    bot.account_score = account_score