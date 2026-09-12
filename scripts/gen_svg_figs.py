# -*- coding: utf-8 -*-
"""代码绘制 4 张精确教学 SVG（AI 生图不做精确图），输出到 app/public/art-svg/。"""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "app" / "public" / "art-svg"
OUT.mkdir(parents=True, exist_ok=True)

GREEN, AMBER, INK, LINE, MUTED = "#2d6a4f", "#b45309", "#201f1c", "#e6e2d8", "#64615a"
FONT = '-apple-system,"Segoe UI","Microsoft YaHei",sans-serif'

HEAD = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 H" font-family="{FONT}">'
defs_arrow = (
    '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
    '<path d="M0,0 L10,5 L0,10 z" fill="' + INK + '"/></marker>'
    '<marker id="arg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
    '<path d="M0,0 L10,5 L0,10 z" fill="' + GREEN + '"/></marker></defs>'
)


def box(x, y, w, h, label, fill="#fff", stroke=INK, tcol=INK, fs=15):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>'
            f'<text x="{x+w/2}" y="{y+h/2+fs*0.36}" text-anchor="middle" font-size="{fs}" fill="{tcol}" font-weight="600">{label}</text>')


def arrow(x1, y1, x2, y2, label="", color=INK, lx=0, ly=-8):
    out = (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.8" marker-end="url(#ar)"/>')
    if label:
        out += f'<text x="{(x1+x2)/2+lx}" y="{(y1+y2)/2+ly}" text-anchor="middle" font-size="12.5" fill="{MUTED}">{label}</text>'
    return out


def save(name, body, h):
    svg = HEAD.replace("0 0 760 H", f"0 0 760 {h}") + defs_arrow + body + "</svg>"
    (OUT / name).write_text(svg, encoding="utf-8")
    print(name, "ok")


# ---------- 1. 进程三态转换图 ----------
b = []
b.append(box(60, 90, 130, 56, "就绪", fill="#e8f1ec", stroke=GREEN))
b.append(box(320, 90, 130, 56, "运行", fill="#e8f1ec", stroke=GREEN))
b.append(box(580, 90, 130, 56, "等待", fill="#fdf1e3", stroke=AMBER))
b.append(arrow(190, 105, 320, 105, "被调度选中", GREEN))
b.append(arrow(320, 132, 190, 132, "时间片到 / 被剥夺"))
b.append(arrow(385, 146, 385, 210))
b.append(f'<path d="M385,210 L580,132" stroke="{INK}" stroke-width="1.8" marker-end="url(#ar)" fill="none"/>')
b.append(f'<text x="470" y="196" text-anchor="middle" font-size="12.5" fill="{MUTED}">等待 I/O 或资源</text>')
b.append(f'<path d="M645,90 L645,40 L255,40 L255,90" stroke="{GREEN}" stroke-width="1.8" marker-end="url(#arg)" fill="none"/>')
b.append(f'<text x="450" y="32" text-anchor="middle" font-size="12.5" fill="{GREEN}">事件完成（不能直达运行）</text>')
b.append(f'<text x="380" y="260" text-anchor="middle" font-size="13" fill="{MUTED}">高频考点：等待态不能直接转运行态，必须先进就绪队列</text>')
save("process-states.svg", "".join(b), 280)

# ---------- 2. TCP 三次握手 ----------
b = []
b.append(box(80, 80, 120, 50, "客户端"))
b.append(box(560, 80, 120, 50, "服务器"))
seq = [("SYN（seq=x）", 200), ("SYN+ACK（seq=y, ack=x+1）", 260), ("ACK（ack=y+1）", 320)]
for i, (t, y) in enumerate(seq):
    x1, x2 = (200, 560) if i % 2 == 0 else (560, 200)
    b.append(arrow(x1, y, x2, y, t, GREEN if i % 2 == 0 else INK, ly=-8))
b.append(f'<line x1="140" y1="130" x2="140" y2="360" stroke="{LINE}" stroke-width="1.4"/>')
b.append(f'<line x1="620" y1="130" x2="620" y2="360" stroke="{LINE}" stroke-width="1.4"/>')
b.append(f'<text x="380" y="395" text-anchor="middle" font-size="13" fill="{MUTED}">目的：确认双方收发能力，同步初始序号 —— 只有"真→假"才失败的连接建立</text>')
save("tcp-handshake.svg", "".join(b), 415)

# ---------- 3. 内聚与耦合梯度 ----------
b = []
couple = ["数据", "标记", "控制", "外部", "公共", "内容"]
cohere = ["偶然", "逻辑", "时间", "过程", "通信", "顺序", "功能"]
b.append(f'<text x="60" y="46" font-size="15" fill="{INK}" font-weight="700">耦合（模块之间，越低越好）</text>')
for i, t in enumerate(couple):
    w = 96
    x = 60 + i * (w + 18)
    shade = "#e8f1ec" if i < 2 else ("#fdf1e3" if i < 4 else "#fbeeed")
    b.append(box(x, 60, w, 42, t, fill=shade, stroke=GREEN if i < 2 else AMBER))
b.append(f'<text x="700" y="86" font-size="13" fill="{MUTED}">低→高</text>')
b.append(f'<text x="60" y="170" font-size="15" fill="{INK}" font-weight="700">内聚（模块内部，越高越好）</text>')
for i, t in enumerate(cohere):
    w = 82
    x = 60 + i * (w + 13)
    shade = "#fbeeed" if i < 2 else ("#fdf1e3" if i < 4 else "#e8f1ec")
    b.append(box(x, 184, w, 42, t, fill=shade, stroke=AMBER if i < 2 else GREEN))
b.append(f'<text x="700" y="210" font-size="13" fill="{MUTED}">低→高</text>')
b.append(f'<text x="380" y="278" text-anchor="middle" font-size="13" fill="{MUTED}">设计目标：高内聚 + 低耦合；速记：偶逻时过通顺功 / 数据标记控制外公共内容</text>')
save("cohesion-coupling.svg", "".join(b), 300)

# ---------- 4. 存储层次金字塔 ----------
b = []
layers = [
    ("寄存器", "#2d6a4f", "#ffffff", 120),
    ("Cache（SRAM）", "#3a7d5f", "#ffffff", 240),
    ("主存（DRAM）", "#6a9c85", "#ffffff", 360),
    ("外存（磁盘/SSD）", "#b7cfc2", INK, 480),
]
y = 40
for name, fill, tc, w in layers:
    x = (760 - w) / 2
    b.append(f'<rect x="{x}" y="{y}" width="{w}" height="46" fill="{fill}" stroke="none"/>')
    b.append(f'<text x="380" y="{y+29}" text-anchor="middle" font-size="14.5" fill="{tc}" font-weight="600">{name}</text>')
    y += 50
b.append(f'<text x="640" y="70" font-size="13" fill="{GREEN}" font-weight="600">↑ 更快 更贵 更小</text>')
b.append(f'<text x="640" y="250" font-size="13" fill="{AMBER}" font-weight="600">↓ 更慢 更便宜 更大</text>')
b.append(f'<text x="380" y="262" text-anchor="middle" font-size="13" fill="{MUTED}">层次依据：局部性原理（时间局部性 + 空间局部性）</text>')
save("memory-pyramid.svg", "".join(b), 290)

print("全部完成")
