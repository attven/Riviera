import sqlite3, json, datetime

with open("./config.json", "r") as f:
    config = json.load(f)

class StatisticsTracker:
    def __init__(self):
        with sqlite3.connect(config["db"]["statistics"]) as conn:
            with conn:
                conn.execute("CREATE TABLE IF NOT EXISTS commands (command TEXT, author INTEGER, channel INTEGER, guild INTEGER, latency INTEGER, timestamp TEXT)")
                conn.execute("CREATE TABLE IF NOT EXISTS events (event TEXT, details TEXT, timestamp TEXT)")
    
    def track_commands(self, ctx):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        latency = ctx.bot.latency * 1000
        with sqlite3.connect(config["db"]["statistics"]) as conn:
            with conn:
                conn.execute("INSERT INTO commands (command, author, channel, guild, latency, timestamp) VALUES (?,?,?,?,?,?)", (ctx.command.name, ctx.author.id, ctx.channel.id, ctx.guild.id, latency, timestamp))
        print(f"- /{ctx.command.name}\nauthor: {ctx.author.id}, channel: {ctx.channel.id}, latency: {latency}")

    def track_transactions(self, receiver, sender, amount, timestamp):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(config["db"]["statistics"]) as conn:
            with conn:
                conn.execute("INSERT INTO transactions (receiver, sender, amount, timestamp) VALUES (?,?,?,?)", (receiver, sender, amount, timestamp))
        print(f"- transaction\nsender: {sender}, receiver: {receiver}, amount: {amount}")

    def track_events(self, event, details):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(config["db"]["statistics"]) as conn:
            with conn:
                conn.execute("INSERT INTO events (event, details, timestamp) VALUES (?,?,?)", (event, details, timestamp))
        print(f"- {event}\ndetails: {details}")