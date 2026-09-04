import re, os

base = r"E:\base_Obsidian\iceaxing's knowledge base\Magneticelectro Theory\Pozar-Microwave Engineering"

files = [
    "02-传输线理论.md", "03-传输线与波导.md", "04-微波网络分析.md",
    "05-阻抗匹配与调谐.md", "07-功分器与耦合器.md",
    "08-微波滤波器.md", "09-铁氧体器件.md", "10-噪声与非线性失真.md",
    "11-有源射频微波器件.md", "12-微波放大器设计.md", "13-振荡器与混频器.md",
    "14-微波系统导论.md",
]
# Note: 01 was never merged (single file), 06 was never merged (just renamed)

for fname in files:
    fpath = os.path.join(base, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Strategy: split into paragraphs/lines. Walk through and identify section starts.
    # A line matching "# X.Y " starts a new section. Everything until the next "# X.Y " 
    # belongs to that section.
    # BUT: because the file was sorted by fragment heading, some content from section 2.1
    # might appear after section 2.8. We need to COLLECT all fragments and then group them.
    
    # Better approach: split the file by the "---" separators that remain from the
    # recovery script. Then group fragments by their logical section based on heading.
    
    # Even better: use a line-by-line scan with state tracking.
    # State: current section number (major, minor)
    # When we see "# X.Y ...", change state.
    # Collect all lines for each section.
    
    sections = {}  # (major, minor) -> list of paragraphs
    current_key = None
    current_lines = []
    
    lines = content.split('\n')
    section_heading = re.compile(r'^# (\d+)\.(\d+)\s')
    subsection_heading = re.compile(r'^## ')
    
    for line in lines:
        m = section_heading.match(line)
        if m:
            # Save previous section
            if current_key is not None and current_lines:
                text = '\n'.join(current_lines).strip()
                if text:
                    if current_key not in sections:
                        sections[current_key] = []
                    sections[current_key].append(text)
            
            current_key = (int(m.group(1)), int(m.group(2)))
            current_lines = [line]
        else:
            if current_key is not None:
                current_lines.append(line)
    
    # Don't forget the last section
    if current_key is not None and current_lines:
        text = '\n'.join(current_lines).strip()
        if text:
            if current_key not in sections:
                sections[current_key] = []
            sections[current_key].append(text)
    
    # Sort sections by key
    sorted_keys = sorted(sections.keys())
    
    # Build output: for each section, join its parts. Between sections, use "---"
    rebuilt = []
    for key in sorted_keys:
        parts = sections[key]
        section_text = '\n\n'.join(parts)
        # Clean up: remove "---" on its own line (leftover separators)
        section_text = re.sub(r'\n---\n', '\n\n', section_text)
        section_text = re.sub(r'\n---\n', '\n\n', section_text)  # twice for overlapping matches
        rebuilt.append(section_text)
    
    final = '\n\n---\n\n'.join(rebuilt) + '\n'
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(final)
    
    print(f"Rebuilt: {fname} ({len(sections)} sections)")

# Handle Ch06 separately — it was never merged, just renamed. Check if it needs fixing.
ch06 = os.path.join(base, "06-微波谐振器.md")
with open(ch06, 'r', encoding='utf-8') as f:
    content = f.read()
# If it's empty or corrupted, we have a problem. Otherwise leave as-is.
if not content.strip():
    print("WARNING: 06-微波谐振器.md is empty!")
else:
    # Check if it starts with # heading
    if content.strip().startswith('# '):
        print("Ch06 looks OK, leaving as-is")
    else:
        print("Ch06 may need fixing")

print("\nDone!")
