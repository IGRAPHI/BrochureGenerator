# PDF Download Feature

## Overview

The Streamlit web app supports downloading generated brochures in **PDF format** in addition to Markdown format, using the professional **ReportLab** library.

## Features

### Professional PDF Styling

- A4 page size with proper margins (72 points / ~2.5cm)
- Professional typography (Arial/Helvetica font family)
- Color-coded headings:
  - H1 (Title): Dark blue (#2c3e50), 24pt
  - H2: Gray blue (#34495e), 18pt with border
  - H3: Medium gray (#555), 14pt
- Styled elements:
  - Bullet points with proper indentation
  - Bold and italic text support
  - Inline code formatting
  - Justified text alignment
  - Proper spacing between elements

### How It Works

1. **Markdown Parsing**: Processes markdown text line by line using Python's `re` module

   - Identifies headers (H1, H2, H3)
   - Handles bullet points and lists
   - Processes inline formatting (bold, italic, code)
   - Removes markdown link syntax while preserving text

2. **PDF Generation**: Uses **ReportLab** to create professional PDFs

   - `reportlab`: Industry-standard PDF generation library
   - Custom paragraph styles for each element type
   - Professional color scheme with HexColor
   - Proper text flow and page breaks

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
from main import markdown_to_pdf

# Generate PDF from markdown text
brochure_markdown = "# Company Brochure\n\n## About Us\n\nWe are awesome!"
pdf_buffer = markdown_to_pdf(brochure_markdown)

# Save to file
with open("brochure.pdf", "wb") as f:
    f.write(pdf_buffer.getvalue())

# Or use in memory
pdf_bytes = pdf_buffer.getvalue()
```

### Custom PDF Generation

For more control over PDF generation:

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from io import BytesIO

def custom_pdf(text):
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)

    # Create content
    story = []
    styles = getSampleStyleSheet()

    # Add paragraphs
    story.append(Paragraph(text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    # Build PDF
    doc.build(story)
    pdf_buffer.seek(0)
    return pdf_buffer
```

## Dependencies

Required packages:

```
reportlab>=3.6.0     # Professional PDF generation
markdown2>=2.4.0     # Markdown parsing
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
