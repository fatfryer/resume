#!/usr/bin/env python3
"""
Unified HTML generator for resumes and match reports.
Reads a unified CSV and generates BOTH resume + match report HTML files for each row.

CSV columns: homeTeam,awayTeam,date,arena,primary,accent,neutral_bg

Every row generates:
- {slug_homeTeam}_resume.html (with colors from CSV)
- {slug_homeTeam}_match_report.html (with team/date/arena + colors from CSV)
"""

import csv
import re
import sys
import os


def slugify(text):
    """Convert text to slug format: lowercase with underscores."""
    return text.strip().lower().replace(" ", "_")


def replace_resume_colors(content, colors):
    """Update RESUME_DATA.colors in resume.html template and CSS :root block."""
    # Update JavaScript RESUME_DATA.colors
    content = re.sub(r'(RESUME_DATA.*?primary:\s*")[^"]*"', f'\\1{colors["primary"]}"', content, flags=re.DOTALL)
    content = re.sub(r'(RESUME_DATA.*?accent:\s*")[^"]*"', f'\\1{colors["accent"]}"', content, flags=re.DOTALL)
    content = re.sub(r'(RESUME_DATA.*?neutralBg:\s*")[^"]*"', f'\\1{colors["neutral_bg"]}"', content, flags=re.DOTALL)

    # Update CSS :root block to match
    content = re.sub(r'(--primary:\s*)[^;]+;', f'\\1{colors["primary"]};', content)
    content = re.sub(r'(--accent:\s*)[^;]+;', f'\\1{colors["accent"]};', content)
    content = re.sub(r'(--neutral-bg:\s*)[^;]+;', f'\\1{colors["neutral_bg"]};', content)

    return content


def replace_report_data(content, row, colors):
    """Replace data values in match_report.html DATA object."""
    # Replace team/date/arena fields
    content = re.sub(
        r'(homeTeam:\s*")[^"]*"',
        f'\\1{row["homeTeam"]}"',
        content
    )
    content = re.sub(
        r'(awayTeam:\s*")[^"]*"',
        f'\\1{row["awayTeam"]}"',
        content
    )
    content = re.sub(
        r'(date:\s*")[^"]*"',
        f'\\1{row["date"]}"',
        content
    )
    content = re.sub(
        r'(arena:\s*")[^"]*"',
        f'\\1{row["arena"]}"',
        content
    )
    # Replace colors in DATA.colors (use DATA context to avoid CSS matches)
    content = re.sub(
        r'(DATA.*?colors.*?primary:\s*")[^"]*"',
        f'\\1{colors["primary"]}"',
        content, flags=re.DOTALL
    )
    content = re.sub(
        r'(DATA.*?colors.*?accent:\s*")[^"]*"',
        f'\\1{colors["accent"]}"',
        content, flags=re.DOTALL
    )

    content = re.sub(
        r'(DATA.*?colors.*?neutralBg:\s*")[^"]*"',
        f'\\1{colors["neutral_bg"]}"',
        content, flags=re.DOTALL
    )
    return content


def main():
    # Hardcoded path to templates.csv in the same directory as this script
    csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates.csv")
    
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        sys.exit(1)
    
    output_dir = os.path.dirname(csv_path) or "."
    
    # Schools subdirectory
    schools_dir = os.path.join(output_dir, "schools")
    os.makedirs(schools_dir, exist_ok=True)

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            home_team = row["homeTeam"].strip()
            if not home_team:
                print("Skipping row with empty homeTeam")
                continue

            slug = slugify(home_team)
            school_dir = os.path.join(schools_dir, slug)
            os.makedirs(school_dir, exist_ok=True)
            colors = {
                "primary": row["primary"].strip(),
                "accent": row["accent"].strip(),
                "neutral_bg": row["neutral_bg"].strip(),
            }

            # Generate Resume (always)
            resume_out = os.path.join(school_dir, "resume.html")
            with open(os.path.join(output_dir, "resume.html"), "r", encoding="utf-8") as tf:
                resume_content = tf.read()
            resume_content = replace_resume_colors(resume_content, colors)
            with open(resume_out, "w", encoding="utf-8") as out:
                out.write(resume_content)
            print(f"Generated: {resume_out}")

            # Generate Match Report (always)
            report_out = os.path.join(school_dir, "match_report.html")
            with open(os.path.join(output_dir, "match_report.html"), "r", encoding="utf-8") as tf:
                report_content = tf.read()
            report_content = replace_report_data(report_content, row, colors)
            with open(report_out, "w", encoding="utf-8") as out:
                out.write(report_content)
            print(f"Generated: {report_out}")


if __name__ == "__main__":
    main()
