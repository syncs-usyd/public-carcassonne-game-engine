# Discord Webhook Notifications

This directory contains GitHub Actions workflows that send notifications to Discord when commits are pushed to the main branch.

## Setup Instructions

### 1. Create a Discord Webhook

1. Go to your Discord server
2. Navigate to the channel where you want to receive notifications
3. Right-click on the channel and select "Edit Channel"
4. Go to the "Integrations" tab
5. Click "Create Webhook"
6. Give it a name (e.g., "GitHub Notifications")
7. Copy the webhook URL

### 2. Add the Webhook URL to GitHub Secrets

1. Go to your GitHub repository
2. Click on "Settings" tab
3. In the left sidebar, click "Secrets and variables" → "Actions"
4. Click "New repository secret"
5. Name: `DISCORD_WEBHOOK_URL`
6. Value: Paste your Discord webhook URL
7. Click "Add secret"

### 3. Choose Your Workflow

You have two workflow options:

#### Option A: `discord-notification.yml` (Recommended)
- Uses a pre-built action for better reliability
- Automatically handles different job statuses
- Includes pull request notifications
- More robust error handling

#### Option B: `discord-webhook.yml`
- Custom webhook implementation
- More control over message formatting
- Only triggers on pushes to main
- Simpler setup

### 4. Test the Setup

1. Make a commit to the main branch
2. Push the changes
3. Check your Discord channel for the notification

## Customization

You can modify the workflow files to:
- Change the notification message format
- Add more information to the embed
- Modify the trigger conditions
- Add different notification types

## Troubleshooting

- Make sure the webhook URL is correct and the secret is properly set
- Check the GitHub Actions tab to see if the workflow is running
- Verify that the Discord webhook is still active in your Discord server 