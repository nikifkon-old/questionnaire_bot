from sqlalchemy import event

from tbot.bot import bot, loop
from tbot.db import Session
from tbot.models import Event, Message
from tbot.utils import list_relevant_users_for_event


@event.listens_for(Session, "after_flush")
def event_handler(session, flush_context):
    # handle deleted messages
    for obj in session.deleted:
        if isinstance(obj, Event):
            for message in obj.messages:
                loop.run_until_complete(bot.delete_message(message.chat_id, message.id))

    # handle updated messages
    for obj in session.dirty:
        if isinstance(obj, Event):
            post = obj.post
            for message in obj.messages:
                loop.run_until_complete(bot.edit_message_text(post, message.chat_id, message.id))

    # handle new message
    for obj in session.new:
        if isinstance(obj, Event):
            chat_ids = [user.id for user in list_relevant_users_for_event(obj)]
            post = obj.post
            for chat_id in chat_ids:
                telegram_message = loop.run_until_complete(bot.send_message(chat_id, post))
                # save message to database
                message = Message(chat_id=chat_id, event_id=obj.id)
                message.id = telegram_message.message_id
                session.add(message)
