#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_sw.py — 依据 sw.js 中 PRECACHE 预缓存资源的内容计算 SHA-256，
将结果注入 sw.js 的 CACHE_VER，实现「预缓存资源变动 → 缓存版本自动更新」。

用法：
    python3 tools/build_sw.py            # 常规：按内容哈希自动更新
    python3 tools/build_sw.py --bump     # 强制升版：在内容哈希后追加/递增 -uN 后缀

设计要点
1. 版本 = 内容哈希（前缀 mathcards- + SHA-256 前 10 位）。
2. --bump：用于「内容哈希恰好与已发布版本相同、但缓存必须刷新」的场景。
   例如仓库习惯按指定路径部分提交时，sw.js 版本号可能超前于仓库实际内容
   （哈希算自工作区全量，而提交只含部分文件），此时后续资源即使变化也可能
   算出与已发布值相同的哈希，导致客户端 SW 不换缓存。用 --bump 强制升版。
3. 后缀保留：若 sw.js 当前值是 <内容哈希>-uN，则常规运行不会把它回退成纯哈希，
   避免手动 --bump 的结果被下一次提交悄悄撤销（回退会让客户端再一次换缓存，
   虽不致命但会造成无意义的重复刷新）。
4. pre-commit 场景自动检测：若内容哈希与 HEAD 中记录值相同，但本次提交确实
   改动了 PRECACHE 资源（git diff --cached HEAD），则自动追加 -u1，保证发布后
   客户端一定换缓存。

供 .githooks/pre-commit 调用：钩子据此判断是否需要 `git add pwa/sw.js`。
不需要手动维护版本号（遵循「有钩子优先创建钩子」约定）。
"""
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, ".."))
PWA_DIR = os.path.join(REPO, "pwa")
SW_PATH = os.path.join(PWA_DIR, "sw.js")
PREFIX = "mathcards-"
VER_RE = re.compile(r"const\s+CACHE_VER\s*=\s*['\"]([^'\"]+)['\"]")
# 用于替换：必须连同语句结尾的分号一起吃掉，否则会残留成 '...';;
VER_STMT_RE = re.compile(r"const\s+CACHE_VER\s*=\s*['\"][^'\"]*['\"]\s*;")
# <mathcards-xxxxxxxxxx>-u<N>
SUFFIX_RE = re.compile(r"^(mathcards-[0-9a-f]{10})-u(\d+)$")


def extract_paths():
    """解析 sw.js 中 PRECACHE 数组里的资源相对路径列表。"""
    with open(SW_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"const\s+PRECACHE\s*=\s*\[(.*?)\];", text, re.S)
    if not m:
        raise RuntimeError("未在 sw.js 中找到 PRECACHE 数组")
    paths = re.findall(r"['\"]([^'\"]+)['\"]", m.group(1))
    if not paths:
        raise RuntimeError("PRECACHE 数组为空或解析失败")
    return paths


def compute_version(paths):
    """按 PRECACHE 资源内容计算内容哈希版本号。"""
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


def _git(*args):
    """在仓库根执行 git 命令，失败返回 (非0, '')。"""
    try:
        r = subprocess.run(
            ["git", *args], cwd=REPO,
            capture_output=True, text=True, encoding="utf-8", errors="ignore",
        )
        return r.returncode, r.stdout
    except Exception:
        return 1, ""


def head_cache_ver():
    """读取 git HEAD 中 sw.js 记录的 CACHE_VER（用于判断是否真的需要换缓存）。"""
    rc, out = _git("show", "HEAD:pwa/sw.js")
    if rc == 0:
        m = VER_RE.search(out)
        if m:
            return m.group(1)
    return None


def precache_changed(paths):
    """本次提交是否改动了 PRECACHE 资源（pre-commit 阶段改动已在 index 中）。"""
    rel = ["pwa/" + p for p in paths]
    rc, out = _git("diff", "--cached", "--name-only", "HEAD", "--", *rel)
    if rc != 0:
        return False
    return bool(out.strip())


def main():
    paths = extract_paths()
    base_ver = compute_version(paths)

    with open(SW_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    m = VER_RE.search(text)
    if not m:
        raise RuntimeError("未在 sw.js 中找到 CACHE_VER 定义")
    cur_ver = m.group(1)

    force = "--bump" in sys.argv

    if force:
        # 强制升版：已有同基线的 -uN 后缀则递增，否则从 -u1 开始
        sm = SUFFIX_RE.match(cur_ver)
        n = (int(sm.group(2)) + 1) if (sm and sm.group(1) == base_ver) else 1
        new_ver = "%s-u%d" % (base_ver, n)
    elif cur_ver == base_ver:
        # 内容哈希一致：若本次提交确实动了 PRECACHE 资源，仍须升版（防 SW 不换缓存）
        if precache_changed(paths):
            new_ver = base_ver + "-u1"
        else:
            print("[build_sw] CACHE_VER 未变 (%s)" % cur_ver)
            return 0
    else:
        sm = SUFFIX_RE.match(cur_ver)
        if sm and sm.group(1) == base_ver:
            # 已是「本基线 + -uN」：保留，避免回退造成客户端无意义重复换缓存
            print("[build_sw] CACHE_VER 未变 (%s)" % cur_ver)
            return 0
        new_ver = base_ver

    new_text = VER_STMT_RE.sub("const CACHE_VER = '%s';" % new_ver, text, count=1)
    if new_text != text:
        with open(SW_PATH, "w", encoding="utf-8") as f:
            f.write(new_text)
        print("[build_sw] CACHE_VER -> %s" % new_ver)
        return 1  # 有变动
    print("[build_sw] CACHE_VER 未变 (%s)" % cur_ver)
    return 0


if __name__ == "__main__":
    sys.exit(main())
