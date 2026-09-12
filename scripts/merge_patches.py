# -*- coding: utf-8 -*-
"""合并答案补丁进 real-choice-raw.json，输出核对清单。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "app" / "src" / "data" / "bank" / "real-choice-raw.json"
PATCH_DIR = ROOT / "scripts" / "patches"

data = json.load(open(BANK, encoding="utf-8"))
by_id = {it["id"]: it for it in data}

applied = 0
for pf in sorted(PATCH_DIR.glob("patch-*.json")):
    patch = json.load(open(pf, encoding="utf-8"))
    for qid, val in patch.items():
        if qid not in by_id:
            print(f"[MISS] {qid} 不在题库")
            continue
        it = by_id[qid]
        it["answer"], it["analysis"], it["chapter"], it["knowledge"], diff = val
        it["difficulty"] = diff
        applied += 1

json.dump(data, open(BANK, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
need = [it for it in data if not it["answer"]]
print(f"应用 {applied} 条补丁；剩余无答案 {len(need)} 题")
for it in need:
    print(f"  {it['id']} [{len(it['stem'])}字] {it['stem'][:40]}")
