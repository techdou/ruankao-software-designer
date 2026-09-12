# -*- coding: utf-8 -*-
"""从真题 PDF 提取含图题的配图。

策略：
1. 每道目标题按题干前缀文本在 PDF 中定位页码与题干 bbox。
2. 页内位图（get_images + get_image_rects）按 y 坐标归属：
   位于"本题题干 y"与"下一题题干 y"之间的图归本题。
3. 命中位图 → 原始分辨率导出；未命中（表格/矢量图）→ 渲染页面区域兜底。
输出：app/public/figures/<qid>.png + 提取报告。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent.parent
PDF_DIR = ROOT / "refs" / "sd_repo" / "02. 真题及解析（2020年-2024年）"
OUT = ROOT / "app" / "public" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

PDFS = {
    "2020年下半年": "2020年11月软件设计师上午真题及答案解析.pdf",
    "2021年上半年": "2021年05月软件设计师上午真题及答案解析.pdf",
    "2021年下半年": "2021年11月软件设计师上午真题+答案解析.pdf",
    "2022年上半年": "2022年05月软件设计师上午真题及答案解析.pdf",
    "2022年下半年": "2022年11月软件设计师上午真题及答案解析.pdf",
}

# 需要配图的题：qid -> (term, no, 题干定位片段)
TARGETS = {
    "r2020x-04": ("2020年下半年", 4, "主频为2.8GHz"),
    "r2020x-20": ("2020年下半年", 20, "语法树如下图所示"),
    "r2020x-23": ("2020年下半年", 23, "进程资源图如图"),
    "r2020x-24": ("2020年下半年", 24, "页面变换表如下表"),
    "r2020x-35": ("2020年下半年", 35, "用白盒测试技术对下面流程图"),
    "r2020x-50": ("2020年下半年", 50, "状态转换图如下图所示"),
    "r2020x-54": ("2020年下半年", 54, "关系R、S 如下表所示"),
    "r2021s-18": ("2021年上半年", 18, "软件项目活动图"),
    "r2021s-25": ("2021年上半年", 25, "页面变换表及状态位"),
    "r2021s-34": ("2021年上半年", 34, "用白盒测试技术对下面流程图"),
    "r2022s-05": ("2022年上半年", 5, "某计算机系统构成如下图所示"),
    "r2022x-17": ("2022年下半年", 17, "项目里程碑"),
    "r2022x-24": ("2022年下半年", 24, "前趋图如下所示"),
    "r2022x-42": ("2022年下半年", 42, "以下活动图中，活动A1"),
    "r2022x-64": ("2022年下半年", 64, "Dijkstra 算法求解下图"),
}


def next_qno_y(page: doc_page, no: int, after_y: float):
    """同页下一个题号标注（（n）A. 或 n、/n.）的 y 坐标，作为图区域下界。"""
    text = page.get_text("dict")
    pat = re.compile(rf"[（(]{no + 1}[)）]|^{no + 1}[.、]", re.M)
    best = None
    for block in text["blocks"]:
        for line in block.get("lines", []):
            line_text = "".join(s["text"] for s in line["spans"])
            if pat.search(line_text):
                y = line["bbox"][1]
                if y > after_y and (best is None or y < best):
                    best = y
    return best


def extract(term: str, no: int, needle: str, qid: str) -> dict:
    doc = fitz.open(PDF_DIR / PDFS[term])
    hits = []
    for pno in range(len(doc)):
        rects = doc[pno].search_for(needle)
        for r in rects:
            hits.append((pno, r))
    if not hits:
        doc.close()
        return {"qid": qid, "ok": False, "why": "题干未定位"}
    pno, stem_rect = hits[0]
    page = doc[pno]
    y0 = stem_rect.y1
    y1 = next_qno_y(page, no, y0) or page.rect.y1

    # 页内位图，按位置归属
    best_img = None
    for xref, *_ in page.get_images():
        for irect in page.get_image_rects(xref):
            if irect.y0 >= y0 - 5 and irect.y0 < y1:
                if best_img is None or irect.width > best_img[1].width:
                    best_img = (xref, irect)
    if best_img:
        xref, irect = best_img
        pix = fitz.Pixmap(doc, xref)
        if pix.n - pix.alpha > 3:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        path = OUT / f"{qid}.png"
        pix.save(path)
        doc.close()
        return {"qid": qid, "ok": True, "how": "bitmap", "page": pno + 1,
                "size": f"{pix.width}x{pix.height}", "bytes": path.stat().st_size}

    # 兜底：渲染题干到下一题之间的区域
    clip = fitz.Rect(40, y0, page.rect.width - 40, min(y1, page.rect.height - 40))
    if clip.height < 30:
        doc.close()
        return {"qid": qid, "ok": False, "why": f"区域过小 {clip}"}
    pix = page.get_pixmap(matrix=fitz.Matrix(2.2, 2.2), clip=clip)
    path = OUT / f"{qid}.png"
    pix.save(path)
    doc.close()
    return {"qid": qid, "ok": True, "how": "clip-render", "page": pno + 1,
            "size": f"{pix.width}x{pix.height}", "bytes": path.stat().st_size}


def main() -> int:
    report = []
    for qid, (term, no, needle) in TARGETS.items():
        try:
            r = extract(term, no, needle, qid)
        except Exception as e:
            r = {"qid": qid, "ok": False, "why": str(e)}
        report.append(r)
        print(r)
    ok = sum(1 for r in report if r["ok"])
    print(f"\n完成 {ok}/{len(report)}")
    (ROOT / "scripts" / "figures_report.txt").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in report), encoding="utf-8")
    return 0


if __name__ == "__main__":
    main()
