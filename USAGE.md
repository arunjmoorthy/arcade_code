# Usage Guide

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your API key**:
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Run the analyzer**:
   ```bash
   python3 analyze_flow.py
   ```

## What Happens When You Run It

The script will:

1. **Parse** the `flow.json` file
2. **Extract** all user interactions (clicks, typing, scrolling)
3. **Generate** an AI-powered summary using GPT-4
4. **Create** a social media image using DALL-E
5. **Output** a comprehensive markdown report (`FLOW_REPORT.md`)

## Output Files

After running the script, you'll have:

- `FLOW_REPORT.md` - Comprehensive analysis report
- `flow_social_media_*.png` - Social media image
- `.cache/` - Cached API responses (gitignored)

## Caching

The script implements smart caching to save costs:

- **First run**: Makes API calls to GPT-4 and DALL-E
- **Subsequent runs**: Uses cached responses (you'll see "📦 Using cached...")

This is especially useful during development and testing!

## Cost Estimate

Approximate costs per run (without caching):
- GPT-4 summary: ~$0.01-0.03
- DALL-E image: ~$0.04

With caching, subsequent runs cost $0!

## Customization

### Changing the Summary Style

Edit the `generate_summary()` method in `analyze_flow.py`:

```python
prompt = f"""Analyze this user flow...
[Your custom prompt here]
"""
```

### Changing the Image Style

Edit the `generate_social_media_image()` method:

```python
prompt = f"""Create a modern image...
[Your custom image prompt here]
"""
```

### Changing the Report Format

Edit the `generate_report()` method to customize the markdown output.

## Troubleshooting

### API Key Not Found

```
❌ Error: OPENAI_API_KEY not found in environment variables
```

**Solution**: Create a `.env` file with your OpenAI API key.

### flow.json Not Found

```
❌ Error: flow.json not found
```

**Solution**: Make sure `flow.json` is in the same directory as the script.

### Module Not Found

```
ModuleNotFoundError: No module named 'openai'
```

**Solution**: Install dependencies with `pip install -r requirements.txt`

## Git Workflow

1. **First time setup**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Arcade Flow Analyzer"
   ```

2. **After running the script**:
   ```bash
   git add FLOW_REPORT.md flow_social_media_*.png
   git commit -m "Add generated flow analysis report"
   ```

3. **Important**: Never commit your `.env` file! The `.gitignore` protects you from this.

## Tips

- Run the script multiple times to see caching in action
- The generated image changes each run, but caching prevents unnecessary API calls
- You can safely delete the `.cache/` directory to force regeneration
- The script is designed to work with any Arcade flow, not just the example

## Need Help?

- Check the OpenAI API documentation: https://platform.openai.com/docs
- Review the Arcade flow structure in `flow.json`
- Look at the example output in `FLOW_REPORT.md`

