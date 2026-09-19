# -*- coding: utf-8 -*-
"""定量验证：用户截图公式在 KaTeX display 渲染下的垂直溢出量（em/px），核对 12px padding 是否足够"""
import json, io, re, subprocess, os

# 用户截图里的公式（偏导数定义，含 \left| \right|_{(0,0)} 大定界符与 \lim 下标）
FORMULA = (r'\left.\dfrac{\partial f}{\partial x}\right|_{(0,0)}'
           r'=\lim_{\Delta x\to0}\frac{f(\Delta x,0)-f(0,0)}{\Delta x}'
           r'=\lim_{\Delta x\to0}\frac{\Delta x-0}{\Delta x}=\lim_{\Delta x\to0}1=1')

tmp = 'C:/Users/cjx/.workbuddy/binaries/node/workspace/_f.txt'
jsf = 'C:/Users/cjx/.workbuddy/binaries/node/workspace/_f.js'
io.open(tmp, 'w', encoding='utf-8').write(FORMULA)
js = (
    "const fs=require('fs');\n"
    "const formula=fs.readFileSync(process.argv[2],'utf8');\n"
    "const vm=require('vm');\n"
    "const ctx={}; vm.createContext(ctx);\n"
    "vm.runInContext(fs.readFileSync('D:/ai code/math-note/pwa/vendor/katex/katex.min.js','utf8'),ctx);\n"
    "const html=ctx.katex.renderToString(formula,{displayMode:true,throwOnError:true});\n"
    "// 1) .katex 根元素的 height/depth（KaTeX 用 em 标注）\n"
    "const root=html.match(/<span class=\"katex\"><span class=\"katex-mathml\">/);\n"
    "const vlists=[...html.matchAll(/height:([0-9.]+)em/g)].map(m=>parseFloat(m[1]));\n"
    "const deps=[...html.matchAll(/vertical-align:-([0-9.]+)em/g)].map(m=>parseFloat(m[1]));\n"
    "const negTop=[...html.matchAll(/margin-top:-([0-9.]+)em/g)].map(m=>parseFloat(m[1]));\n"
    "console.log('vlist 高度(em) 最大:', Math.max(...vlists,0).toFixed(3));\n"
    "console.log('baseline 下方(em) 最大:', Math.max(...deps,0).toFixed(3));\n"
    "console.log('负 margin-top(=上溢)(em) 最大:', Math.max(...negTop,0).toFixed(3), '共', negTop.length, '处');\n"
    "const maxNeg=Math.max(...negTop,0);\n"
    "// .katex-display>.katex 字号 1.6em，基准 16px\n"
    "const px=1.6*16*maxNeg;\n"
    "console.log('换算上溢像素(1.6em字号基准16px):', px.toFixed(1),'px');\n"
    "console.log('结论: 顶部 padding 12px', px<=12?'足够 ✅':'不足 ❌');\n"
)
io.open(jsf, 'w', encoding='utf-8').write(js)
r = subprocess.run(['C:/Users/cjx/.workbuddy/binaries/node/versions/22.22.2-3/node.exe', jsf, tmp],
                   capture_output=True, text=True)
print(r.stdout or r.stderr[:400])
os.remove(tmp)
os.remove(jsf)
