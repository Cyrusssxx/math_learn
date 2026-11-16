# -*- coding: utf-8 -*-
"""按「收藏中的不会+不熟」快照构建笔记目录重点标记数据。

产物 pwa/data/fav_focus.json：
{
  "v": 1,
  "levels": {"hot": 10, "warm": 4},   // 很重点阈值 / 重点阈值（薄弱题数）
  "catNotes": { "<L2 id>": [ {"note":"高数2-一元微分","ch":9,"h3":[2,3]} , ... ] }
}
说明：
- ch = chapters 数组下标（= mdToHtml 里 ch-N 的 N），h3 = 该章内 ### 的全局序号（= h3-N 的 N）。
- 本脚本只在构建期用标题文本定位锚点；运行时 reader.js 读 examFav+examStatus 实时算薄弱题数并渲染，
  因此收藏/标记变化后无需重跑本脚本（只要涉及的知识点已在 catNotes 覆盖）。
- 覆盖 55 个收藏涉及的知识点（含薄弱 <4 的，便于将来涨上来即自动生效）。
"""
import json, re, sys, collections, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTES = os.path.join(ROOT, 'pwa/data/notes.json')
CAT = os.path.join(ROOT, 'pwa/data/exam_categories.json')
SNAP = r'D:/cjx/下载/download/做题数据-2026-11-16.json'
OUT = os.path.join(ROOT, 'pwa/data/fav_focus.json')

HOT, WARM = 10, 4

# 知识点 → [(笔记id, 章标题子串, [小节标题子串...] 可选)]
# 小节子串用于精确定位 h3；省略则只标章级。
RULES = {
    # ===== 高等数学 =====
    365: [  # 导数应用（39）→ 高数2 导数应用相关章 + 21记5 整篇导数应用
        ('高数2-一元微分', '导数应用：切法线与渐近线', ['切线与法线', '三类渐近线']),
        ('高数2-一元微分', '单调性与极值、最值', []),
        ('高数2-一元微分', '凹凸性与拐点', []),
        ('高数2-一元微分', '不等式证明', []),
        ('高数2-一元微分', '方程根', []),
        ('21记5-导数应用', '函数的单调性', []),
        ('21记5-导数应用', '函数极值', []),
        ('21记5-导数应用', '函数最值', []),
        ('21记5-导数应用', '曲线的凹凸性', []),
        ('21记5-导数应用', '曲线的拐点', []),
        ('21记5-导数应用', '不等式证明', []),
        ('21记5-导数应用', '方程根', []),
    ],
    2322: [  # 积分应用（26）→ 高数3.2 一元积分应用整篇
        ('高数3.2-一元积分-应用', '微元法（总纲）', []),
        ('高数3.2-一元积分-应用', '面积', []),
        ('高数3.2-一元积分-应用', '旋转体体积', []),
        ('高数3.2-一元积分-应用', '弧长', []),
        ('高数3.2-一元积分-应用', '形心与质心', []),
        ('21记7-定积分与反常积分', '定积分求平面图形的面积', []),
        ('21记7-定积分与反常积分', '旋转体体积', []),
        ('21记7-定积分与反常积分', '平面曲线弧长', []),
        ('21记7-定积分与反常积分', '质心形心公式', []),
    ],
    367: [  # 导数概念（21）→ 导数定义
        ('高数2-一元微分', '导数定义', ['定义与几何意义', '可导 / 可微 / 连续 关系表']),
        ('21记4-导数与微分', '导数定义', []),
    ],
    2321: [  # 积分计算（18）→ 高数3.1 计算篇
        ('高数3.1-一元积分-计算', '三大积分法', []),
        ('高数3.1-一元积分-计算', '换元法', []),
        ('高数3.1-一元积分-计算', '定积分独有方法', []),
        ('21记7-定积分与反常积分', '定积分的重要性质和计算', []),
    ],
    761: [  # 以各种形式给出微分方程（16）
        ('高数4-微分方程', '类型识别：框框dx + 框框dy', []),
        ('高数4-微分方程', '类型识别：框框·y′', []),
        ('高数4-微分方程', '微分方程综合题', []),
    ],
    762: [  # 解微分方程（15）
        ('高数4-微分方程', '一阶方程：五大类型', []),
        ('高数4-微分方程', '高阶：常系数线性方程', []),
        ('高数4-微分方程', '二阶变系数与可降阶', []),
        ('21记10-微分方程', '一阶微分方程求解', []),
        ('21记10-微分方程', '高阶微分方程求解', []),
    ],
    484: [  # 偏导数（14）
        ('高数5-多元微分', '偏导数', []),
        ('高数5-多元微分', '多元复合函数求偏导', []),
        ('高数5-多元微分', '多元隐函数求偏导', []),
        ('21记8-多元函数微分学', '多元复合函数偏导数和全微分的求法', []),
        ('21记8-多元函数微分学', '二元隐函数偏导数计算', []),
    ],
    177: [  # 特征值特征向量（14）
        ('线代5-特征值与相似', '特征值与特征向量：定义与性质', []),
        ('线代5-特征值与相似', '特征值的求法', []),
        ('21记15-特征值与对角化', '特征值和特征向量', []),
    ],
    179: [  # 相似对角化（12）
        ('线代5-特征值与相似', '相似对角化', []),
        ('21记15-特征值与对角化', '矩阵的相似对角化', []),
    ],
    157: [  # 解的关系（11）
        ('线代4-线性方程组', '解的关系：公共解与同解', []),
        ('21记14-向量与方程组', '方程组同解', []),
        ('21记14-向量与方程组', '方程组公共解', []),
    ],
    486: [  # 多元微分应用（10）
        ('高数5-多元微分', '无条件极值', []),
        ('高数5-多元微分', '条件极值', []),
        ('高数5-多元微分', '闭区域最值', []),
        ('21记8-多元函数微分学', '多元函数的无条件极值、条件极值、闭区域最值', []),
    ],
    # ===== 4–9 档 =====
    759: [('高数4-微分方程', '线性方程解的性质与结构', []),
          ('21记10-微分方程', '线性微分方程解的结构', [])],
    366: [('高数2-一元微分', '求导法则', []),
          ('高数2-一元微分', '基本初等函数求导公式', []),
          ('高数2-一元微分', '高阶导数', []),
          ('21记4-导数与微分', '求导公式和四则运算', []),
          ('21记4-导数与微分', '复合函数的导数', []),
          ('21记4-导数与微分', '隐函数求导', [])],
    202: [('线代6-二次型', '化标准形三大方法', []),
          ('21记16-二次型', '化二次型为标准形', [])],
    562: [('高数6-二重积分', '直角坐标计算', []),
          ('高数6-二重积分', '极坐标计算', []),
          ('21记9-二重积分', '二重积分计算', [])],
    329: [('高数1-极限', '极限计算：七类未定式', []),
          ('高数1-极限', '极限计算：三大思路', []),
          ('21记1-函数极限', '七种未定式极限的计算方法总结', [])],
    120: [('线代3-向量', '线性相关与线性无关', []),
          ('21记14-向量与方程组', '向量组的线性相关性', [])],
    132: [('线代4-线性方程组', '解的判定', []),
          ('21记14-向量与方程组', '齐次线性方程组判定与求解', []),
          ('21记14-向量与方程组', '非齐次线性方程组判定与求解', [])],
    180: [('线代5-特征值与相似', '实对称矩阵', []),
          ('线代5-特征值与相似', '谱分解', []),
          ('21记15-特征值与对角化', '实对称矩阵的相似对角化', [])],
    28:  [('线代2-矩阵', '矩阵高次幂', [])],
    210: [('线代6-二次型', '正定矩阵', []),
          ('21记16-二次型', '正定二次型', [])],
    31:  [('线代2-矩阵', 'AB=□ 专题', [])],
    178: [('线代5-特征值与相似', '矩阵相似', []),
          ('21记15-特征值与对角化', '矩阵的相似', [])],
    208: [('线代6-二次型', '化规范形', []),
          ('21记16-二次型', '惯性定理', [])],
    119: [('线代3-向量', '线性表示', []),
          ('21记14-向量与方程组', '线性表示', [])],
    483: [('高数5-多元微分', '重极限（多元函数的概念）', []),
          ('高数5-多元微分', '全微分', [])],
    758: [('高数4-微分方程', '微分方程综合题', []),
          ('21记10-微分方程', '微分方程综合题', [])],
    # ===== 收藏薄弱题涉及但薄弱数 <4 的知识点（低档，将来涨上来即自动生效） =====
    9:   [('线代1-行列式', '常考题型', []), ('线代1-行列式', '行列式公式', [])],
    10:  [('线代1-行列式', '常考题型', []), ('21记12-行列式与重要矩阵', '抽象型行列式计算（必记）', [])],
    11:  [('线代1-行列式', '（代数）余子式求和', []), ('21记12-行列式与重要矩阵', '代数余子式考点', [])],
    12:  [('线代1-行列式', '常考题型', [])],
    24:  [('线代2-矩阵', '逆矩阵', []), ('线代2-矩阵', '逆的求法', []), ('21记12-行列式与重要矩阵', '逆矩阵', [])],
    25:  [('线代2-矩阵', '伴随矩阵', []), ('21记12-行列式与重要矩阵', '伴随矩阵', [])],
    27:  [('线代2-矩阵', '矩阵的秩：定义与十大性质', []), ('线代2-矩阵', '秩的求法与满秩矩阵', []), ('21记13-初等变换与矩阵的秩', '矩阵的秩', [])],
    29:  [('线代2-矩阵', '初等变换与初等矩阵', []), ('21记13-初等变换与矩阵的秩', '初等矩阵与初等变换', [])],
    30:  [('线代2-矩阵', '分块矩阵', []), ('线代2-矩阵', '分块矩阵的秩', [])],
    32:  [('线代2-矩阵', '常考题型', [])],
    33:  [('线代2-矩阵', '常考题型', [])],
    52:  [('线代2-矩阵', '变形手法与元素特点翻译', [])],
    118: [('线代3-向量', '常考题型', [])],
    121: [('线代3-向量', '向量组等价', []), ('21记14-向量与方程组', '向量组等价', [])],
    135: [('线代4-线性方程组', '基础解系与齐次通解', []), ('线代4-线性方程组', '非齐次通解与特解', []),
          ('21记14-向量与方程组', '齐次线性方程组判定与求解', []), ('21记14-向量与方程组', '非齐次线性方程组判定与求解', [])],
    169: [('线代4-线性方程组', '矩阵方程', []), ('21记14-向量与方程组', '矩阵方程判定与求解', [])],
    203: [('线代6-二次型', '四种变换求变换矩阵', []), ('线代6-二次型', '二次型变换理论', [])],
    204: [('线代6-二次型', '化规范形', []), ('21记16-二次型', '惯性定理', [])],
    205: [('线代6-二次型', '二次型综合应用', [])],
    206: [('线代6-二次型', '二次型综合应用', []), ('高数5-多元微分', '闭区域最值', [])],
    209: [('线代6-二次型', '合同矩阵', []), ('21记16-二次型', '矩阵合同', [])],
    228: [('高数3.3-反常积分', '概念与精确定义', []), ('高数3.3-反常积分', '经典例题：审敛', []),
          ('21记7-定积分与反常积分', '反常积分的计算问题', [])],
    328: [('高数1-极限', '连续', []), ('21记3-连续间断与渐近线', '函数的连续', [])],
    368: [('高数2-一元微分', '微分中值定理', [])],
    485: [('高数5-多元微分', '重极限（多元函数的概念）', []), ('21记8-多元函数微分学', '二元函数连续性、可导性和可微性的判定', [])],
    563: [('高数6-二重积分', '准备工作：观察被积函数', [])],
    760: [('高数4-微分方程', '线性方程解的性质与结构', []), ('21记10-微分方程', '线性微分方程解的结构', [])],
    2708:[('线代2-矩阵', '正交矩阵与矩阵等价', []), ('21记12-行列式与重要矩阵', '正交矩阵（黄金重点）', [])],
}


def strip_src(title):
    """章标题里的 <!-- 源:... --> 注释不影响匹配，去掉再比。"""
    return re.sub(r'\s*<!--.*?-->', '', title).strip()


def main():
    notes = json.load(open(NOTES, encoding='utf-8'))
    # ⚠️ reader.js 初始化会过滤掉 id 以「21记」开头的笔记（考前21记已从主站隐藏），
    #    这些锚点永远不会渲染，构建期就剔除，避免无效数据。
    notes = [n for n in notes if not str(n.get('id', '')).startswith('21记')]
    by_id = {n['id']: n for n in notes}
    # 章标题 -> ch 序号；### 文本 -> h3 全局序号（文档顺序）
    index = {}
    for n in notes:
        chmap = {}
        for i, t in enumerate(n.get('chapters') or []):
            chmap[i] = strip_src(t)
        md = n.get('md', '')
        # 逐 ## 分块，按文档顺序给 ### 编号（与 mdToHtml 的 h3Idx 一致）
        blocks = re.split(r'(?=^## )', md, flags=re.M)
        h3_by_ch = collections.defaultdict(list)
        for b in blocks:
            if not b.startswith('## '):
                continue
            ci = len([k for k in chmap if _ch_title_matches(chmap[k], b.split('\n', 1)[0][3:].strip())]) - 1
            # 更稳妥：用出现顺序
            ci2 = None
            seen = 0
            for k in sorted(chmap):
                if _same_ch(chmap[k], b.split('\n', 1)[0][3:].strip()):
                    ci2 = k
                    break
            ci = ci2 if ci2 is not None else ci
            for h in re.findall(r'^###\s+(.+)$', b, re.M):
                h3_by_ch[ci].append(re.sub(r'\s*<!--.*?-->', '', h).strip())
        index[n['id']] = (chmap, h3_by_ch)

    out = {}
    errors = []
    for cid, rules in RULES.items():
        anchors = []
        for nid, ch_sub, h3_subs in rules:
            if nid.startswith('21记'):
                continue  # 主站隐藏的「考前21记」系列，静默跳过
            if nid not in by_id:
                errors.append(f'cat {cid}: 笔记不存在 {nid}')
                continue
            chmap, h3_by_ch = index[nid]
            # 精确匹配优先：子串恰好等于某章标题时直接取，避免「面积」误命中「旋转侧面积」
            exact = [i for i, t in chmap.items() if t == ch_sub]
            hits = exact if exact else [i for i, t in chmap.items() if ch_sub in t]
            if len(hits) != 1:
                errors.append(f'cat {cid}: 章「{ch_sub}」在 {nid} 命中 {len(hits)} 次: {[chmap[i] for i in hits]}')
                continue
            ch = hits[0]
            hs = []
            for sub in h3_subs:
                hlist = h3_by_ch[ch]
                mex = [j for j, t in enumerate(hlist) if t == sub]
                m = mex if mex else [j for j, t in enumerate(hlist) if sub in t]
                if len(m) != 1:
                    errors.append(f'cat {cid}: 小节「{sub}」在 {nid}/ch{ch} 命中 {len(m)} 次: {h3_by_ch[ch]}')
                    continue
                hs.append(m[0])
            anchors.append({'note': nid, 'ch': ch, 'h3': hs})
        if anchors:
            out[str(cid)] = anchors

    if errors:
        print('ERROR:')
        for e in errors: print(' ', e)
        sys.exit(1)

    snap = json.load(open(SNAP, encoding='utf-8'))
    data = snap['data']
    fav = json.loads(data['examFav'])
    st = json.loads(data['examStatus'])
    weak = {k for k, v in st.items() if v in ('unknown', 'unfamiliar')}
    inter = set(fav.keys()) & weak
    cat = json.load(open(CAT, encoding='utf-8'))
    covered = set(out.keys())
    want = set()
    for fn in ('pwa/data/exam.json', 'pwa/data/core_bank.json', 'pwa/data/dgy_items.json', 'pwa/data/bank_questions.json'):
        d = json.load(open(os.path.join(ROOT, fn), encoding='utf-8'))
        for p in (d if isinstance(d, list) else [d]):
            for s in p.get('sections', []):
                for q in s.get('questions', []):
                    ids = q.get('categoryIds') or []
                    if not ids:
                        continue
                    for key in (f'{p.get("id")}-{q["no"]}', str(q.get('id', '')), str(q.get('qid', ''))):
                        if key and key != 'None' and key in inter:
                            want.add(str(ids[0]))

    missing = sorted(want - covered, key=lambda x: int(x) if x.isdigit() else 0)
    print(f'收藏薄弱题覆盖知识点 {len(want)}；已建映射 {len(covered)}；缺 {len(missing)}')
    if missing:
        for cid in missing:
            print('  缺映射:', cid, cat.get(cid, {}).get('name'), cat.get(cid, {}).get('path'))
        sys.exit(2)

    hot = [c for c, a in out.items() if _count(c, inter, data) >= HOT]
    warm = [c for c, a in out.items() if WARM <= _count(c, inter, data) < HOT]
    print(f'薄弱题 ≥{HOT}: {len(hot)} 个（很重点）；{WARM}–{HOT-1}: {len(warm)} 个（重点）')

    # qid → 知识点：运行时读 examFav + examStatus 算薄弱题数所需。
    # 只收录被映射的知识点下的题；qid 与收藏/标记的主键完全一致（含 core-/DG 前缀与 qidOf 重定向别名）。
    q2cat = {}
    for fn in ('pwa/data/exam.json', 'pwa/data/core_bank.json', 'pwa/data/dgy_items.json',
               'pwa/data/bank_questions.json', 'pwa/data/ys27_items.json'):
        d = json.load(open(os.path.join(ROOT, fn), encoding='utf-8'))
        for p in (d if isinstance(d, list) else [d]):
            pid = p.get('id')
            for s in p.get('sections', []):
                for q in s.get('questions', []):
                    ids = q.get('categoryIds') or []
                    if not ids or str(ids[0]) not in out:
                        continue
                    cid = str(ids[0])
                    for key in (f'{pid}-{q["no"]}', str(q.get('id', '')), str(q.get('qid', '')),
                                str(q.get('linkedQid', ''))):
                        if key and key != 'None':
                            q2cat[key] = cid

    obj = {'v': 1, 'levels': {'hot': HOT, 'warm': WARM},
           'catNotes': out, 'q2cat': q2cat}
    with open(OUT, 'w', encoding='utf-8', newline='') as f:
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))
    print(f'写出 {OUT}: {os.path.getsize(OUT)} 字节, {len(out)} 个知识点映射, {len(q2cat)} 条 qid 索引')


def _same_ch(a, b):
    return strip_src(a) == strip_src(b)


def _ch_title_matches(a, b):
    return a in b or b in a


# 运行时统计由 reader.js 负责；这里只做构建期覆盖检查的占位（不写计数进产物）
def _count(cid, inter, data):
    return 0


if __name__ == '__main__':
    main()
