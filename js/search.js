(function(){
var dlg=document.getElementById('search-dialog'),inp=document.getElementById('search-input'),res=document.getElementById('search-results'),idx=[];
document.querySelectorAll('.guide-section').forEach(function(s){var t=s.dataset.title,
parts=[].slice.call(s.querySelectorAll('h3,h4,p,li,td,th')).map(function(n){return n.textContent.replace(/\s+/g,' ').trim()}).filter(Boolean);
idx.push({id:s.id,title:t,parts:parts})});
function esc(s){return s.replace(/[&<>]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;'}[c]})}
function run(){var q=inp.value.trim().toLowerCase();res.innerHTML='';if(q.length<2)return;var n=0;
idx.forEach(function(s){var hit=s.parts.find(function(p){return p.toLowerCase().indexOf(q)>-1}),tm=s.title.toLowerCase().indexOf(q)>-1;
if(!hit&&!tm)return;n++;var ex=hit||s.title,i=ex.toLowerCase().indexOf(q),a=Math.max(0,i-40),e=ex.slice(a,a+140);
var h=esc(e).replace(new RegExp(q.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'),'gi'),function(m){return'<mark>'+m+'</mark>'});
var li=document.createElement('li');li.innerHTML='<a href="#'+s.id+'"><b>'+esc(s.title)+'</b><span>'+(a>0?'…':'')+h+'…</span></a>';res.appendChild(li)});
if(!n)res.innerHTML='<li class="small">No results.</li>'}
document.getElementById('search-btn').addEventListener('click',function(){dlg.showModal();inp.focus()});
inp.addEventListener('input',run);res.addEventListener('click',function(e){if(e.target.closest('a'))dlg.close()});
document.addEventListener('keydown',function(e){if(e.key==='/'&&!/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName)&&!document.activeElement.isContentEditable&&!dlg.open){e.preventDefault();dlg.showModal();inp.focus()}});
})();
