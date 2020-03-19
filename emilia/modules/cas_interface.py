import html
import emilia.modules.helper_funcs.cas_api as cas

from typing import Optional, List

from telegram import User, Chat, ChatMember, Update, Bot, Message, ParseMode
from telegram.ext import CommandHandler, run_async, Filters, MessageHandler

from emilia import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS
from emilia.modules.helper_funcs.chat_status import user_admin
from emilia.modules.helper_funcs.extraction import extract_user
from emilia.modules.disable import DisableAbleCommandHandler
from emilia.modules.helper_funcs.filters import CustomFilters


@run_async
def get_version(update, context):
    msg = update.effective_message
    ver = cas.vercheck()
    msg.reply_text("CAS API version: " + ver)
    return


@run_async
def caschecker(update, context):
    args = context.args
    msg = update.effective_message  # type: Optional[Message]
    user_id = extract_user(update.effective_message, args)
    if user_id and int(user_id) != 777000:
        user = context.bot.get_chat(user_id)
    elif user_id and int(user_id) == 777000:
        msg.reply_text(
            "This is Telegram. Unless you manually entered this reserved account's ID, it is likely a broadcast from a linked channel.")
        return
    elif not msg.reply_to_message and not args:
        user = msg.from_user
    elif not msg.reply_to_message and (not args or (
            len(args) >= 1 and not args[0].startswith("@") and not args[0].isdigit() and not msg.parse_entities(
                [MessageEntity.TEXT_MENTION]))):
        msg.reply_text("I can't extract a user from this.")
        return
    else:
        return

    text = "<b>CAS Check</b>:" \
           "\nID: <code>{}</code>" \
           "\nFirst Name: {}".format(user.id, html.escape(user.first_name))
    if user.last_name:
        text += "\nLast Name: {}".format(html.escape(user.last_name))
    if user.username:
        text += "\nUsername: @{}".format(html.escape(user.username))
    text += "\n\nCAS Banned: "
    result = cas.banchecker(user.id)
    text += str(result)
    if result:
        text += "\nTotal of Offenses: "
        parsing = cas.offenses(user.id)
        text += str(parsing)
    update.effective_message.reply_text(text, parse_mode=ParseMode.HTML)


@run_async
def casquery(update, context):
    args = context.args
    msg = update.effective_message  # type: Optional[Message]
    try:
        user_id = msg.text.split(' ')[1]
    except BaseException:
        msg.reply_text("There was a problem parsing the query")
        return
    text = "Your query returned: "
    result = cas.banchecker(user_id)
    text += str(result)
    msg.reply_text(text)


__mod_name__ = "Combot Anti-Spam"

__help__ = """
The CAS Interface module is designed to work with a ported CAS API.

*What is CAS?*
CAS stands for Combot Anti-Spam, an automated system designed to detect spammers in Telegram groups. 

*Available commands:*
 - /casver: Returns the pyCombotCAS API version that the bot is currently running.
 - /cascheck <user>/<reply>: Check if users are banned in the CAS database.

NOTE: Hitsuki has an automatic detection of CAS Banned and @SpamWatch Banned.
"""

GETVER_HANDLER = DisableAbleCommandHandler("casver", get_version)
CASCHECK_HANDLER = CommandHandler("cascheck", caschecker, pass_args=True)
CASQUERY_HANDLER = CommandHandler("casquery", casquery, pass_args=True, filters=CustomFilters.sudo_filter)

dispatcher.add_handler(GETVER_HANDLER)
dispatcher.add_handler(CASCHECK_HANDLER)
dispatcher.add_handler(CASQUERY_HANDLER)
