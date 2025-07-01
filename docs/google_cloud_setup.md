# Google Cloud Speech-to-Text Setup Guide

## Quick Setup

The Google Cloud Speech-to-Text API needs to be enabled for your project. Here's how to do it:

### 1. Enable the Speech-to-Text API

**Click this link to enable the API directly:**
https://console.developers.google.com/apis/api/speech.googleapis.com/overview?project=588116594289

Or follow these steps manually:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project (ID: 588116594289)
3. Go to "APIs & Services" > "Library"
4. Search for "Cloud Speech-to-Text API"
5. Click on it and press "Enable"

### 2. Verify Billing is Enabled

1. Go to "Billing" in the Google Cloud Console
2. Make sure billing is enabled for your project
3. Speech-to-Text API has a free tier: 60 minutes per month

### 3. Test the Setup

After enabling the API, wait a few minutes for the changes to propagate, then run:

```bash
python test_google_speech.py
```

### 4. Run Prism with Speech Recognition

Once the API is enabled, you can run the full Prism app:

```bash
python app.py
```

## Environment Variables

Make sure your `.env` file contains:

```
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
```

## Troubleshooting

- **API not enabled**: Follow the link above to enable the Speech-to-Text API
- **Billing issues**: Make sure billing is enabled for your Google Cloud project
- **Credentials**: Ensure your service account key file path is correct in `GOOGLE_APPLICATION_CREDENTIALS`

## Benefits of Google Cloud Speech-to-Text

- Better audio format support (handles webm, mp3, wav, etc.)
- More reliable transcription
- Better handling of browser audio formats
- Free tier available (60 minutes/month) 