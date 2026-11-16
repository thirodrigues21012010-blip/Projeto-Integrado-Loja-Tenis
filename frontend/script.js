let saved;try{saved=JSON.parse(localStorage.getItem('hype-wishlist')||'[]');if(!Array.isArray(saved))saved=[];saved=saved.filter(id=>products.some(p=>p.id===id))}catch{saved=[]}let brand='all';
let expanded=false;
let modelFilter=null;
const mixedProducts=interleaveBrands();
const money=n=>n===null?'Sem oferta no momento':n.toLocaleString('pt-BR',{style:'currency',currency:'BRL'});const search=document.querySelector('#search');
function render(){const filtered=(brand==='all'?mixedProducts:products).filter(p=>(brand==='all'||p.brand===brand)&&(!modelFilter||p.model===modelFilter)&&`${p.brand} ${p.name} ${p.color}`.toLowerCase().includes(search.value.toLowerCase()));const preview=brand==='all'&&!expanded&&!search.value.trim();const visible=preview?filtered.slice(0,4):filtered;const more=document.querySelector('#show-more');more.hidden=brand!=='all'||Boolean(search.value.trim())||filtered.length<=4;more.innerHTML=expanded?'Ver menos <span aria-hidden="true">↑</span>':'Ver mais <span aria-hidden="true">→</span>';more.setAttribute('aria-expanded',String(expanded));document.querySelector('#products').innerHTML=visible.map(p=>`<article class="product"><div class="product-image"><img src="${p.image}" alt="${p.name} — ${p.color}" loading="lazy"><span class="tag">SELEÇÃO HYPE.</span><button class="heart ${saved.includes(p.id)?'selected':''}" data-id="${p.id}" aria-label="${saved.includes(p.id)?'Remover':'Adicionar'} ${p.name} ${saved.includes(p.id)?'da':'à'} lista de desejos" aria-pressed="${saved.includes(p.id)}">${saved.includes(p.id)?'♥':'♡'}</button></div><p class="brand">${p.brand}</p><h3>${p.name}</h3><p class="colorway">${p.color}</p><span class="price-from">${p.price===null?'':'A partir de'}</span><strong class="price">${money(p.price)}</strong><a class="product-source" href="${p.source}" target="_blank" rel="noopener">Ver referência na Droper <span aria-hidden="true">↗</span></a></article>`).join('');document.querySelector('.empty').hidden=filtered.length>0;document.querySelector('#result-count').textContent=`${preview&&filtered.length>4?`${visible.length} de ${filtered.length} tênis`: `${filtered.length} ${filtered.length===1?'tênis encontrado':'tênis encontrados'}`}${brand==='all'?'':` · ${brand}${modelFilter?' '+modelFilter:''}`}`;document.querySelector('#count').textContent=saved.length;document.querySelector('#saved').innerHTML=saved.length?products.filter(p=>saved.includes(p.id)).map(p=>`<div class="saved-row"><img src="${p.image}" alt=""><div>${p.name}<p>${p.color}</p><strong>${money(p.price)}</strong></div><button data-id="${p.id}" aria-label="Remover ${p.name}">×</button></div>`).join(''):'<p class="price-note">Sua lista ainda está vazia. Toque no coração de um tênis para salvá-lo.</p>'}
document.addEventListener('click',e=>{const b=e.target.closest('[data-id]');if(!b)return;const id=Number(b.dataset.id);const exists=saved.includes(id);saved=exists?saved.filter(x=>x!==id):[...saved,id];try{localStorage.setItem('hype-wishlist',JSON.stringify(saved))}catch{}render();const toast=document.querySelector('#toast');toast.textContent=exists?'Tênis removido da lista':'Tênis adicionado à lista de desejos';toast.classList.add('visible');clearTimeout(window.toastTimer);window.toastTimer=setTimeout(()=>toast.classList.remove('visible'),2200)});
renderBrands();document.querySelectorAll('[data-brand]').forEach(b=>b.addEventListener('click',()=>{brand=b.dataset.brand;modelFilter=null;search.value='';if(brand==='all'){expanded=false}document.querySelectorAll('[data-brand]').forEach(x=>(x.classList.toggle('active',x===b),x.setAttribute('aria-pressed',String(x===b))));render()}));document.querySelector('#show-more').addEventListener('click',()=>{expanded=!expanded;render();if(!expanded)document.querySelector('#catalogo').scrollIntoView({block:'start'})});search.addEventListener('input',()=>{modelFilter=null;expanded=false;render()});document.querySelector('form').addEventListener('submit',e=>{e.preventDefault();document.querySelector('#catalogo').scrollIntoView()});document.querySelector('#wishlist').onclick=()=>document.querySelector('#favorites').showModal();document.querySelector('#close').onclick=()=>document.querySelector('#favorites').close();document.querySelector('#favorites').addEventListener('click',e=>{if(e.target===e.currentTarget){const r=e.currentTarget.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)e.currentTarget.close()}});document.addEventListener('keydown',e=>{if(e.key==='/'&&!['INPUT','TEXTAREA'].includes(document.activeElement.tagName)){e.preventDefault();search.focus()}});render();

function renderBrands(){
 const order=['Nike','adidas','Air Jordan','Asics','New Balance','Vans','On Running','Off-White','BAPE'];
 document.querySelector('#brand-options').innerHTML='<button class="brand-tile active" data-brand="all" aria-pressed="true"><span class="brand-circle all-brands" aria-hidden="true"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="3" width="6" height="6" rx="1"/><rect x="3" y="15" width="6" height="6" rx="1"/><rect x="15" y="15" width="6" height="6" rx="1"/></svg></span><span>Todos</span></button>'+order.map(name=>{const p=products.find(p=>p.brand===name);return `<button class="brand-tile" data-brand="${name}" aria-pressed="false"><span class="brand-circle"><img src="${p.brandLogo}" alt="" loading="lazy"></span><span>${name}</span></button>`}).join('');
}

// Intercala as marcas em uma sequência fixa, preservada a cada visita.
function interleaveBrands(){
 const names=['Nike','New Balance','adidas','Air Jordan','Asics','Vans','On Running','Off-White','BAPE'];
 const groups=names.map(name=>products.filter(product=>product.brand===name));
 const result=[];
 for(let index=0;index<Math.max(...groups.map(group=>group.length));index++){
  for(const group of groups){if(group[index])result.push(group[index])}
 }
 return result;
}

// Cada botão do banner seleciona a marca e o modelo no catálogo.
document.querySelectorAll('[data-explore-brand]').forEach(link=>link.addEventListener('click',()=>{
 brand=link.dataset.exploreBrand;
 modelFilter=link.dataset.exploreModel;
 search.value='';expanded=false;
 document.querySelectorAll('[data-brand]').forEach(button=>{
  const selected=button.dataset.brand===brand;
  button.classList.toggle('active',selected);button.setAttribute('aria-pressed',String(selected));
 });
 render();
}));

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
