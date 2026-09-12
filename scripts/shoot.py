# -*- coding: utf-8 -*-
"""逐页截图验收：app/src/../shots/*.png"""
from playwright.sync_api import sync_playwright
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "shots"
OUT.mkdir(exist_ok=True)

PAGES = [
    ("home", "http://localhost:4173/#/"),
    ("notes", "http://localhost:4173/#/notes"),
    ("note-ch04", "http://localhost:4173/#/notes/ch04"),
    ("drill", "http://localhost:4173/#/drill"),
    ("papers", "http://localhost:4173/#/papers"),
    ("cases", "http://localhost:4173/#/cases"),
    ("case-dfd", "http://localhost:4173/#/cases"),
    ("stats", "http://localhost:4173/#/stats"),
    ("settings", "http://localhost:4173/#/settings"),
    ("exam", "http://localhost:4173/#/exam"),
]

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1360, "height": 860})
    errors = []
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.on("pageerror", lambda e: errors.append(str(e)))
    for name, url in PAGES:
        page.goto(url)
        page.wait_for_timeout(700)
        page.screenshot(path=str(OUT / f"{name}.png"))
        print(f"[shot] {name}")
    browser.close()
    if errors:
        print("== console errors ==")
        for e in errors[:10]:
            print(" -", e)
    else:
        print("无控制台错误")
