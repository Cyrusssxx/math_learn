/* test_fsrs.js — node 自测 FSRS 调度器
 * 用法：node test_fsrs.js
 */
const { fsrsInit, fsrsRepeat, RATING, STATE } = require('../pwa/js/fsrs.js');

function daysBetween(a, b) { return Math.round((new Date(b) - a) / 86400000); }
let fails = 0;
function assert(cond, msg) {
    if (!cond) { fails++; console.log('FAIL:', msg); }
    else console.log('ok  :', msg);
}

// 1) 新卡 Good 链：两步学习步骤毕业，之后间隔单调递增
let c = fsrsInit('t1');
let now = new Date('2026-07-27T10:00:00Z');
c = fsrsRepeat(c, RATING.GOOD, now);           // 学习 step0→1
assert(c.state === STATE.LEARNING && c.againToday, '新卡Good进入学习步骤（当天再见）');
c = fsrsRepeat(c, RATING.GOOD, now);           // 毕业
assert(c.state === STATE.REVIEW && !c.againToday, 'Good走完步骤毕业为复习卡');
const ivls = [daysBetween(now, c.due)];
for (let i = 0; i < 4; i++) {
    now = new Date(new Date(c.due) .getTime() + 10 * 3600000);  // 到期日复习
    c = fsrsRepeat(c, RATING.GOOD, now);
    ivls.push(daysBetween(now, c.due));
}
console.log('Good链间隔(天):', ivls.join(' → '));
assert(ivls.every((v, i) => i === 0 || v > ivls[i - 1]), 'Good链间隔单调递增');

// 2) Again 使 lapses+1 且间隔回落、进入重学
const before = c.stability;
now = new Date(new Date(c.due).getTime() + 10 * 3600000);
const lapsed = fsrsRepeat(c, RATING.AGAIN, now);
assert(lapsed.lapses === c.lapses + 1, 'Again后lapses+1');
assert(lapsed.state === STATE.RELEARNING && lapsed.againToday, 'Again进入重学（当天再见）');
assert(lapsed.stability < before, 'Again后稳定性回落');

// 3) 新卡 Easy 直接毕业且间隔 > Good毕业间隔
let e = fsrsInit('t2');
now = new Date('2026-07-27T10:00:00Z');
e = fsrsRepeat(e, RATING.EASY, now);
assert(e.state === STATE.REVIEW, '新卡Easy直接毕业');
console.log('Easy首间隔:', daysBetween(now, e.due), '天; Good毕业首间隔:', ivls[0], '天');
assert(daysBetween(now, e.due) > ivls[0], 'Easy首间隔大于Good');

// 4) 难度边界：连按 Again 难度不越界
let h = fsrsInit('t3');
h = fsrsRepeat(h, RATING.AGAIN, now);
h = fsrsRepeat(h, RATING.GOOD, now);
h = fsrsRepeat(h, RATING.GOOD, now);  // 毕业
for (let i = 0; i < 10; i++) {
    now = new Date(new Date(h.due).getTime() + 10 * 3600000);
    h = fsrsRepeat(h, i % 2 ? RATING.GOOD : RATING.AGAIN, now);
}
assert(h.difficulty >= 1 && h.difficulty <= 10, `难度在[1,10]内: ${h.difficulty.toFixed(2)}`);

console.log(fails ? `\n${fails} 项失败` : '\n全部通过');
process.exit(fails ? 1 : 0);
