# Source Code Documentation

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
