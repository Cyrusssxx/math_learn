# -*- coding: utf-8 -*-
"""mastery.js：掌握率口径接入显式「掌握(mastered)」标记"""
import io

p = 'pwa/js/mastery.js'
s = io.open(p, encoding='utf-8').read()

# 1) 四态计数：优先识别显式 mastered；保留旧「收藏且无薄弱标记」为已掌握（存量收藏数据不流失）
old = """        const qid = qidOf(e.paper.id, e.q.no);
        const s = st[qid] || null;
        const f = !!fav[qid];
        o.total++;
        // 三态互斥 + 未刷：不会 / 不熟 / 已过关(收藏且无薄弱标记) / 未刷(无任何痕迹 → 计 0 掌握)
        if (s === 'unknown') o.unk++;
        else if (s === 'unfamiliar') o.unf++;
        else if (f) o.mst++;          // 刷过且未留薄弱标记 → 已过关
        else o.none++;                // 未刷 → 0 掌握"""
new = """        const qid = qidOf(e.paper.id, e.q.no);
        const s = st[qid] || null;
        const f = !!fav[qid];
        o.total++;
        // 四态互斥：不会 / 不熟 / 已掌握(显式标记，或已收藏且无薄弱标记) / 未刷(计 0 掌握)
        if (s === 'unknown') o.unk++;
        else if (s === 'unfamiliar') o.unf++;
        else if (s === 'mastered') o.mst++;   // 显式「掌握」标记（题卡绿按钮）
        else if (f) o.mst++;                   // 存量口径：刷过(收藏)且未留薄弱标记 → 已掌握
        else o.none++;                         // 未刷 → 0 掌握"""
assert old in s, 'count logic'
s = s.replace(old, new)

# 2) 顶部口径说明
old = """   口径：每个知识点一色块，四态互斥计数
         🔴不会 / 🟡不熟 / ✅已掌握(mastered) / ⚪未刷(无任何标记)
         **掌握率 = 已掌握题数 / 总题数**（未刷、未标记的题一律计 0，不算已掌握）"""
new = """   口径：每个知识点一色块，四态互斥计数
         🔴不会 / 🟡不熟 / ✅已掌握(显式 mastered 标记，或已收藏且无薄弱标记) / ⚪未刷
         **掌握率 = 已掌握题数 / 总题数**（未刷、未标记的题一律计 0，不算已掌握）
         题卡三态标记「掌握🟢 / 不熟🟡 / 不会🔴」互斥（右缘竖条栏），点「掌握」即计入掌握率"""
assert old in s, 'header doc'
s = s.replace(old, new)

# 3) 底部图例与提示文案
old = """                    <span class="mm-legend"><i class="mm-dot mm-ok"></i>✅已过关</span>"""
new = """                    <span class="mm-legend"><i class="mm-dot mm-ok"></i>✅已掌握</span>"""
assert old in s, 'legend'
s = s.replace(old, new)

old = """const MM_TIP = '掌握率 = 已过关题数 / 总题数（未刷、未标记一律计 0）；已过关 = 已收藏且未标「不熟/不会」。薄弱率 =（🔴不会 + 🟡不熟）/ 总数，章节与知识点按薄弱率降序，默认只显示未 100% 掌握的知识点。';"""
new = """const MM_TIP = '掌握率 = 已掌握题数 / 总题数（未刷、未标记一律计 0）；已掌握 = 题卡点过「掌握🟢」，或已收藏且未标「不熟/不会」（存量口径）。薄弱率 =（🔴不会 + 🟡不熟）/ 总数，章节与知识点按薄弱率降序，默认只显示未 100% 掌握的知识点。';"""
assert old in s, 'MM_TIP'
s = s.replace(old, new)

# 4) 总览行文案统一
old = """            总体掌握率 <b>${mmPct(t.rate)}</b>（✅已掌握 <b>${t.mst}</b> / ${t.total} 题）"""
new = """            总体掌握率 <b>${mmPct(t.rate)}</b>（✅已掌握 <b>${t.mst}</b> / ${t.total} 题 · 绿色标记或已收藏无薄弱）"""
assert old in s, 'overview'
s = s.replace(old, new)

io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('mastery.js 5 处修改完成')
