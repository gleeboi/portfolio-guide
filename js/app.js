(function(){
var root=document.documentElement,$=function(s,c){return(c||document).querySelector(s)},$$=function(s,c){return Array.prototype.slice.call((c||document).querySelectorAll(s))};
var SK=function(k,v){try{return v===undefined?localStorage.getItem(k):localStorage.setItem(k,v)}catch(e){return null}};
// theme
var t=SK('guide-theme');if(t)root.setAttribute('data-theme',t);
$('#theme-btn').addEventListener('click',function(){var n=root.getAttribute('data-theme')==='dark'?'light':'dark';root.setAttribute('data-theme',n);SK('guide-theme',n)});
// drawer
var sb=$('#sidebar'),ov=$('#overlay'),mb=$('#menu-btn');
function drawer(o){sb.classList.toggle('open',o);ov.hidden=!o;mb.setAttribute('aria-expanded',o)}
mb.addEventListener('click',function(){drawer(!sb.classList.contains('open'))});ov.addEventListener('click',function(){drawer(false)});
document.addEventListener('keydown',function(e){if(e.key==='Escape')drawer(false)});
$$('.toc a').forEach(function(a){a.addEventListener('click',function(){drawer(false)})});
// progress, back-to-top, active section
var bar=$('#progress-bar'),pt=$('#progress-text'),tt=$('#to-top'),secs=$$('.guide-section'),links=$$('.toc a'),tk=false;
function upd(){tk=false;var h=document.documentElement.scrollHeight-innerHeight,p=h>0?Math.min(100,Math.round(scrollY/h*100)):0;
bar.style.width=p+'%';bar.setAttribute('aria-valuenow',p);pt.textContent='Reading progress: '+p+'%';tt.hidden=scrollY<600;
var cur=null;secs.forEach(function(s){if(s.getBoundingClientRect().top<=120)cur=s.id});
links.forEach(function(a){var on=a.getAttribute('href')==='#'+cur;a.classList.toggle('active',on);if(on)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current')})}
addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(upd)}},{passive:true});upd();
tt.addEventListener('click',function(){scrollTo({top:0})});
// copy buttons
$$('.copy-code').forEach(function(b){b.addEventListener('click',function(){var txt=$('code',b.closest('.code-block')).textContent;
var done=function(){b.textContent='Copied!';setTimeout(function(){b.textContent='Copy'},1500)};
if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(txt).then(done,function(){fb(txt);done()})}else{fb(txt);done()}})});
function fb(t){var a=document.createElement('textarea');a.value=t;document.body.appendChild(a);a.select();try{document.execCommand('copy')}catch(e){}a.remove()}
})();
