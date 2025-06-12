from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from . import config, db, qr


action_keyboard = InlineKeyboardMarkup(
    [[InlineKeyboardButton("\u2705 Я пришёл", callback_data="in")],
     [InlineKeyboardButton("\u274C Я ушёл", callback_data="out")]]
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Сканируйте QR код и отправьте полученную строку.", reply_markup=action_keyboard
    )

async def select_action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    context.user_data["action"] = query.data
    await query.edit_message_text("Отправьте код из QR")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()
    if qr.verify_code(text):
        action = context.user_data.get("action")
        if action:
            db.record_event(update.effective_user.id, action)
            await update.message.reply_text("Отметка сохранена")
        else:
            await update.message.reply_text("Сначала выберите действие через /start")
    else:
        await update.message.reply_text("Неверный или просроченный код")


def main() -> None:
    db.init_db()
    application = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(select_action))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == "__main__":
    main()
