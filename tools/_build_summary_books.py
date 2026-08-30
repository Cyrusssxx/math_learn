# -*- coding: utf-8 -*-
"""待办3：生成 3 篇「点睛总结册」md（高数上 / 高数下 / 线代），写入 D:/ai code/math/导图/。
内容：真题607（按12章）+ 好题240（按篇→书）+ 选填已做80（按内容3分上/下/线），四段凝练为单行。
选填无 categoryIds，按 stem 关键词粗分；缺口416标待补。文件名符合 build_notes.py 的 高数N-/线代N- 规则。
"""
import json, re
from pathlib import Path

ROOT = Path("D:/ai code/math-note")
DATA = ROOT / "pwa/data"
OUT = Path("D:/ai code/math/导图")  # 实际源目录（脚本在仓库内推导）
OUT = ROOT.parent / "math" / "导图"
OUT.mkdir(parents=True, exist_ok=True)

def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)

exam = load(DATA/"exam.json")
good = load(DATA/"good.json")
sel = load(DATA/"selected.json")
cats = load(DATA/"exam_categories.json")

CHAPTERS = {
    321: ("上","极限"), 322: ("上","一元微分"), 224: ("上","一元积分"),
    324: ("下","多元微分"), 326: ("下","二重积分"), 325: ("下","微分方程"),
    2: ("线","行列式"), 3: ("线","矩阵"), 4: ("线","向量"),
    5: ("线","线性方程组"), 6: ("线","特征值与特征向量"), 7: ("线","二次型"),
}
CHAPTER_IDS = set(CHAPTERS.keys())

id2node = {int(k): v for k, v in cats.items()}
def catid_to_chapter(cid):
    cur = id2node.get(cid); seen = set()
    while cur:
        if cur["id"] in CHAPTER_IDS:
            return cur["id"]
        pid = cur.get("parentId")
        if pid is None or pid in seen or pid not in id2node:
            return None
        seen.add(pid); cur = id2node.get(pid)
    return None

# 好题 name(真实) -> 篇（修正 好题8 真实名）
GOOD_BOOK = {
    "好题1-函数的性质":"上","好题2-函数极限连续":"上","好题3-函数极限连续概念题":"上",
    "好题4-极限与函数问题":"上","好题5-数列极限":"上","好题6-连续与间断点":"上",
    "好题7-导数与微分":"上","好题8-导数定义或其他方法求导":"上","好题9-微分概念问题":"上",
    "好题10-导数的应用":"上","好题11-微分证明":"上","好题12-泰勒的运用":"上",
    "好题13-不等式":"上","好题14-放缩":"上","好题15-构造证明":"上",
    "好题16-构图快速解答题":"上","好题17-特例解题":"上","好题18-绝对值与根号问题":"上",
    "好题19-一元函数积分学":"上","好题20-定积分与不定积分的基本运算":"上",
    "好题21-积分中值问题":"上","好题22-反常积分":"上","好题23-积分应用":"上",
    "好题24-微分方程的通特解":"下","好题25-微分方程的应用":"下",
    "好题26-多元微分概念问题":"下","好题27-多元函数偏导与表达式":"下",
    "好题28-多元函数最值问题":"下","好题29-二重积分":"下","好题30-计算错题":"下",
    "好题31-矩阵问题":"线","好题32-求相似正交转置矩阵问题":"线",
    "好题33-线性无关证明":"线","好题34-线性方程组问题":"线",
    "好题35-特征与二次型问题":"线","好题36-二次型最值问题":"线",
}

def parse_good_tips(md):
    out = {}
    segs = re.split(r'(?m)^##\s*(\d+)\.\s', md)
    for i in range(1, len(segs), 2):
        num = int(segs[i]); body = segs[i+1]
        m = re.search(r':::\s*点睛\s*(.*?)\n:::', body, re.S)
        if not m: continue
        block = m.group(1); d = {}
        for key, lab in [("gs","公式"),("yc","易错"),("jq","技巧"),("zy","注意")]:
            mm = re.search(r'-\s*\*\*'+lab+r'\*\*[：:]\s*([\s\S]*?)(?=\n-\s*\*\*|\Z)', block)
            d[key] = mm.group(1).strip() if mm else ""
        out[num] = d
    return out

def fmt_tip(d):
    parts = []
    for key, lab in [("gs","公式"),("yc","易错"),("jq","技巧"),("zy","注意")]:
        v = (d.get(key) or "").strip()
        if v:
            parts.append(f"**【{lab}】** {v}")
    return "；".join(parts)

# 真题按章
exam_ch = {}
for vol in exam:
    yr = vol.get("year")
    for sec in vol.get("sections", []):
        for q in sec.get("questions", []):
            chap = None
            for c in (q.get("categoryIds") or []):
                chap = catid_to_chapter(c)
                if chap: break
            if not chap: continue
            t = q.get("tips") or {}
            exam_ch.setdefault(chap, []).append((yr, q.get("no"),
                {k: t.get(k,"") for k in ("gs","yc","jq","zy")}))
for cid in exam_ch:
    exam_ch[cid].sort(key=lambda x: (x[0] or 0, x[1] or 0))

# 好题四段
good_tips = {g["name"]: parse_good_tips(g.get("md","")) for g in good}
good_in_book = {bk: {n: t for n, t in good_tips.items() if GOOD_BOOK.get(n)==bk}
                for bk in ("上","下","线")}

# 选填：已做(任一四段非空) 按 stem 关键词3分 上/下/线
LIN_KW = ["矩阵","向量","行列式","特征值","二次型","相似","正交","秩","线性相关","线性无关","方程组","伴随","转置","可逆","A^{*}","A^{-1}"]
DOWN_KW = ["偏导","多元","二重积分","累次积分","微分方程","通解","特解","可分离变量","齐次方程","一阶","二阶线性","全微分","方向导数","梯度","条件极值"]
def sel_module(stem):
    if any(k in stem for k in LIN_KW): return "线"
    if any(k in stem for k in DOWN_KW): return "下"
    return "上"
sel_done = {"上":[], "下":[], "线":[]}
sel_total = 0; sel_done_total = 0
for vol in sel.get("papers", []):
    title = vol.get("title","")
    for sec in vol.get("sections", []):
        for q in sec.get("questions", []):
            sel_total += 1
            t = q.get("tips") or {}
            if not any((t.get(k) or "").strip() for k in ("gs","yc","jq","zy")):
                continue
            sel_done_total += 1
            stem = q.get("stem","") or ""
            mod = sel_module(stem)
            sel_done[mod].append((title, q.get("no"),
                {k: t.get(k,"") for k in ("gs","yc","jq","zy")}))

# 输出
BOOKS = {
    "上": ("高数21-高数上·点睛总结册", "高数上·点睛总结册"),
    "下": ("高数22-高数下·点睛总结册", "高数下·点睛总结册"),
    "线": ("线代8-线代·点睛总结册", "线代·点睛总结册"),
}
for bk, (fname, h1) in BOOKS.items():
    L = [f"# {h1}", ""]
    L.append(f"> 本册聚合「真题 + 好题 + 选填」点睛精华（公式 / 易错 / 技巧 / 注意），按模块凝练。选填共 {sel_total} 题，本模块已点睛 {len(sel_done[bk])} 题，其余待补（见待办2）。")
    L.append("")
    # 真题（每章 H2，与现有真题凝练册风格一致）
    chaps = [(cid, name) for cid,(b, name) in CHAPTERS.items() if b==bk]
    for cid, cname in chaps:
        items = exam_ch.get(cid, [])
        L.append(f"## 真题·{cname}（{len(items)} 题）")
        for yr, no, d in items:
            tip = fmt_tip(d)
            if tip:
                L.append(f"- 📌 **{yr}年{no}题**：{tip}")
    # 好题
    gb = good_in_book[bk]
    L.append("")
    L.append(f"## 好题点睛（{bk}模块类，{sum(len(v) for v in gb.values())} 题 / {len(gb)} 篇）")
    for name in sorted(gb.keys(), key=lambda n: int(re.search(r'好题(\d+)', n).group(1))):
        tips = gb[name]
        L.append(f"### {name}（{len(tips)} 题）")
        for num in sorted(tips.keys()):
            tip = fmt_tip(tips[num])
            if tip:
                L.append(f"- 📌 **好题{num}**：{tip}")
    # 选填
    sd = sel_done[bk]
    L.append("")
    L.append(f"## 选填点睛（{bk}模块类已点睛 {len(sd)} 题；选填共 {sel_total}，其余待补）")
    for title, no, d in sd:
        tip = fmt_tip(d)
        if tip:
            L.append(f"- 📌 **[{title} {no}]**：{tip}")
    (OUT/(fname+".md")).write_text("\n".join(L), encoding="utf-8")
    print(f"写 {fname}.md：真题章 {len(chaps)}（{sum(len(exam_ch.get(c,[])) for c,_ in chaps)}题），好题 {len(gb)} 篇（{sum(len(v) for v in gb.values())}题），选填 {len(sd)} 题")

print(f"选填总计 {sel_total}，已点睛 {sel_done_total}（上{len(sel_done['上'])}/下{len(sel_done['下'])}/线{len(sel_done['线'])}），待补 {sel_total-sel_done_total}")
