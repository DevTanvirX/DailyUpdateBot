import discord
import asyncio
import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Replace with your channel ID

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Get today's date info
def get_daily_info():
    now = datetime.datetime.now(ZoneInfo("Asia/Dhaka"))
    week_num = now.isocalendar()[1]
    day_of_year = now.timetuple().tm_yday
    remaining_days = 365 - day_of_year if now.year % 4 != 0 else 366 - day_of_year
    target_date = datetime.datetime(2025, 12, 31, tzinfo=ZoneInfo("Asia/Dhaka"))
    days_to_new_year = (target_date - now).days

    # Simpler greeting and motivational quote with minimal emojis
    greeting = "🌅 Another chance to be better—good morning!"
    quote =    "You don’t need to be perfect—just consistent."
    divider =  "-----------------------------------------------"

    return (
        f"{greeting}\n\n"
        f"⌚ Date: {now.strftime('%A, %d %B %Y')}\n"
        f"📆 Week: {week_num} | Day of Year: {day_of_year}\n"
        f"🎴 {remaining_days} days left in {now.year}\n\n"
        f"{quote}\n"
        f"{divider}"
    )

async def send_daily_message():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)

    # ✅ First run – send today's message immediately
    if channel:
        daily_message = get_daily_info()
        await channel.send(daily_message)
        print("✅ Sent today's initial message.")

    # 🕛 Wait until next 00:00 to repeat daily
    while not client.is_closed():
        now = datetime.datetime.now(ZoneInfo("Asia/Dhaka"))
        next_run = now.replace(hour=0, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
        wait_seconds = (next_run - now).total_seconds()
        print(f"Next message in {int(wait_seconds)} seconds...")

        await asyncio.sleep(wait_seconds)

        if channel:
            daily_message = get_daily_info()
            await channel.send(daily_message)

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    client.loop.create_task(send_daily_message())

client.run(TOKEN)
