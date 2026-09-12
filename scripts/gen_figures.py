# -*- coding: utf-8 -*-
"""批量调用 image2-api 生成本站配图。

用法：python scripts/gen_figures.py [key ...]   # 不带参数 = 全部缺的都生成
清单：assets-src/batch-manifest.json
输出：app/public/art/<key>.png
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "assets-src" / "batch-manifest.json"
OUT = ROOT / "app" / "public" / "art"
OUT.mkdir(parents=True, exist_ok=True)
GEN = r"C:\Users\DouXiulu\.agents\skills\image2-api\scripts\generate_image.py"

m = json.loads(MANIFEST.read_text(encoding="utf-8"))
base = m["style_base"]
only = set(sys.argv[1:])

ok, fail = [], []
for item in m["items"]:
    key = item["key"]
    dest = OUT / f"{key}.png"
    if dest.exists():
        ok.append(key)
        continue
    if only and key not in only:
        continue
    prompt = f"{base} {item['prompt']}"
    pf = ROOT / "assets-src" / f"prompt-{key}.txt"
    pf.write_text(prompt, encoding="utf-8")
    cmd = [
        sys.executable, GEN,
        "--prompt-file", str(pf),
        "--model", "gpt-image-2.5-flare",
        "--model-family", "gpt-image-2.5",
        "--size", item["size"],
        "--quality", "medium",
        "--count", "1",
        "--output-dir", str(ROOT / "assets-src" / "output" / key),
    ]
    if item.get("transparent"):
        cmd += ["--background", "transparent", "--output-format", "png"]
    print(f"[gen] {key} ...", flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True)
    src = Path(ROOT / "assets-src" / "output" / key / "image.png")
    if r.returncode == 0 and src.exists():
        import shutil
        shutil.copy(src, dest)
        ok.append(key)
        print(f"  ok -> {dest.name}", flush=True)
    else:
        fail.append(key)
        print(f"  FAIL: {r.stdout[-200:]} {r.stderr[-200:]}", flush=True)

print(f"\n完成 {len(ok)}，失败 {len(fail)} {fail}")
