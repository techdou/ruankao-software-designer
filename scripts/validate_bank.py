# -*- coding: utf-8 -*-
"""题库结构校验：CI 测试步骤。

校验规则：
- id 唯一且非空
- answer ∈ {A,B,C,D}
- 每题 4 个选项 A/B/C/D 且文本非空
- chapter 在 chapters 注册表内、knowledge 非空、difficulty 1-5
- analysis 非空
- 案例题：caseType 合法、subQuestions 非空且每问有 answer/analysis

用法：python scripts/validate_bank.py  （退出码 0 = 通过）
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / "app" / "src" / "data" / "bank"
CHAPTER_IDS = {f"ch{i:02d}" for i in range(1, 15)}
CASE_TYPES = {"dfd", "db", "uml", "algo", "pattern"}
OPTS = {"A", "B", "C", "D"}

errors: list[str] = []


def load(name: str) -> list:
    p = BANK / name
    if not p.exists():
        errors.append(f"{name}: 文件缺失")
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"{name}: JSON 解析失败 {e}")
        return []


def check_choice(q: dict, source: str, seen: set):
    qid = q.get("id", "")
    if not qid:
        errors.append(f"{source}: 存在无 id 的题目")
        return
    if qid in seen:
        errors.append(f"{source}: id 重复 {qid}")
    seen.add(qid)
    where = f"{source}#{qid}"

    if q.get("answer") not in OPTS:
        errors.append(f"{where}: answer 非法 -> {q.get('answer')!r}")
    opts = q.get("options") or {}
    if set(opts.keys()) != OPTS:
        errors.append(f"{where}: 选项键应为 ABCD -> {sorted(opts)}")
    else:
        for k, v in opts.items():
            if not str(v).strip():
                errors.append(f"{where}: 选项 {k} 为空")
    if q.get("chapter") not in CHAPTER_IDS:
        errors.append(f"{where}: chapter 非法 -> {q.get('chapter')!r}")
    if not str(q.get("knowledge", "")).strip():
        errors.append(f"{where}: knowledge 为空")
    d = q.get("difficulty")
    if not isinstance(d, int) or not (1 <= d <= 5):
        errors.append(f"{where}: difficulty 非法 -> {d!r}")
    if not str(q.get("analysis", "")).strip():
        errors.append(f"{where}: analysis 为空")
    if not str(q.get("stem", "")).strip():
        errors.append(f"{where}: stem 为空")


def check_case(c: dict, source: str, seen: set):
    qid = c.get("id", "")
    if not qid:
        errors.append(f"{source}: 案例题缺 id")
        return
    if qid in seen:
        errors.append(f"{source}: id 重复 {qid}")
    seen.add(qid)
    where = f"{source}#{qid}"
    if c.get("caseType") not in CASE_TYPES:
        errors.append(f"{where}: caseType 非法 -> {c.get('caseType')!r}")
    subs = c.get("subQuestions") or []
    if not subs:
        errors.append(f"{where}: 无小题")
    for sq in subs:
        if not str(sq.get("answer", "")).strip():
            errors.append(f"{where} 小题{sq.get('no')}: answer 为空")
        if not str(sq.get("analysis", "")).strip():
            errors.append(f"{where} 小题{sq.get('no')}: analysis 为空")


def main() -> int:
    seen: set = set()
    for name in ["real-choice-raw.json", "drill-a.json", "drill-b.json"]:
        for q in load(name):
            check_choice(q, name, seen)
    for c in load("cases.json"):
        check_case(c, "cases.json", seen)

    n = len(seen)
    if errors:
        print(f"[FAIL] {len(errors)} 处问题：")
        for e in errors:
            print("  -", e)
        return 1
    print(f"[PASS] 题库校验通过：共 {n} 题（含案例套题），结构完整、答案与解析齐备")
    return 0


if __name__ == "__main__":
    sys.exit(main())
