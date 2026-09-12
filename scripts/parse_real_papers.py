# -*- coding: utf-8 -*-
"""真题 PDF → 结构化题库 JSON（v3，五格式适配）。

A(2020下): n. 题干 + 选项行 + "参考答案：X" + "解析：…"
B(2021上/2022下): （n）A. 选项行锚点，无答案
C(2021下): n、题干 + A、B、C、D 每行一选项，无答案
D(2022上): n. 题干 + 选项行 + "答案：X" + 解析（题图题标注 figureMissing）
E(2023上): 扫描版，另行 OCR，本脚本跳过

输出 app/src/data/bank/real-choice-raw.json + scripts/parse_report.txt
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "refs" / "sd_repo" / "02. 真题及解析（2020年-2024年）"
OUT_DIR = ROOT / "app" / "src" / "data" / "bank"
REPORT = ROOT / "scripts" / "parse_report.txt"

PAPERS = [
    ("2020年11月软件设计师上午真题及答案解析.pdf", "2020年下半年", "A"),
    ("2021年05月软件设计师上午真题及答案解析.pdf", "2021年上半年", "B"),
    ("2021年11月软件设计师上午真题+答案解析.pdf", "2021年下半年", "C"),
    ("2022年05月软件设计师上午真题及答案解析.pdf", "2022年上半年", "D"),
    ("2022年11月软件设计师上午真题及答案解析.pdf", "2022年下半年", "B"),
]

NOISE = [
    re.compile(r"手机端题库.*"),
    re.compile(r"PC端题库.*"),
    re.compile(r"www\.ruankaodaren\.com"),
    re.compile(r"内部资料，禁止传播"),
    re.compile(r"全国计算机技术与软件专业技术资格"),
    re.compile(r"202\d\s*年[上下]半年软件设计师上午试卷"),
    re.compile(r"^\d{1,2}\s*/\s*$"),
    re.compile(r"^\d{1,2}$"),
]

FIG_HINT = re.compile(r"如下图|如图所示|下图|下表|如图")
ANS_PATTERNS = [re.compile(r"参考答案[：:]\s*([ABCD]+)"), re.compile(r"答案[：:]\s*([ABCD]+)")]
ANA_PAT = re.compile(r"解\s*析\s*[：:]?")


def clean(raw: str) -> str:
    out = []
    for ln in raw.splitlines():
        ln = ln.strip()
        if ln and not any(p.search(ln) for p in NOISE):
            out.append(ln)
    return "\n".join(out)


def norm(s: str) -> str:
    s = re.sub(r"\n+", "", s)
    s = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", s)
    return s.strip()


def squeeze_inline(seg: str, letters: str = "ABCD", assume_first_A: bool = False) -> dict[str, str]:
    """单行混排选项：从 A 锚点起按字母顺序切分（B/C/D 前不能是字母数字，避免 IPSec 误切）。"""
    if assume_first_A:
        tail = seg
    else:
        m = re.search(r"A[.．、:：]", seg)
        if not m:
            return {}
        tail = seg[m.start():]
    parts = re.split(r"(?<![A-Za-z0-9])([ABCD])\s*[.．、)）:：]", tail)
    opts = {}
    if assume_first_A and parts:
        opts["A"] = norm(parts[0])
    for i in range(1, len(parts) - 1, 2):
        letter, text = parts[i], parts[i + 1]
        if letter not in opts:
            opts[letter] = norm(text)
    return opts


def squeeze_any(seg: str) -> dict[str, str]:
    """每行一个选项优先，不足 4 个再回退行内混排。
    对所有选项文本截断到答案/解析标记——2020/2022 卷的解析紧跟 D 选项，
    不截断会把 '参考答案：X 解析：…' 整段吞进 D 选项文本。"""
    opts = squeeze_lines(seg)
    if len(opts) != 4:
        mixed = squeeze_inline(seg)
        if len(mixed) > len(opts):
            opts = mixed
    ans_mark = re.compile(r"(参考答案[：:]|答案[：:]|解析\s*[:：]|历年相关试题|试题相关\s*【)")
    for k in opts:
        m = ans_mark.search(opts[k])
        if m:
            opts[k] = opts[k][: m.start()].rstrip()
    return opts


def squeeze_lines(seg: str) -> dict[str, str]:
    """每行一个选项格式：A、xxx \\n B、xxx。"""
    opts = {}
    cur = None
    buf: list[str] = []
    for ln in seg.splitlines():
        m = re.match(r"^([ABCD])[、.．]\s*(.*)$", ln)
        if m:
            if cur:
                opts[cur] = norm(" ".join(buf))
            cur, buf = m.group(1), [m.group(2)]
        elif cur:
            buf.append(ln)
    if cur:
        opts[cur] = norm(" ".join(buf))
    return opts


def find_answer(seg: str) -> tuple[str, str]:
    """在段落里找 参考答案/答案 行，返回 (answer, analysis_text)。"""
    for pat in ANS_PATTERNS:
        m = pat.search(seg)
        if m:
            after = seg[m.end():]
            am = ANA_PAT.search(after)
            analysis = after[am.end():] if am else after
            return m.group(1), norm(analysis)
    return "", ""


def common_blocks(text: str, starts: list[tuple[int, int, int]]) -> list[tuple[int, str, str]]:
    """根据起点列表切块，返回 [(no, head_text(题干来源), block_text)]。"""
    blocks = []
    for i, (n, s, e) in enumerate(starts):
        seg_end = starts[i + 1][1] if i + 1 < len(starts) else len(text)
        head = text[starts[i - 1][2]:s] if i else ""
        blocks.append((n, head, text[e:seg_end]))
    return blocks


def dedupe(starts):
    seen, out = set(), []
    for a in sorted(starts, key=lambda x: x[1]):
        if a[0] not in seen:
            out.append(a)
            seen.add(a[0])
    return out


def parse_a(text: str, term: str):
    """n./n、 起点 + 行内选项 + 答案/解析。2020卷点号/顿号混用。"""
    warns = []
    starts = []
    for m in re.finditer(r"(?m)^(\d{1,2})[.．、]", text):
        n = int(m.group(1))
        if 1 <= n <= 75:
            window = text[m.start():m.start() + 500]
            if re.search(r"A[.．、:：]", window):
                starts.append((n, m.start(), m.end()))
    starts = dedupe(starts)
    items = []
    blocks = common_blocks(text, starts)
    for i, (n, head, block) in enumerate(blocks):
        m = re.search(r"A[.．、:：]", block)
        stem = norm(text[starts[i][1]:starts[i][2]] + block[:m.start()]) if m else norm(head)
        opts = squeeze_any(block[m.start():] if m else block)
        answer, analysis = find_answer(block)
        items.append({"no": n, "term": term, "stem": stem, "options": opts,
                      "answer": answer, "analysis": analysis,
                      "figureMissing": bool(FIG_HINT.search(stem))})
    return items, warns


def inherit_shared_stem(items: list[dict], min_len: int = 14):
    """共干题（一干多题）继承前一道完整题的题干。"""
    last = ""
    for it in items:
        if len(it["stem"]) >= min_len:
            last = it["stem"]
        elif last:
            it["stem"] = last
            it["sharedStem"] = True


def parse_b(text: str, term: str):
    """（n）A. 锚点，无答案。行式状态机：锚点开新题，选项行归当前题，
    其余行累积为题干缓冲（归属下一个锚点）。"""
    warns = []
    anchor = re.compile(r"^[（(](\d{1,2})[)）]\s*(A[.．、:：].*)?$")
    optline = re.compile(r"^([ABCD])\s*[.．、)）:：]\s*(.*)$")
    inline = re.compile(r"(?<![A-Za-z0-9])([ABCD])\s*[.．、)）:：]")

    items: dict[int, dict] = {}
    order: list[int] = []
    cur: dict | None = None
    stem_buf: list[str] = []

    def close(c: dict | None):
        if c:
            c["stem"] = norm("".join(c.pop("buf")))
            items[c["no"]] = c
            order.append(c["no"])

    for ln in text.splitlines():
        am = anchor.match(ln)
        if am:
            n = int(am.group(1))
            if 1 <= n <= 75:
                close(cur)
                cur = {"no": n, "term": term, "buf": stem_buf, "options": {},
                       "answer": "", "analysis": ""}
                stem_buf = []
                if am.group(2):
                    om = inline.search(am.group(2))
                    cur["options"]["A"] = norm(am.group(2)[om.end():] if om else am.group(2))
                continue
        if cur is not None:
            om = optline.match(ln)
            if om and om.group(1) not in cur["options"]:
                cur["options"][om.group(1)] = norm(om.group(2))
                continue
            # 选项续行：选项未齐时追加到最后一个选项
            if len(cur["options"]) in (1, 2, 3) and "D" not in cur["options"]:
                last = sorted(cur["options"])[-1]
                cur["options"][last] += ln
                continue
        stem_buf.append(ln)
    close(cur)

    result = [items[n] for n in sorted(items)]
    missing = [n for n in range(1, 76) if n not in items]
    if missing:
        warns.append(f"{term} 缺失: {missing}")
    for it in result:
        it["figureMissing"] = bool(FIG_HINT.search(it["stem"]))
        it.setdefault("sharedStem", False)
    inherit_shared_stem(result)
    return result, warns


def parse_c(text: str, term: str):
    """n、 题号 + 每行一个 A、选项。"""
    warns = []
    starts = dedupe([(int(m.group(1)), m.start(), m.end())
                     for m in re.finditer(r"(?m)^(\d{1,2})[、.．]", text)
                     if 1 <= int(m.group(1)) <= 75])
    missing = [n for n in range(1, 76) if n not in {s[0] for s in starts}]
    if missing:
        warns.append(f"{term} 缺失: {missing}")
    items = []
    for i, (n, s, e) in enumerate(starts):
        seg_end = starts[i + 1][1] if i + 1 < len(starts) else len(text)
        block = text[e:seg_end]
        # 题干到第一个 A 选项之前
        m = re.search(r"A[、.．]", block)
        stem = norm(block[:m.start()]) if m else norm(block)
        opts = squeeze_any(block[m.start():] if m else block)
        answer, analysis = find_answer(block)
        items.append({"no": n, "term": term, "stem": stem, "options": opts,
                      "answer": answer, "analysis": analysis,
                      "figureMissing": bool(FIG_HINT.search(stem))})
    inherit_shared_stem(items)
    return items, warns


def parse_d(text: str, term: str):
    """同 A 但答案行是 '答案：X'，解析含 '本题选择X 选项'。"""
    items, warns = parse_a(text, term)
    return items, warns


FMT = {"A": parse_a, "B": parse_b, "C": parse_c, "D": parse_d}


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report, all_items = [], []
    for fname, term, fmt in PAPERS:
        path = PDF_DIR / fname
        if not path.exists():
            report.append(f"[SKIP] {fname}")
            continue
        doc = fitz.open(path)
        text = clean("\n".join(doc[i].get_text() for i in range(len(doc))))
        doc.close()
        items, warns = FMT[fmt](text, term)
        all_items.extend(items)
        opt_bad = [it["no"] for it in items if len(it["options"]) != 4]
        ans_ok = sum(1 for it in items if it["answer"])
        fig = sum(1 for it in items if it["figureMissing"])
        report.append(f"[OK] {term}({fmt}): {len(items)}题 | 选项异常{opt_bad or 0} | 有答案{ans_ok} | 含图题{fig} | 警告{len(warns)}")
        report.extend("     " + w for w in warns)
    out = OUT_DIR / "real-choice-raw.json"
    out.write_text(json.dumps(all_items, ensure_ascii=False, indent=1), encoding="utf-8")
    report.append(f"\n总计 {len(all_items)} 题 → {out}")
    REPORT.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
