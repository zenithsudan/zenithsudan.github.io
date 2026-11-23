(function(){
var f=document.getElementById('brief');if(!f)return;
var wa=f.getAttribute('data-wa'),mail=f.getAttribute('data-mail'),intro=f.getAttribute('data-intro'),subj=f.getAttribute('data-subject');
function msg(){var out=[intro,''];[].forEach.call(f.querySelectorAll('[data-label]'),function(el){var v=(el.value||'').trim();if(v)out.push(el.getAttribute('data-label')+': '+v);});return out.join('\n');}
function need(){var n=f.querySelector('[required]');if(n&&!n.value.trim()){n.focus();return false;}return true;}
f.querySelector('[data-send=wa]').addEventListener('click',function(){if(!need())return;window.open('https://wa.me/'+wa+'?text='+encodeURIComponent(msg()),'_blank','noopener');});
f.querySelector('[data-send=mail]').addEventListener('click',function(){if(!need())return;location.href='mailto:'+mail+'?subject='+encodeURIComponent(subj)+'&body='+encodeURIComponent(msg());});
var q=new URLSearchParams(location.search).get('topic');if(q){var m=f.querySelector('[name=message]');if(m&&!m.value)m.value=q;}
})();
