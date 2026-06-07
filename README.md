# AI Presentation & Brochure Studio 🎯

A multipage Streamlit app with two tools:

- **📊 Presentation Strategy Studio** — a creative-director-style intake that turns a few smart questions into a detailed, mode-adaptive creative brief plus build-ready outputs (slide outline, speaker notes, design direction, a PowerPoint-ready content plan, and AI prompts for visuals). It helps you understand the presentation *before* you design a single slide. See [docs/CREATIVE_BRIEF_FEATURE.md](docs/CREATIVE_BRIEF_FEATURE.md).
- **📄 Company Brochure Generator** — automatically generates a professional company brochure from any website URL (documented below).

Run `streamlit run app.py` and switch between the two tools from the sidebar. The Strategy Studio is the default landing page.

## 🤖 AI providers — Claude first, Gemini optional, Demo Mode always-on

The app is **not hard-coded to one model**. A small provider layer (`providers.py`) lets you choose:

| Mode | When it's used | Requires |
| --- | --- | --- |
| **Claude (default & preferred)** | `AI_PROVIDER=claude` (default) | `ANTHROPIC_API_KEY` |
| **Gemini (optional)** | `AI_PROVIDER=gemini` | `GEMINI_API_KEY` (legacy `GENAI_API_KEY` also accepted) |
| **Demo Mode** | no key found, or `AI_PROVIDER=demo` | nothing — runs offline with illustrative output |

**Use Claude first.** Set one environment variable and you're done:

```bash
# .env  (copy from .env.example)
AI_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-...
# ANTHROPIC_MODEL=claude-opus-4-8   # optional override (this is the default)
```

Claude is the default for the creative brief, slide strategy, structure, design direction, and speaker-support notes. The Strategy Studio defaults to Claude Opus 4.8 (override with `ANTHROPIC_MODEL`).

**Gemini is only an optional alternative.** Switch with:

```bash
AI_PROVIDER=gemini
GEMINI_API_KEY=...
# GEMINI_MODEL=gemini-2.0-flash-exp   # optional override
```

**No key? It still runs.** With no key configured the app falls back to **Demo Mode** and produces clearly-labeled sample output so you can explore the full flow (and PDF export) without an API key. You can also pick the provider and paste a key directly in the sidebar at runtime.

> Note: the Company Brochure Generator uses Gemini specifically (it scrapes + classifies website content). It accepts `GEMINI_API_KEY` or the legacy `GENAI_API_KEY`.

## 🔐 Configuring the API key securely

**Add the key as an environment variable or a platform secret — never commit it to the repository.**

- `.env` is already in `.gitignore`, so a local `.env` file is safe for development and is **not** tracked by git. Copy `.env.example` → `.env` and fill in your key locally.
- For hosted/CI/Claude Code on the web, set `ANTHROPIC_API_KEY` as an **environment variable / secret** in the platform's settings rather than putting it in a file.
- The values shown in this README and in `.env.example` (e.g. `sk-ant-...`) are **placeholders**, not real keys.

```bash
# Local development
cp .env.example .env
# then edit .env and set:
#   AI_PROVIDER=claude
#   ANTHROPIC_API_KEY=<your key>   # placeholder — paste your real key locally only
```

```bash
# Or export it in your shell / CI (not committed anywhere)
export AI_PROVIDER=claude
export ANTHROPIC_API_KEY=...        # your key
```

**Verify it's working without exposing the key:**

```bash
python creative_brief.py --check    # prints "OK: Claude connection OK ..." or a redacted error
```

You can also click **🔌 Test connection** in the app sidebar.

**Security guarantees in the code:** the app never prints, logs, or writes the API key to the interface, console, test output, or any generated file. Provider/error messages are passed through a redaction filter (`providers.redact`) and tracebacks are not shown in the UI, so key material cannot leak even on failure. If you accidentally commit a real key, rotate it immediately.

---

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

## ✨ Key Features

- 🤖 **AI-Powered Analysis**: Uses Google Gemini 2.0 Flash for intelligent content extraction
- 🔗 **Smart Link Classification**: Automatically identifies relevant pages (About, Products, Careers, etc.)
- 📄 **PDF Export**: Generate professional PDF brochures with custom styling
- 🎨 **Multiple Formats**: Export as Markdown or PDF
- 🌐 **Web & CLI Interface**: Choose your preferred interaction mode
- 🔒 **Privacy-Focused**: All processing done locally with your API key

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
- `reportlab` - Professional PDF generation library
- `markdown2` - Markdown parsing for PDF conversion
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

**🎉 Quick Start (Recommended):**

For the smoothest experience with all features including PDF generation, use our startup script:

```bash
# Make the script executable (first time only)
chmod +x start.sh

# Run the app with proper environment setup
./start.sh
```

The script will:
- ✅ Check/create virtual environment
- ✅ Activate the environment automatically
- ✅ Install all required dependencies
- ✅ Verify PDF generation support
- ✅ Launch Streamlit with correct configuration

**Using the Web UI:**

1. Enter a company website URL (e.g., `https://www.anthropic.com`)
2. Click "🚀 Generate Brochure"
3. Wait for the AI to analyze and generate the brochure (30-60 seconds)
4. View the beautifully formatted brochure with professional styling
5. Download the brochure:
   - **⬇️ Download as Markdown (.md)**: Original markdown format
   - **⬇️ Download as PDF (.pdf)**: Professional PDF document with A4 formatting, color-coded headings, and clean typography

**✨ Features:**
- 🔄 **Persistent Display**: Generated brochure stays visible after downloading - no need to regenerate!
- 💾 **Session State**: Content is preserved until you enter a new URL
- 📥 **Multiple Downloads**: Download as many times as you want without regenerating
- 🔀 **Smart Refresh**: Only clears content when you change the URL

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
├── website.py      # Website content extraction class
├── utils.py        # Helper functions (link extraction, aggregation)
├── main.py         # Core business logic + CLI interface (does heavy lifting)
├── app.py          # Streamlit web interface (imports from main.py)
├── docs/
│   ├── PDF_FEATURE.md                  # PDF generation feature documentation
│   ├── PDF_IMPLEMENTATION_SUMMARY.md   # Technical implementation details
│   ├── TROUBLESHOOTING_PDF.md          # PDF troubleshooting guide
│   └── WEBSITE_COMPATIBILITY.md        # Website compatibility guide
├── requirements.txt    # Python dependencies
├── start.sh           # Quick startup script (recommended)
├── .env.example       # Environment variables template
├── .env              # Your API keys (create this, not in git)
└── README.md         # This file
```

### 🏗️ Architecture Overview

The project follows the **DRY (Don't Repeat Yourself)** principle:

- **`main.py`**: Contains all core business logic and reusable functions
  - `generate_brochure()` - Main brochure generation function
  - `markdown_to_pdf()` - PDF conversion logic
  - `get_api_key()`, `configure_genai()`, `get_model()` - Configuration helpers
  - CLI interface for command-line usage
- **`app.py`**: Lightweight Streamlit UI that imports from `main.py`

  - No duplicate code
  - Focuses only on UI/UX concerns
  - Calls `main.py` functions for all business logic

- **`utils.py`**: Website-specific utilities

  - `get_links()` - AI-powered link classification
  - `website_content_all()` - Content aggregation
  - `create_brochure()` - Brochure generation pipeline

- **`website.py`**: Website scraping and parsing
  - `Website` class for content extraction

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

### 📁 Module Overview

#### `main.py` - Core Business Logic (Heavy Lifting)

**Purpose**: Central module containing all core business logic and reusable functions. Both CLI and Streamlit app import from this module.

**Key Functions**:

##### `generate_brochure(website_url: str, api_key: str = None) -> str`

The main function for generating company brochures. Used by both CLI and Streamlit app.

```python
from main import generate_brochure

brochure = generate_brochure("https://www.example.com")
print(brochure)
```

##### `markdown_to_pdf(markdown_text: str) -> BytesIO`

Converts markdown text to professionally styled PDF with A4 format and custom CSS.

```python
from main import markdown_to_pdf

pdf_buffer = markdown_to_pdf(brochure_text)
with open("output.pdf", "wb") as f:
    f.write(pdf_buffer.getvalue())
```

##### Helper Functions

- `get_api_key()` - Retrieves API key from environment
- `configure_genai(api_key)` - Configures Gemini AI
- `get_model(system_instruction)` - Returns configured Gemini model
- `normalize_url(url)` - Ensures URL has proper protocol

**CLI Usage**:

```bash
# Interactive mode
python main.py

# Command-line mode
python main.py https://www.example.com
```

---

#### `app.py` - Streamlit Web Interface (Lightweight)

**Purpose**: Provides web UI for interactive brochure generation. Imports all business logic from `main.py`.

**Architecture**: Follows separation of concerns

- UI rendering and user interactions only
- All business logic delegated to `main.py`
- No code duplication
- Uses Streamlit session state for persistent display

**Key Features**:

- 🔄 **Session State Management**: Brochure persists after downloads
- 💾 **Smart Caching**: Content stays visible until URL changes
- 📥 **Multiple Downloads**: No need to regenerate for each download
- 🔀 **Auto-Clear**: Automatically clears when entering a new URL

**Imported Functions**:

```python
from main import (
    get_api_key,
    generate_brochure,
    markdown_to_pdf,
    PDF_AVAILABLE
)
```

**Session State Variables**:

```python
st.session_state.brochure      # Stores generated brochure
st.session_state.last_url      # Tracks current URL
```

**Usage**:

```bash
streamlit run app.py
```

---

#### `website.py`

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

#### `utils.py`

**Purpose**: Website-specific helper functions for link classification and brochure generation

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

#### `create_brochure(website_url: str, model_brochure) -> str`

Complete pipeline for generating a professional brochure. Called by `main.generate_brochure()`.

**Parameters**:

- `website_url`: Company website URL
- `model_brochure`: Gemini model with system instructions

**Returns**: Formatted markdown brochure

**Example**:

```python
from utils import create_brochure
import google.generativeai as genai

genai.configure(api_key="your_key")
model = genai.GenerativeModel("gemini-2.0-flash-exp")

brochure = create_brochure("https://www.example.com", model)
print(brochure)
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
GENAI_API_KEY=your_google_gemini_api_key
```

### Model Configuration

The application uses Gemini models configured in `main.py`:

**System Prompt** (defined in `main.py` as `SYSTEM_PROMPT`):

```python
SYSTEM_PROMPT = """You are a professional marketing copywriter that creates detailed,
engaging company brochures based on website content. Your brochures are well-structured,
informative, and highlight the company's key strengths and offerings."""
```

**Model Instance** (created by `get_model()` function):

```python
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    system_instruction=SYSTEM_PROMPT
)
```

**Link Extraction Model** (configured in `utils.py`):

```python
generation_config = {
    "response_mime_type": "application/json",
}
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config
)
```

---

## 🧪 Testing

### Quick Test - CLI

```bash
# Test brochure generation
python main.py https://www.anthropic.com
```

### Quick Test - Programmatic

```python
# Test main.py functions
from main import generate_brochure, get_api_key

api_key = get_api_key()
brochure = generate_brochure("https://www.python.org", api_key)
print(f"✓ Generated {len(brochure)} characters")

# Test Website extraction
from website import Website
site = Website("https://www.python.org")
assert site.title is not None
assert len(site.links) > 0
print("✓ Website class working")
```

### Quick Test - Streamlit

```bash
# Launch Streamlit and test in browser
streamlit run app.py
```

---

## 🐛 Error Handling

### Common Issues

**1. Import errors from main.py**

- **Cause**: `app.py` cannot find functions from `main.py`
- **Fix**: Ensure both files are in the same directory and run from project root

**2. `AttributeError: 'Website' object has no attribute 'links'`**

- **Cause**: `links` not initialized before use
- **Fix**: Already handled in `Website.__init__()` with `self.links = []`

**3. `AttributeError: 'list' object has no attribute 'links'`**

- **Cause**: Passing `website.links` instead of `website` to functions
- **Fix**: Pass the entire `Website` object: `get_links(website, model)`

**4. `JSONDecodeError`**

- **Cause**: LLM response not valid JSON
- **Fix**: Handled with try-except, returns `{"links": []}`

**5. `GENAI_API_KEY not found`**

- **Cause**: Missing `.env` file or API key
- **Fix**: Create `.env` file with valid API key

**6. Request timeout**

- **Cause**: Slow website response
- **Fix**: Timeout set to 10 seconds with error handling

---

## 📊 Code Flow

```
User Input (URL)
    ↓
main.generate_brochure() → Validates & configures
    ↓
utils.create_brochure() → Orchestrates generation
    ↓
Website(url) → Fetches & parses HTML
    ↓
utils.get_links() → AI classification
    ↓
utils.website_content_all() → Aggregates content
    ↓
Gemini AI → Generates brochure
    ↓
main.markdown_to_pdf() [optional] → PDF conversion
    ↓
Output (Markdown/PDF)
```

### Function Call Hierarchy

```
CLI (main.py)
├── main() → Entry point
└── generate_brochure() → Core logic

Streamlit (app.py)
└── generate_brochure() [imported from main] → Core logic

Shared Core (main.py)
├── generate_brochure()
│   ├── configure_genai()
│   ├── normalize_url()
│   ├── get_model()
│   └── create_brochure() [from utils]
└── markdown_to_pdf()

Utilities (utils.py)
├── create_brochure()
│   ├── Website() [from website.py]
│   ├── get_links()
│   └── website_content_all()
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. **PDF Download Not Working / Module Errors**

**Error Message:**

```
ModuleNotFoundError: No module named 'reportlab'
```

**Cause:** The PDF generation libraries aren't installed or Streamlit is running from the wrong Python environment.

**Solutions:**

**🚀 Quick Fix (Recommended):**

```bash
# Run the startup script which handles everything
./start.sh
```

**Manual Fix:**

```bash
# Activate your virtual environment first!
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Install the PDF libraries
pip install reportlab markdown2

# Verify they're installed
python -c "from reportlab.lib.pagesizes import A4; import markdown2; print('✅ PDF support ready!')"

# Now run Streamlit from the same environment
streamlit run app.py
```

**💡 Why This Happens:**

- You might have multiple Python installations
- Streamlit might be running from a different environment than where libraries are installed
- The virtual environment wasn't activated before running Streamlit

**📚 Detailed Troubleshooting:**
See [TROUBLESHOOTING_PDF.md](docs/TROUBLESHOOTING_PDF.md) for comprehensive solutions.

---

#### 2. **403 Forbidden Error (Access Denied)**

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
- Most corporate/marketing websites
- ❌ `https://openai.com` (blocks automation)
- ❌ Sites behind Cloudflare protection
- ❌ Sites with aggressive bot detection

**📚 Full Compatibility List:**
See [WEBSITE_COMPATIBILITY.md](WEBSITE_COMPATIBILITY.md) for detailed examples.

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

**📚 Detailed Website Compatibility Guide:**
See [WEBSITE_COMPATIBILITY.md](WEBSITE_COMPATIBILITY.md) for a comprehensive list of working and blocked websites.

---

#### 3. **Timeout Error**

**Error Message:**

```
Request timeout for [URL]. The website took too long to respond.
```

**Solutions:**

- Check your internet connection
- The website might be slow or down - try again later
- Try a different website
- Increase timeout in `website.py` (currently 10 seconds)

---

#### 4. **Connection Error**

**Error Message:**

```
Connection error for [URL]. Check your internet connection or the URL.
```

**Solutions:**

- Verify the URL is correct and includes `https://` or `http://`
- Check your internet connection
- Try accessing the URL in your browser first
- The website might be down temporarily

---

#### 5. **AttributeError: 'Website' object has no attribute 'links'**

**Cause:** The `links` list wasn't initialized before use (already fixed in current version)

**Solution:** Update to latest code where `self.links = []` is in `__init__`

---

#### 6. **JSONDecodeError when getting links**

**Cause:** The AI model didn't return valid JSON

**Solution:**

- Already handled with try-except that returns `{"links": []}`
- If persistent, check your API key and quota
- The model might be overloaded - try again

---

#### 7. **GENAI_API_KEY not found**

**Cause:** Missing or incorrectly configured `.env` file

**Solutions:**

1. Create `.env` file in project root (not in `src/`)
2. Add: `GENAI_API_KEY=your_actual_key_here`
3. No quotes needed around the key
4. Make sure there are no spaces around the `=`

- Restart your terminal/application after creating `.env`

---

#### 8. **Module not found errors**

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

## 📚 Additional Documentation

- **[PDF_FEATURE.md](docs/PDF_FEATURE.md)**: Comprehensive PDF generation feature guide
- **[TROUBLESHOOTING_PDF.md](docs/TROUBLESHOOTING_PDF.md)**: Solutions for PDF-related issues
- **[WEBSITE_COMPATIBILITY.md](WEBSITE_COMPATIBILITY.md)**: Which websites work and which don't
- **[src/README.md](src/README.md)**: Detailed source code documentation

---

## 🎯 Design Patterns

- **Single Responsibility Principle**: Each module has one clear purpose
  - `main.py` - Core business logic and CLI
  - `app.py` - UI/UX only
  - `utils.py` - Website utilities
  - `website.py` - Content extraction
- **DRY (Don't Repeat Yourself)**: No code duplication
  - `app.py` imports all logic from `main.py`
  - Shared functions centralized in `main.py`
- **Dependency Injection**: Models and configurations passed as parameters

- **Separation of Concerns**: UI completely separated from business logic

- **Error Recovery**: Graceful fallbacks for failures

- **Type Hints**: Clear function signatures throughout

- **Docstrings**: Comprehensive documentation for all functions

---

## 🔒 Security Notes

- API keys loaded from environment variables (never hardcoded)
- `.env` file excluded from version control (add to `.gitignore`)
- HTTP timeout prevents hanging requests
- Input validation for URLs

---

## 📝 Contributing

When adding new features:

1. **Follow the architecture**:
   - Core logic goes in `main.py`
   - UI changes go in `app.py` (import from main)
   - Website utilities go in `utils.py`
2. **Maintain DRY principle**:
   - Don't duplicate code between CLI and Streamlit
   - Create reusable functions in `main.py`
3. **Code quality**:
   - Add type hints to function signatures
   - Include docstrings with examples
   - Handle errors gracefully
   - Write clean, readable code
4. **Documentation**:

   - Update this README
   - Add comments for complex logic
   - Update relevant docs/ files

5. **Testing**:
   - Test both CLI and Streamlit interfaces
   - Verify PDF generation works
   - Check error handling

---

## 🚀 Performance Tips

- **Code Organization**: Following DRY principle reduces maintenance overhead
- **Batch Processing**: Process multiple URLs in sequence using `main.py` CLI
- **Caching**: Cache website content to avoid re-fetching (future enhancement)
- **Async Requests**: Use `aiohttp` for parallel fetching (future enhancement)
- **Rate Limiting**: Respect API quotas
- **Modular Import**: `app.py` only imports what it needs from `main.py`

---

## 📚 Additional Documentation

- **[PDF_FEATURE.md](docs/PDF_FEATURE.md)**: Comprehensive PDF generation feature guide
- **[TROUBLESHOOTING_PDF.md](docs/TROUBLESHOOTING_PDF.md)**: Solutions for PDF-related issues
- **[WEBSITE_COMPATIBILITY.md](docs/WEBSITE_COMPATIBILITY.md)**: Which websites work and which don't
- **[PDF_IMPLEMENTATION_SUMMARY.md](docs/PDF_IMPLEMENTATION_SUMMARY.md)**: Technical implementation details

---

**Last Updated**: October 2025  
**Python Version**: 3.8+  
**Architecture**: DRY principle with main.py doing heavy lifting  
**Dependencies**: See `requirements.txt` in project root
