# Environment configuration
The existing .env.example also contains legacy Telegram bot settings. For the standalone analytics demo, only POSTGRES_PASSWORD is required. Copy .env.example to .env and set POSTGRES_PASSWORD to a strong local password. Docker Compose uses a separate feedback database and does not start the Telegram bot. The legacy Dockerfile remains available for the original bot.
