# -*- coding: utf-8 -*-
"""把大观园静态版 48 道二重积分题的原图移植到 core_bank.json 的 ansImg 字段。
- 映射来自 _final_map.json（逐题核验过：年份+题号+题干三重信号）
- 图片下载到 pwa/data/img/zx_site/{no}_{i}.webp
- 只写 ansImg 字段，answer/idea/stem 等一律不动
"""
import json, os, subprocess, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'pwa', 'data')
IMGDIR = os.path.join(DATA, 'img', 'zx_site')
MAPFILE = 'C:/Users/cjx/AppData/Local/Temp/_final_map.json'
CACHE = 'C:/Users/cjx/AppData/Local/Temp/dg_qcache'
BASE = 'https://daguan-math-static.pages.dev/'

final = json.load(open(MAPFILE, encoding='utf-8'))['map']
core_path = os.path.join(DATA, 'core_bank.json')
core = json.load(open(core_path, encoding='utf-8'))

# 建 no -> q 索引
idx = {}
for p in core:  # core_bank.json 顶层是 list
    for s in p.get('sections', []):
        for q in s.get('questions', []):
            idx[q['no']] = q

WEBP_MAGIC = b'RIFF'
downloaded = []
for item in final:
    no = item['core_no']
    imgs = item['imgs']
    paths = []
    for i, rel in enumerate(imgs):
        # rel 形如 ./images/<hash>.webp
        fname = f'{no}_{i}.webp'
        dst = os.path.join(IMGDIR, fname)
        cache_f = os.path.join(CACHE, f'img_{no}_{i}.webp')
        if os.path.exists(cache_f) and os.path.getsize(cache_f) > 500:
            raw = open(cache_f, 'rb').read()
        else:
            url = BASE + rel.lstrip('./')
            r = subprocess.run(['curl','-s','-L','--noproxy','*','-A','Mozilla/5.0',
                                url,'-o',cache_f], capture_output=True)
            if r.returncode != 0:
                raise RuntimeError(f'下载失败 no={no} {url}: {r.stderr[:100]}')
            raw = open(cache_f, 'rb').read()
        assert len(raw) > 500, f'图片过小 no={no} {fname} {len(raw)}B'
        assert raw[:4] == WEBP_MAGIC or raw[:4] == b'\x89PNG', f'非图片格式 no={no} {fname} {raw[:8]!r}'
        # 写入目标
        with open(dst, 'wb') as f:
            f.write(raw)
        paths.append(f'data/img/zx_site/{fname}')
        downloaded.append((no, fname, len(raw)))
    # 写 ansImg（只加这个字段）
    q = idx[no]
    old = q.get('ansImg')
    assert not old, f'no={no} 已有 ansImg={old}，拒绝覆盖'
    q['ansImg'] = paths

# 写回：core_bank.json indent=1，无尾换行
out = json.dumps(core, ensure_ascii=False, indent=1)
with open(core_path, 'w', encoding='utf-8', newline='') as f:
    f.write(out)

print(f'写入 {len(final)} 道题 ansImg，共 {len(downloaded)} 张图')
print(f'core_bank.json 大小 {os.path.getsize(core_path)} B')
for no, fn, sz in downloaded[:10]:
    print(f'  {fn}  {sz}B')
print('  ...')
