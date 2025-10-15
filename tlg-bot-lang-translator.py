#!/usr/bin/env python3
"""
Telegram Translation Bot using OpenAI
Translates text between Russian and other languages with explanations for non-native text.
"""

import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Available languages
LANGUAGES = {
    'english': 'English',
    'en': 'English',
    'portuguese': 'Portuguese',
    'pt': 'Portuguese',
    'russian': 'Russian',
    'ru': 'Russian'
}

# User language preferences (will be stored in memory for this example)
user_languages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user_id = update.effective_user.id
    user_languages[user_id] = 'english'  # Default language
    
    welcome_message = """
🤖 Добро пожаловать в переводчик!

Команды:
/start - начать работу с ботом
/lang_en - переводить русский на английский 🇺🇸
/lang_pt - переводить русский на португальский 🇵🇹
/help - показать помощь

Просто отправьте текст, и я переведу его!

Особенности:
• Русский → Английский/Португальский (с объяснениями сложных слов)
• Английский/Португальский → Русский (с объяснениями)
• Для одного слова — все варианты перевода с объяснениями
"""
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
📜 Помощь по командам:

/start - запустить бота
/lang_en - переводить русский на английский 🇺🇸
/lang_pt - переводить русский на португальский 🇵🇹
/help - показать эту помощь

🔄 Как работает перевод:
• Русский текст → перевод на выбранный язык + объяснения
• Английский/Португальский → русский + объяснения
• Одно слово → все возможные переводы + объяснения

Примеры:
/lang_en - для перевода на английский
/lang_pt - для перевода на португальский
"""
    await update.message.reply_text(help_text)

async def set_language_english(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set target language to English."""
    user_id = update.effective_user.id
    user_languages[user_id] = 'english'
    await update.message.reply_text(
        "✅ Язык перевода установлен: Английский 🇺🇸"
    )

async def set_language_portuguese(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set target language to Portuguese."""
    user_id = update.effective_user.id
    user_languages[user_id] = 'portuguese'
    await update.message.reply_text(
        "✅ Язык перевода установлен: Португальский 🇵🇹"
    )

def is_single_word(text: str) -> bool:
    """Check if the text is a single word."""
    return len(text.split()) == 1

def is_russian_text(text: str) -> bool:
    """Check if the text contains Russian characters."""
    import re
    # Check if text contains Cyrillic characters
    return bool(re.search(r'[а-яё]', text.lower()))

def detect_language(text: str) -> str:
    """Detect the language of the input text."""
    import re
    
    # Check for Russian (Cyrillic characters)
    if re.search(r'[а-яё]', text.lower()):
        return 'russian'
    
    # Check for Portuguese specific characters/words
    portuguese_chars = re.search(r'[áàâãçéêíóôõú]', text.lower())
    portuguese_words = re.search(r'\b(que|não|com|para|uma|dos|das|pelo|pela)\b', text.lower())
    if portuguese_chars or portuguese_words:
        return 'portuguese'
    
    # Default to English for Latin characters
    if re.search(r'[a-z]', text.lower()):
        return 'english'
    
    # Unknown language
    return 'unknown'

def get_language_flag(language: str) -> str:
    """Get flag emoji for a language."""
    flags = {
        'russian': '🇷🇺',
        'english': '🇺🇸', 
        'portuguese': '🇵🇹'
    }
    return flags.get(language, '🏳️')

def get_translation_header(source_language: str, target_language: str) -> str:
    """Get translation direction header with flags."""
    source_flag = get_language_flag(source_language)
    target_flag = get_language_flag(target_language)
    source_name = LANGUAGES.get(source_language, source_language).title()
    target_name = LANGUAGES.get(target_language, target_language).title()
    
    return f"{source_flag} {source_name} → {target_flag} {target_name}\n{'─' * 30}\n"

async def translate_text(text: str, source_language: str, target_language: str, is_single: bool = False) -> str:
    """Translate text using OpenAI with explanations for difficult words and phrases."""
    try:
        # If translating TO Russian, provide explanations in Russian
        if target_language == 'russian':
            if is_single:
                prompt = f"""
Переведи слово "{text}" ({source_language}) на русский язык. Дай ВСЕ возможные переводы с объяснениями.
Формат ответа:
Слово: {text}
Переводы:
1. [перевод] - [объяснение/контекст]
2. [перевод] - [объяснение/контекст]
...
"""
            else:
                prompt = f"""
Переведи следующий текст с {source_language} на русский язык и объясни значение всех сложных слов и фраз:

Текст: "{text}"

Формат ответа:
Перевод: [перевод текста]

Объяснение слов и фраз:
- [слово/фраза]: [подробное объяснение]
"""
        # If translating FROM Russian, provide explanations in Russian about target language words/phrases
        else:
            if is_single:
                prompt = f"""
Переведи русское слово "{text}" на {LANGUAGES[target_language]} и дай ВСЕ возможные переводы с объяснениями.
Формат ответа:
Слово: {text}
Переводы:
1. [translation] - [объяснение на русском: когда и как используется]
2. [translation] - [объяснение на русском: контекст и нюансы]
...
"""
            else:
                prompt = f"""
Переведи следующий русский текст на {LANGUAGES[target_language]} и объясни все слова и фразы в переводе, которые могут быть сложными для изучающего язык:

Текст: "{text}"

Формат ответа:
Перевод: [translation]

Объяснение слов и фраз в переводе:
- [word/phrase]: [подробное объяснение на русском: значение, контекст, примеры]
"""
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.3
        )
        
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return "❌ Ошибка перевода. Попробуйте позже."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages and translate them."""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    # Detect the language of input text
    source_language = detect_language(text)
    
    # Check if language is supported
    if source_language == 'unknown':
        await update.message.reply_text(
            "❌ Не могу определить язык текста.\n"
            "Поддерживаемые языки: русский, английский, португальский"
        )
        return
    
    # Get user's preferred language (default to English)
    user_preferred_language = user_languages.get(user_id, 'english')
    
    # Determine target language
    if source_language == 'russian':
        # Russian to other language
        target_language = user_preferred_language
    else:
        # Other language to Russian (native language with explanations)
        target_language = 'russian'
    
    # Check if it's a single word
    is_single = is_single_word(text)
    
    # Show typing indicator
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
    
    # Get translation direction header
    translation_header = get_translation_header(source_language, target_language)
    
    # Translate the text
    translation = await translate_text(text, source_language, target_language, is_single)
    
    # Combine header with translation
    full_response = translation_header + translation
    
    # Send the translation
    await update.message.reply_text(full_response)

def main() -> None:
    """Start the bot."""
    # Get the token from environment variables
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    # Create the Application
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("lang_en", set_language_english))
    application.add_handler(CommandHandler("lang_pt", set_language_portuguese))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()