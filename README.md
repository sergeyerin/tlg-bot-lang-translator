# Telegram Language Translator Bot

A Telegram bot that translates text between Russian and 6 other languages using OpenAI's API, with explanations for difficult words. Specifically designed for Russian speakers learning foreign languages.

## Features

- **Bidirectional translation with explanations**: 
  - Russian → English/Portuguese/Spanish/French/German/Polish (with explanations of difficult words)
  - English/Portuguese/Spanish/French/German/Polish → Russian (with explanations of tricky words)
- **Smart translation**:
  - Single word → All possible translations with detailed explanations
  - Full text → Complete translation with explanations of difficult words and phrases
  - **Always explains**: Provides explanations for difficult vocabulary in both directions
- **User preferences**: Each user can set their preferred target language for Russian text
- **Russian-focused**: Designed specifically for Russian speakers learning other languages

## Supported Languages

- **English** (`english`, `en`) - Default 🇺🇸
- **Portuguese** (`portuguese`, `pt`) 🇵🇹 
- **Spanish** (`spanish`, `es`) 🇪🇸
- **French** (`french`, `fr`) 🇫🇷
- **German** (`german`, `de`) 🇩🇪
- **Polish** (`polish`, `pl`) 🇵🇱

## Bot Commands

- `/start` - Initialize the bot and get welcome message
- `/lang_en` - Set target language to English 🇺🇸
- `/lang_pt` - Set target language to Portuguese 🇵🇹
- `/lang_es` - Set target language to Spanish 🇪🇸
- `/lang_fr` - Set target language to French 🇫🇷
- `/lang_de` - Set target language to German 🇩🇪
- `/lang_pl` - Set target language to Polish 🇵🇱
- `/help` - Show help information

## Installation

### Prerequisites

- Python 3.8+
- Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- OpenAI API Key

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/tlg-bot-lang-translator.git
   cd tlg-bot-lang-translator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` file and add your API keys:
   ```
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the bot:**
   ```bash
   python bot.py
   ```

## Getting API Keys

### Telegram Bot Token

1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` command
3. Choose a name and username for your bot
4. Copy the provided token to your `.env` file

### OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up/login to your account
3. Go to API Keys section
4. Create a new API key
5. Copy the key to your `.env` file

## Usage Examples

1. **Set language:**
   ```
   /lang_en  (English)     /lang_es  (Spanish)    /lang_pl  (Polish)
   /lang_pt  (Portuguese)  /lang_fr  (French)     /lang_de  (German)
   ```

2. **Translate Russian text with explanations:**
   ```
   User: Привет, как дела?
   Bot: 🇷🇺 Russian → 🇺🇸 English
   ──────────────────────────────
   Translation: Hello, how are you?
   
   Explanation of words and phrases in translation:
   - how are you: выражение вежливости, используется при встрече
   ```

3. **Single Russian word with explanations:**
   ```
   User: банк
   Bot: 🇷🇺 Russian → 🇺🇸 English
   ──────────────────────────────
   Word: банк
   Translations:
   1. bank - финансовая организация, также может означать "берег реки"
   2. jar - стеклянная емкость с крышкой, для консервации
   3. can - металлическая банка, обычно для напитков
   ```

4. **English to Russian with explanations:**
   ```
   User: The serendipitous encounter changed everything
   Bot: 🇺🇸 English → 🇷🇺 Russian
   ──────────────────────────────
   Перевод: Случайная встреча изменила все
   
   Объяснение сложных слов:
   - serendipitous: означает "случайный, но приятный и полезный"
   - encounter: встреча, столкновение
   ```

5. **Russian to Spanish with explanations:**
   ```
   /lang_es
   User: Привет, как твои дела?
   Bot: 🇷🇺 Russian → 🇪🇸 Spanish
   ──────────────────────────────
   Translation: Hola, ¿cómo están tus cosas?
   
   Explanation of words and phrases in translation:
   - ¿cómo están tus cosas?: неформальный способ спросить "как дела?"
   ```

6. **Polish to Russian with explanations:**
   ```
   User: Dzień dobry, jak się Pan ma?
   Bot: 🇵🇱 Polish → 🇷🇺 Russian
   ──────────────────────────────
   Перевод: Добрый день, как дела?
   
   Объяснение слов и фраз:
   - Dzień dobry: стандартное вежливое приветствие "добрый день"
   - jak się Pan ma: вежливая форма вопроса "как дела?" к мужчине
   ```

## Project Structure

```
tlg-bot-lang-translator/
├── bot.py              # Main bot implementation
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Technologies Used

- **Python 3.8+**
- **python-telegram-bot** - Telegram Bot API wrapper
- **OpenAI API** - Translation and text processing
- **python-dotenv** - Environment variables management

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Made with ❤️ for Russian language learners**