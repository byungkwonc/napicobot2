#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

async def napico_01_echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    napicobot echo
    """
    await update.message.reply_text(update.message.text)
async def napico_02_simple(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    napicobot simple QA
    """
    message = [
        {"role": "system", "content": MAIN_PROMPT},
        {"role": "user", "content": update.message.text}
    ]
    gpt_response = chatgpt_response(messages=messages)
    await update.message.reply_text(gpt_response)

def chatgpt_response(messages):
    try:
        response = openai.ChatCompletin.create(
            model=CHATGPT_ENGINE,
            messages=messages
        )
        return response.choices[0].message.content
    except (KeyError, IndexError) as e:
        return "GPT3 Error: " + str(e)
    except Exception as e:
        return "GPT3 Unknown Error: " + str(e)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("1749792111:AAHhGbNY1zcwg76ZwIMgdkYbrae3Gfqi6xI").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, napico_01_echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()