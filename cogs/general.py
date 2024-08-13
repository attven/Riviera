import discord
from discord.ext import commands
from main import footer_text

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
        bot_group = bot.create_group("bot", "Bot related commands")

        # /bot ping
        @bot_group.command(name= "ping", description= "Check if bot is alive?")
        async def ping(ctx: discord.ApplicationContext):
            embed = discord.Embed(
                title= ":ping_pong: Pong!",
                description= "This bot is alive and well, thanks for checking in."
            )
            embed.add_field(name= "Latency:", value= f"{round(bot.latency * 1000)}ms")

            # embed.set_footer(text= footer_text, icon_url= bot.user.avatar.url)
            await ctx.respond(embed= embed)
        
        # /bot info
        @bot_group.command(name= "info", description= "General bot information")
        async def bot_info(ctx: discord.ApplicationContext):
            embed = discord.Embed(
                title= "Riviera",
                description= "Community economics, currency and analytics."
            )

            # embed.set_footer(text= footer_text, icon_url= bot.user.avatar.url)
            await ctx.respond(embed= embed)
        
        # /bot calculator
        @bot_group.command(name= "calculator", description= "Basic calculator")
        async def calculator(ctx: discord.ApplicationContext, num1: int, operation: discord.Option(str, choices= ["+", "-", "*", "/"]), num2: int): # type: ignore
            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "*":
                result = num1 * num2
            elif operation == "/":
                result = num1 / num2
            else:
                result = "Invalid operation"
            
            embed = discord.Embed(
                title= "Calculator",
                description= f"{num1} {operation} {num2} = {result}"
            )

            # embed.set_footer(text= footer_text, icon_url= bot.user.avatar.url)
            await ctx.respond(embed= embed)

def setup(bot):
    bot.add_cog(General(bot))