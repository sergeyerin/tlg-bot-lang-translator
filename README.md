# Telegram Language Translator Bot

A Telegram bot that translates text between Russian and other languages using OpenAI's API, with explanations for non-Russian input. Specifically designed for Russian speakers learning other languages.

## Features

- **Bidirectional translation**: 
  - Russian → English/Portuguese
  - English/Portuguese → Russian (with explanations of tricky words)
- **Smart translation**:
  - Single word → All possible translations with context
  - Full text → Complete translation
  - **Non-Russian input**: Provides explanations of difficult words when translating to Russian
- **User preferences**: Each user can set their preferred target language for Russian text
- **Russian-focused**: Designed specifically for Russian speakers learning other languages

## Supported Languages

- **English** (`english`, `en`) - Default
- **Portuguese** (`portuguese`, `pt`)

## Bot Commands

- `/start` - Initialize the bot and get welcome message
- `/lang <language>` - Set target translation language
  - Examples: `/lang english`, `/lang pt`
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
   /lang english
   ```

2. **Translate text:**
   ```
   User: Привет, как дела?
   Bot: Hello, how are you?
   ```

3. **Single Russian word with multiple meanings:**
   ```
   User: банк
   Bot: Word: банк
   Translations:
   1. bank
   2. jar
   3. can
   ...
   ```

4. **English to Russian with explanations:**
   ```
   User: The serendipitous encounter changed everything
   Bot: Перевод: Случайная встреча изменила все
   
   Объяснение сложных слов:
   - serendipitous: означает "случайный, но приятный и полезный"
   - encounter: встреча, столкновение
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