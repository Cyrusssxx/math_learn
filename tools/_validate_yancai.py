# -*- coding: utf-8 -*-
"""核心题库（yancai_bank.json）LaTeX 结构与污染全量校验。

检查项：
1. 反斜杠双写污染（\\命令）
2. 控制字符（\b \f \t 被误解析）
3. $ / $$ 配平（含跨行风险）
4. 花括号配平、\begin/\end 配对
5. 可疑宏（不在常见 KaTeX 白名单里的 \命令）
6. 【不确定：...】 待人工定稿清单
7. 选项完整性（选择题 A-D 是否齐全）
"""
import json, io, re, sys, collections

BANK = 'D:/ai code/math-note/tools/yancai_bank.json'

WHITELIST = set("""
frac dfrac tfrac cfrac sqrt int iint iiint oint sum prod lim to infty alpha beta gamma
delta epsilon varepsilon zeta eta theta vartheta iota kappa lambda mu nu xi pi varpi rho
varrho sigma varsigma tau upsilon phi varphi chi psi omega Gamma Delta Theta Lambda Xi Pi
Sigma Upsilon Phi Psi Omega left right cdot cdots times div pm mp le ge leq geq neq ne
approx equiv sim simeq cong propto in notin subset supset subseteq supseteq cup cap
setminus emptyset varnothing forall exists neg land lor implies iff Rightarrow Leftarrow
Leftrightarrow rightarrow leftarrow leftrightarrow mapsto uparrow downarrow partial nabla
infty angle perp parallel lVert rVert langle rangle lceil rceil lfloor rfloor mid nmid
begin end cases matrix pmatrix bmatrix vmatrix Vmatrix array aligned align gathered
displaystyle textstyle scriptstyle scriptscriptstyle limits nolimits over underline hat
bar vec dot ddot tilde widehat widetilde overrightarrow overleftarrow binom choose
overline mathrm mathbf mathit mathcal mathbb mathfrak boldsymbol text operatorname
quad qquad hspace vspace phantom boxed cancel color overbrace underbrace stackrel overset
underset substack nonumber notag tag log ln lg sin cos tan cot sec csc arcsin arccos
arctan sinh cosh tanh coth exp max min sup inf det dim ker deg gcd hom arg Pr
bmod pmod mod square triangle ast star circ bullet oplus otimes odot wedge vee
prime ldots vdots ddots dots cdot colon therefore because dotsb dotsc
prime ldots vdots ddots dots cdot colon therefore because dotsb dotsc
big Big bigg Bigg bigl bigr Bigl Bigr biggl biggr Biggl Biggr bigm Bigm
bigcap bigcup bigoplus bigotimes bigodot bigvee bigwedge bigsqcup
sgn sech csch arccot arcsec arccsc limsup liminf varlimsup varliminf
underbrace overbrace stackrel mathopen mathclose mathrel mathbin mathord mathpunct
hbox mbox intertext smallmatrix gather align multline split alignedat subarray
dcases subarray ch cr noalign displaylines cases matrix pmatrix bmatrix vmatrix
kappa Theta varphi epsilon in tbinom dbinom eqalign cr noalign
geqslant leqslant ngeqslant nleqslant gtrsim lesssim
""".split())

POLLUTE = re.compile(r'\\\\[A-Za-z]+')
CMDRE = re.compile(r'\\([A-Za-z]+)')


def walk(q):
    """产出 (字段名, 文本)"""
    yield 'stem', q.get('stem') or ''
    if q.get('options'):
        for k, v in q['options'].items():
            yield 'opt' + k, v or ''
    for k, v in (q.get('tips') or {}).items():
        yield 'tip' + k, v or ''


def main():
    bank = json.load(io.open(BANK, encoding='utf-8'))
    qs = bank['questions']
    print('题库题数:', len(qs))
    problems = collections.defaultdict(list)
    unsure = []
    badopt = []
    cmd_counter = collections.Counter()

    for q in qs:
        tag = 'yc-%s-%s' % (q['page'], q['order'])
        for field, txt in walk(q):
            if not txt:
                continue
            if POLLUTE.search(txt):
                problems['双写污染'].append((tag, field, txt[:80]))
            if re.search(r'[\x08\x0c\x07\x0b]', txt):
                problems['控制字符'].append((tag, field, repr(txt[:80])))
            if txt.count('$$') % 2 != 0:
                problems['$$不配平'].append((tag, field, txt[:80]))
            # 去掉 $$ 后检查单 $
            single = txt.replace('$$', '')
            if single.count('$') % 2 != 0:
                problems['$不配平'].append((tag, field, txt[:80]))
            if txt.count('{') != txt.count('}'):
                problems['花括号不配平'].append(
                    (tag, field, '左%d 右%d' % (txt.count('{'), txt.count('}'))))
            nb = len(re.findall(r'\\begin\{', txt))
            ne = len(re.findall(r'\\end\{', txt))
            if nb != ne:
                problems['begin/end不配对'].append((tag, field, 'begin%d end%d' % (nb, ne)))
            # 表格环境对齐符
            for env in re.findall(r'\\begin\{(aligned|array|cases|matrix|pmatrix|bmatrix|vmatrix)\}', txt):
                if env == 'array' and '{' not in txt:
                    problems['array缺列格式'].append((tag, field, txt[:60]))
            for m in CMDRE.finditer(txt):
                c = m.group(1)
                cmd_counter[c] += 1
                if c not in WHITELIST:
                    problems['可疑宏'].append((tag, field, '\\' + c))
            if '【不确定' in txt:
                idx = txt.find('【不确定')
                unsure.append((tag, field, txt[max(0, idx - 40):idx + 80]))
        # 选项完整性
        if q.get('type') == 'choice':
            opts = q.get('options') or {}
            missing = [k for k in 'ABCD' if k not in opts or not (opts.get(k) or '').strip()]
            if missing:
                badopt.append((tag, ''.join(missing), (q.get('stem') or '')[:60]))

    print()
    for k, v in problems.items():
        print('【%s】%d 处' % (k, len(v)))
        for item in v[:12]:
            print('   ', item)
        if len(v) > 12:
            print('    ... 其余 %d 处' % (len(v) - 12))
        print()

    print('【选择题选项缺失】%d 处' % len(badopt))
    for item in badopt[:15]:
        print('   ', item)
    print()

    print('【不确定待定稿】%d 处' % len(unsure))
    for item in unsure[:40]:
        print('   ', item)
    print()

    print('【高频宏 Top40】')
    for c, n in cmd_counter.most_common(40):
        flag = '' if c in WHITELIST else '  <-- 不在白名单'
        print('   \\%-18s %5d%s' % (c, n, flag))


if __name__ == '__main__':
    main()
