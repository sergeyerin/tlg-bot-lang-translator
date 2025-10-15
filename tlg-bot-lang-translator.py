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
• Русский → Английский/Португальский
• Английский/Португальский → Русский (с объяснениями)
• Для одного слова — все варианты перевода
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
• Русский текст → перевод на выбранный язык
• Английский/Португальский → русский + объяснения
• Одно слово → все возможные переводы

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

async def translate_text(text: str, source_language: str, target_language: str, is_single: bool = False) -> str:
    """Translate text using OpenAI with explanations for non-Russian input."""
    try:
        # If translating TO Russian (non-native input), provide explanations
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
Переведи следующий текст с {source_language} на русский язык и объясни значение сложных или неочевидных слов:

Текст: "{text}"

Формат ответа:
Перевод: [перевод текста]

Объяснение сложных слов:
- [слово]: [объяснение]
"""
        # If translating FROM Russian (no explanations needed)
        else:
            if is_single:
                prompt = f"""
Translate the Russian word "{text}" to {LANGUAGES[target_language]}. Provide ALL possible translations of this word.
Format:
Word: {text}
Translations:
1. [translation]
2. [translation]
3. [translation]
...
"""
            else:
                prompt = f'Translate the following Russian text to {LANGUAGES[target_language]}: "{text}"'
        
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
    
    # Translate the text
    translation = await translate_text(text, source_language, target_language, is_single)
    
    # Send the translation
    await update.message.reply_text(translation)

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