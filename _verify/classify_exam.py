#!/usr/bin/env python
# 真题分类器 v3：exam 607 题 → 大观园三级分类（学科/章节/知识点），每题单一 L3 路径。
# 策略：① 题库逐题相似匹配(sim>=0.8) 高置信 → 取其 categoryIds 上卷到 L3；
#       ② 否则 CHAPTER_RULES 定章 → 章内 LEAF_BY_CH 细分到 L3 叶子（章作用域，杜绝跨章污染）；
#       ③ 章内未细分 → 落该章默认叶（DEFAULT_LEAF）；
#       ④ 仍无章 → 全局默认叶（导数计算）。
# 写回每题 categoryIds=[L3_id]；生成 pwa/data/exam_categories.json（2 L1 + 12 L2 + 59 L3，含清洗 display）。
import json, re
from difflib import SequenceMatcher

EXAM = "pwa/data/exam.json"
BANK = r"D:\cjx\下载\Compressed\daguanyuan-for-windows-main.1.1\daguanyuan-for-windows-main\assets\questions.json"
CAT  = r"D:\cjx\下载\Compressed\daguanyuan-for-windows-main.1.1\daguanyuan-for-windows-main\assets\categories.json"
OUT  = "pwa/data/exam_categories.json"

# ---- 章节 id（大观园二级节点，数二范围）----
CH = {
 "limit":   321,  "diff1":   322,  "int1":    224,  "ode":     325,
 "diffm":   324,  "int2":    326,  "det":     2,    "mat":     3,
 "vec":     4,    "lin":     5,    "eig":     6,    "quad":    7,
}
ROOT_IDS = {223, 1}  # 学科根：高等数学 / 线性代数

def is_shizhen(src):
    if "数二" not in src: return False
    m = re.search(r"(19|20)(\d{2})", src)
    if not m: return False
    y = int(m.group(0))
    if not (1987 <= y <= 2026): return False
    for s in ["880","1000题","660","1800","330","108题","习题","模拟","冲刺","强化",
              "基础选择","基础填空","综合选择","综合填空","版","重点题","重点"]:
        if s in src: return False
    return True

def exam_type(sec_title):
    if "选择" in sec_title: return "single_choice"
    if "填空" in sec_title: return "blank"
    return "subjective"

# ---- 分类树 ----
cats = {c["id"]: c for c in json.load(open(CAT, encoding="utf-8"))["items"]}
from collections import defaultdict
children = defaultdict(list)
for c in cats.values():
    if c["parentId"] is not None: children[c["parentId"]].append(c)

L3 = {}   # leaf_id -> chapter_id
for ch in CH.values():
    for c in children.get(ch, []):
        L3[c["id"]] = ch

def leaf_of(cid):
    """沿 parentId 上卷到 L3（其 parent 属于 12 章的那层）；否则 None。"""
    node = cats.get(cid)
    if not node: return None
    cur = cid
    while True:
        n = cats.get(cur)
        if not n: return None
        if n["parentId"] in CH.values(): return cur
        if n["parentId"] in ROOT_IDS: return None
        if n["parentId"] is None: return None
        cur = n["parentId"]

# ---- 章级规则（定章，按特异性排序：先线代→常微分→高数）----
CHAPTER_RULES = [
 (CH["det"],   ["行列式","余子式","代数余子式","|A|","克拉默","Cramer","\\begin{vmatrix"]),
 (CH["vec"],   ["向量组","线性表示","线性相关","线性无关","极大无关组","向量组的秩","\\alpha_1","\\alpha_2","\\beta_1"]),
 (CH["lin"],   ["线性方程组","基础解系","矩阵方程","有解","解的结构","Ax=0","Ax=b","方程组","\\begin{pmatrix}a&1&1","直线"]),
 (CH["eig"],   ["特征值","特征向量","相似","对角化","实对称矩阵","正交矩阵"]),
 (CH["quad"],  ["二次型","惯性指数","规范形","正定","标准形","\\mathbf{P}"]),
 (CH["mat"],   ["矩阵","方阵","伴随矩阵","逆矩阵","可逆","初等变换","初等矩阵","分块矩阵","秩为","矩阵的秩","转置","高次幂","A\\boldsymbol","\\boldsymbol A","A^*","A^2B","B=E"]),
 (CH["ode"],   ["微分方程","初值问题","通解","特解","可降阶","欧拉","污染","减速","的变化率"]),
 (CH["int2"],  ["二重积分","累次积分","极坐标系下积分","\\iint"]),
 (CH["diffm"], ["偏导","全微分","方向导数","梯度","多元","二元","f(x,y)","z=","dz","可微的充分条件","重极限","条件极值"]),
 (CH["diff1"], ["导数","可导","微分","可微","y''","y'''","y^{(n)}","f'(x)","f''(x)","f'(0)","参数方程","由方程","隐函数","切线","法线","曲率","驻点","凹凸","拐点","单调性","极值","零点","\\mathrm{d}y","\\mathrm{d}x","\\begin{cases}x=","f^{(5)}","y'|_{","相关变化率","相切","中值定理","罗尔","拉格朗日","柯西中值","柯西"]),
 (CH["limit"], ["\\lim","收敛","发散","单调有界","麦克劳林","泰勒","o(","等价无穷小","无穷小","数列","x\\to","n\\to\\infty","趋于","连续","间断点","渐近线"]),
 (CH["int1"],  ["不定积分","定积分","反常积分","积分","面积","体积","弧长","旋转体","质心","形心","功","\\int_","引力","液体的压力","抛物线","双曲线","平均值","平均速度"]),
]

# ---- 章内 L3 叶子规则（章作用域；命中即用；末项为本章默认叶）----
LEAF_BY_CH = {
 321: [  # 极限
   (328, ["连续","间断","可去","跳跃","闭区间","零点定理","介值","一致连续","最值定理"]),
   (329, ["\\lim","极限","收敛","发散","数列","无穷小","无穷大","趋向","单调有界","夹逼","渐近线无穷"]),
   (327, ["函数性质","奇偶性","周期性","有界性","反函数","复合函数","定义域"]),
 ],
 322: [  # 一元微分
   (368, ["中值定理","罗尔","拉格朗日","柯西","中值"]),
   (365, ["切线","法线","单调","极值","凹凸","拐点","渐近线","曲率","最值","驻点","凹凸性","作图","不等式","相关变化率","相切"]),
   (367, ["导数定义","可导","导数存在","左导数","右导数","微分概念"]),
   (366, ["求导","导数","微分","隐函数","参数方程","高阶导数","y'","f'(x)","f''(x)","y''"]),
 ],
 224: [  # 一元积分
   (228, ["反常积分","瑕积分","无穷区间","无穷限","收敛积分"]),
   (2322,["面积","体积","弧长","旋转体","质心","形心","功","引力","液体压力","平均值","平面图形","侧面积"]),
   (2321,["不定积分","定积分","积分计算","换元","分部","有理函数","求积分","计算积分"]),
 ],
 325: [  # 微分方程
   (758, ["已知解","逆问题","反求","验证","通解中","特解满足"]),
   (761, ["欧拉方程","伯努利","可降阶","齐次方程","一阶线性","以.*形式给出","隐式方程","变量分离"]),
   (760, ["解的结构","基本解组","通解结构","解空间"]),
   (759, ["初值问题","边值问题"]),
   (762, ["解微分方程","求通解微分方程","求特解微分方程","解方程"]),
 ],
 324: [  # 多元微分
   (485, ["重极限","累次极限","二重极限","极限存在","累次"]),
   (486, ["条件极值","拉格朗日乘数","切平面","法线","方向导数","梯度","空间曲线切线","多元最值","多元极值"]),
   (484, ["偏导","全微分","可微","高阶偏导","dz","偏导存在","混合偏导"]),
   (483, ["概念题","连续性","偏导存在性","可微判定"]),
 ],
 326: [  # 二重积分
   (562, ["二重积分","累次积分","极坐标","直角坐标","交换次序","积分区域","计算二重"]),
   (563, ["其他二重","杂项二重"]),
 ],
 2: [  # 行列式
   (13, ["克拉默","Cramer","克莱姆"]),
   (11, ["余子式","代数余子式","A_{ij}","M_{ij}"]),
   (12, ["以行列式形式","f(x)=|","多项式以行列式"]),
   (10, ["抽象","|kA|","|A^T|","|A^{-1}|","|AB|","行列式性质","范德蒙德","伴随矩阵"]),
   (9,  ["计算行列式","三阶行列式","上三角","下三角","按行展开","数值行列式"]),
 ],
 3: [  # 矩阵
   (24, ["逆矩阵","可逆","A^{-1}","求逆","的逆","不可逆"]),
   (25, ["伴随矩阵","A^*","伴随"]),
   (27, ["矩阵的秩","秩为","满秩","降秩","r(A)","秩"]),
   (28, ["高次幂","A^n","A^{","A^2","矩阵乘方","幂","A^3"]),
   (29, ["初等变换","初等矩阵","行变换","倍加","对换","倍乘","行等价"]),
   (30, ["分块矩阵","分块"]),
   (31, ["AB=","求解矩阵","设A=","满足AB","矩阵等式"]),
   (32, ["矩阵分解","分解","QR分解"]),
   (33, ["其他题型","杂题"]),
 ],
 4: [  # 向量
   (119, ["线性表示","可由","线性表出"]),
   (121, ["向量组等价","等价"]),
   (122, ["极大无关组","极大线性无关组"]),
   (120, ["线性相关","线性无关","相关性","秩为"]),
   (118, ["向量模","夹角","内积","正交","施密特","单位向量","方向向量"]),
 ],
 5: [  # 线性方程组
   (156, ["已知解","若.*是解","反求","推导","通解中"]),
   (157, ["解的关系","公共解","同解","两个解"]),
   (169, ["矩阵方程","AX=B","XA=B","解矩阵方程"]),
   (132, ["解的判定","有解","无解","唯一解","无穷多解","系数矩阵秩","增广矩阵","r(A)"]),
   (135, ["求解","求通解","基础解系","解方程组","通解为","特解为"]),
 ],
 6: [  # 特征值
   (180, ["实对称","对称矩阵","A^T=A","正交矩阵","正交相似","正交变换"]),
   (179, ["对角化","可对角化","相似对角化","对角矩阵"]),
   (178, ["相似于","相似","不相似"]),
   (177, ["特征值","特征向量","|\\lambda E","特征多项式","迹","特征根"]),
 ],
 7: [  # 二次型
   (210, ["正定","半正定","正定性","顺序主子式","P^TAP>0"]),
   (209, ["合同于","合同","不合同"]),
   (208, ["惯性指数","正惯性","负惯性"]),
   (204, ["规范形","规范型"]),
   (203, ["变成另一个","变换矩阵","化.*为.*矩阵","化为二次型"]),
   (207, ["可逆矩阵","P^TAP","P^\\top AP","合同变换"]),
   (206, ["二次型最值","二次型的最值"]),
   (205, ["二次型的解","解方程组二次"]),
   (202, ["标准形","标准型","化二次型","正交变换","配方","用正交变换"]),
   (201, ["二次型的秩","写出矩阵","二次型矩阵","的矩阵为"]),
 ],
}

DEFAULT_LEAF = {
 321:329, 322:366, 224:2321, 325:762, 324:484, 326:563,
 2:10, 3:33, 4:118, 5:135, 6:177, 7:202
}
GLOBAL_DEFAULT_LEAF = 366  # 兜底：一元微分/导数计算

def clean(s):
    s = re.sub(r"\$[^$]*\$", "", s)
    s = s.replace("$", "")
    s = re.sub(r"\s+", "", s)
    return s.strip("，。、 ")

# ---- 题库候选分桶 ----
bank = json.load(open(BANK, encoding="utf-8"))["items"]
cands = [it for it in bank if is_shizhen(it.get("source", ""))]
buckets = {}
for it in cands:
    m = re.search(r"(19|20)(\d{2})", it["source"])
    y = int(m.group(0))
    buckets.setdefault((y, it["type"]), []).append(it)

def detect_chapter(stem):
    for ch, kws in CHAPTER_RULES:
        if any(kw in stem for kw in kws):
            return ch
    return None

def leaf_in_chapter(ch, stem):
    for leaf_id, kws in LEAF_BY_CH.get(ch, []):
        if any(kw in stem for kw in kws):
            return leaf_id
    return None

# ---- 执行 ----
exam = json.load(open(EXAM, encoding="utf-8"))
stats = {lid: 0 for lid in L3}
bank_used = leaf_used = chap_used = fallback = 0
fallback_detail = defaultdict(int)
for e in exam:
    y = int(e["year"])
    for sec in e["sections"]:
        et = exam_type(sec.get("title") or sec.get("name"))
        for q in sec.get("questions", []):
            stem = q.get("stem", "")
            lid = None
            # ① 题库高置信 → L3
            pool = buckets.get((y, et), [])
            best_sim = 0.0; best_it = None
            for it in pool:
                s = SequenceMatcher(None, stem, it.get("stem", "")).ratio()
                if s > best_sim: best_sim = s; best_it = it
            if best_it and best_sim >= 0.8 and best_it.get("categoryIds"):
                for bcid in best_it["categoryIds"]:
                    lo = leaf_of(bcid)
                    if lo is not None:
                        lid = lo; break
                if lid is not None: bank_used += 1
            # ② 章内细分
            if lid is None:
                ch = detect_chapter(stem)
                if ch is not None:
                    lo = leaf_in_chapter(ch, stem)
                    if lo is not None:
                        lid = lo; leaf_used += 1
                    else:
                        lid = DEFAULT_LEAF[ch]; chap_used += 1
                        fallback_detail[ch] += 1
            # ③ 全局默认
            if lid is None:
                lid = GLOBAL_DEFAULT_LEAF; fallback += 1
                fallback_detail[0] = fallback_detail.get(0, 0) + 1
            q["categoryIds"] = [lid]
            stats[lid] += 1

json.dump(exam, open(EXAM, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

node_ids = set(ROOT_IDS) | set(CH.values()) | set(L3.keys())
name_map = {}
for nid in node_ids:
    c = cats[nid]
    level = 0 if nid in ROOT_IDS else (1 if nid in CH.values() else 2)
    name_map[str(nid)] = {
        "id": nid, "name": c["name"],
        "display": clean(c["name"]) or c["name"],
        "parentId": c["parentId"], "level": level, "path": c["path"],
    }
json.dump(name_map, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print("题库高置信:", bank_used, "| 章内细分:", leaf_used, "| 章默认叶:", chap_used, "| 全局兜底:", fallback)
print("各章落默认叶统计(章id->题数, 0=全局兜底):")
for k, v in sorted(fallback_detail.items()):
    print(f"  {('全局兜底' if k==0 else cats[k]['name']+'('+str(k)+')')}: {v}")
print("L3 分布:")
for lid, n in sorted(stats.items(), key=lambda x: -x[1]):
    print(f"  {cats[lid]['path']}: {n}")
print("合计:", sum(stats.values()))
print("已写回 exam.json 并生成", OUT)
