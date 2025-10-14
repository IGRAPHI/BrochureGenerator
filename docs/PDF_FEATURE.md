# PDF Download Feature

## Overview

The Streamlit web app now supports downloading generated brochures in **PDF format** in addition to Markdown format.

## Features

### Professional PDF Styling
- A4 page size with proper margins (2cm)
- Professional typography (Arial/Helvetica font family)
- Color-coded headings:
  - H1: Dark blue with bottom border
  - H2: Gray with lighter border
  - H3: Medium gray
- Styled elements:
  - Code blocks with gray background
  - Blockquotes with blue left border
  - Tables with headers
  - Proper spacing and alignment

### How It Works

1. **Markdown to HTML**: Converts markdown using Python's `markdown` library with extensions:
   - `extra`: Additional markdown features
   - `codehilite`: Code syntax highlighting
   - `tables`: Table support
   - `toc`: Table of contents

2. **HTML to PDF**: Uses `xhtml2pdf` (pisa) to convert styled HTML to PDF

3. **Download**: Streamlit serves the PDF as a downloadable file

## Usage

### In Streamlit App

1. Generate a brochure as usual
2. Scroll to "📥 Download Options" section
3. Choose from two download buttons:
   - **Markdown (.md)**: Original format, editable
   - **PDF (.pdf)**: Professional document, print-ready

### Programmatic PDF Generation

If you want to generate PDFs programmatically:

```python
from io import BytesIO
import markdown
from xhtml2pdf import pisa

def markdown_to_pdf(markdown_text: str) -> BytesIO:
    """Convert markdown to PDF."""
    # Convert to HTML
    html = markdown.markdown(
        markdown_text,
        extensions=['extra', 'codehilite', 'tables', 'toc']
    )
    
    # Add CSS styling (see app.py for full CSS)
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            /* Your CSS here */
        </style>
    </head>
    <body>{html}</body>
    </html>
    """
    
    # Convert to PDF
    pdf_buffer = BytesIO()
    pisa.CreatePDF(
        BytesIO(styled_html.encode('utf-8')),
        dest=pdf_buffer
    )
    pdf_buffer.seek(0)
    return pdf_buffer

# Usage
pdf_bytes = markdown_to_pdf(brochure_markdown)
with open("brochure.pdf", "wb") as f:
    f.write(pdf_bytes.getvalue())
```

## Dependencies

New packages required:
```
markdown==3.5.1      # Markdown to HTML conversion
xhtml2pdf==0.2.13    # HTML to PDF conversion
```

Install with:
```bash
pip install markdown xhtml2pdf
```

Or use the updated `requirements.txt`:
```bash
pip install -r requirements.txt
```

## Testing

Run the test script to verify PDF generation:

```bash
python test_pdf.py
```

Expected output:
```
🧪 Testing PDF generation...
============================================================
✓ Markdown to HTML conversion successful
✓ HTML styling added
✓ PDF generated successfully (3265 bytes)
✓ Test PDF saved as 'test_brochure.pdf'
============================================================
✅ All tests passed! PDF generation is working.
```

## Troubleshooting

### Issue: PDF generation fails

**Error**: `PDF generation failed`

**Solutions**:
1. Check dependencies are installed:
   ```bash
   pip list | grep -E "markdown|xhtml2pdf"
   ```

2. Reinstall dependencies:
   ```bash
   pip install --upgrade markdown xhtml2pdf
   ```

3. Try with simple markdown first (use test_pdf.py)

### Issue: PDF looks broken or unstyled

**Cause**: CSS not being applied or HTML parsing issues

**Solutions**:
1. Check markdown format is valid
2. Verify HTML conversion (check intermediate HTML)
3. Simplify CSS if needed

### Issue: Special characters not displaying

**Cause**: Encoding issues

**Solution**: 
- Ensure UTF-8 encoding: `styled_html.encode('utf-8')`
- Add charset meta tag: `<meta charset="utf-8">`

### Issue: Images not showing in PDF

**Note**: `xhtml2pdf` has limited image support

**Workaround**:
- Use base64 embedded images
- Or use alternative PDF library like `weasyprint`

## Alternative PDF Libraries

If you need more features, consider:

### WeasyPrint (More powerful)
```bash
pip install weasyprint
```

Pros:
- Better CSS support
- Better image handling
- Modern HTML/CSS standards

Cons:
- Requires external dependencies (Cairo, Pango)
- Larger installation

### ReportLab (Low-level)
```bash
pip install reportlab
```

Pros:
- Full control over PDF layout
- No HTML needed
- Fast

Cons:
- More complex API
- Need to build layout programmatically

## Customization

### Changing PDF Styling

Edit the CSS in `app.py` function `markdown_to_pdf()`:

```python
styled_html = f"""
<style>
    /* Modify these styles */
    h1 {{ 
        color: #your-color;
        font-size: 24pt;
    }}
    /* Add more custom styles */
</style>
"""
```

### Adding Logo/Header

```python
styled_html = f"""
<body>
    <div style="text-align: center; margin-bottom: 20px;">
        <img src="data:image/png;base64,..." width="200">
        <h1>Company Brochure</h1>
    </div>
    {html}
</body>
"""
```

### Adding Footer with Page Numbers

```python
styled_html = f"""
<style>
    @page {{
        @bottom-right {{
            content: counter(page);
        }}
    }}
</style>
"""
```

## Limitations

1. **No JavaScript**: PDFs are static, no interactive elements
2. **Limited CSS**: Not all CSS3 features supported by xhtml2pdf
3. **No Web Fonts**: Use standard fonts (Arial, Helvetica, Times, Courier)
4. **Image Sizing**: May need manual adjustment
5. **Complex Layouts**: Tables and multi-column layouts have limited support

## Best Practices

1. **Keep it Simple**: Use basic markdown formatting
2. **Test First**: Always test PDF generation with sample content
3. **Fallback**: Provide Markdown download as alternative
4. **File Size**: Large brochures may take time to generate
5. **Caching**: Consider caching generated PDFs for same URL

## Future Enhancements

- [ ] Custom PDF templates
- [ ] Company logo integration
- [ ] Page numbers and headers/footers
- [ ] Multiple page layouts (portrait/landscape)
- [ ] Font selection options
- [ ] Color theme customization
- [ ] Export to DOCX format
- [ ] Batch PDF generation

---

**Last Updated**: October 14, 2025
