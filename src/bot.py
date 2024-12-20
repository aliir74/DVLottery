import os

from telegram import ChatMember, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    PicklePersistence,
    filters,
)

from consts import (
    DATABASE_FILE,
    PROJECT_ROOT,
    TELEGRAM_ADMIN_ID,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHANNEL_USERNAME,
    VIDEO_PUBLISHED,
    CallbackData,
    Messages,
    UserState,
)
from image_process import start_process_image

yes_no_reply_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=Messages.NO, callback_data=CallbackData.NO_START_QUESTION
            ),
            InlineKeyboardButton(
                text=Messages.YES, callback_data=CallbackData.YES_START_QUESTION
            ),
        ],
    ],
)

join_group_reply_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=Messages.JOINED,
                callback_data=CallbackData.JOINED,
            ),
        ],
        [
            InlineKeyboardButton(
                text=Messages.NOT_JOINED,
                callback_data=CallbackData.NOT_JOINED,
            ),
        ],
    ],
)


def path_generator(extension: str, prefix: str = ""):
    i = 1
    while True:
        yield os.path.join(PROJECT_ROOT, "images", f"{prefix}{i}.{extension}")
        i += 1


async def is_user_in_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    channel_username = TELEGRAM_CHANNEL_USERNAME
    chat_member = await context.bot.get_chat_member(
        chat_id=channel_username, user_id=update.effective_user.id
    )
    return chat_member.status in [
        ChatMember.MEMBER,
        ChatMember.ADMINISTRATOR,
        ChatMember.OWNER,
    ]


async def send_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    good_image = context.user_data.get("good_image")
    file_name = context.user_data.get("file_name")
    edited_file_name = context.user_data.get("edited_file_name")
    if good_image is None or file_name is None or edited_file_name is None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=Messages.DELETED_IMAGE,
        )
        context.bot_data["deleted_error_count"] = (
            context.bot_data.get("deleted_error_count", 0) + 1
        )
        context.user_data["last_message_id"] = None
        await start(update, context)
        return
    final_message = Messages.INVITE_TO_YOUTUBE_VIDEO + "\n\n" if VIDEO_PUBLISHED else ""
    final_message += Messages.SUCCESS if good_image else Messages.NOT_GOOD_IMAGE
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=final_message,
        parse_mode="MarkdownV2",
    )
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=edited_file_name,
    )
    context.bot_data["completed_count"] = context.bot_data.get("completed_count", 0) + 1
    os.remove(file_name)
    os.remove(edited_file_name)
    message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=Messages.BYE,
    )
    context.user_data["state"] = UserState.INITIAL
    context.user_data["last_message_id"] = message.message_id


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("state") is None:
        # first time
        context.bot_data["distinct_user_count"] = (
            context.bot_data.get("distinct_user_count", 0) + 1
        )
    if VIDEO_PUBLISHED:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=Messages.INVITE_TO_YOUTUBE_VIDEO,
            parse_mode="MarkdownV2",
        )
    message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=Messages.START,
        reply_markup=yes_no_reply_markup,
    )
    if context.user_data.get("last_message_id"):
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=context.user_data["last_message_id"],
        )
    context.bot_data["start_count"] = context.bot_data.get("start_count", 0) + 1

    context.user_data["state"] = UserState.START_QUESTION
    context.user_data["last_message_id"] = message.message_id


async def start_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == CallbackData.YES_START_QUESTION:
        message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=Messages.YES_CONVERT,
        )
        context.user_data["state"] = UserState.CONVERT_QUESTION
        context.bot_data["convert_count"] = context.bot_data.get("convert_count", 0) + 1
    elif query.data == CallbackData.NO_START_QUESTION:
        message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=Messages.BYE,
        )
        context.user_data["state"] = UserState.CONVERT_QUESTION
        context.bot_data["bye_count"] = context.bot_data.get("bye_count", 0) + 1
    elif query.data == CallbackData.JOINED:
        context.bot_data["joined_count"] = context.bot_data.get("joined_count", 0) + 1
        if not await is_user_in_group(update, context):
            context.bot_data["fake_joined_count"] = (
                context.bot_data.get("fake_joined_count", 0) + 1
            )
            await context.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=query.message.message_id,
                text=Messages.JOIN_GROUP + "\n" + Messages.JOIN_GROUP_NOT_JOINED,
                reply_markup=join_group_reply_markup,
                parse_mode="MarkdownV2",
            )
            return
        await send_photo(update, context)
    elif query.data == CallbackData.NOT_JOINED:
        context.bot_data["not_joined_count"] = (
            context.bot_data.get("not_joined_count", 0) + 1
        )
        message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=Messages.BYE,
        )
    await query.delete_message()
    context.user_data["last_message_id"] = message and message.message_id


async def image_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot_data["image_received_count"] = (
        context.bot_data.get("image_received_count", 0) + 1
    )
    if context.user_data.get("state", UserState.INITIAL) != UserState.CONVERT_QUESTION:
        return
    download_message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=Messages.RECEIVING_IMAGE,
    )
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING,
    )
    if "last_message_id" in context.user_data:
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=context.user_data["last_message_id"],
        )
    new_file = await update.message.effective_attachment[-1].get_file()
    extension = new_file.file_path.split(".")[-1]
    file_name = await new_file.download_to_drive(next(path_generator(extension)))
    new_image, good_image = start_process_image(file_name)
    edited_file_name = next(path_generator(extension, "edited_"))
    if not new_image:
        await download_message.delete()
        message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=Messages.NOT_WORKING_IMAGE,
        )
        context.bot_data["not_working_image_count"] = (
            context.bot_data.get("not_working_image_count", 0) + 1
        )
        context.user_data["state"] = UserState.CONVERT_QUESTION
        context.user_data["last_message_id"] = message.message_id
        return
    else:
        new_image.save(edited_file_name)

    await download_message.delete()
    context.user_data["good_image"] = good_image
    context.user_data["file_name"] = file_name
    context.user_data["edited_file_name"] = edited_file_name
    context.user_data["last_message_id"] = None

    if await is_user_in_group(update, context):
        await send_photo(update, context)
    else:
        context.bot_data["already_in_group_count"] = (
            context.bot_data.get("already_in_group_count", 0) + 1
        )
        message = await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=Messages.JOIN_GROUP,
            reply_markup=join_group_reply_markup,
            parse_mode="MarkdownV2",
        )
        context.user_data["last_message_id"] = message.message_id


async def admin_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != TELEGRAM_ADMIN_ID:
        return
    message = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Gathering data...",
    )
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING,
    )
    report = ""
    for key, value in context.bot_data.items():
        report += f"{key.upper()}: {value}\n"
    await message.edit_text(report)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot_data["help_count"] = context.bot_data.get("help_count", 0) + 1
    await update.message.reply_text(Messages.HELP, parse_mode="MarkdownV2")


async def post_init(application: Application):
    await application.bot.send_message(
        chat_id=TELEGRAM_ADMIN_ID,
        text="✅ Bot deployed successfully",
    )


if __name__ == "__main__":
    persistence = PicklePersistence(filepath=DATABASE_FILE, update_interval=5 * 60)
    application = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .persistence(persistence)
        .post_init(post_init)
        .build()
    )

    admin_handler = CommandHandler("admin", admin_report)
    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", help)
    start_question_handler = CallbackQueryHandler(start_question)
    image_received_handler = MessageHandler(filters.ATTACHMENT, image_received)

    application.add_handler(admin_handler)
    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(start_question_handler)
    application.add_handler(image_received_handler)

    application.run_polling()
