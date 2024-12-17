import discord
from discord.ext import commands
from flask import Flask, request, render_template_string
import os

# Discord Bot Setup
intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
bot = commands.Bot(command_prefix=".", intents=intents)

TOKEN = os.getenv("BOT_TOKEN")  # Bot Token
client = discord.Client(intents=intents)

# Flask App
app = Flask(__name__)

# HTML Template for Web Interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bot Message Sender</title>
</head>
<body>
    <h1>Send a Message to a Channel</h1>
    <form method="POST" action="/">
        <label for="channel_id">Channel ID:</label><br>
        <input type="text" id="channel_id" name="channel_id" required><br><br>

        <label for="message">Message:</label><br>
        <textarea id="message" name="message" rows="4" cols="50" required></textarea><br><br>

        <button type="submit">Send Message</button>
    </form>
</body>
</html>
"""

# Route: Main Page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        channel_id = request.form["channel_id"]
        message = request.form["message"]

        # Send message to Discord channel as a boxed code block
        try:
            channel = bot.get_channel(int(channel_id))
            if channel:
                # Format the message with triple backticks for code block styling
                boxed_message = f"```\n{message}\n```"
                bot.loop.create_task(channel.send(boxed_message))
                return "Message sent successfully!"
            else:
                return "Invalid channel ID or bot cannot access the channel."
        except Exception as e:
            return f"Error: {e}"

    return render_template_string(HTML_TEMPLATE)

# Run the Bot in the Background
@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")

# Start Flask App
def run_flask():
    app.run(host="0.0.0.0", port=5000)

# Run Flask and Bot
if __name__ == "__main__":
    import threading
    threading.Thread(target=run_flask).start()
    bot.run(TOKEN)
