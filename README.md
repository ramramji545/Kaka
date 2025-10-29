# Telegram File to Channel Bot

A Python Telegram bot that automatically forwards all received files to a specified channel.

## Features

- Automatically forwards all files to channel `-1003161993313`
- Supports all file types (documents, photos, videos, audio, etc.)
- Handles text messages and commands
- Deployed on Render.com

## Environment Variables Required

- `BOT_TOKEN`: Your Telegram bot token
- `API_ID`: Your Telegram API ID
- `API_HASH`: Your Telegram API Hash
- `CHANNEL_ID`: Channel ID where files will be forwarded (-1003161993313)

## Deployment on Render

1. Fork this repository
2. Create a new Web Service on Render
3. Connect your GitHub repository
4. Set environment variables in Render dashboard
5. Deploy

## Usage

1. Start the bot with `/start`
2. Send any file (document, photo, video, audio, etc.)
3. The bot will automatically forward it to the channel