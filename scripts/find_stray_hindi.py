import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/portal.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

unhandled = []

for idx, line in enumerate(lines, 1):
    if 3031 <= idx <= 3228:
        continue
    
    if not re.search(r'[\u0900-\u097f]', line):
        continue

    sline = line.strip()
    if sline.startswith('//') or sline.startswith('/*') or sline.startswith('*'):
        continue

    has_tdual = 'tDual(' in line
    has_ternary = any(k in line for k in ['isHi ?', 'isHi?', '=== "hi" ?', "=== 'hi' ?", 'user.nameHi', 'nameHi:'])

    if not has_tdual and not has_ternary:
        unhandled.append((idx, sline))

print(f'Total lines needing attention: {len(unhandled)}')
for idx, l in unhandled:
    print(f'{idx}: {l[:110]}')
