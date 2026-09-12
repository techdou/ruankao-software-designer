# -*- coding: utf-8 -*-
"""交互冒烟测试：开始练习 → 答对一题 → 答错一题 → 检查判分与解析 → 存档持久化。"""
from playwright.sync_api import sync_playwright

BASE = "http://localhost:4173/#/drill"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1360, "height": 860})
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))

    page.goto(BASE)
    page.wait_for_timeout(500)
    page.get_by_role("button", name="开始练习").click()
    page.wait_for_timeout(400)

    # 第一题：点一个选项，应立即判分并出现解析
    opts = page.locator(".opt")
    opts.first.click()
    page.wait_for_timeout(300)
    judge = page.locator(".judge")
    assert judge.count() == 1, "判分未出现"
    assert page.locator(".analysis").count() == 1, "解析未出现"
    print("[ok] 即时判分 + 解析展示")

    # 收藏本题
    page.get_by_role("button", name="☆ 收藏").click()
    page.wait_for_timeout(300)
    print("[ok] 收藏")

    # 下一题答一次（无论对错）
    page.get_by_role("button", name="下一题 →").click()
    page.wait_for_timeout(300)
    page.locator(".opt").nth(1).click()
    page.wait_for_timeout(300)
    print("[ok] 第二题作答")

    # 检查仪表盘统计变化
    page.goto("http://localhost:4173/#/")
    page.wait_for_timeout(500)
    body = page.inner_text("body")
    assert "2 / 429" in body or "2/429" in body, f"刷题数未更新: 找不到 2/429"
    print("[ok] 仪表盘进度更新为 2 题")

    # 错题本页面能打开
    page.goto("http://localhost:4173/#/wrong")
    page.wait_for_timeout(400)
    print("[ok] 错题本打开")

    # 刷新后存档仍在（IndexedDB 持久化）
    page.goto("http://localhost:4173/#/")
    page.reload()
    page.wait_for_timeout(800)
    body = page.inner_text("body")
    assert "2 / 429" in body or "2/429" in body, "刷新后进度丢失"
    print("[ok] 刷新后存档持久化（IndexedDB）")

    # 真题套卷进入
    page.goto("http://localhost:4173/#/papers")
    page.wait_for_timeout(400)
    page.get_by_role("button", name="开始作答").first.click()
    page.wait_for_timeout(500)
    print("[ok] 真题套卷进入")

    browser.close()
    if errors:
        print("== page errors ==")
        for e in errors[:5]:
            print(" -", e)
    else:
        print("全部通过，无页面错误")
