#!/usr/bin/env python3
"""
Generate a static HTML preview of templates.csv with color swatches.
Requires: webcolors (already in uv environment)
"""

import csv
import sys

try:
    import webcolors
except ImportError:
    print("Missing dependency: webcolors (run: uv add webcolors)")
    sys.exit(1)

CSV_PATH = "/home/lance/Work/GAVC/templates.csv"
OUTPUT_PATH = "/home/lance/Work/GAVC/templates_preview.html"
HEX_COLUMNS = ["primary", "accent", "neutral_bg"]


def get_color_name(hex_code: str) -> str:
    """Return approximate color name for a hex code."""
    try:
        hex_clean = hex_code.strip().upper()
        if not hex_clean.startswith("#"):
            hex_clean = f"#{hex_clean}"
        return webcolors.hex_to_name(hex_clean)
    except (ValueError, KeyError):
        return "Custom"


def normalize_hex(hex_code: str) -> str:
    """Normalize hex code to uppercase with # prefix."""
    hex_str = hex_code.strip().upper()
    if not hex_str.startswith("#"):
        hex_str = f"#{hex_str}"
    return hex_str


def format_hex_cell(hex_code: str) -> str:
    """Generate HTML for a hex cell with swatch, hex code, and color name."""
    hex_str = normalize_hex(hex_code)
    name = get_color_name(hex_code)
    return f'''
        <div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 20px; height: 20px; background-color: {hex_str}; border: 1px solid #ccc; flex-shrink: 0;"></div>
            <span>{hex_str} <span style="color: #666; font-size: 0.9em;">({name})</span></span>
        </div>
    '''


def generate_html(headers: list, rows: list) -> str:
    """Generate complete HTML string."""
    # Build table rows
    table_rows = ""
    for idx, row in enumerate(rows, start=1):
        bg_color = "#ffffff" if idx % 2 == 0 else "#f9f9f9"
        cells = f'<td style="padding: 8px;">{idx}</td>'
        for header in headers:
            value = row[header]
            if header in HEX_COLUMNS:
                cells += f'<td style="padding: 8px;">{format_hex_cell(value)}</td>'
            else:
                cells += f'<td style="padding: 8px;">{value}</td>'
        table_rows += f'<tr style="background-color: {bg_color};">{cells}</tr>\n'

    # Build header row
    header_cells = '<th style="padding: 8px;">#</th>'
    for header in headers:
        header_cells += f'<th style="padding: 8px; text-align: left;">{header}</th>'
    header_row = f'<tr style="background-color: #e0e0e0;">{header_cells}</tr>'

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Templates.csv Preview</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 20px;
            background-color: #fafafa;
        }}
        h1 {{
            color: #333;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            background-color: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        th {{
            border-bottom: 2px solid #ccc;
        }}
        td {{
            border-bottom: 1px solid #eee;
        }}
    </style>
</head>
<body>
    <h1>Templates.csv Preview</h1>
    <p>Generated from {CSV_PATH}</p>
    <table>
        <thead>
            {header_row}
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
</body>
</html>'''
    return html


def main():
    # Load CSV
    with open(CSV_PATH, "r") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        rows = list(reader)

    # Generate HTML
    html_content = generate_html(headers, rows)

    # Write output
    with open(OUTPUT_PATH, "w") as f:
        f.write(html_content)

    print(f"Generated: {OUTPUT_PATH}")
    print(f"Open in browser: file://{OUTPUT_PATH}")


if __name__ == "__main__":
    main()
