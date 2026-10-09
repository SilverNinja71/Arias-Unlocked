#!/usr/bin/env python3
"""
Arias Unlocked - Blog Sync Tool
Syncs blog posts between the Google Drive Blog/ folder and Arias Unlocked blog.html.
"""

import os
import re
import json

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(WORKSPACE_DIR, "Blog")
OUTPUT_JSON = os.path.join(WORKSPACE_DIR, "Blog", "posts.json")

def parse_markdown_post(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    filename = os.path.basename(filepath)
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else filename.replace(".md", "").replace("-", " ").title()

    cat_match = re.search(r"\*\*Category:\*\*\s*(.+)", content)
    category = cat_match.group(1).strip() if cat_match else "Repertoire"

    date_match = re.search(r"\*\*Date:\*\*\s*(.+)", content)
    date = date_match.group(1).strip() if date_match else "Recently Added"

    read_match = re.search(r"\*\*Read Time:\*\*\s*(.+)", content)
    readtime = read_match.group(1).strip() if read_match else "5 min read"

    # Split past header dividers
    body = content
    if "---" in content:
        parts = content.split("---", 1)
        body = parts[1].strip()

    # Create short snippet
    clean_paragraphs = [p.strip() for p in body.split("\n\n") if p.strip() and not p.strip().startswith("#")]
    snippet = clean_paragraphs[0] if clean_paragraphs else body[:180] + "..."
    if len(snippet) > 220:
        snippet = snippet[:220] + "..."

    return {
        "filename": filename,
        "title": title,
        "category": category,
        "date": date,
        "readtime": readtime,
        "snippet": snippet,
        "content": body
    }

def sync():
    if not os.path.exists(BLOG_DIR):
        print(f"Blog folder does not exist at {BLOG_DIR}")
        return

    posts = []
    for fname in sorted(os.listdir(BLOG_DIR)):
        if fname.endswith(".md"):
            post_path = os.path.join(BLOG_DIR, fname)
            try:
                posts.append(parse_markdown_post(post_path))
            except Exception as e:
                print(f"Error parsing {fname}: {e}")

    # Write posts.json in Blog folder for easy importing
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

    print(f"Synced {len(posts)} posts from Google Drive 'Blog' folder -> {OUTPUT_JSON}")

if __name__ == "__main__":
    sync()
