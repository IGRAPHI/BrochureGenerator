# AI-Powered Company Brochure Generator 📄

An intelligent application that automatically generates professional company brochures from any website using Google's Gemini AI.

## 🎯 Features

- **Automated Content Extraction**: Intelligently scrapes and parses website content
- **Smart Link Classification**: Uses AI to identify and categorize relevant pages (About, Products, Careers, Press, etc.)
- **Professional Brochure Generation**: Creates well-structured, marketing-ready brochures
- **Multiple Interfaces**:
  - 💻 CLI for scripting and automation
  - 🎨 Streamlit web UI for interactive use
  - 📓 Jupyter Notebook for experimentation
- **Markdown Output**: Easy to convert to PDF, HTML, or other formats

## 🚀 Use Cases

- **For Prospective Clients**: Showcase company offerings and value propositions
- **For Investors**: Highlight company vision, products, and market positioning
- **For Recruitment**: Present company culture, mission, and career opportunities

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (Python package installer - usually comes with Python)
- **Git** (for cloning the repository)
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))

---

## ⚙️ Local Installation & Setup

Follow these steps to set up the application on your local machine:

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/Nameissammy/AI-Powered-CBG.git

# Navigate to the project directory
cd AI-Powered-CBG
```

### Step 2: Create a Virtual Environment (Recommended)

**On macOS/Linux:**

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

**On Windows:**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

You should see `(venv)` prefix in your terminal, indicating the virtual environment is active.

### Step 3: Install Dependencies

```bash
# Upgrade pip (recommended)
pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**Dependencies installed:**

- `requests` - HTTP library for fetching web pages
- `google-generativeai` - Google Gemini AI SDK
- `beautifulsoup4` - HTML parsing library
- `lxml` - Parser for BeautifulSoup
- `python-dotenv` - Environment variable management
- `streamlit` - Web UI framework
- `ipython` - For Jupyter notebook support

### Step 4: Configure API Key

**Option A: Using .env file (Recommended)**

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Open `.env` file in your favorite text editor:

```bash
# macOS/Linux
nano .env

# Or use any text editor
```

3. Add your Google Gemini API key:

```env
GENAI_API_KEY=your_actual_api_key_here
```

4. Save and close the file (Ctrl+X, then Y, then Enter for nano)

**Option B: Using environment variable directly**

```bash
# macOS/Linux
export GENAI_API_KEY="your_actual_api_key_here"

# Windows (Command Prompt)
set GENAI_API_KEY=your_actual_api_key_here

# Windows (PowerShell)
$env:GENAI_API_KEY="your_actual_api_key_here"
```

### Step 5: Verify Installation

Test that everything is installed correctly:

```bash
# Check Python version
python --version

# Verify packages are installed
pip list | grep -E "requests|google-generativeai|beautifulsoup4|streamlit"

# Quick test (should not produce errors)
python -c "import requests, google.generativeai, bs4, streamlit; print('✓ All packages installed successfully')"
```

---

## 🎮 Running the Application

You can run the application in three different ways:

### Option 1: Streamlit Web UI (Recommended for Beginners) 🎨

The easiest way to use the application with a visual interface:

# Launch Streamlit app

streamlit run app.py

````

The app will automatically open in your default browser at `http://localhost:8501`

**Using the Web UI:**

1. Enter a company website URL (e.g., `https://www.anthropic.com`)
2. Click "🚀 Generate Brochure"
3. Wait for the AI to analyze and generate the brochure (30-60 seconds)
4. View the formatted brochure
5. Download as Markdown file if needed

### Option 2: Command Line Interface (CLI) 💻

For automation and scripting:

```bash
# Navigate to src directory
cd src

# Run with URL as argument
python main.py https://www.anthropic.com

# Or run interactively
python main.py
# Then enter the URL when prompted
````

**CLI Features:**

- Direct URL input via command line
- Interactive mode with prompts
- Option to save brochure to file
- Formatted console output

### Option 3: Jupyter Notebook 📓

For experimentation and customization:

```bash
# From project root directory
jupyter notebook demo.ipynb
```

Then run the cells sequentially to:

1. Test the Website class
2. Experiment with link extraction
3. Customize brochure generation
4. See step-by-step output

---

## 🛠️ Project Structure

```
AI-Powered-CBG/
├── src/
│   ├── website.py      # Website content extraction class
│   ├── utils.py        # Helper functions (link extraction, aggregation)
│   ├── main.py         # CLI interface
│   ├── app.py          # Streamlit web interface
│   └── README.md       # Source code documentation
├── demo.ipynb          # Jupyter notebook for experimentation
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── .env               # Your API keys (create this, not in git)
└── README.md          # This file
```

---

## 🧪 Quick Test

After installation, verify everything works:

```bash
cd src
python -c "
from website import Website
site = Website('https://www.python.org')
print(f'✓ Title: {site.title}')
print(f'✓ Found {len(site.links)} links')
print('✓ Installation successful!')
"
```

Expected output:

```
✓ Title: Welcome to Python.org
✓ Found 150+ links
✓ Installation successful!
```

---

## 📖 Source Code Documentation

This directory contains the source code for the AI-Powered Company Brochure Generator.

## 📁 Module Overview

### `website.py`

**Purpose**: Website content extraction and parsing

**Class**: `Website`

- Fetches and parses HTML content from any URL
- Extracts page title, body text, and all links
- Automatically cleans unwanted elements (scripts, styles, meta tags)
- Falls back to `html.parser` if `lxml` is unavailable

**Usage**:

```python
from website import Website

# Create a Website instance
site = Website("https://www.example.com")

# Access extracted data
print(site.title)           # Page title
print(site.website_content) # Cleaned text content
print(site.links)           # List of all links
```

**Key Features**:

- Timeout handling (10 seconds)
- HTTP status validation
- Safe attribute access for missing elements
- Comprehensive link extraction

---

### `utils.py`

**Purpose**: Helper functions for link classification and brochure generation

**Functions**:

#### `get_links(website: Website, model) -> dict`

Uses AI to classify and filter relevant links from a website.

**Parameters**:

- `website`: Website instance with extracted links
- `model`: Configured Gemini model for JSON output

**Returns**:

```python
{
    "links": [
        {"type": "about", "url": "https://..."},
        {"type": "products", "url": "https://..."},
        # ...
    ]
}
```

**Example**:

```python
from website import Website
from utils import get_links
import google.generativeai as genai

genai.configure(api_key="your_key")
model = genai.GenerativeModel("gemini-2.0-flash-exp")

site = Website("https://www.example.com")
classified_links = get_links(site, model)
```

#### `website_content_all(main_url: str, model) -> str`

Fetches and aggregates content from main page and relevant sub-pages.

**Parameters**:

- `main_url`: The main website URL
- `model`: Configured Gemini model

**Returns**: Aggregated markdown-formatted content string

**Example**:

```python
from utils import website_content_all

content = website_content_all("https://www.example.com", model)
print(content)
```

#### `create_brochure(website_url: str, model_brochure) -> str`

Complete pipeline for generating a professional brochure.

**Parameters**:

- `website_url`: Company website URL
- `model_brochure`: Gemini model with system instructions

**Returns**: Formatted markdown brochure

**Example**:

```python
from utils import create_brochure

brochure = create_brochure("https://www.example.com", model)
print(brochure)
```

---

### `main.py`

**Purpose**: Command-line interface for brochure generation

**Features**:

- Interactive and command-line argument modes
- Automatic URL protocol handling
- Save to file option
- Environment variable validation
- Error handling and user-friendly messages

**Usage**:

**Command-line mode**:

```bash
python main.py https://www.example.com
```

**Interactive mode**:

```bash
python main.py
# Then enter URL when prompted
```

**Environment Variables**:

- `GENAI_API_KEY`: Google Gemini API key (required)

---

### `app.py`

**Purpose**: Streamlit web interface for interactive brochure generation

**Features**:

- Modern, responsive UI with custom CSS
- API key management (`.env` or manual input)
- Progress indicators during generation
- Dual view: formatted markdown and raw code
- Download button for generated brochures
- Helpful sidebar with configuration and tips

**Usage**:

```bash
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

**UI Components**:

- URL input field with validation
- Generate button with loading states
- Tabbed output view (Formatted/Raw)
- Download button (markdown format)
- Sidebar configuration and help

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
GENAI_API_KEY=your_google_gemini_api_key
```

### Model Configuration

The application uses two Gemini model instances:

1. **Link Extraction Model** (JSON output):

```python
generation_config = {
    "response_mime_type": "application/json",
}
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config
)
```

2. **Brochure Generation Model** (with system instructions):

```python
system_prompt = """You are a professional marketing copywriter..."""
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    system_instruction=system_prompt
)
```

---

## 🧪 Testing

### Quick Test

```python
# Test Website extraction
from website import Website
site = Website("https://www.python.org")
assert site.title is not None
assert len(site.links) > 0
print("✓ Website class working")

# Test end-to-end
from utils import create_brochure
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GENAI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-exp")

brochure = create_brochure("https://www.python.org", model)
assert len(brochure) > 100
print("✓ Brochure generation working")
```

---

## 🐛 Error Handling

### Common Issues

**1. `AttributeError: 'Website' object has no attribute 'links'`**

- **Cause**: `links` not initialized before use
- **Fix**: Already handled in `Website.__init__()` with `self.links = []`

**2. `AttributeError: 'list' object has no attribute 'links'`**

- **Cause**: Passing `website.links` instead of `website` to functions
- **Fix**: Pass the entire `Website` object: `get_links(website, model)`

**3. `JSONDecodeError`**

- **Cause**: LLM response not valid JSON
- **Fix**: Handled with try-except, returns `{"links": []}`

**4. `GENAI_API_KEY not found`**

- **Cause**: Missing `.env` file or API key
- **Fix**: Create `.env` file with valid API key

**5. Request timeout**

- **Cause**: Slow website response
- **Fix**: Timeout set to 10 seconds with error handling

---

## 📊 Code Flow

```
User Input (URL)
    ↓
Website(url) → Fetch & Parse HTML
    ↓
get_links() → AI Classification
    ↓
website_content_all() → Aggregate Content
    ↓
create_brochure() → Generate Brochure
    ↓
Output (Markdown)
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. **403 Forbidden Error (Access Denied)**

**Error Message:**

```
HTTPError: 403 Client Error: Forbidden for url: https://openai.com/
```

**Cause:** Some websites (like openai.com, cloudflare-protected sites) block automated scraping requests. They detect bots and deny access.

**Solutions:**

**Option A - Try Alternative URLs:**
Many company websites have subdomains that are less restricted:

- Instead of `https://openai.com`, try `https://openai.com/about` or `https://platform.openai.com`
- Instead of main homepage, try specific pages like `/about`, `/products`, `/blog`

**Option B - Use Different Websites:**
Some websites that generally work well:

- ✅ `https://www.anthropic.com`
- ✅ `https://www.python.org`
- ✅ `https://github.com`
- ✅ Most corporate/marketing websites
- ❌ `https://openai.com` (blocks automation)
- ❌ Sites behind Cloudflare protection
- ❌ Sites with aggressive bot detection

**Option C - Manual Content Input:**
For blocked sites, you can:

1. Manually copy the website content
2. Create a local HTML file
3. Modify the code to accept text input instead of URLs

**What We've Done:**

- Added comprehensive browser headers to mimic real browsers
- Included modern User-Agent string
- Added Accept headers and other browser metadata

**Note:** Even with headers, some websites use advanced bot detection (CAPTCHA, JavaScript challenges, IP filtering) that cannot be bypassed with simple HTTP requests.

#### 2. **Timeout Error**

**Error Message:**

```
Request timeout for [URL]. The website took too long to respond.
```

**Solutions:**

- Check your internet connection
- The website might be slow or down - try again later
- Try a different website
- Increase timeout in `website.py` (currently 10 seconds)

#### 3. **Connection Error**

**Error Message:**

```
Connection error for [URL]. Check your internet connection or the URL.
```

**Solutions:**

- Verify the URL is correct and includes `https://` or `http://`
- Check your internet connection
- Try accessing the URL in your browser first
- The website might be down temporarily

#### 4. **AttributeError: 'Website' object has no attribute 'links'**

**Cause:** The `links` list wasn't initialized before use (already fixed in current version)

**Solution:** Update to latest code where `self.links = []` is in `__init__`

#### 5. **JSONDecodeError when getting links**

**Cause:** The AI model didn't return valid JSON

**Solution:**

- Already handled with try-except that returns `{"links": []}`
- If persistent, check your API key and quota
- The model might be overloaded - try again

#### 6. **GENAI_API_KEY not found**

**Cause:** Missing or incorrectly configured `.env` file

**Solutions:**

1. Create `.env` file in project root (not in `src/`)
2. Add: `GENAI_API_KEY=your_actual_key_here`
3. No quotes needed around the key
4. Make sure there are no spaces around the `=`
5. Restart your terminal/application after creating `.env`

#### 7. **Module not found errors**

**Error Messages:**

```
ModuleNotFoundError: No module named 'requests'
ModuleNotFoundError: No module named 'google.generativeai'
```

**Solutions:**

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

---

## 💡 Best Practices

### Choosing Websites

**✅ Good Choices:**

- Corporate/company marketing websites
- Educational institutions
- Open-source project pages
- Government/public sector sites
- Most .org and .edu domains

**❌ Avoid:**

- Sites explicitly blocking bots in robots.txt
- Sites behind login walls
- Social media platforms
- Sites with heavy JavaScript/SPA architecture
- E-commerce sites with anti-scraping measures

### Testing Before Full Run

Always test with a simple URL first:

```bash
cd src
python -c "
from website import Website
site = Website('https://www.example.com')
print(f'Works! Title: {site.title}')
"
```

### Respecting Website Policies

- Check `robots.txt` (e.g., `https://example.com/robots.txt`)
- Respect rate limits
- Don't overload servers with rapid requests
- Use responsibly for educational/research purposes

---

## 🎯 Design Patterns

- **Single Responsibility**: Each module has one clear purpose
- **Dependency Injection**: Models passed as parameters
- **Error Recovery**: Graceful fallbacks for failures
- **Type Hints**: Clear function signatures
- **Docstrings**: Comprehensive documentation

---

## 🔒 Security Notes

- API keys loaded from environment variables (never hardcoded)
- `.env` file excluded from version control (add to `.gitignore`)
- HTTP timeout prevents hanging requests
- Input validation for URLs

---

## 📝 Contributing

When adding new features:

1. Follow existing code structure
2. Add type hints to function signatures
3. Include docstrings with examples
4. Handle errors gracefully
5. Update this README

---

## 🚀 Performance Tips

- **Batch Processing**: Process multiple URLs in sequence
- **Caching**: Cache website content to avoid re-fetching
- **Async Requests**: Use `aiohttp` for parallel fetching (future enhancement)
- **Rate Limiting**: Respect API quotas

---

**Last Updated**: October 2025  
**Python Version**: 3.8+  
**Dependencies**: See `requirements.txt` in project root
