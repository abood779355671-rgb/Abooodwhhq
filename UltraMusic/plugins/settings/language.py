# ==============================================================================
# language.py - Language Selection Plugin
# ==============================================================================
# Command:
#   /language  → Show two buttons: 🇸🇦 عربي | 🇬🇧 English
# Language choice is stored per-chat in MongoDB.
# ==============================================================================

from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from UltraMusic import app, db


@app.on_message(filters.command(["language", "lang", "setlang"]) & filters.group)
async def language_cmd(_, message: Message):
    """Show language selection buttons."""
    current = await db.get_lang(message.chat.id)
    label_ar = "🇸🇦 عربي" + (" ✓" if current == "ar" else "")
    label_en = "🇬🇧 English" + (" ✓" if current == "en" else "")

    buttons = [
        [
            InlineKeyboardButton(label_ar, callback_data="lang_ar"),
            InlineKeyboardButton(label_en, callback_data="lang_en"),
        ],
        [InlineKeyboardButton("✖ إغلاق / Close", callback_data="lang_close")],
    ]

    await message.reply(
        "<blockquote><b>🌐 اختر لغة البوت / Choose bot language</b>\n\n"
        "سيتم حفظ الاختيار لهذه المجموعة.\n"
        "The choice will be saved for this group.</blockquote>",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="html",
    )


@app.on_callback_query(filters.regex(r"^lang_"))
async def language_cb(_, query: CallbackQuery):
    """Handle language selection callback."""
    data = query.data

    if data == "lang_close":
        await query.message.delete()
        return

    lang_map = {"lang_ar": "ar", "lang_en": "en"}
    lang_code = lang_map.get(data)
    if not lang_code:
        return await query.answer("Invalid option.", show_alert=True)

    await db.set_lang(query.message.chat.id, lang_code)

    if lang_code == "ar":
        text = "✅ تم تعيين اللغة إلى <b>العربية</b> بنجاح."
        answer_text = "✅ تم تعيين اللغة إلى العربية"
    else:
        text = "✅ Language has been set to <b>English</b> successfully."
        answer_text = "✅ Language set to English"

    label_ar = "🇸🇦 عربي" + (" ✓" if lang_code == "ar" else "")
    label_en = "🇬🇧 English" + (" ✓" if lang_code == "en" else "")

    buttons = [
        [
            InlineKeyboardButton(label_ar, callback_data="lang_ar"),
            InlineKeyboardButton(label_en, callback_data="lang_en"),
        ],
        [InlineKeyboardButton("✖ إغلاق / Close", callback_data="lang_close")],
    ]

    await query.message.edit_text(
        f"<blockquote>{text}</blockquote>",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="html",
    )
    await query.answer(answer_text)
