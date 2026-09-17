# -*- coding: utf-8 -*-
"""手工补全最后 9 题（参考库未收录的经典老题）：答案 + 解析 + 2 处题干修正 + 1 处选项格式修正。

每条答案均给出可自查的推导（写入 ref_idea，供「思路」按钮显示）。
注意：含撇号（f'）的字符串一律用双引号 raw string，避免单引号截断。
"""
import json, io, re

BANK = 'D:/ai code/math-note/tools/yancai_bank.json'
b = json.load(io.open(BANK, encoding='utf-8'))
idx = {q['id']: q for q in b['questions']}
log = []

MANUAL = {
    "yc-63-1": (
        r"（D）",
        r"$F(x)=\int_1^x f(t)\,\mathrm{d}t$：当 $0\le x<1$ 时 $F(x)=-\int_x^1 t^{2}\mathrm{d}t=\dfrac{x^{3}}{3}-\dfrac{1}{3}$；"
        r"当 $1\le x\le2$ 时 $F(x)=\int_1^x 1\,\mathrm{d}t=x-1$。故选 (D)。"),
    "yc-78-1": (
        r"（B）",
        r"$f(x)>0$ 且 $f'(x)<0$：矩形高 $f(b)$ 为区间上的最小值，故 $S_2=f(b)(b-a)<\int_a^b f=S_1$；"
        r"又 $f''(x)>0$ 说明曲线在弦下方，梯形 $S_3=\frac12[f(a)+f(b)](b-a)>S_1$。故 $S_2<S_1<S_3$，选 (B)。"),
    "yc-79-4": (
        r"$\dfrac{\pi}{4-\pi}$",
        r"令 $A=\int_0^1 f(x)\mathrm{d}x$，则 $A=\int_0^1\dfrac{\mathrm{d}x}{1+x^{2}}+A\int_0^1\sqrt{1-x^{2}}\,\mathrm{d}x"
        r"=\dfrac{\pi}{4}+A\cdot\dfrac{\pi}{4}$，解得 $A=\dfrac{\pi/4}{1-\pi/4}=\dfrac{\pi}{4-\pi}$。"),
    "yc-79-5": (
        r"（A）",
        r"取极值时 $a_1,b_1$ 是 $x$ 关于 $\{\cos x,\sin x\}$ 的 Fourier 系数："
        r"$a_1=\dfrac{1}{\pi}\int_{-\pi}^{\pi}x\cos x\,\mathrm{d}x=0$（奇函数），"
        r"$b_1=\dfrac{1}{\pi}\int_{-\pi}^{\pi}x\sin x\,\mathrm{d}x=\dfrac{2}{\pi}\int_0^{\pi}x\sin x\,\mathrm{d}x=2$。"
        r"故 $a_1\cos x+b_1\sin x=2\sin x$，选 (A)。"),
    "yc-80-1": (
        r"（D）",
        r"$\dfrac{\sin x}{1+x^{2}}\cos^{4}x$ 为奇函数 $\Rightarrow M=0$；"
        r"$N=\int_{-\pi/2}^{\pi/2}\sin^{3}x\,\mathrm{d}x+\int_{-\pi/2}^{\pi/2}\cos^{4}x\,\mathrm{d}x"
        r"=0+2\int_0^{\pi/2}\cos^{4}x\,\mathrm{d}x>0$；"
        r"$P=0-2\int_0^{\pi/2}\cos^{4}x\,\mathrm{d}x=-N<0$。故 $P<M<N$，选 (D)。"),
    "yc-81-2": (
        r"（D）",
        r"令 $u=tx$，则 $I=t\int_0^{s/t}f(tx)\,\mathrm{d}x=\int_0^{s}f(u)\,\mathrm{d}u$，"
        r"故 $I$ 只依赖于 $s$、不依赖于 $t$，选 (D)。"),
    "yc-81-3": (
        r"（A）",
        r"$\mathrm{e}^{\sin t}\sin t$ 以 $2\pi$ 为周期 $\Rightarrow F(x)$ 为常数；"
        r"由 $\int_0^{2\pi}\mathrm{e}^{\sin t}\sin t\,\mathrm{d}t=\int_0^{2\pi}\mathrm{e}^{\sin t}\cos^{2}t\,\mathrm{d}t>0$"
        r"（分部积分），故为正常数，选 (A)。"),
    "yc-81-5": (
        r"$x f(x^{2})$",
        r"令 $u=x^{2}-t^{2}$，则 $\mathrm{d}u=-2t\,\mathrm{d}t$，"
        r"$\int_0^{x} t f(x^{2}-t^{2})\,\mathrm{d}t=\frac12\int_0^{x^{2}} f(u)\,\mathrm{d}u$，"
        r"故 $\dfrac{\mathrm{d}}{\mathrm{d}x}\int_0^{x} t f(x^{2}-t^{2})\,\mathrm{d}t=x f(x^{2})$。"),
    "yc-81-7": (
        r"（A）$(0,1)$",
        r"令 $G(x)=\int_1^{x}\dfrac{\sin t}{t}\mathrm{d}t-\ln x$，则 $G(1)=0$，"
        r"$G'(x)=\dfrac{\sin x-1}{x}\le0$（$x>0$），故 $G$ 单调不增，"
        r"于是 $x<1$ 时 $G(x)>0$，即 $x\in(0,1)$，选 (A)。"),
}

# 题干修正（PDF 文字层为据）
STEM_FIX = {
    "yc-81-2": (r"$I=t\int_0^{t}f(x)\,\mathrm{d}x$",
                r"$I=t\displaystyle\int_0^{\frac{s}{t}}f(tx)\,\mathrm{d}x$"),
    "yc-81-5": (r"\int_0^x f(x^2-t^2)\,\mathrm{d}t",
                r"\int_0^x t f(x^2-t^2)\,\mathrm{d}t"),
}

# 选项格式修正：yc-81-7 的 B、C 缺 $...$ 包裹（会渲染成裸 LaTeX）
OPT_FIX = {
    "yc-81-7": {
        "B": (r"\left(1,\frac{\pi}{2}\right).", r"$\left(1,\dfrac{\pi}{2}\right)$．"),
        "C": (r"\left(\frac{\pi}{2},\pi\right).", r"$\left(\dfrac{\pi}{2},\pi\right)$．"),
    },
}

for qid, (old, new) in STEM_FIX.items():
    q = idx[qid]
    if old in q["stem"]:
        q["stem"] = re.sub(r"\s*【不确定[^】]*】", "", q["stem"].replace(old, new)).strip()
        log.append((qid, "题干修正", old, new))
    else:
        log.append((qid, "题干未匹配！", old, ""))

for qid, fixes in OPT_FIX.items():
    q = idx[qid]
    for k, (old, new) in fixes.items():
        if old in q["options"][k]:
            q["options"][k] = q["options"][k].replace(old, new)
            log.append((qid + ".opt" + k, "选项 LaTeX 修正", old, new))
        else:
            log.append((qid + ".opt" + k, "选项未匹配！", old, q["options"][k][:40]))

for qid, (ans, idea) in MANUAL.items():
    q = idx[qid]
    q["ref_answer"] = ans
    q["ref_idea"] = idea
    q["ans_ref"] = "manual:数学推导"
    q["ans_tier"] = "manual"
    q["ans_score"] = 1.0
    log.append((qid, "手工答案", "（无）", ans))

with io.open(BANK, "w", encoding="utf-8", newline="") as f:
    json.dump(b, f, ensure_ascii=False, indent=1)

tot = len(b["questions"])
ok = sum(1 for q in b["questions"] if (q.get("ref_answer") or "").strip()
         or (q.get("ref_idea") or "").strip())
print("手工处理 %d 项：" % len(log))
for it in log:
    print("  [%s] %s：%s -> %s" % (it[0], it[1], it[2][:46], it[3][:46]))
print()
print("答案覆盖：%d / %d（%.1f%%）" % (ok, tot, 100.0 * ok / tot))
