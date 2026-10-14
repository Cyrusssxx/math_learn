#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""1) 新增 core-1076（2017 第八届全国大学生数学竞赛·正号版，用户截图收录）
   2) 全库答案排版修复：解析步骤分段（。由/。故/… → 。\n\n由，$ 平衡保护）
      + answer 开头重复的【答案】归一
   dry-run 先报告；不带 --dry-run 写回（JSON 往返自检 + 自动备份）。
"""
import io, json, os, sys, collections, shutil, time, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, 'pwa', 'data', *a)
DRY = '--dry-run' in sys.argv

# ---------- 新题 ----------
NEW_NO = 1076
NEW_Q = {
    "no": NEW_NO,
    "source": "2017年第八届全国大学生数学竞赛题（重点）",
    "catId": 484,
    "categoryIds": [484],
    "stem": r"设 $ f(x,y) $ 可微，满足 $ f^{\prime}_{x}(x,y)=f(x,y) $，$ \lim\limits_{n\to\infty}\left[\dfrac{f\left(0,y+\frac{1}{n}\right)}{f(0,y)}\right]^{n}=\mathrm{e}^{\cot y} $，且 $ f\left(0,\dfrac{\pi}{2}\right)=1 $，求 $ f(x,y) $。",
    "answer": (
        "【答案】$ f(x,y)=\\mathrm{e}^{x}\\sin y $。\n\n"
        "【分析】极限的底数 $ \\dfrac{f(0,y+\\frac{1}{n})}{f(0,y)} \\to 1 $，属「$ 1^{\\infty} $」型，"
        "用 $ \\lim(1+u)^{\\frac{1}{u}}=\\mathrm{e} $ 或取对数化成导数定义，"
        "即可把条件转化为 $ \\dfrac{f‘_y(0,y)}{f(0,y)}=\\cot y $，先求出 $ f(0,y) $，"
        "再由 $ f‘_x=f $ 视 $ y $ 为常数积分并定常数。\n\n"
        "【解】先由极限条件求 $ f(0,y) $。取对数：\n\n"
        "$ \\ln\\lim\\limits_{n\\to\\infty}\\left[\\dfrac{f(0,y+\\frac{1}{n})}{f(0,y)}\\right]^{n}"
        "=\\lim\\limits_{n\\to\\infty}\\dfrac{n\\left[f(0,y+\\frac{1}{n})-f(0,y)\\right]}{f(0,y)}"
        "=\\dfrac{f‘_y(0,y)}{f(0,y)}=\\cot y $。\n\n"
        "故 $ \\dfrac{\\partial}{\\partial y}\\ln|f(0,y)|=\\cot y $，积分得 $ \\ln|f(0,y)|=\\ln|\\sin y|+\\ln|C| $，"
        "即 $ f(0,y)=C\\sin y $。由 $ f(0,\\frac{\\pi}{2})=1 $ 得 $ C=1 $，故 $ f(0,y)=\\sin y $。\n\n"
        "再由 $ f‘_x(x,y)=f(x,y) $，得 $ \\dfrac{f‘_x(x,y)}{f(x,y)}=1 $，视 $ y $ 为常数，"
        "对 $ x $ 积分：$ \\ln|f(x,y)|=x+\\varphi(y) $，即 $ f(x,y)=C(y)\\,\\mathrm{e}^{x} $。\n\n"
        "令 $ x=0 $：$ C(y)=f(0,y)=\\sin y $。故 $ f(x,y)=\\mathrm{e}^{x}\\sin y $。\n\n"
        "【易错】① 化极限为导数定义时，分母是 $ f(0,y) $，需 $ f(0,y)\\neq0 $ "
        "（由 $ \\ln|f(0,y)|=\\ln|\\sin y|+\\ln|C| $ 反推自洽）；"
        "② 对 $ x $ 积分时的“常数”是 $ C(y) $，必须用 $ x=0 $ 的条件定出，不能写成 $ C $。"
    ),
    "idea": (
        "**思路概括：**「$ 1^{\\infty} $」型极限取对数化成导数定义，得 $ f‘_y(0,y)/f(0,y)=\\cot y $，"
        "积分并用 $ f(0,\\frac{\\pi}{2})=1 $ 定常数求出 $ f(0,y)=\\sin y $；"
        "再由 $ f‘_x=f $ 对 $ x $ 积分得 $ f=C(y)\\mathrm{e}^{x} $，令 $ x=0 $ 定 $ C(y) $ 即可。"
    ),
}

STEP_RE = re.compile(r'。(ustr)')


def balance_split(text):
    r"""在公式外的「。」后、且紧跟步骤词（由/故/因此/所以/解/另解/法一/法二/注/（Ⅰ/Ⅱ/Ⅲ）时插 \n\n。
    $ 计数平衡保护：只处理公式外的句号。返回 (新文本, 插入数)。"""
    out = []
    n = len(text)
    i = 0
    dollar = 0
    ins = 0
    steps = '由故因所解另法注（'
    while i < n:
        c = text[i]
        out.append(c)
        if c == '$':
            dollar ^= 1
        elif c == '。' and dollar % 2 == 0:
            # 看后面的字符（跳过可能存在的换行）
            j = i + 1
            while j < n and text[j] in '\n':
                j += 1
            nxt = text[j] if j < n else ''
            if nxt in '由故解注' or text[j:j + 2] in ('因此', '所以', '另解', '法一', '法二', '法三', '（Ⅰ', '（Ⅱ', '（Ⅲ'):
                # 若紧跟已换行则不重复插
                if not (i + 1 < n and text[i + 1] == '\n'):
                    out.append('\n\n')
                    ins += 1
        i += 1
    return ''.join(out), ins


def fix_answer(a):
    """返回 (新 answer, 归一【答案】? 0/1, 插入分段数)"""
    orig = a
    # 归一开头重复的【答案】
    m = re.match(r'^(【答案】)+', a)
    norm = 0
    if m and (m.end() - m.start()) > 4:      # 超过一个【答案】的长度
        a = '【答案】' + a[m.end():]
        norm = 1
    b, ins = balance_split(a)
    if b != orig or norm:
        return b, norm, ins
    return a, 0, 0


def main():
    path = P('core_bank.json')
    raw = io.open(path, encoding='utf-8').read()
    core = json.loads(raw)
    secs = core[0]['sections']

    # 备份
    if not DRY:
        bak = os.path.join(ROOT, 'tools', '_bak_deepcats', time.strftime('%Y%m%d-%H%M%S') + '-fmt')
        os.makedirs(bak, exist_ok=True)
        shutil.copy2(path, os.path.join(bak, 'core_bank.json'))
        print('已备份', bak)

    # ---- 1) 新增 1076 ----
    dup = [q for s in secs for q in s['questions'] if q['no'] == NEW_NO]
    maxno = max(q['no'] for s in secs for q in s['questions'])
    print('新增前：最大 no=%d，no=%d 重复=%d' % (maxno, NEW_NO, len(dup)))
    added = False
    if not dup:
        assert NEW_NO == maxno + 1, '新题号必须接在最大号后（%d）' % (maxno + 1)
        sec = next((s for s in secs if s['title'] == '多元微分'), None)
        assert sec, '找不到「多元微分」节'
        sec['questions'].append(dict(NEW_Q))
        sec['questions'].sort(key=lambda q: q['no'])
        added = True
        print('已新增 core-%d（多元微分/偏导数484，正号版）' % NEW_NO)

    # ---- 2) 全库答案排版 ----
    stat = collections.Counter()
    for s in secs:
        for q in s['questions']:
            a = q.get('answer') or ''
            b, norm, ins = fix_answer(a)
            if b != a:
                q['answer'] = b
                stat['排版修改'] += 1
                if norm:
                    stat['归一【答案】'] += 1
                stat['插分段'] += ins
                if len(stat) and stat['排版修改'] <= 3:
                    pass
    print('排版修复：%d 题，共插分段 %d 处，归一【答案】 %d 题' % (
        stat['排版修改'], stat['插分段'], stat['归一【答案】']))
    # 679 专项确认
    q679 = next(q for s in secs for q in s['questions'] if q['no'] == 679)
    a679 = q679['answer']
    print('679 段落数（\\n\\n+1）:', a679.count('\n\n') + 1, '｜开头:', repr(a679[:8]))

    if DRY:
        print('（dry-run，未写）')
        return 0

    out = json.dumps(core, ensure_ascii=False, separators=(',', ':'))
    assert json.loads(out) == core, '往返自检失败'
    io.open(path, 'w', encoding='utf-8', newline='\n').write(out)
    print('已写回 core_bank.json（紧凑，往返自检 OK），总题数',
          sum(len(s['questions']) for s in secs))
    return 0


if __name__ == '__main__':
    sys.exit(main())
