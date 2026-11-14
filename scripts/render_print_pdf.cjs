/* A4 pagination and KaTeX vector typesetting for build_print_pdf.py. */
const fs = require('fs');
const path = require('path');
const {pathToFileURL} = require('url');
const {execFileSync} = require('child_process');
const [work, modules, katexDir] = process.argv.slice(2);
const katex = require(path.join(katexDir, 'katex.js'));
const {chromium} = require(path.join(modules, 'playwright'));
const source = JSON.parse(fs.readFileSync(path.join(work, 'input.json'), 'utf8'));
const css = fs.readFileSync(path.join(__dirname, 'print_pdf.css'), 'utf8');
const math = {};
for (const e of source.equations) {
  try { math[e.id] = katex.renderToString(e.tex, {displayMode:e.display, throwOnError:true, strict:'ignore'}); }
  catch (err) { throw new Error(e.source + ': ' + err.message); }
}
function html(body) {
  return '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><link rel="stylesheet" href="' + pathToFileURL(path.join(katexDir, 'katex.min.css')) + '"><style>' + css + '</style><article>' + body + '</article></html>';
}
function escape(text) { return text.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
async function print(page, file) {
  await page.evaluate(() => document.fonts.ready);
  return page.pdf({path:file, format:'A4', preferCSSPageSize:true, printBackground:true, tagged:true});
}
// Only divide at outer spacing commands, preserving matrices and bracketed groups.
function wrap(tex) {
  let braces=0, env=0, left=0, start=0;const chunks=[];
  for(let i=0;i<tex.length;i++) {
    if(tex.startsWith('\\begin{',i))env++;
    if(tex.startsWith('\\end{',i))env--;
    if(/^\\left(?![A-Za-z])/.test(tex.slice(i)))left++;
    if(/^\\right(?![A-Za-z])/.test(tex.slice(i)))left--;
    if(braces===0&&env===0&&left===0) {
      const token=['\\qquad','\\quad'].find(t=>tex.startsWith(t,i));
      if(token){chunks.push(tex.slice(start,i).trim());i+=token.length-1;start=i+1;continue;}
    }
    if(tex[i]==='{'&&tex[i-1]!=='\\')braces++;
    if(tex[i]==='}'&&tex[i-1]!=='\\')braces--;
  }
  chunks.push(tex.slice(start).trim());
  return chunks.length>1?'\\begin{gathered}'+chunks.filter(Boolean).join('\\\\[2pt]')+'\\end{gathered}':tex;
}
async function main() {
  const browser=await chromium.launch({executablePath:process.env.CHROME_BIN||'/usr/bin/google-chrome',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
  const page=await browser.newPage({viewport:{width:1000,height:1100}});
  await page.emulateMedia({media:'print'});
  const count=async file=>Number(execFileSync('pdfinfo',[file],{encoding:'utf8'}).match(/^Pages:\s+(\d+)/m)[1]);
  const units=[];const adjustments=[];
  for(const doc of source.documents) {
    let body=doc.body.replace(/MATHEQ\d+TOKEN/g, id=>'<span data-equation="'+id+'">'+math[id]+'</span>');
    const file=path.join(work, doc.id+'.html');
    fs.writeFileSync(file,html(body));
    await page.goto(pathToFileURL(file).href);await page.evaluate(()=>document.fonts.ready);
    const wide=await page.evaluate(()=>[...document.querySelectorAll('.display-equation .katex-html')].filter(el=>el.getBoundingClientRect().width>el.closest('.display-equation').clientWidth+1).map(el=>el.closest('[data-equation]').dataset.equation));
    for(const id of wide){
      const eq=source.equations.find(e=>e.id===id);const wrapped=wrap(eq.tex);
      if(wrapped!==eq.tex){
        const rendered=katex.renderToString(wrapped,{displayMode:true,throwOnError:true,strict:'ignore'});
        await page.locator('[data-equation="'+id+'"]').evaluate((el,content)=>{el.innerHTML=content;},rendered);
        adjustments.push({id,source:eq.source,kind:'line-wrap'});
      }
    }
    const scaled=await page.evaluate(()=>{
      const reports=[];
      for(const box of document.querySelectorAll('.display-equation')) {
        const el=box.querySelector('.katex');const content=box.querySelector('[data-equation]');
        let width=el.getBoundingClientRect().width;
        if(width>box.clientWidth+1){
          const font=parseFloat(getComputedStyle(el).fontSize);const newSize=font*box.clientWidth/width*.98;
          el.style.fontSize=newSize+'px';reports.push({id:content.dataset.equation,kind:'fit',points:newSize*.75});
        }
      }
      const outside=[...document.querySelectorAll('.katex-html')].filter(el=>{const r=el.getBoundingClientRect();return r.left < -1||r.right>document.querySelector('article').clientWidth+1;}).map(el=>el.parentElement.querySelector('annotation')?.textContent);
      return {reports,outside};
    });
    adjustments.push(...scaled.reports);
    if(scaled.reports.some(r=>r.points<8)||scaled.outside.length)throw new Error(doc.title+': formula overflow '+JSON.stringify(scaled));
    // Save the exact print DOM after fitting, for reproducible visual inspection.
    fs.writeFileSync(file,await page.content());
    const pdf=path.join(work,doc.id+'.pdf');await print(page,pdf);
    const pages=await count(pdf);units.push({...doc,pdf,pages});
    console.log(doc.title+': '+pages+' pages');
  }
  const manifest={};
  for(const volume of ['notes','practice','book']){
    const selected=units.filter(d=>volume==='book'||d.volume===volume);
    const label={notes:'正文',practice:'练习与答案',book:'合订本'}[volume];
    const description=volume==='practice'?'符号与做题方法 · 40 道综合练习 · 完整推导与检验':volume==='notes'?'18 个正文大章 · 核心定义与推导 · 例题与矢量图解':'18 个正文大章 · 40 道综合练习 · 核心公式与完整推导';
    const frontFile=path.join(work,'front-'+volume+'.html');const frontPdf=path.join(work,'front-'+volume+'.pdf');
    let frontPages=2;
    for(let attempt=0;attempt<3;attempt++){
      let offset=frontPages+1;
      const lines=selected.map(d=>{const line='<div class="toc-line"><span>'+escape(d.title)+'</span><span class="dots"></span><span class="page">'+offset+'</span></div>';offset+=d.pages;return line;}).join('');
      const front='<section class="front cover"><div class="eyebrow">LINEAR ALGEBRA</div><h1>线性代数</h1><h2>中文精简版 · '+label+'</h2><div class="description">'+description+'</div><div class="print-note">A4 打印版 · 白底排版 · 公式与图解采用矢量输出<br>打印建议：实际大小（100%），双面长边翻页。<br>2026 年 11 月修订</div></section><section class="front toc"><h1>目录</h1><p class="toc-label">按知识点依次阅读；页码为本册 PDF 的连续页码。</p>'+lines+'</section>';
      fs.writeFileSync(frontFile,html(front));await page.goto(pathToFileURL(frontFile).href);await print(page,frontPdf);
      const actual=await count(frontPdf);if(actual===frontPages)break;frontPages=actual;
    }
    manifest[volume]=[{pdf:frontPdf,title:'封面与目录'},...selected.map(d=>({pdf:d.pdf,title:d.title,pages:d.pages,source:d.source}))];
  }
  fs.writeFileSync(path.join(work,'manifest.json'),JSON.stringify(manifest,null,2));
  fs.writeFileSync(path.join(work,'formula-adjustments.json'),JSON.stringify(adjustments,null,2));
  console.log('Rendered '+source.equations.length+' formulas; '+adjustments.length+' print layout adjustments');
  await browser.close();
}
main().catch(err=>{console.error(err);process.exitCode=1;});
