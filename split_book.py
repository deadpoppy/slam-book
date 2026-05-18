#!/usr/bin/env python3
"""Split the single large markdown book into chapters for MkDocs."""

import re
import os
import json
from pathlib import Path

INPUT_FILE = "slam_book.agent.final.md"
DOCS_DIR = Path("docs")
DOCS_DIR.mkdir(exist_ok=True)

with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Find all level-1 headings with their line numbers
headings = []
for i, line in enumerate(lines):
    if re.match(r'^#\s+', line):
        headings.append((i, line))

print(f"Found {len(headings)} level-1 headings")

# Build segments: (start_line, end_line_exclusive, heading_text)
segments = []
for idx, (line_no, heading) in enumerate(headings):
    start = line_no
    end = headings[idx + 1][0] if idx + 1 < len(headings) else len(lines)
    text = heading.lstrip('#').strip()
    segments.append((start, end, text))

# First pass: classify and determine sections
classified = []  # (start, end, text, type, chap_num, section_name)
book_title = None
current_section = None

for start, end, text in segments:
    # Book title
    if book_title is None:
        book_title = text
        classified.append((start, end, text, "title", None, None))
        continue

    # 导论
    if text == "导论":
        classified.append((start, end, text, "preface", 0, None))
        continue

    # 第X篇
    if re.match(r'第[一二三四五六七八九十]+篇[：:]', text):
        current_section = text
        # Don't create a separate file for section headers alone
        continue

    # 第X章
    m_chap = re.match(r'第\s*(\d+)\s*章', text)
    if m_chap:
        chap_num = int(m_chap.group(1))
        classified.append((start, end, text, "chapter", chap_num, current_section))
        continue

    # 附录
    if text.startswith("附录"):
        classified.append((start, end, text, "appendix", None, current_section))
        continue

    # Fallback
    classified.append((start, end, text, "other", None, current_section))

# Merge preface with chapter 0 if both exist
preface_idx = None
chap0_idx = None
for i, (start, end, text, typ, chap_num, sec) in enumerate(classified):
    if typ == "preface":
        preface_idx = i
    if typ == "chapter" and chap_num == 0:
        chap0_idx = i

if preface_idx is not None and chap0_idx is not None:
    # Merge preface into chapter 0
    p_start, p_end, p_text, _, _, _ = classified[preface_idx]
    c_start, c_end, c_text, _, _, c_sec = classified[chap0_idx]
    merged_start = p_start
    merged_end = c_end
    merged_text = "第0章 从 SLAM 到 Spatial AI"
    classified[chap0_idx] = (merged_start, merged_end, merged_text, "chapter", 0, c_sec)
    classified.pop(preface_idx)

# Write files
nav = []
for start, end, text, typ, chap_num, sec in classified:
    segment_lines = lines[start:end]
    
    if typ == "title":
        fname = "index.md"
        # Keep as is
        file_content = '\n'.join(segment_lines)
        nav.append((fname, text, None))
    elif typ == "chapter":
        fname = f"chapter{chap_num:02d}.md"
        # Prepend section heading if exists
        if sec:
            file_content = f"# {sec}\n\n" + '\n'.join(segment_lines)
        else:
            file_content = '\n'.join(segment_lines)
        nav.append((fname, text, sec))
    elif typ == "appendix":
        fname = "appendix.md"
        if sec:
            file_content = f"# {sec}\n\n" + '\n'.join(segment_lines)
        else:
            file_content = '\n'.join(segment_lines)
        nav.append((fname, text, sec))
    else:
        # other / fallback
        safe = re.sub(r'[^\w\u4e00-\u9fff\s-]', '', text).strip().replace(' ', '-')
        fname = f"page_{safe[:30]}.md"
        if sec:
            file_content = f"# {sec}\n\n" + '\n'.join(segment_lines)
        else:
            file_content = '\n'.join(segment_lines)
        nav.append((fname, text, sec))
    
    (DOCS_DIR / fname).write_text(file_content, encoding='utf-8')

# Save nav info
with open("nav.json", "w", encoding="utf-8") as f:
    json.dump(nav, f, ensure_ascii=False, indent=2)

print(f"\nDone! Wrote {len(nav)} pages to {DOCS_DIR}/")
print("\nNavigation structure:")
for item in nav:
    print(f"  {item[0]} -> {item[1]} (section: {item[2]})")
