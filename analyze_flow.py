#!/usr/bin/env python3
"""
Arcade Flow Analyzer
Analyzes Arcade flow recordings and generates comprehensive reports.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
import hashlib
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Cache directory
CACHE_DIR = Path('.cache')
CACHE_DIR.mkdir(exist_ok=True)


class CacheManager:
    """Manages caching of expensive API responses."""
    
    @staticmethod
    def get_cache_key(data: Any) -> str:
        """Generate a cache key from data."""
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.md5(json_str.encode()).hexdigest()
    
    @staticmethod
    def get_cached(cache_key: str) -> Any:
        """Retrieve cached data."""
        cache_file = CACHE_DIR / f"{cache_key}.json"
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)
        return None
    
    @staticmethod
    def set_cache(cache_key: str, data: Any):
        """Store data in cache."""
        cache_file = CACHE_DIR / f"{cache_key}.json"
        with open(cache_file, 'w') as f:
            json.dump(data, f, indent=2)


class FlowAnalyzer:
    """Analyzes Arcade flow recordings."""
    
    def __init__(self, flow_path: str):
        """Initialize with path to flow.json."""
        with open(flow_path, 'r') as f:
            self.flow_data = json.load(f)
        self.cache = CacheManager()
    
    def extract_user_interactions(self) -> List[Dict[str, Any]]:
        """Extract human-readable user interactions from the flow."""
        interactions = []
        steps = self.flow_data.get('steps', [])
        
        for step in steps:
            step_type = step.get('type')
            
            if step_type == 'CHAPTER':
                # Chapter steps are navigational/informational
                title = step.get('title', '')
                if title and 'thank you' not in title.lower():
                    interactions.append({
                        'type': 'chapter',
                        'action': f"Started section: {title}",
                        'details': step.get('subtitle', '')
                    })
            
            elif step_type == 'IMAGE':
                # IMAGE steps typically represent user clicks
                click_context = step.get('clickContext', {})
                page_context = step.get('pageContext', {})
                hotspots = step.get('hotspots', [])
                
                element_text = click_context.get('text', '')
                element_type = click_context.get('elementType', '')
                url = page_context.get('url', '')
                
                # Generate human-readable action
                action = self._generate_action_description(
                    element_text, element_type, click_context, page_context, hotspots
                )
                
                if action:
                    interactions.append({
                        'type': 'click',
                        'action': action,
                        'url': url,
                        'element_type': element_type
                    })
            
            elif step_type == 'VIDEO':
                # Video steps show user interactions in motion (typing, scrolling, etc.)
                # We can infer from captured events
                pass
        
        # Also extract from captured events
        events = self.flow_data.get('capturedEvents', [])
        for event in events:
            event_type = event.get('type')
            if event_type == 'typing':
                interactions.append({
                    'type': 'typing',
                    'action': 'Typed search query',
                    'details': 'User entered text in search field'
                })
            elif event_type == 'scrolling':
                interactions.append({
                    'type': 'scroll',
                    'action': 'Scrolled page to view more content',
                    'details': 'User browsed through available options'
                })
        
        return interactions
    
    def _generate_action_description(
        self, text: str, element_type: str, click_context: Dict, 
        page_context: Dict, hotspots: List
    ) -> str:
        """Generate a human-readable description of an action."""
        
        # Get hotspot label if available (usually most descriptive)
        if hotspots:
            hotspot_label = hotspots[0].get('label', '')
            if hotspot_label:
                # Clean up the hotspot label for readability
                return hotspot_label.replace('*', '').strip()
        
        # Fallback to generating from context
        if element_type == 'button':
            if 'cart' in text.lower():
                return f"Clicked '{text}' button"
            return f"Clicked the '{text}' button"
        
        elif element_type == 'image':
            if text:
                return f"Clicked on '{text}' image"
            return "Clicked on product image"
        
        elif element_type == 'link':
            if 'cart' in text.lower():
                return "Clicked on shopping cart icon to view cart"
            return f"Clicked link: {text}"
        
        elif element_type == 'other' and 'search' in text.lower():
            return "Clicked the search bar to start looking for products"
        
        return f"Interacted with {text}" if text else "Performed an action"
    
    def generate_summary(self, interactions: List[Dict[str, Any]]) -> str:
        """Generate a human-friendly summary using GPT-4."""
        
        # Create cache key
        cache_key = self.cache.get_cache_key({
            'task': 'summary',
            'flow_name': self.flow_data.get('name', ''),
            'interactions': interactions
        })
        
        # Check cache
        cached = self.cache.get_cached(cache_key)
        if cached:
            print("📦 Using cached summary")
            return cached['summary']
        
        # Prepare context for GPT
        flow_name = self.flow_data.get('name', 'Unknown Flow')
        interaction_list = "\n".join([
            f"{i+1}. {interaction['action']}"
            for i, interaction in enumerate(interactions)
        ])
        
        prompt = f"""Analyze this user flow recording from Arcade and provide a comprehensive summary.

Flow Name: {flow_name}

User Actions:
{interaction_list}

Please provide:
1. A clear, 2-3 sentence summary of what the user was trying to accomplish
2. The key steps they took to achieve this goal
3. Any notable patterns or insights about their behavior

Write in a friendly, professional tone suitable for a product demo or tutorial."""
        
        print("🤖 Generating summary with GPT-4...")
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "You are an expert at analyzing user behavior and creating clear, engaging summaries of user flows."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        summary = response.choices[0].message.content.strip()
        
        # Cache the result
        self.cache.set_cache(cache_key, {'summary': summary})
        
        return summary
    
    def generate_social_media_image(self, summary: str) -> str:
        """Generate a creative social media image using DALL-E."""
        
        flow_name = self.flow_data.get('name', 'Arcade Flow')
        
        # Create cache key
        cache_key = self.cache.get_cache_key({
            'task': 'image',
            'flow_name': flow_name,
            'summary': summary
        })
        
        # Check cache
        cached = self.cache.get_cached(cache_key)
        if cached:
            print("📦 Using cached image URL")
            image_url = cached['image_url']
        else:
            # Generate image with DALL-E
            prompt = f"""Create a modern, eye-catching social media image for a product tutorial.

Theme: {flow_name}

The image should:
- Feature a clean, modern e-commerce interface design
- Show a shopping journey with visual elements like a search bar, product cards, and a shopping cart
- Use a vibrant color scheme with blues, reds, and whites (Target brand colors)
- Include abstract representations of user interactions (clicks, selections)
- Have a professional, engaging look suitable for social media
- Show the concept of online shopping made easy
- No text in the image

Style: Modern, minimal, professional, engaging, suitable for LinkedIn or Twitter"""
            
            print("🎨 Generating social media image with DALL-E...")
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            
            # Cache the result
            self.cache.set_cache(cache_key, {'image_url': image_url})
        
        # Download the image
        import requests
        
        image_filename = f"flow_social_media_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        print(f"💾 Downloading image to {image_filename}...")
        img_data = requests.get(image_url).content
        with open(image_filename, 'wb') as f:
            f.write(img_data)
        
        return image_filename
    
    def generate_report(self) -> str:
        """Generate comprehensive markdown report."""
        
        print("\n🔍 Analyzing flow...")
        interactions = self.extract_user_interactions()
        
        print("📝 Generating summary...")
        summary = self.generate_summary(interactions)
        
        print("🖼️  Creating social media image...")
        image_filename = self.generate_social_media_image(summary)
        
        # Generate markdown report
        flow_name = self.flow_data.get('name', 'Unknown Flow')
        flow_description = self.flow_data.get('description', 'No description available')
        
        report = f"""# Arcade Flow Analysis Report

**Flow Name:** {flow_name}

**Generated:** {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

---

## 📊 Overview

{summary}

---

## 👆 User Interactions

The following actions were performed during this flow:

"""
        
        # Add interactions
        for i, interaction in enumerate(interactions, 1):
            action = interaction['action']
            report += f"{i}. **{action}**\n"
            
            if interaction.get('details'):
                report += f"   - _{interaction['details']}_\n"
            
            report += "\n"
        
        report += f"""---

## 🎯 Key Insights

This flow demonstrates a typical e-commerce user journey on Target.com. The user successfully:

- Navigated to the website and used the search functionality
- Browsed through product listings to find the right item
- Viewed product details and explored customization options (colors)
- Made a purchase decision and added the item to their cart
- Handled optional add-ons (protection plan)
- Completed the add-to-cart process

The flow showcases a smooth, intuitive shopping experience with clear calls-to-action at each step.

---

## 🖼️ Social Media Image

![Flow Social Media Image](./{image_filename})

*Generated image suitable for sharing on social platforms*

---

## 📈 Flow Statistics

- **Total Steps:** {len(self.flow_data.get('steps', []))}
- **User Interactions:** {len(interactions)}
- **Flow Type:** {self.flow_data.get('useCase', 'Unknown')}
- **Created With:** {self.flow_data.get('createdWith', 'Unknown')}

---

## 🔗 Resources

- **Original Flow:** [View on Arcade](https://app.arcade.software/share/{self.flow_data.get('uploadId', '')})

---

*Report generated by Arcade Flow Analyzer*
"""
        
        return report


def main():
    """Main entry point."""
    
    print("🚀 Arcade Flow Analyzer")
    print("=" * 50)
    
    # Check for API key
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY not found in environment variables")
        print("Please create a .env file with your OpenAI API key")
        sys.exit(1)
    
    # Check for flow.json
    flow_path = 'flow.json'
    if not os.path.exists(flow_path):
        print(f"❌ Error: {flow_path} not found")
        sys.exit(1)
    
    try:
        # Analyze flow
        analyzer = FlowAnalyzer(flow_path)
        report = analyzer.generate_report()
        
        # Save report
        report_filename = 'FLOW_REPORT.md'
        with open(report_filename, 'w') as f:
            f.write(report)
        
        print(f"\n✅ Analysis complete!")
        print(f"📄 Report saved to: {report_filename}")
        print(f"\n🎉 All done! You can now commit these files to your repository.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

