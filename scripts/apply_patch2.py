# -*- coding: utf-8 -*-
"""patch2：重建选项/修复题干/删除不可用题。"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "app" / "src" / "data" / "bank" / "real-choice-raw.json"

data = json.load(open(BANK, encoding="utf-8"))
by_id = {it["id"]: it for it in data}

patch = json.load(open(ROOT / "scripts" / "patches" / "patch2-rebuild.json", encoding="utf-8"))
for qid, val in patch.items():
    it = by_id[qid]
    if "fixStem" in val:
        it["stem"] = val["fixStem"]
    if "options" in val:
        it["options"] = val["options"]
    it["answer"] = val["answer"]
    it["analysis"] = val["analysis"]
    it["chapter"] = val["chapter"]
    it["knowledge"] = val["knowledge"]
    it["difficulty"] = val["difficulty"]

# 不可用题：题干缺失/图缺失无法作答
DROP = ["r2021s-48", "r2021s-49", "r2021s-50", "r2021x-08", "r2021x-17",
        "r2021x-20", "r2021x-22", "r2021x-33", "r2021x-70"]
data = [it for it in data if it["id"] not in DROP]

json.dump(data, open(BANK, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
need = [it for it in data if not it["answer"]]
print(f"修复 {len(patch)} 题，删除 {len(DROP)} 题；剩余无答案 {len(need)}")
for it in need:
    print(" ", it["id"], it["stem"][:40])

# 已有答案但缺章节标注的
unlabeled = [it for it in data if it["answer"] and not it.get("chapter")]
print("已有答案缺标注:", len(unlabeled))
