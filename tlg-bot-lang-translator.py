#!/usr/bin/env python3
"""
Telegram Translation Bot using OpenAI
Translates text between Russian and other languages with explanations for non-native text.
"""

import os
import logging
import time
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI, APIError, RateLimitError, APIConnectionError

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
    'spanish': 'Spanish',
    'es': 'Spanish',
    'french': 'French',
    'fr': 'French',
    'german': 'German',
    'de': 'German',
    'polish': 'Polish',
    'pl': 'Polish',
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
/lang_en - английский 🇺🇸  /lang_pt - португальский 🇵🇹
/lang_es - испанский 🇪🇸     /lang_fr - французский 🇫🇷
/lang_de - немецкий 🇩🇪      /lang_pl - польский 🇵🇱
/help - помощь

Просто отправьте текст, и я переведу его!

Особенности:
• Русский → 6 языков (с объяснениями сложных слов)
• 6 языков → Русский (с объяснениями)
• Для одного слова — все варианты перевода с объяснениями
"""
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
📜 Помощь по командам:

/start - запустить бота

🌍 Доступные языки:
/lang_en - английский 🇺🇸      /lang_es - испанский 🇪🇸
/lang_pt - португальский 🇵🇹  /lang_fr - французский 🇫🇷
/lang_de - немецкий 🇩🇪        /lang_pl - польский 🇵🇱

🔄 Как работает перевод:
• Русский текст → перевод на выбранный язык + объяснения
• Иностранный текст → русский + объяснения
• Одно слово → все возможные переводы + объяснения
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

async def set_language_spanish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set target language to Spanish."""
    user_id = update.effective_user.id
    user_languages[user_id] = 'spanish'
    await update.message.reply_text(
        "✅ Язык перевода установлен: Испанский 🇪🇸"
    )

async def set_language_french(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set target language to French."""
    user_id = update.effective_user.id
    user_languages[user_id] = 'french'
    await update.message.reply_text(
        "✅ Язык перевода установлен: Французский 🇫🇷"
    )

async def set_language_german(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set target language to German."""
    user_id = update.effective_user.id
    user_languages[user_id] = 'german'
    await update.message.reply_text(
        "✅ Язык перевода установлен: Немецкий 🇩🇪"
    )

async def set_language_polish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Set target language to Polish."""
    user_id = update.effective_user.id
    user_languages[user_id] = 'polish'
    await update.message.reply_text(
        "✅ Язык перевода установлен: Польский 🇵🇱"
    )

def is_single_word(text: str) -> bool:
    """Check if the text is a single word."""
    return len(text.split()) == 1

def is_russian_text(text: str) -> bool:
    """Check if the text contains Russian characters."""
    import re
    # Check if text contains Cyrillic characters
    return bool(re.search(r'[а-яё]', text.lower()))

def get_language_flag(language: str) -> str:
    """Get flag emoji for a language."""
    flags = {
        'russian': '🇷🇺',
        'english': '🇺🇸', 
        'portuguese': '🇵🇹',
        'spanish': '🇪🇸',
        'french': '🇫🇷',
        'german': '🇩🇪',
        'polish': '🇵🇱'
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
        
        # Retry logic with exponential backoff
        max_retries = 3
        base_delay = 1
        
        for attempt in range(max_retries):
            try:
                response = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1000,
                    temperature=0.3
                )
                
                return response.choices[0].message.content.strip()
            
            except RateLimitError as e:
                # Check if it's a quota issue or rate limit
                error_message = str(e)
                if 'insufficient_quota' in error_message or 'quota' in error_message.lower():
                    logger.error(f"OpenAI quota exceeded: {e}")
                    return """❌ Ошибка: превышен лимит OpenAI API

Сервис перевода временно недоступен из-за исчерпания квоты OpenAI API.

Пожалуйста, свяжитесь с администратором бота или попробуйте позже."""
                
                # Rate limit - retry with backoff
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"Rate limit hit, retrying in {delay}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                else:
                    logger.error(f"Rate limit exceeded after {max_retries} attempts: {e}")
                    return """❌ Ошибка: превышен лимит запросов

OpenAI API временно недоступен из-за большого количества запросов.

Пожалуйста, попробуйте через несколько минут."""
            
            except APIConnectionError as e:
                logger.error(f"API connection error: {e}")
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    logger.warning(f"Connection error, retrying in {delay}s (attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                else:
                    return """❌ Ошибка подключения к OpenAI API

Не удалось подключиться к сервису перевода.

Пожалуйста, проверьте интернет-соединение или попробуйте позже."""
            
            except APIError as e:
                logger.error(f"OpenAI API error: {e}")
                return f"""❌ Ошибка API OpenAI

Произошла ошибка при обработке запроса.

Детали: {str(e)[:100]}

Попробуйте позже или свяжитесь с администратором."""
    
    except Exception as e:
        logger.error(f"Unexpected translation error: {e}", exc_info=True)
        return """❌ Неожиданная ошибка перевода

Произошла непредвиденная ошибка.

Пожалуйста, попробуйте позже или свяжитесь с администратором."""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages and translate them."""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    # Get user's preferred language (default to English)
    user_preferred_language = user_languages.get(user_id, 'english')
    
    # Simple logic: Russian text detected by Cyrillic characters, everything else is user's target language
    if is_russian_text(text):
        # Russian to user's target language
        source_language = 'russian'
        target_language = user_preferred_language
    else:
        # User's target language to Russian
        source_language = user_preferred_language  
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
    
    # Verify OpenAI API key is configured
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        logger.error("OPENAI_API_KEY not found in environment variables")
        return
    
    logger.info("Configuration loaded successfully")
    logger.info(f"OpenAI API Key configured: {api_key[:20]}...")
    
    # Create the Application
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("lang_en", set_language_english))
    application.add_handler(CommandHandler("lang_pt", set_language_portuguese))
    application.add_handler(CommandHandler("lang_es", set_language_spanish))
    application.add_handler(CommandHandler("lang_fr", set_language_french))
    application.add_handler(CommandHandler("lang_de", set_language_german))
    application.add_handler(CommandHandler("lang_pl", set_language_polish))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
