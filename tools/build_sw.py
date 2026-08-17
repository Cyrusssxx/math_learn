#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sw.py — 依据 sw.js 中 PRECACHE 预缓存资源的内容计算 SHA-256，
将结果注入 sw.js 的 CACHE_VER，实现「预缓存资源变动 → 缓存版本自动更新」。

用法：python3 tools/build_sw.py
- 若计算出的版本与当前不一致，则改写 sw.js 并返回退出码 1（表示有变动）；
- 若一致，则不改动并返回 0。

供 .githooks/pre-commit 调用：钩子据此判断是否需要 `git add pwa/sw.js`。
不需要手动维护版本号（遵循「有钩子优先创建钩子」约定）。
"""
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PWA_DIR = os.path.normpath(os.path.join(HERE, "..", "pwa"))
SW_PATH = os.path.join(PWA_DIR, "sw.js")
PREFIX = "mathcards-"


def compute_version():
    with open(SW_PATH, "r", encoding="utf-8") as f:
        text = f.read()

    m = re.search(r"const\s+PRECACHE\s*=\s*\[(.*?)\];", text, re.S)
    if not m:
        raise RuntimeError("未在 sw.js 中找到 PRECACHE 数组")

    block = m.group(1)
    paths = re.findall(r"['\"]([^'\"]+)['\"]", block)
    if not paths:
        raise RuntimeError("PRECACHE 数组为空或解析失败")

    h = hashlib.sha256()
    for p in paths:
        fp = os.path.join(PWA_DIR, p)
        if os.path.isfile(fp):
            with open(fp, "rb") as ff:
                h.update(ff.read())
        else:
            # 资源缺失：用占位串参与哈希，保证幂等且能感知删除
            h.update(b"__MISSING__" + p.encode("utf-8"))
    return PREFIX + h.hexdigest()[:10]


def main():
    new_ver = compute_version()
    with open(SW_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    new_text = re.sub(
        r"const\s+CACHE_VER\s*=\s*['\"][^'\"]*['\"];",
        "const CACHE_VER = '%s';" % new_ver,
        text,
        count=1,
    )
    if new_text != text:
        with open(SW_PATH, "w", encoding="utf-8") as f:
            f.write(new_text)
        print("[build_sw] CACHE_VER -> %s" % new_ver)
        return 1  # 有变动
    print("[build_sw] CACHE_VER 未变 (%s)" % new_ver)
    return 0


if __name__ == "__main__":
    sys.exit(main())
