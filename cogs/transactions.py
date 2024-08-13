import discord, sqlite3, json
from discord.ext import commands
from main import footer_text

from scripts.tracker import StatisticsTracker
stats = StatisticsTracker()

with open("./config.json", "r") as f:
    config = json.load(f)

def transaction_user(sender_type, sender: int, receiver: int, amount: float):
    # Perform deduction from sender
    with sqlite3.connect(config["db"]["accounts"][sender_type]) as conn:
        with conn:
            conn.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, sender))
    # Perform addition to receiver
    with sqlite3.connect(config["db"]["accounts"]["users"]) as conn:
        with conn:
            conn.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, receiver))

class Transactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        # Command group
        transfer = bot.create_group("transfer", "Transaction-related commands")

        # /transfer user
        @transfer.command(name= "user", description= "Transfer funds to another user")
        async def transfer_user(ctx: discord.ApplicationContext, receiver: discord.User, amount: float):
            self.bot.account_exists("users", ctx.author.id)
            self.bot.account_exists("users", receiver.id)
            sender_balance = self.bot.account_balance("users", ctx.author.id)

            # Check for sufficient balance
            if sender_balance < amount:
                embed = discord.Embed(
                    title= "Transaction failed",
                    description= "Your account does not have a sufficient balance to complete this transaction.",
                    color= discord.Color.brand_red()
                )

                embed.set_footer(text= footer_text)
                await ctx.respond(embed= embed)

            # Check if amount negative
            elif amount < 0:
                embed = discord.Embed(
                    title= "Transaction failed",
                    description= "You cannot transfer a negative amount of money.",
                    color= discord.Color.brand_red()
                )

                embed.set_footer(text= footer_text)
                await ctx.respond(embed= embed)

            # Proceed with transaction
            else:
                transaction_user("users", ctx.author.id, receiver.id, amount)
                embed = discord.Embed(
                    title= "Transaction successful",
                    description= "You can't keep wasting your life earnings.",
                    color= discord.Color.brand_green()
                )
                embed.add_field(name= "Receiver", value= receiver.mention, inline= True)
                embed.add_field(name= "Amount", value= f"QD{amount}", inline= True)

                embed.set_footer(text= footer_text)
                await ctx.respond(embed= embed)
                stats.track_commands(ctx)

        # /transfer guild

        # /transfer shared

def setup(bot):
    bot.add_cog(Transactions(bot))