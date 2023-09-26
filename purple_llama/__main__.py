import json
import os
import sqlite3
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from twitchio.ext import commands
from playwright.sync_api import sync_playwright
from llama_cpp import Llama
from cachetools import LRUCache, cached
from sklearn.feature_extraction.text import CountVectorizer
from ratelimit import limits, sleep_and_retry

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize twitch_token and initial_channels with default values
twitch_token = None
initial_channels = ["freedomdao"]

def truncate_twitch_message(message):
    if len(message) > 500:
        return message[:497] + "..."
    return message

# Load configuration from config.json
try:
    with open("config.json", "r") as f:
        config = json.load(f)
    twitch_token = config.get("TWITCH_TOKEN")
    initial_channels = config.get("INITIAL_CHANNELS", ["freedomdao"])
except Exception as e:
    logging.error(f"Failed to load config.json: {e}")

if not twitch_token:
    logging.error("Twitch token not found. Exiting.")
    exit(1)

class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(token=twitch_token, prefix="!", initial_channels=initial_channels)

    async def event_ready(self):
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message):
        await self.handle_commands(message)

    @commands.command(name="llama")
    async def llama_command(self, ctx):
        prompt = ctx.message.content.replace("!llama ", "")
        reply = await generate_text(prompt)
        truncated_reply = truncate_twitch_message(reply)
        await ctx.send(truncated_reply)

# Initialize job_hat_prompts as an empty dictionary
job_hat_prompts = {}

# Load job hat prompts
try:
    with open("job_hat_prompts.json", "r") as f:
        job_hat_prompts = json.load(f)
except Exception as e:
    logging.error(f"Failed to load job_hat_prompts.json: {e}")

# Initialize Llama model
try:
    llm = Llama(model_path="llama-2-7b-chat.ggmlv3.q8_0.bin", n_ctx=3900)
except Exception as e:
    logging.error(f"Failed to initialize Llama model: {e}")

executor = ThreadPoolExecutor(max_workers=3)

# Initialize SQLite3 database
try:
    conn = sqlite3.connect("replies.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model TEXT,
            prompt TEXT,
            reply TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
except Exception as e:
    logging.error(f"Failed to initialize SQLite database: {e}")

# Initialize FastAPI
app = FastAPI()

# Initialize Cache
cache = LRUCache(maxsize=100)

# Create folders for each job hat
for job_hat in job_hat_prompts.keys():
    os.makedirs(f"{job_hat}_folder", exist_ok=True)

class Prompt(BaseModel):
    prompt: str

# Rate limiting: 1 request per second
@sleep_and_retry
@limits(calls=1, period=1)
@app.post("/generate/")
async def generate_story(prompt: Prompt):
    try:
        reply = await generate_text(prompt.prompt)
        return {"story": reply}
    except Exception as e:
        logging.error(f"Failed to generate story: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@cached(cache)
async def apply_job_hat(job_hat, text):
    prompt = job_hat_prompts[job_hat].format(text=text)
    output = await asyncio.get_event_loop().run_in_executor(executor, lambda: llm(prompt, max_tokens=200))
    return output['choices'][0]['text']

@cached(cache)
async def generate_text(prompt):
    try:
        cursor.execute("SELECT reply FROM replies WHERE prompt=?", (prompt,))
        cached_reply = cursor.fetchone()
        if cached_reply:
            return cached_reply[0]

        output = await asyncio.get_event_loop().run_in_executor(executor, lambda: llm(prompt, max_tokens=200))
        reply = output['choices'][0]['text']

        cursor.execute("INSERT INTO replies (model, prompt, reply) VALUES (?, ?, ?)", ("llama", prompt, reply))
        conn.commit()

        for job_hat, job_hat_prompt in job_hat_prompts.items():
            job_hat_text = await apply_job_hat(job_hat, reply)
            reply += f"\n[{job_hat.capitalize()} Hat]: {job_hat_text}"

            with open(f"{job_hat}_folder/{hash(prompt)}.txt", "a") as f:
                f.write(job_hat_text)

        return reply
    except Exception as e:
        logging.error(f"Failed to generate text: {e}")
        return "An error occurred."

def main():
    bot = TwitchBot()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.run())

if __name__ == "__main__":
    main()
