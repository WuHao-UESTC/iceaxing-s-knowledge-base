import re, os, sys

base = r"E:\base_Obsidian\iceaxing's knowledge base\Magneticelectro Theory\Pozar-Microwave Engineering"

# Files to fix: all merged chapters except ch01 (wasn't merged)
files_to_fix = [
    "02-传输线理论.md",
    "03-传输线与波导.md",
    "04-微波网络分析.md",
    "05-阻抗匹配与调谐.md",
    "06-微波谐振器.md",
    "07-功分器与耦合器.md",
    "08-微波滤波器.md",
    "09-铁氧体器件.md",
    "10-噪声与非线性失真.md",
    "11-有源射频微波器件.md",
    "12-微波放大器设计.md",
    "13-振荡器与混频器.md",
    "14-微波系统导论.md",
]

for fname in files_to_fix:
    fpath = os.path.join(base, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into sections by "---" separator
    # First, find the chapter title line and remove it
    lines = content.split('\n')
    
    # Remove leading "# ChapterTitle" and following blank lines
    # Find start of first real section
    sections_raw = content.split('\n---\n')
    
    # Parse sections: extract heading number for sorting
    parsed_sections = []
    for sec in sections_raw:
        sec = sec.strip()
        if not sec:
            continue
        # Check if this is just the chapter title (no ## heading)
        if sec.startswith('# ') and not sec.startswith('## '):
            continue  # skip chapter title
        
        # Extract section number from first heading (## X.Y or ## X.Y.Z)
        m = re.match(r'^##\s+(\d+)\.(\d+)', sec)
        if m:
            major = int(m.group(1))
            minor = int(m.group(2))
            parsed_sections.append(((major, minor), sec))
        else:
            # No heading found, keep at end
            parsed_sections.append(((999, 999), sec))
    
    # Sort by section number
    parsed_sections.sort(key=lambda x: x[0])
    
    # Rebuild: promote headings, then join with ---
    rebuilt = []
    for (major, minor), sec in parsed_sections:
        # Promote headings: ## → #, ### → ##, #### → ###, ##### → ####
        # Do deepest first to avoid double-promotion
        promoted = sec
        promoted = re.sub(r'^##### ', '#### ', promoted, flags=re.MULTILINE)
        promoted = re.sub(r'^#### ', '### ', promoted, flags=re.MULTILINE)
        promoted = re.sub(r'^### ', '## ', promoted, flags=re.MULTILINE)
        promoted = re.sub(r'^## ', '# ', promoted, flags=re.MULTILINE)
        rebuilt.append(promoted)
    
    final = '\n\n---\n\n'.join(rebuilt) + '\n'
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(final)
    
    print(f"Fixed: {fname} ({len(parsed_sections)} sections reordered)")

print("\nDone!")
