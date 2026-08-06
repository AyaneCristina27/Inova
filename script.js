document.addEventListener('DOMContentLoaded', function() {
    // Animação da tela de apresentação
    const splashScreen = document.querySelector('.splash-screen');
    if (splashScreen) {
        setTimeout(() => { splashScreen.style.display = 'none'; }, 1500);
    }
    
    // Menu mobile
    const burger = document.querySelector('.burger');
    const navLinks = document.querySelector('.nav-links');
    if (burger && navLinks) {
        burger.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            burger.classList.toggle('active');
        });
    }
    
    const navItems = document.querySelectorAll('.nav-links a');
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                burger.classList.remove('active');
            }
        });
    });

    const sections = document.querySelectorAll('.section');
    const header = document.getElementById('header');
    if (sections.length > 0) {
        let lastVisibleSection = sections[0];
        const observerOptions = { threshold: 0.3 };
        
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('active');
                    lastVisibleSection = entry.target;
                    const sectionId = entry.target.getAttribute('id');

                    if (header) {
                        const navItemsInHeader = header.querySelectorAll('.nav-links a');
                        navItemsInHeader.forEach(item => {
                            const href = item.getAttribute('href') || '';
                            if (href.includes('#')) {
                               item.classList.toggle('active', href.endsWith(`#${sectionId}`));
                            }
                        });
                    }
                } else {
                    entry.target.classList.remove('active');
                }
            });
            const bgColor = lastVisibleSection.getAttribute('data-color');
            if (bgColor) document.body.style.backgroundColor = bgColor;
        }, observerOptions);
        
        sections.forEach(section => { observer.observe(section); });
        
        window.addEventListener('scroll', function() {
            if (header) {
                if (window.scrollY > 50) {
                    header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
                } else {
                    header.style.boxShadow = 'none';
                }
            }
        });
        
        if (sections[0]) {
            sections[0].classList.add('active');
            const initialColor = sections[0].getAttribute('data-color');
            if(initialColor) document.body.style.backgroundColor = initialColor;
        }
    }

    const CONTENTFUL_SPACE_ID = 'wekesenct0h5';
    const CONTENTFUL_ACCESS_TOKEN = '8gTfpPEsehtMOMsW8_RKPRUuSXPV2wyrxFr7eY2DRYQ';

    async function fetchAndDisplayMainCarousel() {
        const wrapper = document.getElementById('main-carousel-wrapper');
        if (!wrapper) return;
        
        const url = `https://cdn.contentful.com/spaces/${CONTENTFUL_SPACE_ID}/environments/master/entries?access_token=${CONTENTFUL_ACCESS_TOKEN}&content_type=imagemCarrosselPrincipal`;
        try {
            const response = await fetch(url);
            const data = await response.json();
            const assets = data.includes ? data.includes.Asset : [];
            
            console.log(`Imagens do Carrossel Principal recebidas: ${data.items.length}`);
            if (data.items.length === 0) {
                 wrapper.innerHTML = `<div style="display:flex; align-items:center; justify-content:center; height:100%; color:white; background:rgba(0,0,0,0.1); border-radius:10px;">Nenhuma imagem encontrada. Verifique se as imagens estão publicadas no Contentful.</div>`;
                 return;
            }

            data.items.forEach(item => {
                const { titulo, imagem } = item.fields;
                if (imagem && imagem.sys) {
                    const asset = assets.find(a => a.sys.id === imagem.sys.id);
                    if (asset) {
                        const imageUrl = `https:${asset.fields.file.url}`;
                        const slide = document.createElement('div');
                        slide.className = 'swiper-slide';
                        slide.innerHTML = `<img src="${imageUrl}" alt="${titulo || 'Imagem do Carrossel'}">`;
                        wrapper.appendChild(slide);
                    }
                }
            });
            new Swiper('.main-carousel', {
                loop: true,
                autoplay: { delay: 5000, disableOnInteraction: false },
                pagination: { el: '.swiper-pagination', clickable: true },
                navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' }
            });
        } catch (error) { console.error('Erro ao buscar imagens do carrossel principal:', error); }
    }

    async function fetchAndDisplayPartners() {
        const grid = document.getElementById('partners-grid');
        if (!grid) return;
        
        grid.innerHTML = '';
        const url = `https://cdn.contentful.com/spaces/${CONTENTFUL_SPACE_ID}/environments/master/entries?access_token=${CONTENTFUL_ACCESS_TOKEN}&content_type=parceiro`;
        
        try {
            const response = await fetch(url);
            const data = await response.json();
            const assets = data.includes ? data.includes.Asset : [];
            
            data.items.forEach(item => {
                const { nome, logo, link } = item.fields;
                if (logo && logo.sys) {
                    const asset = assets.find(a => a.sys.id === logo.sys.id);
                    if (asset) {
                        const logoUrl = `https:${asset.fields.file.url}`;
                        const partnerDiv = document.createElement('a');
                        partnerDiv.className = 'partner-item';
                        partnerDiv.href = link || '#';
                        partnerDiv.target = '_blank';
                        partnerDiv.rel = 'noopener noreferrer';
                        partnerDiv.innerHTML = `<img src="${logoUrl}" alt="Logo ${nome}">`;
                        grid.appendChild(partnerDiv);
                    }
                }
            });
        } catch (error) { 
            console.error('Erro ao buscar parceiros:', error); 
        }
    }

    async function fetchAndDisplayMembers() {
        const membersGrid = document.getElementById('members-grid');
        if (!membersGrid) return;
        const url = `https://cdn.contentful.com/spaces/${CONTENTFUL_SPACE_ID}/environments/master/entries?access_token=${CONTENTFUL_ACCESS_TOKEN}&content_type=membro`;
        try {
            const response = await fetch(url);
            const data = await response.json();
            const assets = data.includes ? data.includes.Asset : [];
            membersGrid.innerHTML = '';
            if (data.items.length === 0) {
                membersGrid.innerHTML = '<p class="loading-message">Nenhum membro encontrado.</p>';
                return;
            }
            data.items.forEach(item => {
                const { nome, descricao, foto } = item.fields;
                let fotoUrl = 'https://via.placeholder.com/120';
                if (foto && foto.sys && foto.sys.id) {
                    const asset = assets.find(asset => asset.sys.id === foto.sys.id);
                    if (asset) fotoUrl = `https:${asset.fields.file.url}`;
                }
                const descText = descricao || 'Sem descrição.';
                const card = document.createElement('div');
                card.className = 'member-card';
                card.innerHTML = `<img src="${fotoUrl}" alt="Foto de ${nome}"><div class="member-info"><h3>${nome}</h3><p>${descText}</p></div>`;
                membersGrid.appendChild(card);
            });
        } catch (error) { console.error('Erro ao buscar dados dos membros:', error); }
    }

    async function fetchAndDisplayEvents() {
        const grid = document.getElementById('events-grid');
        if (!grid) return;
        const url = `https://cdn.contentful.com/spaces/${CONTENTFUL_SPACE_ID}/environments/master/entries?access_token=${CONTENTFUL_ACCESS_TOKEN}&content_type=evento`;
        try {
            const response = await fetch(url);
            const data = await response.json();
            const assets = data.includes ? data.includes.Asset : [];
            grid.innerHTML = '';
            if (data.items.length === 0) {
                    grid.innerHTML = '<p class="loading-message">Nenhum evento encontrado.</p>';
                return;
            }
            data.items.forEach(item => {
                const { nome, descricao, foto } = item.fields;
                let fotoUrl = 'https://via.placeholder.com/120';
                if (foto && foto.sys && foto.sys.id) {
                    const asset = assets.find(asset => asset.sys.id === foto.sys.id);
                    if (asset) fotoUrl = `https:${asset.fields.file.url}`;
                }
                const descText = descricao || 'Sem descrição.';
                const card = document.createElement('div');
                    card.className = 'member-card';
                card.innerHTML = `<img src="${fotoUrl}" alt="Foto de ${nome}"><div class="event-info"><h3>${nome}</h3><p>${descText}</p></div>`;
                grid.appendChild(card);
            });
        } catch (error) { console.error('Erro ao buscar dados dos eventos:', error); }
    }

    fetchAndDisplayMainCarousel();
    fetchAndDisplayPartners();
    fetchAndDisplayMembers();
    fetchAndDisplayEvents();
});