// Генерує окремі атласні версії локалізаційних карт для розділу матеріалів.
// Оригінальні SVG залишаються незмінними: їхні цифрові маркери використовуються в тестах.
// Важливо: сучасний географічний контур — орієнтир, а НЕ кордони історичних держав.
import { readFileSync, writeFileSync, mkdirSync, readdirSync } from "node:fs";
import { join } from "node:path";
const ROOT=process.cwd();
const sourceDir=join(ROOT,"public","img","history");
const destDir=join(sourceDir,"atlas");
mkdirSync(destDir,{recursive:true});

function extractJson(path,pattern,label) {
 const source=readFileSync(join(ROOT,path),"utf8");
 const matched=source.match(pattern);
 if(!matched) throw new Error("Не знайдено метадані атласу: "+label);
 return JSON.parse(matched[1]);
}
const noteRows=extractJson("src/lib/history-map-notes.ts",/Object\.fromEntries\(\s*(\[[\s\S]*?\])\.map\(/,"map notes");
const legendRows=extractJson("src/lib/history-atlas-legends.ts",/Object\.fromEntries\(\s*(\[[\s\S]*?\])\s*\);/,"numbered legends");
const NOTES=Object.fromEntries(noteRows.map(([id,title,description,tip])=>[id,{title,description,tip}]));
const LEGENDS=Object.fromEntries(legendRows);
const esc=(s)=>String(s??"").replaceAll("&","&amp;").replaceAll("<","&lt;").replaceAll(">","&gt;").replaceAll('"',"&quot;").replaceAll("'","&apos;");
const wrap=(value,max)=>{
 const words=String(value).split(/\s+/),out=[];let cur="";
 for(const word of words){if((cur+" "+word).trim().length>max&&cur){out.push(cur);cur=word;}else cur=(cur+" "+word).trim();}
 if(cur)out.push(cur);return out;
};
const textLines=(value,x,y,width,size,spacing,max,fill="#26413b",weight="400")=>
 wrap(value,width).slice(0,max).map((s,i)=>`<text x="${x}" y="${y+i*spacing}" font-size="${size}" fill="${fill}" font-weight="${weight}">${esc(s)}</text>`).join("");
const eras=(s)=>s==="map_rus"?"IX–XIII ст.":s==="map_halych"?"XII–XIV ст.":s==="map_vkl"?"XIV–XVI ст.":/^map_h3/.test(s)?"XVI–XVIII ст.":/^map_h4/.test(s)?"XVIII – поч. XX ст.":/^map_h5/.test(s)?"1917–1921":/^map_h6/.test(s)?"1921–1945":/^map_h7/.test(s)?"1945–1991":"1991–2023";
function recolor(svg) {
 const palette={
  "#f1f5f9":"#f2f0e7","#f8fafc":"#f2f0e7","#dbeafe":"#d5e7e5",
  "#ecfccb":"#e1dbc0","#cfe8fc":"#c8dede","#3b82f6":"#497c82",
  "#60a5fa":"#3d8293","#64748b":"#837f70","#94a3b8":"#72877f",
  "#1e293b":"#254743","#dc2626":"#b75344"
 };
 for(const [a,b] of Object.entries(palette))svg=svg.replaceAll(a,b);
 // Сучасні назви сусідніх держав на старих схемах пояснюємо як географічні орієнтири.
 for(const [a,b] of Object.entries({"ПОЛЬЩА":"Суч. Польща","БІЛОРУСЬ":"Суч. Білорусь","РОСІЯ":"Суч. Росія","МОЛДОВА":"Суч. Молдова","РУМУНІЯ":"Суч. Румунія"}))
   svg=svg.replaceAll(">"+a+"<",">"+b+"<");
 return svg;
}
function render(svg,slug){
 const note=NOTES[slug];
 if(!note)throw new Error("Для карти бракує опису: "+slug);
 const labels=(LEGENDS[slug]||[]).map((label,i)=>({label,num:i+1})).filter(item=>item.label);
 const inner=recolor(svg.replace(/^<svg\b[^>]*>/,"").replace(/<\/svg>\s*$/,""));
 const legend=labels.map((item,i)=>{
   const y=207+i*68,lines=wrap(item.label,29);
   return `<circle cx="873" cy="${y-7}" r="18" fill="#284b43"/><text x="873" y="${y-1}" fill="#fff" text-anchor="middle" font-weight="bold" font-size="16">${item.num}</text>
   <text x="908" y="${y-5}" fill="#243f39" font-size="17" font-weight="bold">${esc(lines[0])}</text>
   ${lines.length>1?`<text x="908" y="${y+15}" fill="#51655a" font-size="15">${esc(lines.slice(1).join(" "))}</text>`:""}
   <line x1="852" y1="${y+22}" x2="1268" y2="${y+22}" stroke="#e2d8c5"/>`;
 }).join("");
 return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1320 860" role="img" aria-labelledby="atlas-title atlas-description">
 <title id="atlas-title">${esc(note.title)}</title>
 <desc id="atlas-description">${esc(note.description)}; ${esc(note.tip)}. Картографічна схема з сучасним географічним контуром, не історичними кордонами.</desc>
 <defs>
  <linearGradient id="atlas-paper" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#fcfaf3"/><stop offset="1" stop-color="#ece6d6"/></linearGradient>
  <pattern id="atlas-specks" width="27" height="27" patternUnits="userSpaceOnUse"><circle cx="4" cy="5" r="0.8" fill="#ad936a" opacity=".14"/><circle cx="19" cy="21" r="0.6" fill="#ad936a" opacity=".12"/></pattern>
 </defs>
 <rect width="1320" height="860" fill="url(#atlas-paper)"/><rect width="1320" height="860" fill="url(#atlas-specks)"/>
 <rect width="1320" height="115" fill="#1f423c"/><rect y="112" width="1320" height="3" fill="#c49d62"/>
 <text x="36" y="29" fill="#d9c699" letter-spacing="2.6" font-family="Arial, sans-serif" font-size="12" font-weight="bold">ІСТОРИЧНИЙ АТЛАС · ПІДГОТОВКА ДО НМТ</text>
 ${textLines(note.title,36,73,56,28,32,1,"#fff8e7","700")}
 <rect x="1091" y="35" width="195" height="44" rx="22" fill="#3a6055" stroke="#a1b3a0"/>
 <text x="1189" y="63" text-anchor="middle" fill="#fff5df" font-family="Arial, sans-serif" font-size="17" font-weight="bold">${esc(eras(slug))}</text>
 <rect x="29" y="131" width="789" height="638" rx="13" fill="#f7f4e9" stroke="#d1c2a7" stroke-width="2"/>
 <rect x="40" y="144" width="765" height="544" rx="9" fill="#e4ece7" stroke="#b9b9a5"/>
 <svg x="43" y="146" width="760" height="536" viewBox="0 0 639 445" preserveAspectRatio="xMidYMid meet">${inner}</svg>
 <rect x="45" y="703" width="757" height="54" rx="8" fill="#ede7d5"/>
 <circle cx="66" cy="727" r="10" fill="#8f7956"/>
 <text x="66" y="732" text-anchor="middle" fill="white" font-family="Arial" font-weight="bold" font-size="15">i</text>
 <text x="86" y="724" fill="#4d5142" font-family="Arial" font-size="14" font-weight="bold">Сучасний контур України — географічний орієнтир.</text>
 <text x="86" y="743" fill="#746c57" font-family="Arial" font-size="13">Політичні кордони минулих епох тут не відтворені.</text>
 <rect x="838" y="131" width="455" height="638" rx="13" fill="#fffdf7" stroke="#d1c2a7" stroke-width="2"/>
 <text x="858" y="168" fill="#98713a" font-size="13" letter-spacing="1.6" font-family="Arial" font-weight="bold">ЛЕГЕНДА · ПОЗНАЧКИ ТЕСТІВ</text>
 <line x1="858" x2="1273" y1="183" y2="183" stroke="#be9a64" stroke-width="2"/>
 ${legend}
 <text x="858" y="488" fill="#98713a" font-size="13" letter-spacing="1.6" font-family="Arial" font-weight="bold">ІСТОРИЧНИЙ КОНТЕКСТ</text>
 <line x1="858" x2="1273" y1="502" y2="502" stroke="#d8ceba"/>
 ${textLines(note.description,858,530,43,15.5,25,5)}
 <rect x="854" y="663" width="424" height="91" rx="9" fill="#f2e8d3"/>
 <text x="870" y="685" fill="#8b6130" font-size="13" font-family="Arial" font-weight="bold">ЗАПАМ’ЯТАЙ ДО НМТ</text>
 ${textLines(note.tip,870,708,48,14,19,2,"#624c35","600")}
 <line x1="31" x2="1288" y1="794" y2="794" stroke="#cbbda5"/>
 <text x="33" y="821" fill="#586c63" font-size="13" font-family="Arial">Навчальна локалізаційна картосхема · не в масштабі · цифрові позначки відповідають питанням сайту</text>
 <text x="1283" y="821" text-anchor="end" fill="#466157" font-family="Arial" font-size="14" font-weight="bold">НМТ НА 200</text>
 </svg>`;
}
let count=0;
for(const file of readdirSync(sourceDir).filter(x=>/^map_.*\.svg$/.test(x))){
 const slug=file.slice(0,-4);
 const src=readFileSync(join(sourceDir,file),"utf8");
 writeFileSync(join(destDir,file),render(src,slug),"utf8");count++;
}
if(count!==45)throw new Error("Очікувалося 45 карт; знайдено "+count);
console.log("[atlas] Згенеровано "+count+" атласних карт без зміни оригінальних карт тестів.");
