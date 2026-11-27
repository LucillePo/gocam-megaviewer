"""The HTML/JS template for the interactive connectivity app.
Placeholders: __LIBS__ (inlined JS libs), __CACHE__ (model records JSON),
__DEFAULT_IDS__ (newline-joined default model IDs)."""

APP_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>GO-CAM connectivity — interactive (Viewer 2)</title>
__LIBS__
<style>
  html,body{margin:0;height:100%;font-family:-apple-system,Segoe UI,Roboto,sans-serif;color:#1a1a2e}
  #app{display:flex;height:100vh}
  #left{width:300px;min-width:0;border-right:1px solid #dde;display:flex;flex-direction:column;box-sizing:border-box;flex:0 0 auto}
  .resizer{flex:0 0 6px;cursor:col-resize;background:#e3e7ef}
  .resizer:hover{background:#b9c4da}
  #left .pad{padding:12px 14px;overflow:auto}
  #main{flex:1;display:flex;flex-direction:column;min-width:0}
  #cy{flex:1;min-height:400px;background:#f7f8fb}
  .boxgrip{position:fixed;width:16px;height:16px;cursor:nwse-resize;z-index:50;border-right:4px solid #556;border-bottom:4px solid #556;border-radius:0 0 4px 0;opacity:.65;box-sizing:border-box}
  .boxgrip:hover{opacity:1;border-color:#2a6ef0}
  #err{display:none;background:#fdecea;color:#611a15;border-bottom:1px solid #f5c6c2;
    padding:8px 12px;font-size:12px;font-family:ui-monospace,Menlo,monospace;white-space:pre-wrap}
  #modal{position:fixed;inset:0;background:rgba(20,25,40,.45);display:none;align-items:center;justify-content:center;z-index:1000}
  #modal .box{background:#fff;border-radius:8px;padding:16px 18px;max-width:680px;max-height:84vh;overflow:auto;box-shadow:0 10px 34px rgba(0,0,0,.35)}
  #modal textarea{width:100%;box-sizing:border-box;font-family:ui-monospace,Menlo,monospace;font-size:11px;border:1px solid #ccd;border-radius:5px;padding:6px}
  #modal img{max-width:100%;height:auto;border:1px solid #ddd;border-radius:4px}
  #modalmsg{font-size:12px;color:#2a7d2a;min-height:14px}
  #colpop{position:fixed;z-index:50;display:none;background:#fff;border:1px solid #9ab;border-radius:8px;padding:8px 10px;box-shadow:0 6px 22px rgba(0,0,0,.25);font-size:12px;max-width:300px}
  #colpop .ttl{font-weight:bold;margin-right:18px} #colpop .x{position:absolute;top:4px;right:8px;cursor:pointer;color:#666;font-size:15px}
  #colpop .sw{display:inline-block;width:20px;height:20px;border:1px solid #999;border-radius:4px;margin:3px 4px 0 0;cursor:pointer;vertical-align:middle}
  #side{width:320px;min-width:0;flex:0 0 auto;border-left:1px solid #dde;overflow:auto;padding:12px 14px;box-sizing:border-box}
  h1{font-size:14px;margin:0 0 6px}
  h2{font-size:12px;margin:12px 0 4px;color:#445}
  .sub{color:#667;font-size:12px}
  textarea{width:100%;height:150px;box-sizing:border-box;font-family:ui-monospace,Menlo,monospace;
    font-size:12px;border:1px solid #ccd;border-radius:6px;padding:7px;resize:vertical}
  button{font-size:12px;padding:5px 10px;border:1px solid #bcd;background:#eef4ff;border-radius:6px;cursor:pointer}
  button:hover{background:#dfeaff}
  button.primary{background:#2a6ef0;color:#fff;border-color:#2a6ef0}
  button.primary:hover{background:#1f5fd8}
  .bar{padding:8px 12px;border-bottom:1px solid #dde;display:flex;gap:8px;align-items:center;flex-wrap:wrap;background:#fff}
  input[type=search]{padding:5px 8px;border:1px solid #ccd;border-radius:6px;font-size:13px;width:180px}
  .stat{display:inline-block;background:#eef;border-radius:5px;padding:2px 7px;margin:2px 3px 2px 0;font-size:11px}
  .legend div{font-size:11px;margin:3px 0;display:flex;align-items:center;gap:6px}
  .swatch{width:22px;border-top:3px solid;display:inline-block}
  .dot{width:12px;height:12px;border-radius:50%;display:inline-block;border:2px solid #333}
  .row{font-size:12px;margin:3px 0;line-height:1.4}
  .k{color:#889;display:inline-block;min-width:34px}
  .tag{display:inline-block;background:#eef;border-radius:4px;padding:1px 6px;font-size:11px;margin:2px 3px 0 0}
  .tag.model{background:#e7f0ff;cursor:pointer}
  .mono{font-family:ui-monospace,Menlo,monospace;font-size:11px;color:#557}
  .warn{color:#b5480f;font-size:12px;margin-top:6px}
  label.chk{font-size:12px;display:flex;align-items:center;gap:4px}
  a{color:#2a6ef0}
</style>
</head>
<body>
<div id="app">
  <div id="left"><div class="pad">
    <h1>GO-CAM connectivity — Viewer 2 <span class="sub" style="font-weight:normal" title="when this app.html was built (models baked live at that time)">build __BUILD__</span></h1>
    <div class="sub">Enter any GO-CAM model IDs (one per line), then Build — models are fetched live from GO. Drag boxes to arrange. Move several at once: Shift/Ctrl/Cmd-click them (or Shift-drag a rectangle on the background), then drag one; Esc or a click on the background clears the selection.</div>
    <h2>Model IDs</h2>
    <textarea id="ids" placeholder="Enter GO-CAM model IDs, one per line — e.g. gomodel:6918f23700000035 — then click Build graph">__DEFAULT_IDS__</textarea>
    <div style="margin-top:8px;display:flex;gap:8px;align-items:center;flex-wrap:wrap">
      <button class="primary" id="build">Build graph</button>
      <button id="sharelink" title="Copy a link that opens this exact set of models">Copy share link</button>
      <label class="chk"><input type="radio" name="mode" value="loose" checked> loose</label>
      <label class="chk"><input type="radio" name="mode" value="strict"> strict</label>
    </div>
    <div class="row" style="margin-top:6px" title="Uncheck an aspect to ignore it when merging — units differing only in that aspect will then merge">Merge requires same:
      <label class="chk"><input type="checkbox" id="mON" checked> MF</label>
      <label class="chk" title="the BP and its whole part_of chain"><input type="checkbox" id="bON" checked> BP (+ part_of chain)</label>
      <label class="chk"><input type="checkbox" id="cON" checked> CC (+ part_of chain)</label>
    </div>
    <div class="row" style="margin-top:6px" title="Production + dev (default): every model is read from live production first; a model not yet in production is read from the Noctua dev server and marked 'dev server'. Production only: dev-only models are left out.">Models from:
      <label class="chk"><input type="radio" name="srcmode" value="prod"> production only</label>
      <label class="chk"><input type="radio" name="srcmode" value="dev" checked> production + dev</label>
    </div>
    <div class="row" style="margin-top:6px" title="By cell type: one box per cell type (the first CL term in the CC part_of chain); extracellular units sit between the cells; units with no cell type are flagged and left loose: drag one into a cell box to place it (view only, the model is not changed)">Layout:
      <label class="chk"><input type="radio" name="cellmode" value="flow" checked> by model flow</label>
      <label class="chk"><input type="radio" name="cellmode" value="cell"> by cell type</label>
    </div>
    <div id="loadwarn"></div>
    <h2>Loaded models <span class="sub" id="ncache"></span></h2>
    <div id="cachelist" class="sub"></div>
    <div class="warn" id="notloaded"></div>
    <h2>Quality control <span class="sub" id="nqc"></span></h2>
    <div id="qc" class="sub">Build a graph to run QC checks.</div>
  </div></div>

  <div class="resizer" id="rzL"></div>

  <div id="main">
    <div id="err"></div>
    <div class="bar">
      <input id="q" type="search" placeholder="search protein / function / model…"/>
      <label class="chk"><input type="checkbox" id="onlyBridges"> bridges only</label>
      <button id="undo" title="undo the last change">↶ undo</button>
      <button id="fit">fit</button>
      <button id="zoomin" title="zoom in">+</button>
      <button id="zoomout" title="zoom out">&minus;</button>
      <button id="relayout">auto-layout</button>
      <button id="savelayout">save layout</button>
      <button id="loadlayout" title="paste a saved layout to rebuild its exact graph">load layout</button>
      <button id="png">PNG</button>
      <span id="stats"></span>
    </div>
    <div id="cy"></div>
  </div>

  <div class="resizer" id="rzR"></div>

  <div id="side">
    <div class="legend">
      <div><span class="swatch" style="border-top-color:#2e8b57"></span> positively regulates</div>
      <div><span class="swatch" style="border-top-color:#c0392b"></span> negatively regulates</div>
      <div><span class="swatch" style="border-top-color:#888"></span> provides input for</div>
      <div><span class="swatch" style="border-top-color:#7a97a8;border-top-style:dashed"></span> input / output (molecule)</div>
      <div id="celllegend" style="display:none">
        <div style="margin-top:6px"><span class="dot" style="border-radius:3px;background:#e8f1fb;border-color:#6d8fb8"></span> cell type box (CL)</div>
        <div class="sub">extracellular units: no box, placed between the cells</div>
        <div><span class="dot" style="background:#dcecff;border-color:#e67e22;border-style:dashed"></span> no cell type (CL) in model <span style="color:#777">(drag into a box)</span></div>
      </div>
    </div>
    <div id="detail" style="display:none;margin-top:12px;border-top:1px solid #dde;padding-top:8px"></div>
    <div id="cats" style="display:none;margin-top:14px;border-top:1px solid #dde;padding-top:6px">
      <h2>Colours</h2>
      <div class="row">default scheme:
        <select id="colorBy">
          <option value="grey" selected>light grey (molecules green)</option>
          <option value="bridge">bridge / single</option>
          <option value="model">by model</option>
        </select>
        <button id="clearcol">reset all</button>
      </div>
      <!-- legend of the chosen scheme only (user 2026-11-27) -->
      <div class="schemeleg" data-s="grey" style="margin:4px 0 0 4px">
        <div><span class="dot" style="background:#f2f2f2;border-color:#8c8c8c"></span> activity unit</div>
        <div><span class="dot" style="background:#eaf6e6;border-color:#8ab17d"></span> molecule node</div></div>
      <div class="schemeleg" data-s="bridge" style="margin:4px 0 0 4px">
        <div><span class="dot" style="background:#ffd166;border-color:#a67400"></span> bridge node <span style="color:#777">(shared by &gt;1 model)</span></div>
        <div><span class="dot" style="background:#dcecff;border-color:#2a63a8"></span> single node <span style="color:#777">(1 model)</span></div>
        <div><span class="dot" style="background:#eaf6e6;border-color:#8ab17d"></span> molecule node</div></div>
      <div class="schemeleg" data-s="model" style="margin:4px 0 0 4px">
        <div class="row sub">Colour of each model (change it here; "reset" goes back to the scheme colour):</div>
        <div id="modeltags"></div></div>
      <div class="row" style="margin-top:6px">My colours: <span id="palette"></span>
        <input type="color" id="palAdd" value="#3f8fd0" style="width:26px;height:20px;vertical-align:middle;padding:0;border:1px solid #ccd">
        <button id="palAddBtn">add</button></div>
      <div class="row sub">Click a swatch to apply it to the selected unit; click its × to remove just that colour.</div>
      <div class="row sub" style="margin-top:6px">…or click any unit or molecule: its colour row is under its details above (pick a colour, ★ keeps it in My colours, "back to default" removes it).</div>
    </div>
    <div id="colpop"></div>
  </div>
</div>

<div id="modal"><div class="box">
  <div id="modalbody"></div>
  <div style="text-align:right;margin-top:10px"><button id="modalclose">close</button></div>
</div></div>

<script>
function showErr(msg){
  const e=document.getElementById("err");
  if(e){ e.style.display="block"; e.textContent="⚠ "+msg; }
}
// benign when the page is embedded in a cross-origin frame (e.g. a JupyterLab-hosted tab):
// a library probes window.top/parent; it doesn't affect the app. Don't alarm the user.
function benignXorigin(m){ return /cross-origin|Permission denied to access property|SecurityError|accessing a cross-origin frame/i.test(String(m||"")); }
window.addEventListener("error",ev=>{ if(benignXorigin(ev.message)) return; showErr((ev.message||"error")+ (ev.filename?("  @"+ev.lineno+":"+ev.colno):"")); });
window.addEventListener("unhandledrejection",ev=>{ const m=(ev.reason&&ev.reason.message)||ev.reason; if(benignXorigin(m)) return; showErr("promise: "+m); });
if(typeof cytoscape==="undefined"){ showErr("Cytoscape library did not load — the graph engine is unavailable in this browser context."); }
</script>
<script>
const CACHE = __CACHE__;
// model colours, ordered so the FIRST n are as different as possible (n models loaded -> first n colours):
// yellow (user wants the first model in the list yellow), blue, red, green, purple, orange, grey, brown, cyan, pink.
const palette = ["#ffe98a","#a9d6ff","#ffbdbd","#b4efbe","#d3c4ff","#ffd6a6","#dcdfe3","#e3cdb1","#a6ecf2","#ffc2d9"];   // light tints so dark labels stay readable
const MCOL = {};   // assigned per build over the LOADED models only (see doBuild), not over every baked model
const ECOL = {pos:"#2e8b57", neg:"#c0392b", input:"#888888", mol:"#7a97a8"};
let cy = null;
let colorBy = "grey";  // default scheme (user 2026-11-27): every unit light grey, molecules light green; alt: "bridge" = bridge/single, "model" = one colour per model
const GREY={fill:"#f2f2f2", stroke:"#8c8c8c"};   // fill lightened #e6e6e6 -> #f2f2f2 (user 2026-11-27)

// --- persisted free colour overrides, keyed by unit signature ---
function lsGet(k,d){ try{ return JSON.parse(localStorage.getItem(k))??d; }catch(e){ return d; } }
function lsSet(k,v){ try{ localStorage.setItem(k,JSON.stringify(v)); }catch(e){} }
const DEFAULT_STATE = __DEFAULT_STATE__;     // baked-in layout/colours/scheme (from layout.json)
let OVERRIDE = Object.assign({}, DEFAULT_STATE.colors || {});   // start clean each session (no localStorage auto-load)
let PALETTE  = (DEFAULT_STATE.palette || []).slice();           // "My colours" — blank unless added this session
let MERGE_ON = {mf:true, bp:true, cc:true};   // which GO aspects count toward merging (user-toggleable filter)
const canonId = id => String(id||"");   // identity: isoform accessions (Q14028-1) are NOT folded into canonical — they never merge, QC flags them (user rule 2026-09-22)
// --- cell-type layout (Viewer 2, user design 2026-10-26) ---
let CELL_ON = false;          // "Layout: by cell type": one compound box per CL; units in different cells never merge
let BOXSIZE = {};            // cell box id -> {w,h} minimum inner size set by dragging its corner grip (save layout keeps it)
let CELL_PLACE = {};          // no-CL unit sig -> cell box id the curator dropped it in (VIEW ONLY, never written to a model)
const EXTRA_ID = "EXTRA";     // pseudo cell key for extracellular units (CC under GO:0005576), drawn between the cells
const EXTRA_GO = new Set(["GO:0005576","GO:0005615","GO:0031012","GO:0043083"]);   // fallback if QuickGO is unreachable
const CELL_TINT = [["#e8f1fb","#6d8fb8"],["#fdeee4","#c08a5f"],["#eaf6ec","#6fa07a"],["#f3ecfb","#8f78b5"],["#fbf7e1","#b5a34f"],["#e6f6f6","#5f9e9e"]];
// (2026-10-26, REPLACED 2026-11-26 by the extracellular no-merge rule, see slotId) a synaptic-cleft molecule used to be ONE
// shared node per chemical across activities and models. isPoolLoc now only marks cleft molecules to be drawn between the cells.
// Deliberately NOT for "extracellular region": the phototransduction ions there (CNG channel Ca/Na in, SLC24 Ca out)
// must stay separate per activity (user design 2026-09).
let XMOL_RULE = "link";   // "link" (default) = rule of 2026-11-26; "strict" = also one input node per model on a merged unit; "pool" = old 2026-10-26 behaviour
function isPoolLoc(id){ return id==="GO:0043083" || !!(_ancCache[id] && _ancCache[id].has("GO:0043083")); }
function isExtracellular(id){ return EXTRA_GO.has(id) || !!(_ancCache[id] && _ancCache[id].has("GO:0005576")); }
let PRESENT_CL = {};   // CL id -> label, for the cell types of the loaded units (set in doBuild)
function foldCL(id){   // a subclass is folded into the most general ancestor cell type that also has units loaded (user 2026-10-26)
  const anc=_clAnc[id]; if(!anc) return id;
  const cands=Object.keys(PRESENT_CL).filter(o=>o!==id && anc.has(o));
  if(!cands.length) return id;
  cands.sort((x,y)=>(_clAnc[x]||new Set()).size-(_clAnc[y]||new Set()).size);   // fewest ancestors = most general
  return cands[0];
}
// the cell type of a unit = the first CL in the CC part_of chain, together with any CL directly after it: a cell
// part_of another cell (e.g. ON-bipolar cell part_of cone retinal bipolar cell = "ON cone bipolar", no such CL class) is
// ONE combined cell type "CL:a+CL:b" with its own box; it is not folded into either part (user 2026-11-26)
function cellTypeOf(a){
  const ch=a.cc_chain||[]; const i=ch.findIndex(c=>/^CL:/.test(c.id||"")); if(i<0) return null;
  const run=[]; for(let k=i;k<ch.length && /^CL:/.test(ch[k].id||"");k++) if(!run.some(r=>r.id===ch[k].id)) run.push(ch[k]);
  if(run.length===1) return {id:run[0].id, label:run[0].label||run[0].id};
  run.sort((x,y)=>x.id.localeCompare(y.id));
  return {id:run.map(r=>r.id).join("+"), label:run.map(r=>r.label||r.id).join(" + "), combo:true};
}
function cellOf(a){   // first CL in the CC part_of chain (folded into a present parent cell type); else extracellular if the CC (or its chain) is under GO:0005576; else null
  const ch=a.cc_chain||[];
  const cl=cellTypeOf(a);
  if(cl){ const f=CELL_ON?foldCL(cl.id):cl.id; return {id:f, label:(f===cl.id?(cl.label||cl.id):(PRESENT_CL[f]||f)), spec:cl.id, specLabel:cl.label||cl.id}; }
  if([a.cc_id].concat(ch.map(c=>c.id)).some(id=>/^GO:/.test(id||"") && isExtracellular(id))) return {id:EXTRA_ID, label:"extracellular"};
  return null;
}
const _clAnc={};   // CL id -> Set(CL ancestor ids) from OLS, memoised; used to nest a subclass box in its parent box
async function clAncestorsOf(ids){
  const need=ids.filter(id=>/^CL:/.test(id||"") && !(id in _clAnc));
  await Promise.all(need.map(async id=>{
    _clAnc[id]=new Set();
    try{
      const iri=encodeURIComponent(encodeURIComponent("http://purl.obolibrary.org/obo/"+id.replace(":","_")));
      const r=await fetch("https://www.ebi.ac.uk/ols4/api/ontologies/cl/terms/"+iri+"/hierarchicalAncestors?size=500",{headers:{Accept:"application/json"}});
      if(r.ok){ const d=await r.json(); ((d._embedded||{}).terms||[]).forEach(t=>{ if(t.obo_id) _clAnc[id].add(t.obo_id); }); }
    }catch(e){}
  }));
}
function currentCellMode(){ const r=document.querySelector('input[name=cellmode]:checked'); return r ? r.value : "flow"; }
let PENDING_LAYOUT = null;   // saved positions to apply on the next build (from a restored layout), instead of auto-layout
let selectedSig = null;                       // sig of the currently clicked unit
if(DEFAULT_STATE.scheme) colorBy = DEFAULT_STATE.scheme;

function addToPalette(c){ if(c && !PALETTE.includes(c)){ PALETTE.push(c); lsSet("gocam-palette",PALETTE); renderPalette(); } }
function renderPalette(){
  const el=document.getElementById("palette"); if(!el) return;
  el.innerHTML = PALETTE.map(c=>
    `<span style="position:relative;display:inline-block;margin:0 5px 0 2px;vertical-align:middle">`
    +`<span class="swatchbtn" data-c="${c}" title="${c} — click to apply to the unit, molecule or model you clicked last"`
    +` style="display:inline-block;width:18px;height:18px;border:1px solid #999;border-radius:3px;background:${c};cursor:pointer;vertical-align:middle"></span>`
    +`<span class="swatchdel" data-c="${c}" title="remove this colour"`
    +` style="position:absolute;top:-6px;right:-7px;width:13px;height:13px;line-height:11px;text-align:center;font-size:10px;color:#611;background:#fff;border:1px solid #999;border-radius:50%;cursor:pointer">×</span>`
    +`</span>`).join("");
  el.querySelectorAll(".swatchbtn").forEach(s=>s.onclick=()=>{
    const c=s.dataset.c; const pa=document.getElementById("palAdd"); if(pa) pa.value=c;   // "get" the colour
    if(COLOR_TARGET && COLOR_TARGET.model){ pushHistory(); setModelColor(COLOR_TARGET.model, c); showModelColour(COLOR_TARGET.model); flash("applied "+c+" to model "+COLOR_TARGET.model.split(":")[1]); }
    else if(COLOR_TARGET && COLOR_TARGET.node && cy && cy.getElementById(COLOR_TARGET.node).length){ pushHistory(); setNodeColor(cy.getElementById(COLOR_TARGET.node), c);
      const pk=document.querySelector("#detail .colpick"); if(pk) pk.value=c; const rs=document.querySelector("#detail .colreset"); if(rs) rs.disabled=false; const st=document.querySelector("#detail .colstate"); if(st) st.textContent="your colour"; flash("applied "+c); }
    else { flash("got "+c+" — click a unit, a molecule or a model first"); }
  });
  el.querySelectorAll(".swatchdel").forEach(s=>s.onclick=(e)=>{
    e.stopPropagation(); const c=s.dataset.c;
    PALETTE=PALETTE.filter(x=>x!==c); lsSet("gocam-palette",PALETTE); renderPalette();
  });
}

// --- undo history (colours, palette, scheme, positions) ---
let HISTORY=[];
function snapshot(){
  const pos={}; if(cy) cy.nodes("[!is_cell]").forEach(n=>{ const p=n.position(); pos[n.data("sig")]={x:p.x,y:p.y}; });
  return {colors:Object.assign({},OVERRIDE), palette:PALETTE.slice(), scheme:colorBy, pos};
}
function pushHistory(){ HISTORY.push(snapshot()); if(HISTORY.length>80) HISTORY.shift(); }
function restoreSnap(s){
  OVERRIDE=Object.assign({},s.colors); PALETTE=s.palette.slice(); colorBy=s.scheme;
  lsSet("gocam-colors",OVERRIDE); lsSet("gocam-palette",PALETTE);
  const sel=document.getElementById("colorBy"); if(sel) sel.value=colorBy;
  if(cy) cy.nodes("[!is_cell]").forEach(n=>{ const p=s.pos[n.data("sig")]; if(p) n.position(p); });
  renderPalette(); applyColors(); if(typeof showSchemeLegend==="function") showSchemeLegend();
}
function undo(){ if(!HISTORY.length){ flash("nothing to undo"); return; } restoreSnap(HISTORY.pop()); flash("reverted"); }

function darken(hex,f){   // return a slightly darker shade of a #rrggbb colour
  f = (f===undefined) ? 0.52 : f;   // darker outlines (2026-09-22)
  const m=/^#?([0-9a-fA-F]{6})$/.exec(hex||""); if(!m) return "#3a4a5a";
  const n=parseInt(m[1],16);
  const r=Math.round(((n>>16)&255)*f), g=Math.round(((n>>8)&255)*f), b=Math.round((n&255)*f);
  return "#"+((1<<24)+(r<<16)+(g<<8)+b).toString(16).slice(1);
}
function schemeFill(n){
  if(colorBy==="grey") return GREY.fill;
  if(colorBy==="model") return MCOL[(n.data("models")||[])[0]]||"#dcecff";
  return n.data("bridge")?"#ffd166":"#dcecff";  // bridge/single (complexes coloured like any other unit)
}
function nodeFill(n){
  if(n.data("is_mol")) return nodeOverride(n) || "#eaf6e6";   // molecules light green by default in every scheme (user 2026-11-27); own colour if given
  return OVERRIDE[n.data("sig")] || OVERRIDE[n.data("bsig")] || schemeFill(n);   // free override first (bsig = same unit without the cell part, so colours carry across layouts), else the default scheme
}
function nodeStroke(n){
  if(n.data("is_mol")){ const o=nodeOverride(n); return o ? darken(o) : "#8ab17d"; }
  if(CELL_ON && n.data("nocl")) return "#e67e22";       // no cell type: orange dashed outline (style .nocl)
  const o=OVERRIDE[n.data("sig")] || OVERRIDE[n.data("bsig")];
  if(o) return darken(o);                              // darker shade of the chosen colour
  if(colorBy==="grey") return GREY.stroke;
  if(colorBy==="model") return darken(schemeFill(n));
  return n.data("bridge")?"#a67400":"#2a63a8";
}
function applyColors(){
  if(!cy) return;
  cy.nodes("[!is_cell]").forEach(n=>{ n.style("background-color",nodeFill(n)); n.style("border-color",nodeStroke(n)); });
}
function setUnitColor(sig,color){ const n=cy?cy.nodes().filter(x=>x.data("sig")===sig):null; if(n&&n.length) return setNodeColor(n[0],color);
  if(color) OVERRIDE[sig]=color; else delete OVERRIDE[sig]; lsSet("gocam-colors",OVERRIDE); applyColors(); }
// a node's own colour: stored under its layout-independent key (bsig), so it survives switching layout; "back to default"
// removes every key it could be stored under (sig and bsig), so the colour really goes (user 2026-11-27)
function nodeOverride(n){ return OVERRIDE[n.data("sig")] || (n.data("bsig") ? OVERRIDE[n.data("bsig")] : undefined); }
function setNodeColor(n,color,noApply){ const s=n.data("sig"), b=n.data("bsig");
  delete OVERRIDE[s]; if(b) delete OVERRIDE[b]; if(color) OVERRIDE[b||s]=color;
  if(!noApply){ lsSet("gocam-colors",OVERRIDE); applyColors(); } }
let COLOR_TARGET=null;   // what a click on a "My colours" swatch colours: {node:id} or {model:mid}; set by clicking a node / a model
function colourRowHtml(label, cur, custom){
  return `<div class="row" style="margin-top:8px"><span class="k">${label}</span>`+
    `<input type="color" class="colpick" value="${cur}"> `+
    `<button class="colsave" title="add this colour to My colours">★ add to My colours</button> `+
    `<button class="colreset"${custom?"":" disabled"}>back to default</button> `+
    `<span class="sub colstate">${custom?"your colour":"default colour"}</span></div>`;
}
function wireColourRow(root, apply){   // apply(colour|null)
  const pk=root.querySelector(".colpick"), sv=root.querySelector(".colsave"), rs=root.querySelector(".colreset"), st=root.querySelector(".colstate");
  const mark=c=>{ if(rs) rs.disabled=!c; if(st) st.textContent=c?"your colour":"default colour"; };
  if(pk){ pk.addEventListener("focus",pushHistory); pk.oninput=()=>{ apply(pk.value); mark(true); }; pk.onchange=()=>{ apply(pk.value); addToPalette(pk.value); mark(true); }; }
  if(sv) sv.onclick=()=>{ addToPalette(pk.value); flash("added "+pk.value+" to My colours"); };
  if(rs) rs.onclick=()=>{ pushHistory(); apply(null); mark(false); flash("back to the default colour"); };
}
function modelCurrentColour(mid){
  const us=cy.nodes("[!is_mol][!is_cell]").filter(n=>(n.data("models")||[]).includes(mid));
  const cs=new Set(us.map(n=>nodeOverride(n)||"")); return (cs.size===1 && [...cs][0]) ? [...cs][0] : null;
}
// colour box next to the clicked unit / molecule (user 2026-11-27: the colour row in the side panel was out of sight)
function clearDetail(){ const d=document.getElementById("detail"); if(d){ d.innerHTML=""; d.style.display="none"; } }   // unclick -> details gone (user 2026-11-27)
function hideColPop(){ const p=document.getElementById("colpop"); if(p) p.style.display="none"; }
function showColPop(node){
  const pop=document.getElementById("colpop"); if(!pop||!cy) return;
  const cur=nodeOverride(node), def=nodeFill(node);
  pop.innerHTML=`<span class="x" title="close">&times;</span><span class="ttl">${(node.data("gp")||"").replace(/</g,"&lt;")}</span>`+
    colourRowHtml("colour", cur||def, !!cur)+
    (PALETTE.length?`<div style="margin-top:4px"><span class="sub">My colours:</span><br>`+PALETTE.map(c=>`<span class="sw" data-c="${c}" title="${c}" style="background:${c}"></span>`).join("")+`</div>`
                   :`<div class="sub" style="margin-top:4px">My colours is empty: pick a colour, then ★ to keep it.</div>`);
  const apply=c=>{ setNodeColor(node,c); const side=document.querySelector("#unitcolrow .colpick, #detail > .row .colpick"); };
  wireColourRow(pop, c=>{ apply(c); if(c===null){ const pk=pop.querySelector(".colpick"); if(pk) pk.value=nodeFill(node); } });
  pop.querySelector(".colsave").addEventListener("click",()=>showColPop(node));   // refresh the swatches
  pop.querySelectorAll(".sw").forEach(sw=>sw.onclick=()=>{ pushHistory(); setNodeColor(node,sw.dataset.c); showColPop(node); flash("applied "+sw.dataset.c); });
  pop.querySelector(".x").onclick=hideColPop;
  // place it beside the node, inside the graph area
  const r=document.getElementById("cy").getBoundingClientRect(), bb=node.renderedBoundingBox();
  pop.style.display="block";
  const w=pop.offsetWidth, h=pop.offsetHeight;
  let x=r.left+bb.x2+12, y=r.top+bb.y1;
  if(x+w>r.right) x=r.left+bb.x1-w-12;
  x=Math.max(r.left+4, Math.min(x, r.right-w-4)); y=Math.max(r.top+4, Math.min(y, r.bottom-h-4));
  pop.style.left=x+"px"; pop.style.top=y+"px";
}
function showModelColour(mid){   // colour row for a whole model, under the unit details
  COLOR_TARGET={model:mid};
  const box=document.getElementById("modelcolrow"); if(!box) return;
  const cur=modelCurrentColour(mid);
  box.innerHTML=`<div class="row" style="margin-top:8px"><b>Model ${mid.split(":")[1]}</b> <span class="sub">(highlighted; colours its units)</span></div>`+
    colourRowHtml("model colour", cur||MCOL[mid]||"#3f8fd0", !!cur);
  wireColourRow(box, c=>setModelColor(mid,c));
}
function setModelColor(mid,color){
  if(!cy) return;
  cy.nodes("[!is_mol][!is_cell]").forEach(n=>{ if((n.data("models")||[]).includes(mid)) setNodeColor(n,color,true); });
  lsSet("gocam-colors",OVERRIDE); applyColors();
}
function clearAllOverrides(){ pushHistory(); OVERRIDE={}; lsSet("gocam-colors",OVERRIDE); applyColors(); }
function renderModelTags(loaded){
  const el=document.getElementById("modeltags"); if(!el) return;
  el.innerHTML = loaded.map(mid=>{
    const h=mid.split(':')[1];
    return `<div class="row" style="display:flex;align-items:center;gap:6px">`
      +`<input type="color" data-m="${mid}" class="mcol" value="${MCOL[mid]||'#3f8fd0'}">`
      +`<span class="mono" style="flex:1">${h}</span>`
      +`<button data-m="${mid}" class="mclear" style="padding:1px 5px">reset</button></div>`;
  }).join("");
  el.querySelectorAll("input.mcol").forEach(c=>{ c.addEventListener("focus",pushHistory); c.oninput=()=>setModelColor(c.dataset.m,c.value); c.onchange=()=>addToPalette(c.value); });
  el.querySelectorAll("button.mclear").forEach(b=>b.onclick=()=>setModelColor(b.dataset.m,null));
}

function normId(s){ s=(s||"").trim(); if(!s) return ""; return s.startsWith("gomodel:")?s:("gomodel:"+s); }
const short = s => { s=s||""; return s.length>26 ? s.slice(0,25)+"…" : s; };

// --- render the "loaded models" panel ---
function renderCacheList(ids){
  ids = ids || [];
  document.getElementById("ncache").textContent = "("+ids.length+")";
  const el = document.getElementById("cachelist");
  el.innerHTML = ids.slice().sort((a,b)=>a.localeCompare(b)).map(id=>CACHE[id]).filter(Boolean).map(m=>
    `<div class="row"><span class="dot" style="width:9px;height:9px;border:none;background:${MCOL[m.id]||'#c9c9c9'}"></span> `+
    `<span class="mono">${m.id.split(':')[1]}</span> ${m.title.replace(/_.*/,'')}`+
    (m._src==="dev"||m._src==="DEV"?` <span class="sub" title="read from the Noctua DEV server (model is not on live)">&#9432; dev server</span>`:``)+
    (m._src==="mirror"?` <span class="sub" title="GO's HTTPS publication of production models (live-go-cam), regenerated from live Noctua by the GO pipeline; this file dated ${m._asof}">&#9432; production mirror, as of ${m._asof}</span>`:``)+
    `</div>`).join("");
}

// --- merge logic (client-side port) ---
// "same BP" = same direct BP AND the same part_of chain above it (user 2026-10-30: GUCA1A in 6a0784b700000336 vs
// 6a18a9ba00002973, cellular response to calcium ion part_of visual perception vs part_of photoresponse recovery
// part_of visual perception, must NOT merge)
const bpKey = a => [a.bp_id].concat((a.bp_chain||[]).map(c=>c.id)).join(">");
const bpChainStr = n => [n.bp||n.bp_id||"(none)"].concat((n.bp_chain||[]).map(c=>c.label||c.id)).join(" → ");
// same for CC: "same CC" = same CC AND the same part_of chain (cell type / anatomy) above it (user 2026-10-30)
const ccKey = a => [a.cc_id].concat((a.cc_chain||[]).map(c=>c.id)).join(">");
const ccChainStr = n => [n.cc||n.cc_id||"(none)"].concat((n.cc_chain||[]).map(c=>c.label||c.id)).join(" → ");
function intrinsicKey(a){
  const eb = a.is_complex ? ("complex:"+a.gp_id+":"+(a.complex_part_ids||[]).map(canonId).sort().join(",")) : ("gp:"+canonId(a.gp_id));
  const parts=[eb];
  if(MERGE_ON.mf) parts.push("mf:"+a.mf_id);
  if(MERGE_ON.bp) parts.push("bp:"+bpKey(a));
  if(MERGE_ON.cc) parts.push("cc:"+ccKey(a));
  if(CELL_ON){ const c=cellOf(a); parts.push("cl:"+(c?c.id:"none")); }   // by-cell layout: units in different cell types never merge
  return parts.join("|");
}

function buildGraph(selectedIds, mode, showMols){
  const acts = [];              // {mid, a}
  const intrinsicOf = {};       // full local_id -> intrinsic key (for strict target resolution)
  selectedIds.forEach(mid=>{
    const m = CACHE[mid]; if(!m) return;
    m.activities.forEach(a=>{ acts.push({mid, a}); intrinsicOf[a.local_id]=intrinsicKey(a); });
  });

  function nodeKey(a){
    if(mode!=="strict") return intrinsicKey(a);
    const inputs = (a.mols||[]).map(x=>x[0]+"::"+x[2]).sort().join(",");
    const targets = (a.edges||[]).map(e=>e.cls+"->"+(intrinsicOf[e.downstream]||"?")).sort().join(",");
    return intrinsicKey(a)+"||IN["+inputs+"]||T["+targets+"]";
  }

  const keyToId = {}, nodes = {}, actToNode = {};
  let c = 0;
  acts.forEach(({mid,a})=>{
    const k = nodeKey(a);
    if(!(k in keyToId)) keyToId[k] = "n"+(c++);
    const nid = keyToId[k];
    actToNode[a.local_id] = nid;
    if(!nodes[nid]){
      nodes[nid] = {id:nid, sig:intrinsicKey(a), gp:a.gp, gp_id:a.gp_id, is_complex:a.is_complex,
        complex_parts:a.complex_parts, complex_part_ids:a.complex_part_ids,
        mf:a.mf, mf_id:a.mf_id, bp:a.bp, bp_id:a.bp_id, bp_key:bpKey(a), cc_key:ccKey(a),
        cc:a.cc, cc_id:a.cc_id, cell:a.cell, cell_id:a.cell_id, bp_chain:a.bp_chain||[], cc_chain:a.cc_chain||[], prot_io:a.prot_io||[], mols:[], models:[],
        bsig:intrinsicKey(a).replace(/\|cl:[^|]*$/,""), cell_key:null, cell_label:null, nocl:true};
    }
    const n = nodes[nid];
    { const c=cellOf(a);
      if(c && !n.cell_key){ n.cell_key=c.id; n.cell_label=c.label; n.nocl=false; }
      if(c && c.spec && c.spec!==c.id){ n.cell_spec=n.cell_spec||[]; let e=n.cell_spec.find(x=>x.id===c.spec);
        if(!e){ e={id:c.spec,label:c.specLabel,models:[]}; n.cell_spec.push(e); } if(!e.models.includes(mid)) e.models.push(mid); } }
    if(!n.models.includes(mid)) n.models.push(mid);
    (a.mols||[]).forEach(x=>{ if(!n.mols.some(y=>y[0]===x[0]&&y[1]===x[1])) n.mols.push([x[0],x[1],x[2],x[5]||null]); });   // keep the term id (x[2]) too
  });

  const edges = {};
  acts.forEach(({mid,a})=>{
    const src = actToNode[a.local_id];
    (a.edges||[]).forEach(e=>{
      const tgt = actToNode[e.downstream];
      if(!src||!tgt) return;
      const key = src+"|"+tgt+"|"+e.cls;
      if(!edges[key]) edges[key]={id:"e"+Object.keys(edges).length,source:src,target:tgt,label:e.label,cls:e.cls,models:[]};
      if(!edges[key].models.includes(mid)) edges[key].models.push(mid);
    });
  });

  Object.values(nodes).forEach(n=>n.bridge = n.models.length>1);

  if(showMols){
    // Molecules = CHEBI small molecules ONLY (proteins excluded). Node identity is
    // a "slot" = (activity node, ion, direction in/out), so a transporter shows
    // ONE in-node + ONE out-node per ion (no stoichiometry, in != out). Slots are
    // then unified where the GO-CAM reuses the SAME molecule individual across
    // activities -- that's how the channel's cytoplasmic Ca-out becomes the same
    // node as SLC24A1's Ca-in (both are the individual GUCA1B senses), while the
    // channel's extracellular Ca-in and SLC24A1's extruded Ca-out stay separate.
    const parent={};
    function find(x){ if(parent[x]===undefined)parent[x]=x; while(parent[x]!==x){parent[x]=parent[parent[x]];x=parent[x];} return x; }
    // RULE (user 2026-11-26): an EXTRACELLULAR molecule (located in GO:0005576 or a subterm, incl. the synaptic cleft) is
    // never merged across models: a synaptic cleft is specific to its synapse, and a molecule released at one synapse is
    // not the one received at another. It is one node per molecule individual of its own model, joined only where that
    // model itself uses the same individual (e.g. glutamate released by the SNARE complex and sensed by GRM6 in one model).
    // Replaces the 2026-10-26 pool (one synaptic-cleft node per chemical across all models). To be narrowed case by case.
    function slotId(an,term,pred,loc,mid,molid){
      if((XMOL_RULE==="strict"||XMOL_RULE==="link") && loc && isExtracellular(loc)) return "XM|"+mid+"|"+(molid||(an+"|"+term+"|"+pred));
      if(XMOL_RULE==="pool" && loc && isPoolLoc(loc)) return "X|"+term+"|"+loc;
      return an+"|"+term+"|"+((pred==="has output")?"out":"in"); }
    const indSlots={};   // molecule individual -> [slotIds]
    acts.forEach(({mid,a})=>{
      const an=actToNode[a.local_id];
      (a.mols||[]).forEach(x=>{ const pred=x[0],term=x[2],molid=x[3];
        if(!/^CHEBI:/.test(term||"")) return;
        const s=slotId(an,term,pred,x[4],mid,molid); find(s);
        (indSlots[molid]=indSlots[molid]||[]).push(s); });
    });
    Object.values(indSlots).forEach(ss=>{ for(let i=1;i<ss.length;i++) parent[find(ss[0])]=find(ss[i]); });

    // an extracellular molecule node that touches only ONE unit (one direction) links nothing: shown once per unit, not
    // once per model (avoids 7 identical Ca2+ inputs on the merged CNG channel). One that touches two or more units (a
    // release -> reception link) keeps its own model (user rule 2026-11-26).
    const xTouch={};
    if(XMOL_RULE==="link") acts.forEach(({mid,a})=>{ const an=actToNode[a.local_id];
      (a.mols||[]).forEach(x=>{ if(!/^CHEBI:/.test(x[2]||"") || !(x[4] && isExtracellular(x[4]))) return;
        const g=find(slotId(an,x[2],x[0],x[4],mid,x[3])); (xTouch[g]=xTouch[g]||new Set()).add(an+"|"+((x[0]==="has output")?"out":"in")); }); });
    // NARROWED (user 2026-11-26, 6ac817cf00001061 + 6ab067da00012618): an extracellular molecule touching ONE unit joins the
    // molecule of another model that touches that same (merged) unit with the same chemical, direction and location, when
    // there is exactly one such molecule: the models share the unit connected to it. Two molecules that each touch several
    // units (two release sites) are never joined, even through a shared unit.
    const xByUnit={};   // unit|dir|chemical|location -> multi-unit extracellular groups touching it
    if(XMOL_RULE==="link") acts.forEach(({mid,a})=>{ const an=actToNode[a.local_id];
      (a.mols||[]).forEach(x=>{ if(!/^CHEBI:/.test(x[2]||"") || !(x[4] && isExtracellular(x[4]))) return;
        const g=find(slotId(an,x[2],x[0],x[4],mid,x[3])); if(!xTouch[g] || xTouch[g].size<2) return;
        const k=an+"|"+((x[0]==="has output")?"out":"in")+"|"+x[2]+"|"+x[4]; (xByUnit[k]=xByUnit[k]||new Set()).add(g); }); });
    const molGroup=(an,x,mid)=>{ const g=find(slotId(an,x[2],x[0],x[4],mid,x[3]));
      if(!(xTouch[g] && xTouch[g].size===1)) return g;
      const t=[...xTouch[g]][0], hit=xByUnit[t+"|"+x[2]+"|"+x[4]];
      if(hit && hit.size===1) return [...hit][0];
      return "XU|"+t+"|"+x[2]+"|"+x[4]; };
    const molNodes={};
    acts.forEach(({mid,a})=>{
      const anode=actToNode[a.local_id];
      (a.mols||[]).forEach(x=>{
        const pred=x[0], label=x[1], term=x[2];
        if(!/^CHEBI:/.test(term||"")) return;
        const grp=molGroup(anode,x,mid);
        const mnid="m_"+grp.replace(/[^a-zA-Z0-9]/g,"_");
        const xl = x[4] && isPoolLoc(x[4]);
        if(!molNodes[mnid]) molNodes[mnid]={id:mnid, sig:mnid, is_mol:true, gp:label, gp_id:term, loc_id:x[4]||null, loc:x[5]||null, xmol:!!xl,
          mlabel: label+(x[5]?"\n["+x[5]+"]":""),
          is_complex:false, complex_parts:[], complex_part_ids:[], mf:"", mf_id:"", bp:"", bp_id:"", cc:"", cc_id:"", cell:"", cell_id:"",
          mols:[], models:[], bridge:false};
        if(!molNodes[mnid].models.includes(mid)) molNodes[mnid].models.push(mid);
        let src, tgt, cls;
        if(pred==="has output"){ src=anode; tgt=mnid; cls="mol"; }
        else if(pred==="has small molecule activator"){ src=mnid; tgt=anode; cls="pos"; }
        else if(pred==="has small molecule inhibitor"){ src=mnid; tgt=anode; cls="neg"; }
        else { src=mnid; tgt=anode; cls="mol"; }  // has input
        if(src===tgt) return;
        const key=src+"|"+tgt+"|"+cls;
        if(!edges[key]) edges[key]={id:"e"+Object.keys(edges).length,source:src,target:tgt,label:pred,cls:cls,models:[]};
        if(!edges[key].models.includes(mid)) edges[key].models.push(mid);
      });
    });
    Object.values(molNodes).forEach(n=>{ n.bridge = n.models.length>1; nodes[n.id]=n; });
  }

  return {nodes:Object.values(nodes), edges:Object.values(edges)};
}

// --- layout persistence ---
function layoutKey(ids){ return "gocam-layout:"+ids.slice().sort().join(","); }
function loadLayout(ids){ try{ return JSON.parse(localStorage.getItem(layoutKey(ids))||"null"); }catch(e){ return null; } }
function saveLayout(ids){
  if(!cy) return;
  const pos={}; cy.nodes("[!is_cell]").forEach(n=>{ pos[n.data("sig")] = n.position(); });
  try{ localStorage.setItem(layoutKey(ids), JSON.stringify(pos)); flash("layout saved"); }
  catch(e){ flash("layout can't be saved here (sandbox)"); }
}
function flash(msg){
  const s=document.getElementById("stats"); const old=s.innerHTML;
  s.innerHTML=`<span class="stat" style="background:#dfe">${msg}</span>`+old;
  setTimeout(()=>{ s.innerHTML=old; }, 1400);
}

// molecule node size from its name (+ location line): the name is HTML text, so the ellipse is sized to fit it
const MOLF={name:20, loc:15};
function molSize(n){
  const wrapN=(t,per)=>{ const out=[]; let cur="";
    String(t||"").split(/\s+/).forEach(w=>{ while(w.length>per){ if(cur){ out.push(cur); cur=""; } out.push(w.slice(0,per)); w=w.slice(per); }
      const c=cur?cur+" "+w:w; if(c.length>per && cur){ out.push(cur); cur=w; } else cur=c; });
    if(cur) out.push(cur); return out.length?out:[""]; };
  const nl=wrapN(n.gp,16), ll=n.loc?wrapN("["+n.loc+"]",21):[];
  const tw=Math.round(Math.min(176, Math.max(...nl.map(l=>l.length*11.2), ...ll.map(l=>l.length*8.2), 40)));
  const th=nl.length*MOLF.name*1.15 + (ll.length? 2+ll.length*MOLF.loc*1.2 : 0);
  return {tw, mw:Math.round(tw/0.74+18), mh:Math.round(Math.max(52, th/0.74+14))};
}

// --- cell boxes: compound nodes "cell:<CL>" (+ "cell:EXTRA"); sets .parent on the graph's node data ---
function cellCompartments(g){
  const boxes={};   // id -> box data
  const add=(key,label)=>{ const id="cell:"+key;
    if(!boxes[id]){ const extra=key===EXTRA_ID, t=extra?["#f7f7f7","#999999"]:CELL_TINT[Object.values(boxes).filter(b=>!b.extra).length%CELL_TINT.length];
      boxes[id]={id, is_cell:true, extra, cl:extra?"":key, label:extra?"extracellular":(label+"  "+key), tint:t[0], edge:t[1], sig:id}; }
    return id; };
  const units=g.nodes.filter(n=>!n.is_mol);
  units.forEach(n=>{ if(n.cell_key===EXTRA_ID) n.xzone=true; else if(n.cell_key) n.parent=add(n.cell_key, n.cell_label); });   // extracellular: no box, laid out between the cells (user 2026-10-26)
  // nest a subclass box inside the most specific parent cell box present (CL is_a / part_of ancestry from OLS)
  Object.values(boxes).forEach(b=>{ if(b.extra) return;
    const anc=_clAnc[b.cl]||new Set();
    const cands=Object.values(boxes).filter(o=>!o.extra && o.id!==b.id && anc.has(o.cl));
    cands.sort((x,y)=>(_clAnc[y.cl]||new Set()).size-(_clAnc[x.cl]||new Set()).size);   // deepest ancestor first
    if(cands.length) b.parent=cands[0].id; });
  // no-CL units: loose, unless the curator dropped them in a box earlier (CELL_PLACE, view only)
  units.forEach(n=>{ if(!n.cell_key && CELL_PLACE[n.sig] && boxes[CELL_PLACE[n.sig]]){ n.parent=CELL_PLACE[n.sig]; n.placed=true; } });
  // molecules: in the box of the units they touch; touching units in two different boxes -> extracellular (between the cells)
  const byId={}; g.nodes.forEach(n=>byId[n.id]=n);
  g.nodes.filter(n=>n.is_mol).forEach(m=>{
    const ps=new Set();
    g.edges.forEach(e=>{ const o = e.source===m.id ? e.target : (e.target===m.id ? e.source : null); if(o && byId[o] && byId[o].parent) ps.add(byId[o].parent); });
    // located in the synaptic cleft: never in a box. Touching units of ONE cell -> just outside that cell's box, beside its
    // unit (like other extracellular molecules); touching units of two cells -> between them, near its units (user 2026-11-26:
    // the cleft molecules used to sit in one row between the columns, far from their units)
    if(m.xmol){ const tops=new Set([...ps].map(b=>{ let t=b; while(boxes[t] && boxes[t].parent) t=boxes[t].parent; return t; }));
      if(tops.size>1) m.xzone=true; else m.outer=true; }
    else if(m.loc_id && isExtracellular(m.loc_id)) m.outer=true;   // other extracellular location: just outside its cell box (user 2026-10-26)
    else if(ps.size===1) m.parent=[...ps][0];
    else if(ps.size>1) m.xzone=true;
  });
  return Object.values(boxes);
}

// --- render ---
function render(g, selectedIds){
  const savedPos = PENDING_LAYOUT || DEFAULT_STATE.layout || null;   // Build always auto-lays-out; saved layouts apply only via "load layout"
  const els=[];
  function estHeight(n){ // rough box height so the HTML label fits (name big, MF small)
    const nameLines=Math.max(1,Math.ceil((n.gp||"").length/13));   // Arial bold 24px ≈ 13 chars per 208px line
    const mfLines = n.mf ? Math.max(1,Math.ceil(n.mf.length/17)) : 0;   // Arial 18px ≈ 17 chars/line
    return Math.max(66, nameLines*29 + mfLines*23 + 22);
  }
  g.nodes.forEach(n=>{ delete n.parent; delete n.placed; delete n.xzone; delete n.outer; });
  if(CELL_ON) cellCompartments(g).forEach(b=>els.push({data:b}));   // boxes first, children reference them
  g.nodes.forEach(n=>{ if(n.is_mol) Object.assign(n, molSize(n)); });
  g.nodes.forEach(n=>els.push({data:{...n, label:(n.gp||"")+(n.mf?("\n"+n.mf):""), h:estHeight(n)+(CELL_ON&&n.nocl&&!n.is_mol?24:0)+(CELL_ON&&n.cell_spec&&n.cell_spec.length?22:0)},
    classes:(CELL_ON&&n.nocl&&!n.is_mol)?"nocl":""}));
  g.edges.forEach(e=>els.push({data:{id:e.id,source:e.source,target:e.target,label:e.label,cls:e.cls,models:e.models}}));

  clearDetail();   // a new graph: no stale details
  cy = cytoscape({
    container:document.getElementById("cy"),
    elements:els,
    style:[
      {selector:"node[?is_cell]",style:{
        "shape":"round-rectangle","background-color":"data(tint)","background-opacity":0.6,
        "border-width":3,"border-color":"data(edge)","border-style":e=>e.data("extra")?"dashed":"solid",
        "label":"data(label)","text-valign":"top","text-halign":"center","text-margin-y":-12,
        "font-size":"40px","font-weight":"bold","font-family":"Arial, Helvetica, Liberation Sans, sans-serif","color":"#000","text-wrap":"wrap","text-max-width":"560px",
        "padding":"36px"}},
      {selector:"node[!is_mol][!is_cell]",style:{
        "label":"","width":"224px","height":"data(h)","shape":"round-rectangle",
        "background-color":e=>e.data("bridge")?"#ffd166":"#dcecff",
        "border-width":e=>e.data("bridge")?2:1,
        "border-color":e=>e.data("bridge")?"#a67400":"#2a63a8",
        "padding":"6px"}},
      {selector:"node[?is_mol]",style:{   // name drawn as sharp HTML text (nodeHtmlLabel), not canvas text (blurry when zoomed; user 2026-10-26)
        "label":"","width":"data(mw)","height":"data(mh)","shape":"ellipse",
        "background-color":"#eaf6e6","border-width":1.5,"border-color":"#8ab17d"}},
      {selector:"edge",style:{
        "curve-style":"bezier","width":e=>e.data("cls")==="mol"?2.5:3.5,   // thicker connectors (2026-09-22)
        "line-style":e=>e.data("cls")==="mol"?"dashed":"solid",
        "line-color":e=>ECOL[e.data("cls")]||"#888",
        "target-arrow-color":e=>ECOL[e.data("cls")]||"#888",
        "target-arrow-shape":e=>e.data("cls")==="neg"?"tee":"triangle","arrow-scale":1.7}},
      {selector:".nocl",style:{"border-style":"dashed","border-width":4}},
      {selector:".faded",style:{"opacity":0.12}},
      {selector:".hi",style:{"border-color":"#1a1a2e","border-width":4}},
      // several nodes selected (Shift/Ctrl/Cmd-click, or Shift-drag a rectangle): blue, and they move together (user 2026-11-26)
      {selector:"node:selected[!is_cell]",style:{"outline-width":5,"outline-color":"#1f6feb","outline-offset":4,"outline-opacity":1}},   // outline, not a tint: the node keeps its colour (user 2026-11-27)
      {selector:"node:selected[?is_cell]",style:{"border-color":"#1f6feb","border-width":8}},
    ],
    layout:{name:"preset"}, // we position manually below
    boxSelectionEnabled:true, selectionType:"single",   // Shift/Ctrl/Cmd-click adds; Shift-drag on the background draws a selection rectangle
  });

  // rich labels: gene product BIG, molecular function small underneath
  if(typeof cy.nodeHtmlLabel==="function"){
    cy.nodeHtmlLabel([{
      query:"node[?is_mol]", halign:"center", valign:"center", halignBox:"center", valignBox:"center",
      tpl:function(d){
        const esc=t=>String(t||"").replace(/&/g,"&amp;").replace(/</g,"&lt;");
        return '<div style="width:'+d.tw+'px;text-align:center;pointer-events:none;overflow-wrap:anywhere;font-family:Arial,Helvetica,&quot;Liberation Sans&quot;,sans-serif;color:#0b1220">'
          +'<div style="font-size:'+MOLF.name+'px;font-weight:600;line-height:1.15">'+esc(d.gp)+'</div>'
          +(d.loc?'<div style="font-size:'+MOLF.loc+'px;line-height:1.2;color:#445;margin-top:2px">['+esc(d.loc)+']</div>':'')
          +'</div>';
      }
    },{
      query:"node[!is_mol][!is_cell]", halign:"center", valign:"center", halignBox:"center", valignBox:"center",
      tpl:function(d){
        const gp=(d.gp||"").replace(/</g,"&lt;");
        const mf=(d.mf||"").replace(/</g,"&lt;");
        const spec=(CELL_ON&&d.cell_spec&&d.cell_spec.length) ? '<div style="font-size:15px;color:#556;margin-top:3px">'+d.cell_spec.map(x=>x.label).join(", ").replace(/</g,"&lt;")+'</div>' : '';
        const tag=(CELL_ON&&d.nocl) ? '<div style="font-size:15px;font-weight:700;color:#b85c00;margin-top:4px">'+(d.placed?"placed by you, not in model":"no CL")+'</div>' : '';
        return '<div style="width:208px;text-align:center;pointer-events:none;font-family:Arial,Helvetica,&quot;Liberation Sans&quot;,sans-serif">'
          +'<div style="font-size:24px;font-weight:700;line-height:1.15;color:#0b1220">'+gp+'</div>'
          +(mf?'<div style="font-size:18px;line-height:1.2;color:#0b1220;margin-top:3px">'+mf+'</div>':'')
          +spec+tag
          +'</div>';
      }
    }]);
  }

  if(savedPos){
    cy.nodes("[!is_cell]").forEach(n=>{ const k=n.data("sig"); if(savedPos[k]) n.position(savedPos[k]); });
    cy.fit(null,40);
  } else {
    CELL_ON ? cellLayout() : autoLayout();
  }
  { const cl=document.getElementById("celllegend"); if(cl) cl.style.display=CELL_ON?"":"none"; }
  PENDING_LAYOUT=null;   // one-shot: consumed by this build only

  wireInteractions();
  applyBoxSizes(); setupBoxGrips(); pushOutExtracellular();
  renderModelTags(selectedIds);
  renderPalette();
  applyColors();
  const nb = g.nodes.filter(n=>n.bridge).length;
  document.getElementById("stats").innerHTML =
    `<span class="stat">${selectedIds.length} models</span>`+
    `<span class="stat">${g.nodes.length} nodes</span>`+
    `<span class="stat">${nb} bridges</span>`+
    `<span class="stat">${g.edges.length} edges</span>`;
}

function wireInteractions(){
  // molecules ride along with what is dragged, keeping the place the curator gave them (offsets taken when the drag
  // starts, not from the last auto-layout; user 2026-10-26): a unit carries its own molecules (those touching only it,
  // except a shared synaptic-cleft pool); a cell box carries the extracellular molecules drawn just outside it.
  cy.on("grab","node[!is_mol]",evt=>{ const a=evt.target, p=a.position(); let fol=cy.collection();
    if(a.data("is_cell")){ const kids=a.descendants("[!is_mol]"); fol=cy.nodes("[?outer]").filter(m=>m.neighborhood("node").some(u=>kids.contains(u))); }
    else fol=a.neighborhood("node[?is_mol]").filter(m=>m.degree()===1 && !m.data("xmol") && !m.parent().same(a));
    fol=fol.filter(m=>!m.selected() && !m.ancestors().some(b=>b.selected()));   // moving a selection: selected nodes move by themselves
    a.scratch("_fol", fol.map(m=>({m, x:m.position().x, y:m.position().y}))); a.scratch("_p0", {x:p.x, y:p.y}); });
  cy.on("drag","node[!is_mol]",evt=>{ const a=evt.target, f=a.scratch("_fol"), p0=a.scratch("_p0"); if(!f||!p0) return;
    const p=a.position(), dx=p.x-p0.x, dy=p.y-p0.y;
    f.forEach(o=>{ if(!a.data("is_cell") || !o.m.parent().length) o.m.position({x:o.x+dx, y:o.y+dy}); }); });
  cy.on("free","node[!is_mol]",evt=>{ const a=evt.target; a.removeScratch("_fol"); a.removeScratch("_p0");
    if(!a.data("is_cell") && !a.data("nocl") && a.parent().length) separateBoxes(a.parent());   // box grew -> push neighbours aside
    pushOutExtracellular(); });
  cy.on("free","node[?is_mol]",evt=>{ pushOutExtracellular();   // a molecule dropped inside a box is pushed back out
    const m=evt.target; if(m.data("outer")||m.data("xzone")) orientIntra(m.neighborhood("node[!is_mol][!is_cell]")); });
  // no-CL unit dropped onto a cell box -> placed in it (view only). Smallest box under the drop point wins.
  // A placed unit dragged OUT of its box (past the box edge as it was when the drag started; the box grows while
  // dragging) is taken out again: loose, or into the other box it was dropped on (user 2026-11-25).
  cy.on("grab","node[?nocl]",evt=>{ const cur=evt.target.parent();
    evt.target.scratch("_box0", cur.length ? Object.assign({}, cur.boundingBox()) : null); });
  cy.on("free","node[?nocl]",evt=>{
    if(!CELL_ON) return;
    const n=evt.target, p=n.position(), cur=n.parent(), b0=n.scratch("_box0"); n.removeScratch("_box0");
    const inside=bb=>p.x>bb.x1 && p.x<bb.x2 && p.y>bb.y1 && p.y<bb.y2;
    const hit=cy.nodes("[?is_cell]").filter(c=>{ if(cur.length && (c.same(cur) || cur.ancestors().contains(c))) return false;
      return inside(c.boundingBox()); })
      .sort((x,y)=>x.boundingBox().w*x.boundingBox().h - y.boundingBox().w*y.boundingBox().h);
    if(hit.length) placeUnit(n.id(), hit[0].id());
    else if(cur.length && b0 && !inside(b0)) placeUnit(n.id(), null);
    else if(cur.length){ separateBoxes(cur); pushOutExtracellular(); }
  });
  cy.on("tap","node",evt=>{
    const n=evt.target.data();
    document.getElementById("detail").style.display="";   // shown only while a node is clicked (user 2026-11-27)
    cy.elements().removeClass("hi faded"); evt.target.addClass("hi");
    if(n.is_cell){ hideColPop();
      const kids=evt.target.descendants("[!is_mol][!is_cell]");
      document.getElementById("detail").innerHTML=
        `<h1>${n.extra?"extracellular":(n.label||"")}</h1>`+
        (n.extra?`<div class="row sub">units whose CC is under GO:0005576 extracellular region, and molecules shared by units in two different cells</div>`
                :`<div class="row"><span class="k">cell type</span><span class="mono">${n.cl}</span></div>`)+
        `<div class="row"><span class="k">units</span>${kids.length} (${kids.filter("[?placed]").length} placed by you)</div>`+
        `<div class="row" style="margin-top:6px"><span class="k">size</span>${BOXSIZE[n.id]?"set by you ":"fits its contents "}`+
        `<button id="boxfit"${BOXSIZE[n.id]?"":" disabled"}>fit to contents</button> <span class="sub">drag the corner grip &#9698; to resize</span></div>`;
      { const bf=document.getElementById("boxfit"); if(bf) bf.onclick=()=>{ delete BOXSIZE[n.id]; applyBoxSizes(); pushOutExtracellular(); bf.disabled=true; flash("box fits its contents again"); }; }
      return;
    }
    selectedSig = n.is_mol ? null : n.sig;
    COLOR_TARGET={node:n.id};   // colour row is in the details panel; no pop-up box (user 2026-11-27: "I don't want this window")
    if(n.is_mol){
      document.getElementById("detail").innerHTML=
        `<h1>◦ ${n.gp||"?"}</h1><div class="row"><span class="k">id</span><span class="mono">${n.gp_id||""}</span></div>`+
        (n.loc?`<div class="row"><span class="k" title="located in (RO:0001025)">located in</span>${n.loc} <span class="mono">${n.loc_id||""}</span>${n.xmol?' <span class="sub">(extracellular: never merged across models; a synaptic cleft belongs to its own synapse)</span>':''}</div>`:"")+
        `<div class="row"><span class="k">in models</span>${(n.models||[]).map(id=>id.split(":")[1]).join(", ")}${n.bridge?' <b style="color:#c98a00">↔ bridge</b>':''}</div>`+
        `<div class="row sub">molecule (input/output of activities)</div>`+
        colourRowHtml("colour", nodeOverride(evt.target)||nodeFill(evt.target), !!nodeOverride(evt.target));
      wireColourRow(document.getElementById("detail"), c=>setNodeColor(evt.target,c));
      return;
    }
    const mols=(n.mols||[]).map(m=>`<span class="tag">${m[0]}: ${m[1]}${m[2]?` <span class="mono">${m[2]}</span>`:""}${m[3]?` <i>in ${m[3]}</i>`:""}</span>`).join(" ")||"<span class='sub'>none</span>";
    let downstream="<span class='sub'>none</span>";
    try{ const outs=evt.target.outgoers("edge").filter(e=>e.data("cls")!=="mol");
      if(outs.length) downstream=outs.map(e=>{ const t=e.target().data(); return `<span class="tag">${e.data("label")} &rarr; ${t.gp||t.mf||"?"}${t.mf_id?` <span class="mono">${t.mf_id}</span>`:""}</span>`; }).join(" "); }catch(e){}
    const models=(n.models||[]).map(id=>`<span class="tag model" data-m="${id}"><span class="mono">${id.split(':')[1]}</span></span>`).join(" ");
    document.getElementById("detail").innerHTML=
      `<h1>${n.is_complex?"⬡ ":""}${n.gp||"?"}</h1>`+
      (n.is_complex?`<div class="row"><span class="k">gene product</span><span class="mono">${n.gp_id||""}</span></div>`:`<div class="row"><span class="k">gene product</span><span class="mono">${n.gp_id||""}</span></div>`)+
      (n.is_complex?`<div class="row"><span class="k" title="complex subunits">subunits</span>${(n.complex_parts||[]).map((lbl,i)=>`${lbl} <span class="mono">${(n.complex_part_ids||[])[i]||""}</span>`).join("<br>")||"<span class='sub'>(none listed)</span>"}</div>`:"")+
      `<div class="row"><span class="k" title="molecular function">MF</span>${n.mf||"<span class='sub'>(none)</span>"} <span class="mono">${n.mf_id||""}</span></div>`+
      `<div class="row"><span class="k" title="biological process (part_of)">BP</span>${n.bp||"<span class='sub'>(none)</span>"} <span class="mono">${n.bp_id||""}</span></div>`+
      (n.bp_chain||[]).map(c=>`<div class="row"><span class="k" title="this BP is part_of">&nbsp;&nbsp;&#8627; part of</span>${c.label} <span class="mono">${c.id||""}</span></div>`).join("")+
      `<div class="row"><span class="k" title="cellular component (occurs_in)">CC</span>${n.cc||"<span class='sub'>(none)</span>"} <span class="mono">${n.cc_id||""}</span></div>`+
      (n.cc_chain&&n.cc_chain.length ? n.cc_chain.map(c=>`<div class="row"><span class="k" title="the CC is part_of this cell / anatomy">&nbsp;&nbsp;&#8627; ${/^CL:/.test(c.id||"")?"cell type":"part of"}</span>${c.label} <span class="mono">${c.id||""}</span></div>`).join("")
        : (n.cell?`<div class="row"><span class="k" title="cell / anatomy the CC is part_of">&nbsp;&nbsp;&#8627; cell type</span>${n.cell} <span class="mono">${n.cell_id||""}</span></div>`:""))+
      (n.prot_io&&n.prot_io.length?`<div class="row"><span class="k" title="protein inputs / outputs of this activity">protein in/out</span>${n.prot_io.map(x=>`${x[0]}: ${x[1]} <span class="mono">${x[2]}</span>`).join("<br>")}</div>`:"")+
      `<div class="row" style="margin-top:6px"><span class="k" title="molecular inputs / outputs / regulators">in/out</span>${mols}</div>`+
      `<div class="row" style="margin-top:6px"><span class="k" title="activities this one causally acts on">regulates</span>${downstream}</div>`+
      `<div class="row" style="margin-top:6px"><span class="k">in models</span>${models}`+(n.bridge?` <b style="color:#c98a00">↔ bridge</b>`:"")+`</div>`+
      (CELL_ON ? (n.nocl
        ? `<div class="row" style="margin-top:6px;color:#b85c00"><b>No cell type (CL)</b> in this unit's CC chain. Place it in: <select id="placesel"><option value="">(loose)</option>`+
            cy.nodes("[?is_cell]").map(c=>`<option value="${c.id()}"${c.id()===evt.target.parent().id()?" selected":""}>${c.data("extra")?"extracellular":c.data("label")}</option>`).join("")+
            `</select><div class="sub">View only: the model is not changed. Save layout keeps it. Or drag the unit onto a box; drag it out of the box to make it loose again.</div></div>`
        : `<div class="row" style="margin-top:6px"><span class="k">cell box</span>${n.cell_key===EXTRA_ID?"extracellular":(n.cell_label+" <span class='mono'>"+n.cell_key+"</span>")}</div>`+
          (n.cell_spec||[]).map(x=>`<div class="row"><span class="k" title="cell type in the model; it is_a the box's cell type, so it is shown in that box">&nbsp;&nbsp;&#8627; in model</span>${x.label} <span class="mono">${x.id}</span> <span class="sub">(${x.models.map(m=>m.split(":")[1]).join(", ")})</span></div>`).join("")) : "")+
      `<div id="unitcolrow">`+colourRowHtml("colour", nodeOverride(evt.target)||schemeFill(evt.target), !!nodeOverride(evt.target))+`</div>`+
      `<div class="row sub">Click a model number above to colour that whole model.</div><div id="modelcolrow"></div>`;
    document.querySelectorAll(".tag.model").forEach(t=>t.onclick=()=>{ spotlight(t.dataset.m); showModelColour(t.dataset.m); });
    wireColourRow(document.getElementById("unitcolrow"), c=>setNodeColor(evt.target,c));
    const ps=document.getElementById("placesel"); if(ps) ps.onchange=()=>placeUnit(n.id, ps.value||null);
  });
  cy.on("tap",evt=>{ if(evt.target===cy){ cy.elements().removeClass("hi faded"); selectedSig=null; COLOR_TARGET=null; hideColPop(); clearDetail(); } });
  cy.on("pan zoom",hideColPop); cy.on("grab","node",hideColPop);
  cy.on("grabon","node",()=>pushHistory());   // snapshot before a drag (once, also when several selected nodes move), so undo reverts it
  document.addEventListener("keydown",e=>{ if(e.key==="Escape" && cy){ cy.nodes(":selected").unselect(); hideColPop(); cy.elements().removeClass("hi faded"); selectedSig=null; COLOR_TARGET=null; clearDetail(); } });
}

// --- resizable cell boxes: a corner grip (DOM overlay) sets the box's min-width/min-height; it grows right/down ---
const BOXPAD=36;   // must match the cell box "padding" style
function applyBoxSizes(){
  if(!cy) return;
  cy.nodes("[?is_cell]").forEach(b=>{ const z=BOXSIZE[b.id()];
    if(z) b.style({"min-width":z.w+"px","min-height":z.h+"px","min-width-bias-left":"0%","min-width-bias-right":"100%","min-height-bias-top":"0%","min-height-bias-bottom":"100%"});
    else b.removeStyle("min-width min-height min-width-bias-left min-width-bias-right min-height-bias-top min-height-bias-bottom"); });
}
// extracellular molecules (synaptic cleft pool + molecules drawn outside their cell) must never sit inside a cell box:
// push any that overlaps a box out across that box's nearest edge (user 2026-10-30). A few passes, in case a push
// lands a molecule in a neighbouring box.
function pushOutExtracellular(){
  if(!cy || !CELL_ON) return;
  const mols=cy.nodes("[?is_mol]").filter(m=>m.data("xzone") || m.data("outer"));
  if(!mols.length) return;
  const Bs=cy.nodes("[?is_cell]").filter(b=>!b.parent().length).map(b=>b.boundingBox({includeLabels:false}));
  let moved=cy.collection();
  const g=OUTGAP/2, hit=(M,dx,dy)=>Bs.find(B=>M.x1+dx<B.x2 && B.x1<M.x2+dx && M.y1+dy<B.y2 && B.y1<M.y2+dy);
  mols.forEach(m=>{
    const M=m.boundingBox({includeLabels:false}); if(!hit(M,0,0)) return;
    // try the 4 directions; in each, keep stepping past whatever box is in the way until clear of ALL boxes
    const tries=[[-1,0],[1,0],[0,-1],[0,1]].map(([sx,sy])=>{ let dx=0,dy=0;
      for(let k=0;k<30;k++){ const B=hit(M,dx,dy); if(!B) break;
        if(sx<0) dx=B.x1-M.x2-g; else if(sx>0) dx=B.x2-M.x1+g; else if(sy<0) dy=B.y1-M.y2-g; else dy=B.y2-M.y1+g; }
      return {dx,dy,ok:!hit(M,dx,dy)}; }).filter(t=>t.ok).sort((a,c)=>Math.abs(a.dx)+Math.abs(a.dy)-Math.abs(c.dx)-Math.abs(c.dy));
    if(tries.length){ const p=m.position(); m.position({x:p.x+tries[0].dx, y:p.y+tries[0].dy}); moved=moved.union(m); }
  });
  if(moved.length) orientIntra(moved.neighborhood("node[!is_mol][!is_cell]"));
}
// a unit with extracellular molecules: its own intracellular molecules (those touching only this unit) go on the
// OPPOSITE side of the unit: extracellular left -> intracellular right, above -> below, ... (user 2026-10-30)
function orientIntra(units){
  if(!cy || !CELL_ON) return;
  units.forEach(h=>{
    const ext=h.neighborhood("node[?is_mol]").filter(m=>m.data("outer")||m.data("xzone")); if(!ext.length) return;
    const ins=h.neighborhood("node[?is_mol]").filter(m=>m.degree()===1 && !m.data("outer") && !m.data("xzone")); if(!ins.length) return;
    const hp=h.position(), vx=ext.reduce((a,m)=>a+m.position().x,0)/ext.length-hp.x, vy=ext.reduce((a,m)=>a+m.position().y,0)/ext.length-hp.y;
    const hw=h.outerWidth()/2, hh=h.outerHeight()/2, ws=ins.map(m=>m.outerWidth()), hs=ins.map(m=>m.outerHeight());
    if(Math.abs(vx)>=Math.abs(vy)){   // extracellular left/right -> a column on the other side
      const side=vx>0?-1:1, colW=Math.max(...ws), rowH=Math.max(...hs)+SAT.GY, y0=-((ins.length-1)*rowH)/2;
      ins.forEach((m,i)=>{ const dx=side*(hw+SAT.EDGE+colW/2), dy=y0+i*rowH; m.position({x:hp.x+dx,y:hp.y+dy}); m.data("_host",h.id()); m.data("_dx",dx); m.data("_dy",dy); });
    } else {                          // extracellular above/below -> a row on the other side
      const side=vy>0?-1:1, rowH=Math.max(...hs), tot=ws.reduce((a,w)=>a+w,0)+SAT.GX*(ins.length-1); let x=-tot/2;
      ins.forEach((m,i)=>{ const dx=x+ws[i]/2, dy=side*(hh+SAT.EDGE+rowH/2); x+=ws[i]+SAT.GX; m.position({x:hp.x+dx,y:hp.y+dy}); m.data("_host",h.id()); m.data("_dx",dx); m.data("_dy",dy); });
    }
  });
}
function setupBoxGrips(){
  document.querySelectorAll(".boxgrip").forEach(g=>g.remove());
  if(!cy || !CELL_ON) return;
  const grips={};
  cy.nodes("[?is_cell]").forEach(b=>{
    const g=document.createElement("div"); g.className="boxgrip"; g.title="drag to resize this cell box (it can't be smaller than its contents)";
    document.body.appendChild(g); grips[b.id()]=g;
    g.addEventListener("mousedown",e=>{
      e.preventDefault(); e.stopPropagation();
      const box=cy.getElementById(b.id()), bb=box.boundingBox({includeLabels:false});
      document.body.style.userSelect="none"; document.body.style.cursor="nwse-resize";
      const move=ev=>{ const r=cy.container().getBoundingClientRect(), pan=cy.pan(), z=cy.zoom();
        const mx=(ev.clientX-r.left-pan.x)/z, my=(ev.clientY-r.top-pan.y)/z;
        BOXSIZE[b.id()]={w:Math.max(60,Math.round(mx-bb.x1-2*BOXPAD)), h:Math.max(60,Math.round(my-bb.y1-2*BOXPAD))};
        applyBoxSizes(); pushOutExtracellular(); };
      const up=()=>{ document.removeEventListener("mousemove",move); document.removeEventListener("mouseup",up);
        document.body.style.userSelect=""; document.body.style.cursor=""; };
      document.addEventListener("mousemove",move); document.addEventListener("mouseup",up);
    });
  });
  const place=()=>{ if(!cy) return; const r=cy.container().getBoundingClientRect();
    Object.entries(grips).forEach(([id,g])=>{ const b=cy.getElementById(id); if(!b.length){ g.style.display="none"; return; }
      const bb=b.renderedBoundingBox({includeLabels:false});
      const x=r.left+bb.x2-16, y=r.top+bb.y2-16;
      const inside = x>r.left && y>r.top && x<r.right-8 && y<r.bottom-8;
      g.style.display=inside?"":"none"; g.style.left=x+"px"; g.style.top=y+"px"; }); };
  cy.on("render", place);
  if(window._gripScroll) window.removeEventListener("scroll", window._gripScroll, true);
  window._gripScroll=place; window.addEventListener("scroll", place, true); place();
}

// a cell box that grew (unit placed in it, unit dragged near its edge) must not cover another box: push every
// overlapping top-level box (with its units, molecules, and the extracellular molecules drawn outside it) the
// shortest way out, and so on for any box that push lands on (user 2026-11-25). Labels count, with a gap.
function separateBoxes(grown){
  if(!cy || !CELL_ON || !grown || !grown.length) return;
  const top=b=>{ while(b.parent().length) b=b.parent(); return b; };
  const GAP=60, bbOf=b=>{ const r=b.boundingBox({includeLabels:true}); return {x1:r.x1-GAP/2,x2:r.x2+GAP/2,y1:r.y1-GAP/2,y2:r.y2+GAP/2}; };
  const over=(A,B)=>A.x1<B.x2 && B.x1<A.x2 && A.y1<B.y2 && B.y1<A.y2;
  const carry=b=>{ const kids=b.descendants("[!is_cell]");
    return kids.union(cy.nodes("[?outer]").filter(m=>!m.parent().length && m.neighborhood("node").some(u=>kids.contains(u)))); };
  const settled=[top(grown)], queue=[top(grown)];
  for(let guard=0; queue.length && guard<50; guard++){
    const a=queue.shift(), A=bbOf(a);
    cy.nodes("[?is_cell]").filter(b=>!b.parent().length && !settled.some(s=>s.same(b))).forEach(b=>{
      const B=bbOf(b); if(!over(A,B)) return;
      const opts=[[A.x2-B.x1,0],[A.x1-B.x2,0],[0,A.y2-B.y1],[0,A.y1-B.y2]].sort((u,v)=>Math.abs(u[0]+u[1])-Math.abs(v[0]+v[1]));
      const [dx,dy]=opts[0];
      carry(b).forEach(m=>{ const q=m.position(); m.position({x:q.x+dx, y:q.y+dy}); });
      settled.push(b); queue.push(b); });
  }
}
// put a no-CL unit (and its satellite molecules) into a cell box, or back out (boxId null). View only.
function placeUnit(nodeId, boxId){
  if(!cy) return;
  const n=cy.getElementById(nodeId); if(!n.length || !n.data("nocl")) return;
  const sig=n.data("sig"), sats=cy.nodes("[?is_mol]").filter(m=>m.data("_host")===nodeId);
  if(boxId) CELL_PLACE[sig]=boxId; else delete CELL_PLACE[sig];
  const target = boxId || null;
  const box = boxId ? cy.getElementById(boxId) : null;
  if(box && box.length){   // placed from the menu while far away: bring it into the box, under its contents (user 2026-11-25:
    const bb=box.boundingBox({includeLabels:false}), p=n.position();   // the box used to stretch out to the unit and cover other boxes)
    if(!(p.x>bb.x1 && p.x<bb.x2 && p.y>bb.y1 && p.y<bb.y2)){
      const kids=box.descendants("[!is_cell]").not(n).not(sats), kb=kids.length ? kids.boundingBox({includeLabels:false}) : bb;
      const nx=kb.x1+n.outerWidth()/2, ny=kb.y2+60+n.outerHeight()/2, dx=nx-p.x, dy=ny-p.y;
      n.position({x:nx, y:ny}); sats.forEach(m=>{ const q=m.position(); m.position({x:q.x+dx, y:q.y+dy}); });
    }
  }
  sats.forEach(m=>m.move({parent:target}));
  n.move({parent:target});
  cy.getElementById(nodeId).data("placed", !!boxId);
  if(box && box.length) separateBoxes(box);
  pushOutExtracellular();
  applyColors();
  const b=boxId?cy.getElementById(boxId):null;
  flash(boxId ? ("placed in "+(b&&b.data("extra")?"extracellular":(b?b.data("label"):boxId))+" (view only)") : "unit is loose again");
}

function spotlight(mid){
  cy.elements().removeClass("faded hi");
  cy.nodes("[!is_cell]").forEach(n=>{ if(!(n.data("models")||[]).includes(mid)) n.addClass("faded"); });
  cy.edges().forEach(e=>{ if(!(e.data("models")||[]).includes(mid)) e.addClass("faded"); });
}

// --- controls ---
function currentIds(){
  // robust: handle newline / comma / space separated AND ids pasted with no
  // separators (gomodel:AAAgomodel:BBB) by inserting a break before each prefix.
  let t = document.getElementById("ids").value.replace(/gomodel:/gi, "\ngomodel:");
  const seen = new Set(), out = [];
  t.split(/[\s,;]+/).map(normId).filter(Boolean).forEach(id=>{ if(!seen.has(id)){ seen.add(id); out.push(id); } });
  return out;
}
function currentMode(){ return document.querySelector('input[name=mode]:checked').value; }
function currentSrcMode(){ const r=document.querySelector('input[name=srcmode]:checked'); return r ? r.value : "dev"; }   // default production + dev: live first, dev if not on live (user 2026-11-25)
function isDevModel(id){ return !!(CACHE[id] && /^dev$/i.test(CACHE[id]._src||"")); }

// ---- LIVE fetch straight from Noctua's barista (anonymous read = what the Noctua UI uses to view a model).
//      NEVER the api.geneontology.org snapshot (it lags live). Live first, dev fallback. HTTP-only servers:
//      a page served over https cannot call them (browser mixed-content block) — detected below.
const LIVE_SERVERS = [
  ["live","http://barista.berkeleybop.org/api/minerva_public/m3Batch"],
  ["dev", "http://barista-dev.berkeleybop.org/api/minerva_public_dev/m3Batch"]
];
const _CAUSAL = {
  "RO:0002629": ["directly positively regulates","pos"],
  "RO:0002630": ["directly negatively regulates","neg"],
  "RO:0002304": ["causally upstream of, positive effect","pos"],
  "RO:0002305": ["causally upstream of, negative effect","neg"],
  "RO:0002413": ["provides input for","input"],
  "RO:0002411": ["causally upstream of","input"]
};
const _MOLPRED = { "RO:0002233":"has input","RO:0002234":"has output",
  "RO:0012001":"has small molecule activator","RO:0012002":"has small molecule inhibitor" };
const _INVMOL = { "RO:0012005":"has small molecule activator","RO:0012006":"has small molecule inhibitor" };
const _EB="RO:0002333",_PO="BFO:0000050",_OI="BFO:0000066",_HP="BFO:0000051",_MFROOT="GO:0003674";

function minervaToRecord(mid, m){
  if(!m || !Array.isArray(m.individuals) || !Array.isArray(m.facts))
    return {id:mid,title:mid,status:null,activities:[],error:"no model data"};
  const ind={}; for(const i of m.individuals) ind[i.id]=i;
  const clsOf=id=>{ const i=ind[id]; const t=(i&&i.type&&i.type[0])||{}; return {id:t.id||null,label:t.label||t.id||null}; };
  const roots=id=>new Set((((ind[id]||{})["root-type"])||[]).map(t=>t.id));
  const bySub={}; for(const f of m.facts){ (bySub[f.subject]=bySub[f.subject]||[]).push(f); }
  let title=mid,status=null;
  for(const a of (m.annotations||[])){ if(a.key==="title") title=a.value; if(a.key==="state") status=a.value; }
  const extraMols={};
  for(const f of m.facts){ const lbl=_INVMOL[f.property];
    if(lbl){ const c=clsOf(f.subject); (extraMols[f.object]=extraMols[f.object]||[]).push([lbl,c.label,c.id,f.subject]); } }
  const activities=[];
  for(const i of m.individuals){
    if(!roots(i.id).has(_MFROOT)) continue;
    const outs=bySub[i.id]||[];
    if(!outs.some(f=>f.property===_EB)) continue;
    const self=clsOf(i.id);
    let gp=null,gp_id=null,is_complex=false,complex_parts=[],complex_part_ids=[],bp=null,bp_id=null,cc=null,cc_id=null,cell=null,cell_id=null;
    const mols=[],edges=[],prot_io=[]; let bp_chain=[],cc_chain=[];
    const chain=(node,limit)=>{ const out=[],seen=new Set(); while(node&&out.length<(limit||5)){ const nx=(bySub[node]||[]).filter(f=>f.property===_PO).map(f=>f.object); if(!nx.length||seen.has(nx[0])) break; node=nx[0]; seen.add(node); const c=clsOf(node); out.push({id:c.id,label:c.label}); } return out; };
    for(const f of outs){ const p=f.property,tgt=f.object;
      if(p===_EB){ const c=clsOf(tgt); gp=c.label; gp_id=c.id;
        const parts=(bySub[tgt]||[]).filter(x=>x.property===_HP).map(x=>clsOf(x.object));
        parts.sort((a,b)=>a.id<b.id?-1:a.id>b.id?1:0);   // sort by ID so complex_parts[i] <-> complex_part_ids[i] stay aligned
        is_complex=parts.length>0; complex_parts=parts.map(x=>x.label); complex_part_ids=parts.map(x=>x.id); }
      else if(p===_PO && bp_id===null){ const c=clsOf(tgt); bp=c.label; bp_id=c.id; bp_chain=chain(tgt); }   // + the BPs this BP is part_of
      else if(p===_OI && cc_id===null){ const c=clsOf(tgt); cc=c.label; cc_id=c.id; cc_chain=chain(tgt);
        if(cc_chain.length){ cell=cc_chain[0].label; cell_id=cc_chain[0].id; } }   // the cell/anatomy the CC is part_of
      else if(_MOLPRED[p]){ const c=clsOf(tgt); if(/^CHEBI:/.test(c.id||"")) mols.push([_MOLPRED[p],c.label,c.id,tgt]); else if(p==="RO:0002233"||p==="RO:0002234") prot_io.push([_MOLPRED[p],c.label,c.id]); else mols.push([_MOLPRED[p],c.label,c.id,tgt]); }
      else if(_CAUSAL[p]){ const cz=_CAUSAL[p]; edges.push({cls:cz[1],label:cz[0],downstream:tgt}); }
    }
    for(const em of (extraMols[i.id]||[])) mols.push(em);
    for(const mm of mols){ const lf=(bySub[mm[3]]||[]).find(f=>f.property==="RO:0001025");   // molecule located in -> mols[i][4], [5]
      if(lf){ const c=clsOf(lf.object); mm[4]=c.id; mm[5]=c.label; } }
    activities.push({local_id:i.id,gp,gp_id,is_complex,complex_parts,complex_part_ids,
      mf:self.label,mf_id:self.id,bp,bp_id,cc,cc_id,cell,cell_id,bp_chain,cc_chain,prot_io,mols,edges});
  }
  return {id:mid,title,status,activities};
}

// GO's own HTTPS publication of PRODUCTION models (regenerated by the GO pipeline from live Noctua; per-file
// Last-Modified tells how fresh). Used when this page is HTTPS (browser blocks the HTTP barista call) — labelled
// "production mirror, as of <date>" so it is never mistaken for real-time. NOT the stale api.geneontology.org.
const MIRROR_BASE = "https://live-go-cam.geneontology.io/product/json/low-level/";
const HTTPS_BLOCKED = location.protocol==="https:";
async function fetchMirror(id, bare){
  const r=await fetch(MIRROR_BASE+bare+".json",{headers:{Accept:"application/json"}});
  if(!r.ok) throw new Error("mirror: HTTP "+r.status+(r.status===404||r.status===403?" (not a production model, or not yet published)":""));
  const m=await r.json();
  const rec=minervaToRecord(id,m);
  if(rec.error||!rec.activities.length) throw new Error("mirror: "+(rec.error||"no activities"));
  const lm=r.headers.get("last-modified"); rec._src="mirror"; rec._asof= lm ? new Date(lm).toISOString().slice(0,10) : "?";
  CACHE[id]=rec; return {id,ok:true};
}
async function fetchModel(id){
  const bare=id.replace(/^gomodel:/,"");
  const errs=[];
  if(HTTPS_BLOCKED){   // HTTPS page cannot call HTTP barista -> GO production mirror
    try{ return await fetchMirror(id,bare); }catch(e){ return {id,ok:false,error:(e&&e.message)||String(e)}; }
  }
  for(const [src,base] of LIVE_SERVERS){
    try{
      const q=JSON.stringify([{entity:"model",operation:"get",arguments:{"model-id":"gomodel:"+bare}}]);
      const r=await fetch(base+"?requests="+encodeURIComponent(q),{headers:{Accept:"application/json"}});
      if(!r.ok){ errs.push(src+": HTTP "+r.status); continue; }
      const d=await r.json();
      if(d["message-type"]!=="success" || !d.data || !Array.isArray(d.data.individuals)){ errs.push(src+": not found"); continue; }
      const rec=minervaToRecord(id,d.data);
      if(rec.error||!rec.activities.length){ errs.push(src+": "+(rec.error||"no activities")); continue; }
      rec._src=src;   // "live" = Noctua production server, "dev" = Noctua dev server (never a snapshot)
      CACHE[id]=rec; return {id,ok:true};
    }catch(e){ errs.push(src+": "+((e&&e.message)||String(e))); }
  }
  try{ return await fetchMirror(id,bare); }catch(e){ errs.push((e&&e.message)||String(e)); }   // last resort on http/file pages
  return {id,ok:false,error:errs.join("; ")};
}

// ---- QC: flag same-protein units that fail to merge only because one GO term
//      is a parent/child (ancestor/descendant) of the other ----
const _ancCache={};   // GO id -> Set(ancestor ids), memoised
async function ancestorsOf(ids){
  const need=ids.filter(id=>/^GO:/.test(id) && !(id in _ancCache));
  for(let i=0;i<need.length;i+=20){
    const chunk=need.slice(i,i+20);
    try{
      const r=await fetch("https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/"+chunk.join(",")+"/ancestors?relations=is_a,part_of",{headers:{Accept:"application/json"}});
      if(r.ok){ const d=await r.json(); (d.results||[]).forEach(t=>{ _ancCache[t.id]=new Set(t.ancestors||[]); }); }
    }catch(e){}
    chunk.forEach(id=>{ if(!(id in _ancCache)) _ancCache[id]=new Set(); });  // don't refetch failures
  }
}
function subsumption(t1,t2){   // null, or which term is the more specific one
  if(!t1||!t2||t1===t2) return null;
  const a1=_ancCache[t1]||new Set(), a2=_ancCache[t2]||new Set();
  if(a2.has(t1)) return {general:t1, specific:t2};
  if(a1.has(t2)) return {general:t2, specific:t1};
  return null;
}
function qcHighlight(ids){   // focus + halo the two mismatched units in the graph
  if(!cy) return;
  let coll=cy.collection();
  ids.forEach(id=>{ const n=cy.getElementById(id); if(n&&n.length) coll=coll.union(n); });
  if(!coll.length) return;
  coll.style({"display":"element","overlay-color":"#e0a800","overlay-opacity":0.35,"overlay-padding":12});
  cy.animate({fit:{eles:coll, padding:90}},{duration:350});
  setTimeout(function(){ try{ coll.removeStyle("display overlay-color overlay-opacity overlay-padding"); }catch(e){} },4000);
}
async function runQC(nodes, loaded){
  const box=document.getElementById("qc"), cnt=document.getElementById("nqc");
  if(!box) return;
  try{
    const devs=(loaded||[]).filter(id=>CACHE[id] && /^dev$/i.test(CACHE[id]._src||""));
    const mirs=(loaded||[]).filter(id=>CACHE[id] && CACHE[id]._src==="mirror");
    let caveat='';
    if(devs.length) caveat+='<div class="sub" style="margin-bottom:6px;color:#a15c00">&#9432; '+devs.length+' of '+(loaded||[]).length+' model(s) read from the Noctua DEV server (not on live).</div>';
    if(mirs.length) caveat+='<div class="sub" style="margin-bottom:6px;color:#a15c00">&#9432; '+mirs.length+' of '+(loaded||[]).length+' model(s) from GO\'s production mirror (as of '+[...new Set(mirs.map(id=>CACHE[id]._asof))].join(", ")+') — not real-time; verify any flag against live Noctua.</div>';
    // units with no cell type: no CL in the CC part_of chain, and the CC is not extracellular (user rule 2026-10-26)
    const nocl=nodes.filter(n=>!n.is_mol && !n.cell_key);
    const ncnames=ms=>ms.map(m=>(CACHE[m]&&CACHE[m].title)||m).join(", ");
    caveat += nocl.map(n=>'<div class="qcitem" data-a="'+n.id+'" data-b="'+n.id+'" title="click to highlight the unit in the graph" '
      +'style="cursor:pointer;border-left:3px solid #e67e22;background:#fff3e6;padding:6px 8px;margin:6px 0;border-radius:4px;color:#333;line-height:1.35">'
      +'&#9888; <b>'+(n.gp||n.gp_id)+'</b> &mdash; no cell type (CL) in the CC chain:<br>'
      +'CC '+(n.cc?('&ldquo;'+n.cc+'&rdquo; <span class="mono">'+(n.cc_id||"")+'</span>'):'(none)')
      +((n.cc_chain||[]).length?' &rarr; '+n.cc_chain.map(c=>c.label+' <span class="mono">'+(c.id||"")+'</span>').join(' &rarr; '):'')+'<br>'
      +'<span class="sub">models &mdash; '+ncnames(n.models||[])+'</span><span class="sub"> &middot; click to highlight</span></div>').join("");
    const N0=nocl.length;
    const wireQC=()=>box.querySelectorAll(".qcitem").forEach(el=>{
      el.addEventListener("click",e=>{ if(e.target.tagName==="A") return; qcHighlight([el.dataset.a, el.dataset.b]); }); });
    box.innerHTML="checking annotations…"; cnt.textContent="";
    const asp={MF:["mf_id","mf"], BP:["bp_id","bp"], CC:["cc_id","cc"]};
    const byGp={};
    nodes.forEach(n=>{ if(n.gp_id){ const k=canonId(n.gp_id); (byGp[k]=byGp[k]||[]).push(n); } });
    const pairs=[];
    Object.values(byGp).forEach(g=>{
      for(let i=0;i<g.length;i++) for(let j=i+1;j<g.length;j++){
        const A=g[i], B=g[j], d=[];
        if(MERGE_ON.mf && A.mf_id!==B.mf_id) d.push("MF");
        if(MERGE_ON.bp && A.bp_key!==B.bp_key) d.push("BP");   // direct BP or its part_of chain
        if(MERGE_ON.cc && A.cc_key!==B.cc_key) d.push("CC");   // direct CC or its part_of chain
        // composition compared on subunit IDs (not labels): "CNGB1" Q14028 vs Q14028-1 look identical by label but never merge
        const idsA=(A.complex_part_ids||[]).map(canonId).sort(), idsB=(B.complex_part_ids||[]).map(canonId).sort();   // canonId is identity when the isoform toggle is off
        const cxDiff = A.is_complex!==B.is_complex || idsA.join()!==idsB.join();
        if(d.length===1 && !cxDiff) pairs.push({A,B,aspect:d[0]});
        else if(d.length===2 && !cxDiff) pairs.push({A,B,aspect:"TWO", aspects:d});   // differs in two aspects (user rule 2026-10-26)
        else if(d.length===0 && cxDiff) pairs.push({A,B,aspect:"CX", idsA, idsB});   // GO terms all agree; only the complex membership/IDs differ
      }
    });
    if(!pairs.length){ box.innerHTML=caveat+"No same-protein near-miss pairs to check."; cnt.textContent="("+N0+")"; wireQC(); return; }
    const terms=new Set();
    pairs.filter(p=>p.aspect!=="CX").forEach(p=>{ (p.aspects||[p.aspect]).forEach(a=>{ const idk=asp[a][0]; terms.add(p.A[idk]); terms.add(p.B[idk]); }); });
    await ancestorsOf([...terms]);
    const hits=[];
    const names=ms=>ms.map(m=>(CACHE[m]&&CACHE[m].title)||m).join(", ");
    const canon=id=>String(id||"").replace(/-\d+$/,"");   // always strip, to recognise the isoform-only case when the toggle is off
    pairs.forEach(p=>{
      const A=p.A, B=p.B;
      if(p.aspect==="CX"){
        const onlyA=p.idsA.filter(x=>!p.idsB.includes(x)), onlyB=p.idsB.filter(x=>!p.idsA.includes(x));
        const isoOnly = p.idsA.map(canon).join()===p.idsB.map(canon).join();   // same proteins, isoform vs canonical accession
        const lab=(n,ids)=>ids.map(id=>{ const i=(n.complex_part_ids||[]).findIndex(x=>canonId(x)===id); return ((n.complex_parts||[])[i]||"?")+" "+((n.complex_part_ids||[])[i]||id); }).join(", ")||"(none)";
        hits.push({kind:"complex", iso:isoOnly, gp:A.gp||A.gp_id,
          x:{term:lab(A,onlyA), models:names(A.models), node:A.id},
          y:{term:lab(B,onlyB), models:names(B.models), node:B.id}});
        return;
      }
      if(p.aspect==="TWO"){   // one row per differing aspect, each tagged parent/child or not
        hits.push({kind:"two", gp:A.gp||A.gp_id, nodeA:A.id, nodeB:B.id, modelsA:names(A.models), modelsB:names(B.models),
          rows:p.aspects.map(a=>{ const [idk,lblk]=asp[a];
            if(a==="BP" && A.bp_id===B.bp_id) return {aspect:a, rel:"same BP term, different part_of chain",
              a:{id:A.bp_id, term:bpChainStr(A)}, b:{id:B.bp_id, term:bpChainStr(B)}};
            if(a==="CC" && A.cc_id===B.cc_id) return {aspect:a, rel:"same CC term, different part_of chain",
              a:{id:A.cc_id, term:ccChainStr(A)}, b:{id:B.cc_id, term:ccChainStr(B)}};
            const s=subsumption(A[idk], B[idk]);
            return {aspect:a, rel:s?(s.general===A[idk]?"first is parent of second":"first is child of second"):"not parent/child",
                    a:{id:A[idk], term:A[lblk]||A[idk]}, b:{id:B[idk], term:B[lblk]||B[idk]}}; })});
        return;
      }
      if((p.aspect==="BP" && A.bp_id===B.bp_id) || (p.aspect==="CC" && A.cc_id===B.cc_id)){   // same term, but its part_of chain differs
        const cs=p.aspect==="BP"?bpChainStr:ccChainStr;
        hits.push({kind:"chain", aspect:p.aspect, gp:A.gp||A.gp_id, x:{chain:cs(A), models:names(A.models), node:A.id}, y:{chain:cs(B), models:names(B.models), node:B.id}});
        return;
      }
      const [idk,lblk]=asp[p.aspect];
      const s=subsumption(A[idk], B[idk]);   // null if the two terms are not parent/child
      if(s){
        const specNode=(A[idk]===s.specific)?A:B, genNode=(A[idk]===s.specific)?B:A;
        hits.push({kind:"precision", aspect:p.aspect, gp:A.gp||A.gp_id,
          x:{id:s.general,  term:genNode[lblk]||s.general,  models:names(genNode.models), node:genNode.id},
          y:{id:s.specific, term:specNode[lblk]||s.specific, models:names(specNode.models), node:specNode.id}});
      } else {
        hits.push({kind:"different", aspect:p.aspect, gp:A.gp||A.gp_id,
          x:{id:A[idk], term:A[lblk]||A[idk], models:names(A.models), node:A.id},
          y:{id:B[idk], term:B[lblk]||B[idk], models:names(B.models), node:B.id}});
      }
    });
    cnt.textContent="("+(hits.length+N0)+")";
    if(!hits.length){ box.innerHTML=caveat+"No same-protein annotation mismatches found (checked "+pairs.length+" pair(s))."; wireQC(); return; }
    const q=id=>'<a href="https://www.ebi.ac.uk/QuickGO/term/'+id+'" target="_blank" rel="noopener">'+id+'</a>';
    box.innerHTML = caveat + hits.map(h=>{
      if(h.kind==="complex"){
        const iso=h.iso, border=iso?"#e0a800":"#c0392b", bg=iso?"#fff8e6":"#fdecea";
        const head=iso ? "complex subunit uses isoform vs canonical UniProt accession (same protein)"
                       : "complex composition differs (MF/BP/CC all agree)";
        return '<div class="qcitem" data-a="'+h.x.node+'" data-b="'+h.y.node+'" title="click to highlight both units in the graph" '
          +'style="cursor:pointer;border-left:3px solid '+border+';background:'+bg+';padding:6px 8px;margin:6px 0;border-radius:4px;color:#333;line-height:1.35">'
          +'&#9888; <b>'+h.gp+'</b> &mdash; '+head+' (units did not merge):<br>'
          +'only in first: '+h.x.term+'<br>only in second: '+h.y.term+'<br>'
          +'<span class="sub">models &mdash; '+h.x.models+'  |  '+h.y.models+'</span>'
          +'<span class="sub"> &middot; click to highlight</span>'
          +'</div>';
      }
      if(h.kind==="chain"){
        return '<div class="qcitem" data-a="'+h.x.node+'" data-b="'+h.y.node+'" title="click to highlight both units in the graph" '
          +'style="cursor:pointer;border-left:3px solid #c0392b;background:#fdecea;padding:6px 8px;margin:6px 0;border-radius:4px;color:#333;line-height:1.35">'
          +'&#9888; <b>'+h.gp+'</b> &mdash; '+h.aspect+' part_of chain differs (units did not merge):<br>'
          +h.x.chain+'<br>vs '+h.y.chain+'<br>'
          +'<span class="sub">models &mdash; '+h.x.models+'  |  '+h.y.models+'</span><span class="sub"> &middot; click to highlight</span></div>';
      }
      if(h.kind==="two"){
        const qq=id=>/^GO:/.test(id||"")?q(id):(id||"(none)");
        return '<div class="qcitem" data-a="'+h.nodeA+'" data-b="'+h.nodeB+'" title="click to highlight both units in the graph" '
          +'style="cursor:pointer;border-left:3px solid #6c5ce7;background:#f1effd;padding:6px 8px;margin:6px 0;border-radius:4px;color:#333;line-height:1.35">'
          +'&#9888; <b>'+h.gp+'</b> &mdash; differs in two aspects: '+h.rows.map(r=>r.aspect).join(" + ")+' (units did not merge):<br>'
          +h.rows.map(r=>'<b>'+r.aspect+'</b> <span class="sub">('+r.rel+')</span>: '+qq(r.a.id)+' &ldquo;'+r.a.term+'&rdquo; vs '+qq(r.b.id)+' &ldquo;'+r.b.term+'&rdquo;').join("<br>")+'<br>'
          +'<span class="sub">models &mdash; first: '+h.modelsA+'  |  second: '+h.modelsB+'</span>'
          +'<span class="sub"> &middot; click to highlight</span>'
          +'</div>';
      }
      const prec=h.kind==="precision";
      const border=prec?"#e0a800":"#c0392b", bg=prec?"#fff8e6":"#fdecea";
      const head=prec ? (h.aspect+" precision mismatch (parent/child)")
                      : (h.aspect+" differs &mdash; not parent/child; check for inconsistency/error");
      const xl=prec?"general: ":"", yl=prec?"specific: ":"vs ";
      return '<div class="qcitem" data-a="'+h.x.node+'" data-b="'+h.y.node+'" title="click to highlight both units in the graph" '
        +'style="cursor:pointer;border-left:3px solid '+border+';background:'+bg+';padding:6px 8px;margin:6px 0;border-radius:4px;color:#333;line-height:1.35">'
        +'&#9888; <b>'+h.gp+'</b> &mdash; '+head+' (units did not merge):<br>'
        +xl+q(h.x.id)+' &ldquo;'+h.x.term+'&rdquo;<br>'
        +yl+q(h.y.id)+' &ldquo;'+h.y.term+'&rdquo;<br>'
        +'<span class="sub">models &mdash; '+h.x.models+'  |  '+h.y.models+'</span>'
        +'<span class="sub"> &middot; click to highlight</span>'
        +'</div>';
    }).join("");
    box.querySelectorAll(".qcitem").forEach(el=>{
      el.addEventListener("click",e=>{ if(e.target.tagName==="A") return; qcHighlight([el.dataset.a, el.dataset.b]); });
    });
  }catch(e){ box.innerHTML="QC error: "+((e&&e.message)||e); }
}

async function doBuild(){
  try{
    document.getElementById("err").style.display="none";
    { const _q=document.getElementById("qc"), _n=document.getElementById("nqc");   // clear stale QC from the previous run
      if(_q) _q.innerHTML="Build a graph to run QC checks."; if(_n) _n.textContent=""; }
    const nl=document.getElementById("notloaded");
    const ids=currentIds();
    if(!ids.length){ nl.innerHTML=""; renderCacheList([]); { const _c=document.getElementById("cats"); if(_c) _c.style.display="none"; } if(cy){ cy.elements().remove(); } return; }
    const need=ids.filter(id=>!CACHE[id]);
    if(need.length){
      nl.style.color="#555"; nl.innerHTML="Fetching "+need.length+" model(s) from "+(HTTPS_BLOCKED?"GO's production mirror":"live Noctua")+"…";
      const res=await Promise.all(need.map(fetchModel));
      const bad=res.filter(r=>!r.ok);
      nl.style.color=""; nl.innerHTML = bad.length
        ? "Could not load: "+bad.map(b=>b.id.replace(/^gomodel:/,"")+" ("+b.error+")").join("; ") : "";
    } else { nl.innerHTML=""; }
    const SRC=currentSrcMode();
    const devOnly=ids.filter(id=>isDevModel(id));
    const loaded=ids.filter(id=>CACHE[id] && (SRC==="dev" || !isDevModel(id)));
    if(SRC==="prod" && devOnly.length){ nl.innerHTML += (nl.innerHTML?"<br>":"") + '<span class="sub" style="color:#a15c00">&#9432; '+devOnly.length+' dev-only model(s) left out (choose "production + dev" to include): '+devOnly.map(id=>id.replace(/^gomodel:/,"")).join(", ")+'</span>'; }
    if(SRC==="dev" && HTTPS_BLOCKED){ const miss=ids.filter(id=>!CACHE[id]); if(miss.length) nl.innerHTML += (nl.innerHTML?"<br>":"") + '<span class="sub">&#9432; Dev models can\'t be fetched from an https page (the dev server has no https). To use a dev model, add its ID to my-models.txt and run refresh.sh on the hub; it is then baked into the app.</span>'; }
    const snap=loaded.filter(id=>isDevModel(id));
    if(snap.length){ nl.innerHTML += (nl.innerHTML?"<br>":"") + '<span class="sub">&#9432; '+snap.length+' model(s) read from the Noctua DEV server (not on live): '+snap.map(id=>id.replace(/^gomodel:/,"")).join(", ")+'</span>'; }
    const mirs=loaded.filter(id=>CACHE[id] && CACHE[id]._src==="mirror");
    if(mirs.length){ nl.innerHTML += (nl.innerHTML?"<br>":"") + '<span class="sub">&#9432; '+mirs.length+' model(s) fetched from GO\'s production mirror (live-go-cam, as of '+[...new Set(mirs.map(id=>CACHE[id]._asof))].join(", ")+'), because live barista is HTTP-only and this page is HTTPS.</span>'; }
    if(!loaded.length){ showErr("None of the "+ids.length+" ID(s) entered could be loaded."); return; }
    if(typeof cytoscape==="undefined"){ showErr("Cytoscape not loaded; cannot draw."); return; }
    const showMols=true;   // molecules are always shown (checkbox removed at user's request 2026-09-22)
    MERGE_ON={ mf:document.getElementById("mON").checked, bp:document.getElementById("bON").checked, cc:document.getElementById("cON").checked };
    CELL_ON = currentCellMode()==="cell";
    { const gos=new Set(), cls=new Set();   // ancestry for "extracellular" (QuickGO) and for nesting cell boxes (OLS); memoised
      loaded.forEach(id=>CACHE[id].activities.forEach(a=>{ if(a.cc_id) gos.add(a.cc_id); (a.mols||[]).forEach(x=>{ if(/^GO:/.test(x[4]||"")) gos.add(x[4]); });
        (a.cc_chain||[]).forEach(c=>{ if(/^GO:/.test(c.id||"")) gos.add(c.id); else if(/^CL:/.test(c.id||"")) cls.add(c.id); }); }));
      await Promise.all([ancestorsOf([...gos]), CELL_ON ? clAncestorsOf([...cls]) : Promise.resolve()]);
      PRESENT_CL={}; loaded.forEach(id=>CACHE[id].activities.forEach(a=>{ const c=cellTypeOf(a); if(c) PRESENT_CL[c.id]=c.label; })); }
    Object.keys(MCOL).forEach(k=>delete MCOL[k]);   // recolour from scratch: the n loaded models get the n most distinct colours
    loaded.slice().sort().forEach((m,i)=>MCOL[m]=palette[i%palette.length]);
    const g=buildGraph(loaded,currentMode(),showMols);
    render(g,loaded);
    renderCacheList(loaded);
    { const _c=document.getElementById("cats"); if(_c) _c.style.display=""; }
    if(cy){ cy.resize(); cy.fit(null,40); }  // guard against zero-size container at init
    runQC(g.nodes, loaded);   // QC on all loaded models (dev-server ones get a note)
  }catch(e){ showErr((e&&e.stack)||String(e)); }
}
window.addEventListener("resize",()=>{ if(cy) cy.resize(); });

document.getElementById("build").onclick=doBuild;
document.querySelectorAll('input[name=mode]').forEach(r=>r.onchange=doBuild);
document.querySelectorAll('input[name=srcmode]').forEach(r=>r.onchange=doBuild);
document.querySelectorAll('input[name=cellmode]').forEach(r=>r.onchange=doBuild);
["mON","bON","cON"].forEach(id=>{ const e=document.getElementById(id); if(e) e.addEventListener("change",doBuild); });
document.getElementById("fit").onclick=()=>cy&&cy.fit(null,40);
function zoomByF(f){ if(!cy) return; const z=Math.max(0.05,Math.min(4,cy.zoom()*f)); cy.zoom({level:z,renderedPosition:{x:cy.width()/2,y:cy.height()/2}}); }
document.getElementById("zoomin").onclick=()=>zoomByF(1.2);
document.getElementById("zoomout").onclick=()=>zoomByF(1/1.2);
// after dagre lays out the whole graph, spread the disconnected clusters into
// side-by-side, top-aligned columns so independent models don't overlap
function tileComponents(){
  if(!cy) return;
  const comps=cy.elements().components();
  comps.sort((a,b)=>b.nodes().length-a.nodes().length);
  const gap=120; let x=0;
  comps.forEach(comp=>{
    const nodes=comp.nodes(); if(!nodes.length) return;
    const bb=nodes.boundingBox();
    const dx=x-bb.x1, dy=-bb.y1;
    nodes.forEach(n=>{ const p=n.position(); n.position({x:p.x+dx, y:p.y+dy}); });
    x += bb.w + gap;
  });
  cy.fit(null,40);
}
// Compact layout (2026-09-22): molecules attached to ONE activity only (degree 1 — a channel's
// ions, a receptor's ligand…) are NOT given their own dagre slots (that spread activity units far
// apart); they are placed as "satellites" beside their activity box, alternating right/left and
// stacking. Shared molecules (degree >= 2, e.g. cGMP between cyclase and channel) stay in dagre
// as true connectors. Satellites follow their box when it is dragged.
const SAT={GX:18,GY:12,EDGE:70};   // GX/GY: gaps between stacked satellites; EDGE: unit -> its own molecule (was 18; longer arrows, user 2026-11-26)
// satellites: reserve room beside each host box for dagre (satPrep), then place them beside it (satPlace)
function satPrep(){
  const sat=cy.nodes("[?is_mol]").filter(m=>m.degree()===1 && !m.data("xzone") && !m.data("outer"));   // xzone molecules sit between the cells instead
  const hosts={};
  sat.forEach(m=>{ const a=m.neighborhood("node")[0]; if(a) (hosts[a.id()]=hosts[a.id()]||[]).push(m); });
  // side rule (transport reads left->right): INPUTS / activators / inhibitors (edge molecule->activity) on the LEFT,
  // OUTPUTS (edge activity->molecule) on the RIGHT — e.g. a channel's Ca/Na "in" left, Ca/Na "out" right.
  const sideOf=m=>{ const e=m.connectedEdges()[0]; return (e && e.source().id()===m.id()) ? -1 : 1; };
  const geom={};   // measured (rendered) sizes, so placement adapts to real label widths/heights
  Object.entries(hosts).forEach(([id,ms])=>{ const a=cy.getElementById(id);
    const perSide=Math.max(ms.filter(m=>sideOf(m)<0).length, ms.filter(m=>sideOf(m)>0).length);
    const hostW=a.outerWidth(), hostH=a.outerHeight();
    const colW=Math.max(...ms.map(m=>m.outerWidth())), rowH=Math.max(...ms.map(m=>m.outerHeight()))+SAT.GY;
    geom[id]={hostW,colW,rowH,perSide};
    const extraW=2*(colW+SAT.EDGE), needH=perSide*rowH-SAT.GY;   // symmetric: cytoscape centres the widened box, so reserve a full column on BOTH sides even for k=1
    a.style({width:a.width()+extraW, height:Math.max(a.height(), a.height()+(needH-hostH))}); });   // reserve room beside the box for dagre
  return {sat, hosts, geom, sideOf};
}
function satPlace(S, onlyIds){
  Object.entries(S.hosts).forEach(([id,ms])=>{ if(onlyIds && !onlyIds.has(id)) return;
    const a=cy.getElementById(id), p=a.position(), G=S.geom[id];
    const left=ms.filter(m=>S.sideOf(m)<0), right=ms.filter(m=>S.sideOf(m)>0);
    const place=(list,side)=>{ const y0=-((list.length-1)*G.rowH)/2; list.forEach((m,row)=>{
      const dx=side*(G.hostW/2+SAT.EDGE+G.colW/2), dy=y0+row*G.rowH;
      m.position({x:p.x+dx, y:p.y+dy}); m.data("_host",id); m.data("_dx",dx); m.data("_dy",dy); }); };
    place(left,-1); place(right,1);
    a.removeStyle("width"); a.removeStyle("height"); });
}
// ---- layout quality (user 2026-10-26): fewest edge crossings, then units of the same model close together.
//      Several dagre runs are tried and the best-scoring one is kept. ----
function segCross(a,b,c,d){   // proper intersection of segments ab and cd
  const o=(p,q,r)=>Math.sign((q.x-p.x)*(r.y-p.y)-(q.y-p.y)*(r.x-p.x));
  return o(a,b,c)*o(a,b,d)<0 && o(c,d,a)*o(c,d,b)<0;
}
function countCrossings(edges){
  const sg=edges.map(e=>[e.source().position(),e.target().position(),e.source().id(),e.target().id()]);
  let n=0;
  for(let i=0;i<sg.length;i++) for(let j=i+1;j<sg.length;j++){ const A=sg[i],B=sg[j];
    if(A[2]===B[2]||A[2]===B[3]||A[3]===B[2]||A[3]===B[3]) continue;   // edges sharing a unit don't "cross"
    if(segCross(A[0],A[1],B[0],B[1])) n++; }
  return n;
}
function modelSpread(nodes){   // mean distance of units to their model's centroid, in ~box widths
  const by={}; nodes.forEach(n=>(n.data("models")||[]).forEach(m=>(by[m]=by[m]||[]).push(n.position())));
  let s=0,k=0; Object.values(by).forEach(ps=>{ if(ps.length<2) return;
    const mx=ps.reduce((a,p)=>a+p.x,0)/ps.length, my=ps.reduce((a,p)=>a+p.y,0)/ps.length;
    ps.forEach(p=>{ s+=Math.hypot(p.x-mx,p.y-my); k++; }); });
  return k ? s/k/250 : 0;
}
const layoutScore=(nodes,edges)=>countCrossings(edges)*2 + modelSpread(nodes);
let LAST_LAYOUT_INFO="";
function bestDagre(nodes, edges){   // run dagre a few ways on nodes+edges, keep the positions with the lowest score
  if(!nodes.length) return;
  const pm=n=>((n.data("models")||[]).slice().sort()[0])||"";
  const key=e=>e.isNode() ? pm(e)+"|"+e.id() : pm(e.source())+"|"+pm(e.target())+"|"+e.id();
  const byModel=(a,b)=>key(a).localeCompare(key(b));
  const variants=[{name:"plain"},{name:"by model",sort:byModel},{name:"by model, reversed",sort:(a,b)=>-byModel(a,b)}];   // a "model glue" variant (invisible minLen-0 edges) was tried and dropped: dagre hangs on it
  let best=null;
  variants.forEach(v=>{
    let glue=cy.collection();
    try{
      if(v.glue){   // invisible, weak edges chaining the units of each model, removed right after
        const by={}; nodes.forEach(n=>{ const m=pm(n); if(m) (by[m]=by[m]||[]).push(n.id()); });
        const add=[]; Object.values(by).forEach(ids=>{ for(let i=1;i<ids.length;i++) add.push({group:"edges",data:{id:"glue_"+ids[i-1]+"_"+ids[i],source:ids[i-1],target:ids[i],glue:true}}); });
        glue=cy.add(add);
      }
      const opts={name:"dagre",rankDir:"TB",nodeSep:45,rankSep:60,fit:false,animate:false,
        minLen:e=>e.data("glue")?0:1, edgeWeight:e=>e.data("glue")?0.3:1};
      if(v.sort) opts.sort=v.sort;
      nodes.union(edges).union(glue).layout(opts).run();   // animate:false -> synchronous
    }catch(err){ glue.remove(); return; }
    glue.remove();
    const sc=layoutScore(nodes,edges);
    if(!best || sc<best.sc-1e-9){ const pos={}; nodes.forEach(n=>{ pos[n.id()]={...n.position()}; }); best={sc,pos,name:v.name,x:countCrossings(edges)}; }
  });
  if(best){ nodes.forEach(n=>{ const p=best.pos[n.id()]; if(p) n.position(p); }); LAST_LAYOUT_INFO=best.name+": "+best.x+" crossing(s)"; }
  return best;
}
function autoLayout(){
  if(!cy) return;
  const S=satPrep();
  const core=cy.elements("[!is_cell]").not(S.sat).not(S.sat.connectedEdges());
  bestDagre(core.nodes(), core.edges());
  satPlace(S); tileComponents();
}
// "by cell type" layout: dagre inside each cell box separately, then the boxes in columns by signalling order
// (cells that send causal arrows to other cells first); extracellular column between senders and receivers;
// a subclass box sits under its parent's own units; loose (no-CL) units in a row underneath.
const CELLGAP={COL:260, ROW:170, NEST:110, LOOSE:220};
const OUTGAP=34;   // distance between a cell box edge and the extracellular molecules drawn just outside it
// extracellular molecules (not synaptic cleft): just outside the box of the units they touch, on the side nearer to
// those units, at their height; stacked so they don't overlap
function placeOuter(){
  if(!cy) return;
  const used={};   // box id + side -> bottom of the last molecule placed there
  const items=cy.nodes("[?outer]").map(m=>{ const nb=m.neighborhood("node[!is_mol]");
    const my=nb.length ? nb.reduce((a,u)=>a+u.position().y,0)/nb.length : m.position().y;
    const mx=nb.length ? nb.reduce((a,u)=>a+u.position().x,0)/nb.length : m.position().x;
    let box=nb.length ? nb[0].parent() : cy.collection(); while(box.length && box.parent().length) box=box.parent();
    return {m,mx,my,box}; }).sort((a,b)=>a.my-b.my);
  items.forEach(({m,mx,my,box})=>{
    const w=m.outerWidth(), h=m.outerHeight();
    let x, key;
    if(box.length){ const bb=box.boundingBox({includeLabels:false}); const side = mx<(bb.x1+bb.x2)/2 ? -1 : 1;
      x = side<0 ? bb.x1-OUTGAP-w/2 : bb.x2+OUTGAP+w/2; key=box.id()+(side<0?"L":"R"); }
    else { x=mx+260; key="loose"; }
    const y=Math.max(my, (used[key]===undefined ? -Infinity : used[key]+10+h/2));
    m.position({x,y}); used[key]=y+h/2; });
}
// synaptic-cleft molecules linking units in two different cells: at the midpoint of their units (not in a row of their own),
// nudged apart so they don't overlap each other; pushOutExtracellular() then moves any that lands in a box to its edge
function placeBetween(){
  if(!cy) return;
  const ms=cy.nodes("[?is_mol][?xzone]").map(m=>{ const nb=m.neighborhood("node[!is_mol][!is_cell]");
    return {m, x:nb.length?nb.reduce((a,u)=>a+u.position().x,0)/nb.length:m.position().x, y:nb.length?nb.reduce((a,u)=>a+u.position().y,0)/nb.length:m.position().y}; })
    .sort((a,b)=>a.y-b.y);
  const done=[];
  ms.forEach(o=>{ const w=o.m.outerWidth(), h=o.m.outerHeight(); let y=o.y;
    for(let k=0;k<50;k++){ const hit=done.find(d=>Math.abs(d.x-o.x)<(d.w+w)/2+10 && Math.abs(d.y-y)<(d.h+h)/2+10); if(!hit) break; y=hit.y+(hit.h+h)/2+10; }
    o.m.position({x:o.x, y}); done.push({x:o.x, y, w, h}); });
}
function cellLayout(){
  if(!cy) return;
  const S=satPrep();
  const units=cy.nodes("[!is_cell]").not(S.sat).filter(n=>!n.data("outer") && !(n.data("is_mol") && n.data("xzone")));   // cleft molecules between two cells: placed by placeBetween()
  const outer=cy.nodes("[?outer]"), outerW=outer.length ? Math.max(...outer.map(m=>m.outerWidth())) : 0;
  const COLGAP=CELLGAP.COL + (outer.length ? 2*(outerW+OUTGAP) : 0);   // room for molecules drawn outside the boxes
  const groups={};   // box id ("" = loose) -> collection of non-satellite nodes directly in that box
  units.forEach(n=>{ const k=n.parent().length ? n.parent().id() : (n.data("xzone") ? EXTRA_ID : ""); groups[k]=(groups[k]||cy.collection()).union(n); });
  const block={};    // box id -> {eles, w, h} with eles translated so the block's top-left is (0,0)
  const shift=(eles,dx,dy)=>eles.forEach(n=>{ const p=n.position(); n.position({x:p.x+dx, y:p.y+dy}); });
  Object.entries(groups).forEach(([k,g])=>{
    const inner=g.connectedEdges().filter(e=>g.contains(e.source()) && g.contains(e.target()));
    bestDagre(g, inner);
    satPlace(S, new Set(g.map(n=>n.id())));
    const bb=g.union(S.sat.filter(m=>g.contains(cy.getElementById(m.data("_host"))))).boundingBox({includeLabels:false});   // size incl. satellites
    shift(g,-bb.x1,-bb.y1); block[k]={eles:g, w:bb.w, h:bb.h, ox:0, oy:0};   // only units move with the block; satellites follow their host (resat)
  });
  // top-level box of a node (climb nested boxes)
  const topOf=n=>{ let p=n.parent(); if(!p.length) return ""; while(p.parent().length) p=p.parent(); return p.id(); };
  const boxes=cy.nodes("[?is_cell]"), tops=boxes.filter(b=>!b.parent().length);
  const cellTops=tops.map(b=>b.id()), extra=block[EXTRA_ID] ? [EXTRA_ID] : [];   // extracellular = unboxed block between the cells
  // rank cell boxes by inter-cell edges (longest path from the senders); cycles are cut after n rounds
  const succ={}; cellTops.forEach(t=>succ[t]=new Set());
  cy.edges().forEach(e=>{ const a=topOf(e.source()), b=topOf(e.target());
    if(a && b && a!==b && succ[a] && succ[b]) succ[a].add(b); });
  const rank={}; cellTops.forEach(t=>rank[t]=0);
  for(let i=0;i<cellTops.length;i++) cellTops.forEach(a=>succ[a].forEach(b=>{ if(rank[b]<rank[a]+1) rank[b]=rank[a]+1; }));
  const maxR=Math.max(0,...Object.values(rank));
  let cols=[];
  if(maxR===0) cols=cellTops.slice().sort((x,y)=>cy.getElementById(x).data("label").localeCompare(cy.getElementById(y).data("label"))).map(t=>[t]);
  else for(let r=0;r<=maxR;r++) cols.push(cellTops.filter(t=>rank[t]===r).sort((x,y)=>cy.getElementById(x).data("label").localeCompare(cy.getElementById(y).data("label"))));
  cols=cols.filter(c=>c.length);
  if(extra.length){ const at = maxR===0 ? Math.floor(cols.length/2) : 1; cols.splice(Math.min(at,cols.length),0,extra); }
  // a top box's stack: its own units, then each nested box (recursively) underneath
  const stackOf=id=>{ const parts=[]; if(block[id]) parts.push({id, b:block[id]});
    boxes.filter(b=>b.parent().length && b.parent().id()===id).forEach(c=>parts.push({id:c.id(), nested:stackOf(c.id())}));
    return parts; };
  const sizeOf=parts=>parts.reduce((s,p)=>{ const z=p.b?{w:p.b.w,h:p.b.h}:sizeOf(p.nested); return {w:Math.max(s.w,z.w+(p.b?0:2*CELLGAP.NEST/2)), h:s.h+z.h+(s.h?CELLGAP.NEST:0)}; },{w:0,h:0});
  const placeStack=(parts,x,y)=>{ let yy=y; parts.forEach(p=>{
    if(p.b){ shift(p.b.eles,x-p.b.ox,yy-p.b.oy); p.b.ox=x; p.b.oy=yy; yy+=p.b.h+CELLGAP.NEST; }
    else { const z=sizeOf(p.nested); placeStack(p.nested,x+CELLGAP.NEST/2,yy); yy+=z.h+CELLGAP.NEST; } }); };
  let bottom=0, H=0;
  const placeAll=()=>{ let x=0; bottom=0;
    const colH=cols.map(c=>c.reduce((h,id)=>h+Math.max(sizeOf(stackOf(id)).h,(BOXSIZE[id]||{h:0}).h)+CELLGAP.ROW,-CELLGAP.ROW)); H=Math.max(0,...colH);
    cols.forEach((c,i)=>{ let y=(H-colH[i])/2; let w=0;   // columns centred on a common mid-line
      c.forEach(id=>{ const st=stackOf(id), z=sizeOf(st), bz=BOXSIZE[id]||{w:0,h:0}; placeStack(st,x,y);   // room for a box the curator enlarged
        y+=Math.max(z.h,bz.h)+CELLGAP.ROW; w=Math.max(w,z.w,bz.w); });
      x+=w+COLGAP; bottom=Math.max(bottom,y); });
    if(block[""]){ const lb=block[""], ty=Math.max(bottom,H)+CELLGAP.LOOSE; shift(lb.eles,0-lb.ox,ty-lb.oy); lb.ox=0; lb.oy=ty; }   // loose units underneath
    resat(); };
  const resat=()=>S.sat.forEach(m=>{ const h=cy.getElementById(m.data("_host")||""); if(h.length){ const p=h.position(); m.position({x:p.x+m.data("_dx"), y:p.y+m.data("_dy")}); } });
  // order of the boxes inside each column: try every order (columns of up to 6 boxes) and keep the one with
  // fewest crossings over the whole graph, then the most compact models
  const coreN=units, coreE=cy.edges("[!glue]").filter(e=>coreN.contains(e.source()) && coreN.contains(e.target()));
  const perms=a=>a.length<=1?[a]:a.flatMap((v,i)=>perms(a.slice(0,i).concat(a.slice(i+1))).map(r=>[v].concat(r)));
  cols.forEach((c,ci)=>{ if(c.length<2 || c.length>6) return;
    let bestP=null, bestS=Infinity;
    perms(c).forEach(pp=>{ cols[ci]=pp; placeAll(); const sc=layoutScore(coreN,coreE); if(sc<bestS-1e-9){ bestS=sc; bestP=pp; } });
    cols[ci]=bestP; });
  placeAll();
  placeBetween();
  placeOuter();
  orientIntra(cy.nodes("[!is_mol][!is_cell]"));
  pushOutExtracellular();
  LAST_LAYOUT_INFO="cell layout: "+countCrossings(coreE)+" crossing(s)";
  cy.fit(null,40);
}
document.getElementById("relayout").onclick=()=>{ CELL_ON ? cellLayout() : autoLayout(); };
function showModal(html){ document.getElementById("modalbody").innerHTML=html; document.getElementById("modal").style.display="flex"; }
document.getElementById("modalclose").onclick=()=>document.getElementById("modal").style.display="none";
document.getElementById("modal").addEventListener("click",e=>{ if(e.target.id==="modal") document.getElementById("modal").style.display="none"; });

document.getElementById("png").onclick=()=>{
  if(!cy) return;
  // Keep the boxes EXACTLY as the viewer draws them (same size + alignment); just
  // overlay the two-tier label (protein name big+bold, MF smaller) since cy.png
  // can't capture the HTML-overlay labels.
  const NF=26, MF=18;   // MF enlarged 2026-09-22 to match on-screen 18/20 ratio
  const bb=cy.elements().boundingBox();
  // up to 4x for print quality, but capped: browsers fail silently on very large canvases (user 2026-10-27:
  // "PNG doesn't work"; the rod set at 4x was 12,300 x 6,800 px). Longest side <= 8000 px and <= 40 Mpx.
  const scale=Math.max(0.5, Math.min(4, 8000/Math.max(bb.w,bb.h), Math.sqrt(40e6/Math.max(1,bb.w*bb.h))));
  flash("making PNG…");
  const base=cy.png({full:true, scale:scale, bg:"#ffffff"});
  const img=new Image();
  img.onload=function(){
    const cv=document.createElement("canvas");
    cv.width=img.width; cv.height=img.height;
    const ctx=cv.getContext("2d");
    ctx.drawImage(img,0,0);
    const sx=cv.width/bb.w, sy=cv.height/bb.h;
    ctx.textAlign="center"; ctx.textBaseline="top";
    function wrap(text,maxW){
      const words=(text||"").split(/\s+/), lines=[]; let cur="";
      for(const w of words){ const t=cur?cur+" "+w:w;
        if(ctx.measureText(t).width>maxW && cur){ lines.push(cur); cur=w; } else cur=t; }
      if(cur) lines.push(cur); return lines.length?lines:[""];
    }
    cy.nodes("[!is_mol][!is_cell]").forEach(n=>{
      const p=n.position(), cx=(p.x-bb.x1)*sx, cyc=(p.y-bb.y1)*sy;
      const maxW=(n.width()-14)*sx;
      ctx.font="bold "+(NF*scale)+"px Arial, Helvetica, sans-serif"; const nl=wrap(n.data("gp"),maxW);
      ctx.font=(MF*scale)+"px Arial, Helvetica, sans-serif";         const ml=n.data("mf")?wrap(n.data("mf"),maxW):[];
      const items=nl.map(t=>({t,f:"bold "+(NF*scale)+"px Arial, Helvetica, sans-serif",lh:NF*scale*1.18,c:"#0b1220"}))
        .concat(ml.map(t=>({t,f:(MF*scale)+"px Arial, Helvetica, sans-serif",lh:MF*scale*1.35,c:"#0b1220"})));
      const total=items.reduce((s,i)=>s+i.lh,0); let y=cyc-total/2;
      items.forEach(it=>{ ctx.font=it.f; ctx.fillStyle=it.c; ctx.fillText(it.t,cx,y); y+=it.lh; });
    });
    cy.nodes("[?is_mol]").forEach(n=>{   // molecule names (HTML on screen, so drawn here for the PNG)
      const p=n.position(), cx=(p.x-bb.x1)*sx, cyc=(p.y-bb.y1)*sy, maxW=(n.data("tw")+6)*sx;
      const fn="600 "+(MOLF.name*scale)+"px Arial, Helvetica, sans-serif", fl=(MOLF.loc*scale)+"px Arial, Helvetica, sans-serif";
      ctx.font=fn; const nl=wrap(n.data("gp"),maxW); ctx.font=fl; const ll=n.data("loc")?wrap("["+n.data("loc")+"]",maxW):[];
      const items=nl.map(t=>({t,f:fn,lh:MOLF.name*scale*1.15,c:"#0b1220"})).concat(ll.map(t=>({t,f:fl,lh:MOLF.loc*scale*1.2,c:"#445"})));
      const total=items.reduce((s,i)=>s+i.lh,0); let y=cyc-total/2;
      items.forEach(it=>{ ctx.font=it.f; ctx.fillStyle=it.c; ctx.fillText(it.t,cx,y); y+=it.lh; });
    });
    cv.toBlob(function(blob){   // a file (object URL), not a huge data: string
      if(!blob){ showErr("Could not make the PNG (image too large for this browser)."); return; }
      const url=URL.createObjectURL(blob), name="gocam-network-"+new Date().toISOString().slice(0,10)+".png";
      showModal('<h1 style="font-size:15px;margin:0 0 6px">Network image</h1>'
        +'<div style="margin-bottom:8px"><a class="primary" href="'+url+'" download="'+name+'" style="display:inline-block;padding:6px 12px;background:#2a6ef0;color:#fff;border-radius:6px;text-decoration:none">&#11015; Download PNG</a> '
        +'<span class="sub">'+cv.width+' &times; '+cv.height+' px, '+(blob.size/1e6).toFixed(1)+' MB</span></div>'
        // opened from JupyterLab: the file server sends "sandbox allow-scripts", the browser then blocks downloads (user 2026-11-27)
        +((window.origin==="null" && location.protocol!=="file:")
          ? '<div style="margin:0 0 8px;padding:6px 8px;background:#fff4e5;border:1px solid #f0c27a;border-radius:6px;font-size:13px">'
            +'<b>Download is blocked in this tab</b>: this copy is opened from JupyterLab, which sandboxes HTML files. '
            +'Right-click the image below &rarr; <b>Save image as&hellip;</b>, or use the public page '
            +'<span class="mono">lucillepo.github.io/gocam-megaviewer/viewer2.html</span>, where Download works.</div>'
          : '<div class="sub" style="margin:0 0 8px">If the download does not start, right-click the image &rarr; Save image as&hellip;</div>')
        +'<img src="'+url+'" title="right-click &rarr; Save image as&hellip;">');
    }, "image/png");
  };
  img.onerror=function(){ showErr("Could not render PNG image."); };
  img.src=base;
};

function applyState(s){
  if(!s||!cy) return;
  pushHistory();   // so loading a layout can be undone
  if(s.scheme){ colorBy=s.scheme; const sel=document.getElementById("colorBy"); if(sel) sel.value=s.scheme; if(typeof showSchemeLegend==="function") showSchemeLegend(); }
  if(s.colors){ OVERRIDE=s.colors; lsSet("gocam-colors",OVERRIDE); }
  if(s.palette){ PALETTE=s.palette; lsSet("gocam-palette",PALETTE); renderPalette(); }
  if(s.layout){ cy.nodes("[!is_cell]").forEach(n=>{ const p=s.layout[n.data("sig")]; if(p) n.position(p); }); cy.fit(null,40); }
  applyColors();
}

// full restore: rebuild the saved models (if the blob carries IDs) then apply layout+colours
async function restoreState(s){
  if(!s || typeof s!=="object") throw new Error("bad state");
  if(s.scheme){ colorBy=s.scheme; const sel=document.getElementById("colorBy"); if(sel) sel.value=s.scheme; if(typeof showSchemeLegend==="function") showSchemeLegend(); }
  if(s.colors) OVERRIDE=Object.assign({}, s.colors);
  if(s.palette){ PALETTE=s.palette.slice(); renderPalette(); }
  if(s.merge){ const m=document.getElementById("mON"),b=document.getElementById("bON"),c=document.getElementById("cON");
    if(m) m.checked=!!s.merge.mf; if(b) b.checked=!!s.merge.bp; if(c) c.checked=!!s.merge.cc; }
  if(s.mode){ const r=document.querySelector('input[name=mode][value="'+s.mode+'"]'); if(r) r.checked=true; }
  if(s.src){ const r=document.querySelector('input[name=srcmode][value="'+s.src+'"]'); if(r) r.checked=true; }
  { const r=document.querySelector('input[name=cellmode][value="'+(s.cell?"cell":"flow")+'"]'); if(r) r.checked=true; }
  CELL_PLACE = Object.assign({}, s.place||{});
  BOXSIZE = Object.assign({}, s.boxsize||{});
  if(Array.isArray(s.ids) && s.ids.length){
    document.getElementById("ids").value = s.ids.map(id=>String(id).startsWith("gomodel:")?id:"gomodel:"+id).join("\n");
    PENDING_LAYOUT = s.layout || null;      // render() will use these positions instead of auto-layout
    await doBuild();                        // fetch + build the models
  } else if(s.layout && cy){
    cy.nodes("[!is_cell]").forEach(n=>{ const p=s.layout[n.data("sig")]; if(p) n.position(p); }); cy.fit(null,40);
  }
  applyColors();
}
document.getElementById("savelayout").onclick=()=>{
  if(!cy) return;
  const ids=currentIds().filter(id=>CACHE[id]);
  const pos={}; cy.nodes("[!is_cell]").forEach(n=>{ pos[n.data("sig")]=n.position(); });
  const blob=JSON.stringify({v:2, ids:ids, merge:MERGE_ON, mode:currentMode(), src:currentSrcMode(), cell:CELL_ON, place:CELL_PLACE, boxsize:BOXSIZE, layout:pos, colors:OVERRIDE, scheme:colorBy, palette:PALETTE});
  let saved=false;
  try{ localStorage.setItem(layoutKey(ids),JSON.stringify(pos)); lsSet("gocam-colors",OVERRIDE); saved=true; }catch(e){}
  showModal('<h1 style="font-size:15px;margin:0 0 6px">Save / restore layout &amp; colours</h1>'
    +'<div class="sub" style="margin-bottom:6px">'
      +'Copy this text. On <b>any</b> page (even a fresh one), click <b>load layout</b> and paste it — '
      +'it rebuilds these exact models with this layout &amp; colours. '
      +(saved?'(Also remembered in this browser for this model set.) ':'')
      +'To make it the permanent default, save it as <span class="mono">gocam-viewer/layout.json</span> and rebuild.</div>'
    +'<textarea id="stateout" readonly rows="6">'+blob.replace(/</g,"&lt;")+'</textarea>'
    +'<div style="margin:6px 0"><button id="copystate">copy</button> <span id="modalmsg"></span></div>'
    +'<div class="sub" style="margin-top:8px">Restore — paste saved text and Apply:</div>'
    +'<textarea id="statein" rows="4" placeholder="paste saved text here…"></textarea>'
    +'<div style="margin-top:6px"><button id="applystate">apply</button></div>');
  document.getElementById("copystate").onclick=()=>{
    const t=document.getElementById("stateout"); t.focus(); t.select();
    let ok=false; try{ ok=document.execCommand("copy"); }catch(e){}
    document.getElementById("modalmsg").textContent = ok ? "copied ✓" : "select the text and copy manually";
  };
  document.getElementById("applystate").onclick=async()=>{
    try{ await restoreState(JSON.parse(document.getElementById("statein").value)); document.getElementById("modal").style.display="none"; }
    catch(e){ document.getElementById("modalmsg").style.color="#b5480f"; document.getElementById("modalmsg").textContent="couldn't read that text"; }
  };
};
// load layout: available even on an empty page — paste a saved blob to rebuild its graph
document.getElementById("loadlayout").onclick=()=>{
  showModal('<h1 style="font-size:15px;margin:0 0 6px">Load a saved layout</h1>'
    +'<div class="sub" style="margin-bottom:6px">Paste text from a previous <b>save layout</b>. It rebuilds those models with the saved layout &amp; colours.</div>'
    +'<textarea id="statein" rows="6" placeholder="paste saved layout text here…"></textarea>'
    +'<div style="margin-top:6px"><button id="applystate">load</button> <span id="modalmsg"></span></div>');
  document.getElementById("applystate").onclick=async()=>{
    const msg=document.getElementById("modalmsg");
    try{ msg.style.color=""; msg.textContent="loading…"; await restoreState(JSON.parse(document.getElementById("statein").value)); document.getElementById("modal").style.display="none"; }
    catch(e){ msg.style.color="#b5480f"; msg.textContent="couldn't read that text"; }
  };
};
document.getElementById("q").addEventListener("input",e=>{
  if(!cy) return; const q=e.target.value.toLowerCase().trim();
  cy.elements().removeClass("faded hi"); if(!q) return;
  cy.nodes("[!is_cell]").forEach(n=>{ const hay=`${n.data("gp")} ${n.data("mf")} ${n.data("bp")} ${n.data("cc")} ${(n.data("models")||[]).join(" ")}`.toLowerCase();
    if(!hay.includes(q)) n.addClass("faded"); else n.addClass("hi"); });
});
function showSchemeLegend(){ document.querySelectorAll(".schemeleg").forEach(d=>d.style.display = d.dataset.s===colorBy ? "" : "none"); }
document.getElementById("colorBy").addEventListener("change",e=>{ colorBy=e.target.value; applyColors(); showSchemeLegend(); });
document.getElementById("clearcol").addEventListener("click",clearAllOverrides);
document.getElementById("palAddBtn").addEventListener("click",()=>{ pushHistory(); addToPalette(document.getElementById("palAdd").value); });
document.getElementById("undo").addEventListener("click",undo);
document.getElementById("onlyBridges").addEventListener("change",e=>{
  if(!cy) return; cy.elements().removeClass("faded");
  if(e.target.checked) cy.nodes("[!is_cell]").forEach(n=>{ if(!n.data("bridge")) n.addClass("faded"); });
});

// --- draggable side panels ---
function makeResizer(handleId, panelId, grow){
  const handle=document.getElementById(handleId), panel=document.getElementById(panelId);
  if(!handle||!panel) return;
  handle.addEventListener("mousedown",e=>{
    e.preventDefault();
    const startX=e.clientX, startW=panel.getBoundingClientRect().width;
    document.body.style.userSelect="none"; document.body.style.cursor="col-resize";
    function move(ev){
      const dx=ev.clientX-startX;
      let w = grow==="left" ? startW+dx : startW-dx;   // left panel grows with +dx; right panel with -dx
      w=Math.max(60, Math.min(760, w));
      panel.style.width=w+"px";
      if(cy) cy.resize();
    }
    function up(){ document.removeEventListener("mousemove",move); document.removeEventListener("mouseup",up);
      document.body.style.userSelect=""; document.body.style.cursor=""; if(cy){ cy.resize(); } }
    document.addEventListener("mousemove",move); document.addEventListener("mouseup",up);
  });
}
makeResizer("rzL","left","left");
makeResizer("rzR","side","right");

document.getElementById("colorBy").value = colorBy;   // reflect baked-in default scheme
showSchemeLegend();
renderPalette();
renderCacheList([]);

// --- shareable links: read model IDs from the URL (?ids=a,b,c) and build; and a Copy-link button ---
function shareURL(){
  const ids=currentIds().map(s=>s.replace(/^gomodel:/,""));
  return location.origin+location.pathname+(ids.length?("?ids="+ids.join(",")+(currentSrcMode()==="prod"?"&src=prod":"")+(currentCellMode()==="cell"?"&cell=1":"")):"");
}
const _sl=document.getElementById("sharelink");
if(_sl) _sl.onclick=()=>{
  const url=shareURL();
  if(currentIds().length===0){ flash("enter model IDs first"); return; }
  (navigator.clipboard&&navigator.clipboard.writeText(url).then(()=>flash("share link copied"))
    .catch(()=>window.prompt("Copy this link:",url))) || window.prompt("Copy this link:",url);
};
(function initFromURL(){
  const p=new URLSearchParams(location.search);
  const raw=p.get("ids")||p.get("models")||"";
  if(p.get("src")){ const r=document.querySelector('input[name=srcmode][value="'+(p.get("src")==="prod"?"prod":"dev")+'"]'); if(r) r.checked=true; }
  if(p.get("cell")==="1"){ const r=document.querySelector('input[name=cellmode][value="cell"]'); if(r) r.checked=true; }
  if(raw){
    document.getElementById("ids").value =
      raw.split(/[\s,;]+/).filter(Boolean).map(s=>s.startsWith("gomodel:")?s:"gomodel:"+s).join("\n");
  }
  doBuild();   // empty box -> returns quietly; ?ids= -> fetches + draws immediately
})();
</script>
</body>
</html>
"""
