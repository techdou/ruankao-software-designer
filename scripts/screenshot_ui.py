"""对备考站全部页面截图，供 UI/UX 评审。用法：先起 dev server（默认 5199），再 python scripts/screenshot_ui.py"""
import os
import sys
from playwright.sync_api import sync_playwright

BASE = "http://localhost:5199/#"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "refs", "ui-audit")
PAGES = [
    ("dashboard", "/"),
    ("notes", "/notes"),
    ("notereader", "/notes/ch01"),
    ("drill", "/drill"),
    ("papers", "/papers"),
    ("exam", "/exam"),
    ("cases", "/cases"),
    ("wrong", "/wrong"),
    ("favorites", "/favorites"),
    ("stats", "/stats"),
    ("settings", "/settings"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    for name, path in PAGES:
        page.goto(BASE + path)
        page.wait_for_timeout(1200)
        page.screenshot(path=f"{OUT}\\{name}.png", full_page=True)
        print(f"ok {name}")
    # 移动端宽度过一遍主要页
    m = browser.new_page(viewport={"width": 390, "height": 844})
    for name, path in [("m-dashboard", "/"), ("m-notes", "/notes"), ("m-notereader", "/notes/ch01"), ("m-drill", "/drill")]:
        m.goto(BASE + path)
        m.wait_for_timeout(1200)
        m.screenshot(path=f"{OUT}\\{name}.png", full_page=True)
        print(f"ok {name}")
    browser.close()
print("done")
