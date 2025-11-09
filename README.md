# Arcade Flow Analyzer

A Python tool that analyzes Arcade flow recordings and generates comprehensive reports with AI-powered insights.

## 🌟 Features

- **User Interaction Analysis**: Extracts and lists all user actions in human-readable format
- **AI-Powered Summaries**: Uses GPT-4 to generate clear, engaging summaries of user flows
- **Social Media Images**: Creates custom images with DALL-E suitable for sharing
- **Smart Caching**: Implements intelligent caching to minimize API costs during development
- **Markdown Reports**: Generates professional markdown reports with all insights

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_key_here
   ```

### Usage

Run the analyzer on the flow.json file:

```bash
python3 analyze_flow.py
```

The script will:
1. Parse the flow.json file
2. Extract all user interactions
3. Generate an AI-powered summary
4. Create a social media image
5. Output everything to `FLOW_REPORT.md`

## 📁 Project Structure

```
arcade/
├── flow.json              # Input flow data
├── analyze_flow.py        # Main analysis script
├── requirements.txt       # Python dependencies
├── .env                   # API keys (gitignored)
├── .cache/               # Cached API responses (gitignored)
├── FLOW_REPORT.md        # Generated report
└── flow_social_media_*.png # Generated image
```

## 💰 Cost Management

The script implements intelligent caching for API responses:
- **GPT-4 Summaries**: Cached based on flow content
- **DALL-E Images**: Cached to avoid regeneration

This significantly reduces costs during development and testing.

## 🔒 Security

**Important**: Never commit your API keys! 

The `.gitignore` file is configured to exclude:
- `.env` files
- Cache directories
- Generated images (except the final ones)

## 📊 Output

The script generates:
1. **FLOW_REPORT.md**: A comprehensive markdown report containing:
   - Flow overview and summary
   - Detailed list of user interactions
   - Key insights
   - Social media image
   - Flow statistics

2. **Social Media Image**: A professional image suitable for sharing on platforms like LinkedIn, Twitter, etc.

## 🛠️ How It Works

1. **Parse Flow Data**: Reads and parses the Arcade flow JSON
2. **Extract Interactions**: Identifies user actions (clicks, typing, scrolling)
3. **Generate Context**: Uses GPT-4 to understand the user's intent
4. **Create Visuals**: Generates engaging images with DALL-E
5. **Compile Report**: Assembles everything into a markdown document

## 📝 Example Output

The tool analyzes flows like:
- E-commerce shopping journeys
- Product demos
- Tutorial walkthroughs
- User onboarding flows

And generates clear, shareable reports perfect for:
- Product documentation
- User guides
- Marketing materials
- Social media content

## 🔧 Customization

You can customize the analysis by modifying:
- `extract_user_interactions()`: Change how interactions are parsed
- `generate_summary()`: Adjust the GPT-4 prompt
- `generate_social_media_image()`: Customize the DALL-E prompt
- `generate_report()`: Modify the report format

## 📜 License

This project is created as part of the Arcade AI Interview Challenge.

## 🤝 Contributing

This is an interview project, but feel free to fork and adapt for your own use!

