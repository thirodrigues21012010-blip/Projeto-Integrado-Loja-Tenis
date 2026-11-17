/* A API é a fonte de dados; nenhum favorito é salvo no localStorage. */
let products=[], saved=[], user=null, csrf='', brand='all', expanded=false, modelFilter=null;
let catalogReady=false;
const $=s=>document.querySelector(s);
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const money=n=>Number(n).toLocaleString('pt-BR',{style:'currency',currency:'BRL'});
function notice(msg){const dlg=document.querySelector('dialog[open]');if(dlg){let status=dlg.querySelector('.form-status');if(!status){status=document.createElement('p');status.className='form-status';status.setAttribute('role','status');dlg.prepend(status)}status.textContent=msg;}$('#toast').textContent=msg;$('#toast').classList.add('visible');clearTimeout(window.toastTimer);window.toastTimer=setTimeout(()=>$('#toast').classList.remove('visible'),5000)}
async function api(path,method='GET',body){const r=await fetch('/api/'+path,{method,headers:{'Content-Type':'application/json','X-CSRF-Token':csrf},...(body?{body:JSON.stringify(body)}:{})});const d=await r.json();if(!r.ok)throw Error(d.error||'Não foi possível concluir.');return d}
async function sessionLoad(){const s=await api('sessao');user=s.usuario;csrf=s.csrf;$('#account').textContent=user?user.nome_completo:'Entrar / Cadastrar';$('#exit').hidden=!user;$('#manage').hidden=!user||user.perfil==='CLIENTE';saved=user?await api('lista'):[];updateManage();render()}
function updateManage(){
 $('#manage').disabled=!catalogReady;
 $('#manage').title=catalogReady?'Gerenciar catálogo e estoque':'Aguarde o carregamento do catálogo';
}
async function load(){
 catalogReady=false;updateManage();
 try{products=await api('produtos');renderBrands();render();catalogReady=true}
 finally{updateManage()}
}
function syncExistingModel(){
 const form=$('#new-product-form');
 const selected=products.find(p=>String(p.id_modelo)===$('#existing-model').value);
 for(const [field,key] of [['nome','name'],['marca','brand']]){
  const input=form.elements.namedItem(field);
  input.value=selected?selected[key]:'';
  input.readOnly=Boolean(selected);
 }
}
$('#existing-model').onchange=syncExistingModel;
function renderBrands(){const names=[...new Set(products.map(p=>p.brand))];const logos={'Nike':'nike','adidas':'adidas','Air Jordan':'air-jordan','Asics':'asics','New Balance':'new-balance','Vans':'vans','On Running':'on-running','Off-White':'off-white','BAPE':'bape'};$('#brand-options').innerHTML='<button class="brand-tile" data-brand="all">Todos</button>'+names.map(n=>`<button class="brand-tile" data-brand="${esc(n)}"><span class="brand-circle">${logos[n]?`<img src="assets/brand-${logos[n]}.webp" alt="">`:esc(n[0])}</span><span>${esc(n)}</span></button>`).join('');}
function render(){const filtered=products.filter(p=>(brand==='all'||p.brand===brand)&&(!modelFilter||p.model.includes(modelFilter))&&`${p.brand} ${p.name} ${p.color}`.toLowerCase().includes($('#search').value.toLowerCase()));const visible=expanded?filtered:filtered.slice(0,4);$('#products').innerHTML=visible.map(p=>`<article class="product"><div class="product-image"><img src="${esc(p.image)}" alt="${esc(p.name)}" loading="lazy"><span class="tag">SELEÇÃO HYPE.</span><button class="heart ${saved.some(v=>v.id_coloracao===p.id)?'selected':''}" data-detail="${p.id}" aria-label="Escolher tamanho e salvar">♡</button></div><p class="brand">${esc(p.brand)}</p><h3>${esc(p.name)}</h3><p class="colorway">${esc(p.color)}</p><strong class="price">${p.price===0?'Consulte a loja':money(p.price)}</strong><button class="product-source" data-detail="${p.id}">Ver tamanhos e detalhes →</button></article>`).join('');$('#result-count').textContent=`${filtered.length} tênis encontrados`;$('.empty').hidden=filtered.length>0;$('#show-more').hidden=filtered.length<=4;$('#show-more').textContent=expanded?'Ver menos ↑':'Ver mais →';$('#show-more').setAttribute('aria-expanded',String(expanded));$('#count').textContent=saved.length;$('#saved').innerHTML=saved.length?saved.map(v=>`<div class="saved-row"><div>${esc(v.nome)}<p>${esc(v.cor)} · Tamanho ${esc(v.tamanho)}</p><strong>${v.preco?money(v.preco):'Consulte a loja'}</strong><p>Estoque: ${v.quantidade_estoque}</p></div><button data-remove="${v.id_variante}" aria-label="Remover item">×</button></div>`).join(''):(user?'Sua lista está vazia.':'Entre na conta para acessar sua lista.');document.querySelectorAll('[data-brand]').forEach(b=>{b.classList.toggle('active',b.dataset.brand===brand);b.setAttribute('aria-pressed',String(b.dataset.brand===brand))})}
function detail(id){const p=products.find(p=>p.id===id);if(!p)return;$('#detail-content').innerHTML=`<h2>${esc(p.name)}</h2><img class="detail-image" src="${esc(p.image)}" alt="${esc(p.name)}"><p>${esc(p.color)} · ${p.price?money(p.price):'Consulte a loja'}</p><label>Coloração <select id="color-select">${products.filter(x=>x.id_modelo===p.id_modelo).map(x=>`<option value="${x.id}" ${x.id===p.id?'selected':''}>${esc(x.color)}</option>`).join('')}</select></label><label>Tamanho <select id="variant">${p.variantes.map(v=>`<option value="${v.id_variante}">${esc(v.tamanho)} — ${v.quantidade_estoque} em estoque</option>`).join('')}</select></label><button id="save-variant" class="button">Salvar na lista de desejos</button><p>A lista não reserva nem reduz o estoque.</p>`;$('#color-select').onchange=e=>detail(Number(e.target.value));$('#save-variant').onclick=()=>run(async()=>{if(!user){$('#detail').close();$('#auth').showModal();return}await api('lista/'+$('#variant').value,'POST');saved=await api('lista');render();notice('Item salvo na sua conta.');});if(!$('#detail').open)$('#detail').showModal()}
async function run(fn){try{await fn()}catch(e){notice(e.message)}}
document.addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;if(b.dataset.detail)detail(Number(b.dataset.detail));if(b.dataset.remove)run(async()=>{await api('lista/'+b.dataset.remove,'DELETE');saved=await api('lista');render()});if(b.dataset.brand){brand=b.dataset.brand;modelFilter=null;expanded=false;render()}if(b.dataset.close)$('#'+b.dataset.close).close()});
$('#search').oninput=()=>{modelFilter=null;expanded=true;render()};$('form[role="search"]').onsubmit=e=>{e.preventDefault();$('#catalogo').scrollIntoView()};$('#show-more').onclick=()=>{expanded=!expanded;render()};$('#wishlist').onclick=()=>$('#favorites').showModal();$('#close').onclick=()=>$('#favorites').close();$('#account').onclick=()=>{if(user)notice('Perfil: '+user.perfil);else $('#auth').showModal()};$('#exit').onclick=()=>run(async()=>{await api('logout','POST');await sessionLoad();notice('Você saiu da conta.')});
for(const kind of ['login','cadastro'])$('#'+kind+'-form').onsubmit=e=>{e.preventDefault();const form=e.currentTarget;run(async()=>{await api(kind,'POST',Object.fromEntries(new FormData(form)));await sessionLoad();form.reset();$('#auth').close();notice('Conta conectada.');})};
$('#manage').onclick=()=>{if(!user||user.perfil==='CLIENTE')return;if(!catalogReady){notice('Aguarde o carregamento do catálogo.');return}const f=$('#new-product-form');f.hidden=user.perfil!=='GERENTE';$('#stock-color').innerHTML=products.map(p=>`<option value="${p.id}">${esc(p.name)} · ${esc(p.color)}</option>`).join('');$('#existing-model').innerHTML='<option value="">Criar novo modelo</option>'+[...new Map(products.map(p=>[p.id_modelo,p])).values()].map(p=>`<option value="${p.id_modelo}">${esc(p.name)}</option>`).join('');syncExistingModel();$('#admin').showModal()};
$('#stock-form').onsubmit=e=>{e.preventDefault();const d=Object.fromEntries(new FormData(e.currentTarget));if(!catalogReady||!d.id_coloracao){notice('Aguarde o catálogo e selecione uma coloração cadastrada.');return}run(async()=>{await api('estoque/'+d.id_coloracao,'PUT',d);await load();notice('Tamanho e estoque atualizados.')})};$('#new-product-form').onsubmit=e=>{e.preventDefault();const form=e.currentTarget;run(async()=>{await api('produtos','POST',Object.fromEntries(new FormData(form)));await load();form.reset();syncExistingModel();notice('Coloração cadastrada com foto e tamanho.');})};
document.querySelectorAll('[data-explore-brand]').forEach(link=>link.onclick=()=>{brand=link.dataset.exploreBrand;modelFilter=link.dataset.exploreModel;expanded=true;$('#search').value='';render()});
document.addEventListener('keydown',e=>{if(e.key==='/'&&!['INPUT','TEXTAREA','SELECT'].includes(document.activeElement.tagName)){e.preventDefault();$('#search').focus()}});
run(async()=>{await sessionLoad();await load()});
const carousel=document.querySelector('.carousel');
const slides=[...document.querySelectorAll('[data-slide]')];
const previousSlide=document.querySelector('.carousel-prev');
const nextSlide=document.querySelector('.carousel-next');
let slideIndex=0,carouselTimer=null;
function scheduleSlide(){
 clearTimeout(carouselTimer);
 carouselTimer=setTimeout(()=>{showSlide(slideIndex+1);},5000);
}
function showSlide(index,manual=false){
 slideIndex=(index+slides.length)%slides.length;
 slides.forEach((slide,i)=>{slide.hidden=i!==slideIndex});
 document.querySelector('#slide-number').textContent=String(slideIndex+1).padStart(2,'0');
 if(manual)document.querySelector('#slide-status').textContent=slides[slideIndex].getAttribute('aria-label');
 scheduleSlide();
}
previousSlide.addEventListener('click',()=>showSlide(slideIndex-1,true));
nextSlide.addEventListener('click',()=>showSlide(slideIndex+1,true));
scheduleSlide();
