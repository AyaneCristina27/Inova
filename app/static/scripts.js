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
        const observerOptions = { threshold: 0 };
        
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

    // Carrossel de fotos da seção "Sobre" - único uso restante do Contentful
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

    fetchAndDisplayMainCarousel();
});