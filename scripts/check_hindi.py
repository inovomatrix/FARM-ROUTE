import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

check_dirs = ["frontend", "backend", "tests"]
results = {}

for bdir in check_dirs:
    for root, dirs, files in os.walk(bdir):
        for f in files:
            if f.endswith(('.html', '.js', '.py')):
                full_path = os.path.join(root, f)
                with open(full_path, "r", encoding="utf-8", errors="ignore") as file:
                    lines = file.readlines()
                hindi_lines = [i + 1 for i, l in enumerate(lines) if re.search(r"[\u0900-\u097F]", l)]
                if hindi_lines:
                    results[full_path.replace("\\", "/")] = len(hindi_lines)

print("--- HINDI / DEVANAGARI CHARACTER SCAN ACROSS FRONTEND, BACKEND, TESTS ---")
for k, v in sorted(results.items()):
    print(f"{k}: {v} lines")
if not results:
    print("Zero Hindi / Devanagari occurrences found! 100% English verified.")
