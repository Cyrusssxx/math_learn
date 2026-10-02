# -*- coding: utf-8 -*-
"""分类页默认排序改为「掌握度分组」：不会 → 不熟 → 收藏 → 无标记 → 掌握（掌握排最下）
   组内仍按年份（受年份排序开关控制）与收藏时间；「⭕ 无标记」开关保留为「无标记优先」模式。
"""
import io

JS = 'pwa/js/category.js'
s = io.open(JS, encoding='utf-8').read()

OLD = """/** 排序比较器：开启「无标记优先」时无标记的排前，其余沿用「收藏时间倒序 → 年份排序（默认倒序/可选顺序）」 */
function compareEntries(a, b) {
    if (unmarkedFirst) {
        const ua = isUnmarked(a) ? 0 : 1;
        const ub = isUnmarked(b) ? 0 : 1;
        if (ua !== ub) return ua - ub;
    }
    const ta = favTime(qidOf(a.paper.id, a.q.no));
    const tb = favTime(qidOf(b.paper.id, b.q.no));
    if (ta && tb) return tb - ta;
    // 年份排序（兜底 0：无年份的补充题排到有年份真题之后，避免 NaN 失序淹没真题）
    const ya = parseInt(a.paper.year, 10) || 0;
    const yb = parseInt(b.paper.year, 10) || 0;
    if (yb !== ya) {
        return yearSortDesc ? (yb - ya) : (ya - yb);
    }
    return 0;
}"""

NEW = """/** 掌握度分组：不会 0 → 不熟 1 → 收藏 2 → 无标记 3 → 掌握 4（掌握排最下，即使同时收藏） */
function masteryRankOf(qid) {
    const st = statusOf(qid);
    if (st === 'unknown') return 0;
    if (st === 'unfamiliar') return 1;
    if (isFav(qid)) return 2;
    if (st === 'mastered') return 4;
    return 3;   // 无任何标记
}

/** 排序比较器
 *  默认：按掌握度分组（不会 → 不熟 → 收藏 → 无标记 → 掌握），组内「收藏时间倒序 → 年份（倒序/顺序由开关控制）」
 *  开启「⭕ 无标记」：无标记的排最前，其余仍按掌握度分组
 */
function compareEntries(a, b) {
    const qa = qidOf(a.paper.id, a.q.no);
    const qb = qidOf(b.paper.id, b.q.no);
    if (unmarkedFirst) {
        const ua = isUnmarked(a) ? 0 : 1;
        const ub = isUnmarked(b) ? 0 : 1;
        if (ua !== ub) return ua - ub;
        if (ua === 1) {                    // 两者都有标记 → 再按掌握度
            const ra = masteryRankOf(qa), rb = masteryRankOf(qb);
            if (ra !== rb) return ra - rb;
        }
    } else {
        const ra = masteryRankOf(qa), rb = masteryRankOf(qb);
        if (ra !== rb) return ra - rb;
    }
    const ta = favTime(qa);
    const tb = favTime(qb);
    if (ta && tb) return tb - ta;
    // 年份排序（兜底 0：无年份的补充题排到有年份真题之后，避免 NaN 失序淹没真题）
    const ya = parseInt(a.paper.year, 10) || 0;
    const yb = parseInt(b.paper.year, 10) || 0;
    if (yb !== ya) {
        return yearSortDesc ? (yb - ya) : (ya - yb);
    }
    return 0;
}"""

assert OLD in s, '未匹配到 compareEntries'
s = s.replace(OLD, NEW, 1)

# 排序说明：默认展示「掌握度排序」提示
old_meta = "${unmarkedFirst ? ` · <b>无标记优先</b>（未标记 ${unmarkedN} 题已提前）` : ''}"
new_meta = "${unmarkedFirst ? ` · <b>无标记优先</b>（未标记 ${unmarkedN} 题已提前）` : ' · <b>掌握度排序</b>（不会→不熟→收藏→无标记→掌握）'}"
assert old_meta in s, 'paper-meta 排序说明'
s = s.replace(old_meta, new_meta, 1)

io.open(JS, 'w', encoding='utf-8', newline='').write(s)
print('category.js：默认排序改为掌握度分组（不会→不熟→收藏→无标记→掌握）')
