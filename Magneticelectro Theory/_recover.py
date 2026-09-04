import re, os

base = r"E:\base_Obsidian\iceaxing's knowledge base\Magneticelectro Theory\Pozar-Microwave Engineering"

files = [
    "02-传输线理论.md", "03-传输线与波导.md", "04-微波网络分析.md",
    "05-阻抗匹配与调谐.md", "06-微波谐振器.md", "07-功分器与耦合器.md",
    "08-微波滤波器.md", "09-铁氧体器件.md", "10-噪声与非线性失真.md",
    "11-有源射频微波器件.md", "12-微波放大器设计.md", "13-振荡器与混频器.md",
    "14-微波系统导论.md",
]

for fname in files:
    fpath = os.path.join(base, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by --- separators (current fragmentation)
    fragments = content.split('\n---\n')
    
    # Parse fragments into sections
    # A fragment starting with "# X.Y " (or "# X.Y.Z ") starts a new section
    # All other fragments belong to the current section
    
    section_pattern = re.compile(r'^# (\d+)\.(\d+)')
    
    sections = {}  # key: (major, minor) -> list of fragments
    section_order = []  # ordered list of (major, minor) as encountered
    current_key = None
    
    for frag in fragments:
        frag = frag.strip()
        if not frag:
            continue
        
        m = section_pattern.match(frag)
        if m:
            key = (int(m.group(1)), int(m.group(2)))
            if key not in sections:
                sections[key] = []
                section_order.append(key)
            sections[key].append(frag)
            current_key = key
        else:
            if current_key:
                sections[current_key].append(frag)
            else:
                # Orphan at start — create a dummy section
                if (0, 0) not in sections:
                    sections[(0, 0)] = []
                    section_order.append((0, 0))
                sections[(0, 0)].append(frag)

    # Sort sections numerically
    sorted_keys = sorted(section_order)
    
    # Rebuild: within each section, join fragments (strip out the --- that were
    # added by the Python script between them). Between sections, insert ---.
    rebuilt = []
    for key in sorted_keys:
        frags = sections[key]
        # Join fragments within same section with double newline (no ---)
        # But preserve any markdown content
        section_text = '\n\n'.join(frags)
        rebuilt.append(section_text)
    
    final = '\n\n---\n\n'.join(rebuilt) + '\n'
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(final)
    
    print(f"Recovered: {fname} ({len(sections)} sections)")

print("\nDone!")
