# Website Compatibility Guide

## 🟢 Tested & Working Websites

These websites are confirmed to work well with the brochure generator:

- ✅ **Anthropic**: https://www.anthropic.com
- ✅ **Python**: https://www.python.org
- ✅ **GitHub**: https://github.com
- ✅ **Mozilla**: https://www.mozilla.org
- ✅ **Wikipedia**: https://en.wikipedia.org
- ✅ **Khan Academy**: https://www.khanacademy.org
- ✅ **Django**: https://www.djangoproject.com
- ✅ **React**: https://react.dev
- ✅ **Stripe**: https://stripe.com
- ✅ **Shopify**: https://www.shopify.com

## 🟡 Partially Working / May Have Issues

- ⚠️ **AWS**: https://aws.amazon.com (slow, may timeout)
- ⚠️ **Microsoft**: https://www.microsoft.com (large, slow loading)
- ⚠️ **Google**: https://about.google (redirects, complex structure)

## 🔴 Known to Block Automated Requests

These websites actively block or restrict automated access:

- ❌ **OpenAI**: https://openai.com (403 Forbidden)
- ❌ **Cloudflare**: https://www.cloudflare.com (bot protection)
- ❌ **LinkedIn**: https://www.linkedin.com (requires login)
- ❌ **Twitter/X**: https://twitter.com (API only)
- ❌ **Facebook**: https://www.facebook.com (requires login)
- ❌ **Instagram**: https://www.instagram.com (requires login)

## 🎯 Workarounds for Blocked Sites

### For OpenAI and Similar Sites

**Option 1: Try specific pages instead of homepage**

```python
# Instead of:
website = Website("https://openai.com")

# Try:
website = Website("https://platform.openai.com/docs")
website = Website("https://openai.com/blog")
```

**Option 2: Use Internet Archive**

```python
# Use Wayback Machine cached version
website = Website("https://web.archive.org/web/20231001000000/https://openai.com")
```

**Option 3: Manual content extraction**

1. Open the website in your browser
2. Copy the HTML source (View Page Source)
3. Save to a local file
4. Modify the code to parse local files

### For Sites with CAPTCHA/Cloudflare

These sites cannot be scraped with simple HTTP requests. Alternatives:

- Use official APIs if available
- Use browser automation (Selenium/Playwright) - more complex
- Request permission from the website owner

## 📝 Testing New Websites

Before using a website with the full brochure generator, test it first:

```bash
cd src
python3 << 'EOF'
from website import Website

test_url = "https://your-website.com"  # Replace with your URL

try:
    site = Website(test_url)
    print(f"✅ SUCCESS!")
    print(f"Title: {site.title}")
    print(f"Links found: {len(site.links)}")
    print(f"Content length: {len(site.website_content)} chars")
except Exception as e:
    print(f"❌ FAILED: {e}")
EOF
```

## 🔍 How to Check if a Site Will Work

### Method 1: Check robots.txt

```
https://example.com/robots.txt
```

Look for:

- `User-agent: *` with `Disallow: /` = Site blocks all bots
- `Disallow:` with specific paths = Only those paths blocked
- No robots.txt or empty = Generally allows scraping

### Method 2: Try a simple curl request

```bash
curl -I https://example.com \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
```

- Status `200 OK` = Good
- Status `403 Forbidden` = Blocked
- Status `429 Too Many Requests` = Rate limited

### Method 3: Browser Developer Tools

1. Open the website in browser
2. Open Developer Tools (F12)
3. Go to Network tab
4. Refresh page
5. Check if there are anti-bot scripts (Cloudflare, Recaptcha, etc.)

## 🎓 Understanding Bot Detection

### Why Some Sites Block Bots

1. **Security**: Prevent DDoS attacks and malicious scraping
2. **Business**: Protect proprietary data and content
3. **Performance**: Reduce server load from automated requests
4. **Legal**: Comply with data protection laws

### What Gives Away a Bot

1. ❌ Missing or generic User-Agent header
2. ❌ Too many requests in short time
3. ❌ No JavaScript execution
4. ❌ Missing browser fingerprinting data
5. ❌ Suspicious request patterns
6. ❌ Known data center IP addresses

### What We Do to Mimic Browsers

1. ✅ Realistic User-Agent header
2. ✅ Standard Accept headers
3. ✅ Browser-like request headers
4. ✅ Reasonable timeout settings

### What We Can't Do (Without Advanced Tools)

- Execute JavaScript
- Handle CAPTCHAs
- Maintain session/cookies across requests
- Bypass Cloudflare challenges
- Simulate mouse movements
- Change IP addresses

## 💡 Recommendations

### For Educational/Learning Purposes

Use these simple, scraping-friendly sites:

- Example.com
- Python.org
- Wikipedia.org
- Open-source project sites
- Your own websites

### For Real Projects

- Always check terms of service
- Use official APIs when available
- Contact website owners for permission
- Consider legal and ethical implications
- Respect rate limits and robots.txt

### For Commercial Use

- Obtain explicit permission
- Use official APIs and partnerships
- Implement proper rate limiting
- Follow GDPR and data protection laws
- Consider liability and legal risks

## 🚨 Legal & Ethical Considerations

**⚠️ Important Disclaimer:**

This tool is for **educational purposes only**. Users are responsible for:

- Complying with website terms of service
- Respecting robots.txt directives
- Following local laws and regulations
- Obtaining necessary permissions
- Not overloading servers
- Not scraping personal/sensitive data

**When in doubt:**

1. Check the website's robots.txt
2. Read terms of service
3. Contact website owners
4. Use official APIs instead
5. Consult legal advice

---

**Last Updated**: October 14, 2025
