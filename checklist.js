(function(){
var K='guide-checklist',s={};try{s=JSON.parse(localStorage.getItem(K)||'{}')}catch(e){}
var boxes=[].slice.call(document.querySelectorAll('input[data-check]'));
function save(){try{localStorage.setItem(K,JSON.stringify(s))}catch(e){}}
boxes.forEach(function(b){b.checked=!!s[b.dataset.check];b.addEventListener('change',function(){if(b.checked)s[b.dataset.check]=1;else delete s[b.dataset.check];save()})});
document.querySelectorAll('.reset-checklist').forEach(function(r){r.addEventListener('click',function(){boxes.forEach(function(b){b.checked=false});s={};save()})});
})();
