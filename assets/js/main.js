// サイト全体のJavaScriptロジック
document.addEventListener('DOMContentLoaded', () => {

    const navToggle = document.querySelector('.nav-toggle');
    const siteNav = document.querySelector('.site-nav');
    const body = document.body;

    // --- 1. ログ出力制御 (本番環境での抑制) ---
    const isProduction = typeof JEKYLL_ENV !== 'undefined' && JEKYLL_ENV === 'production';
    
    function log(message, type = 'log') {
        if (!isProduction) {
            const prefix = "Counseling Space paz [JS]: ";
            if (type === 'warn') {
                console.warn(prefix + message);
            } else {
                console.log(prefix + message);
            }
        }
    }

    if (!navToggle || !siteNav) {
        log("ナビゲーション要素が見つかりません: .nav-toggle または .site-nav", 'warn');
        return;
    }
    
    const firstNavLink = siteNav.querySelector('ul a');

    // --- 2. ナビゲーション（ハンバーガーメニュー）の開閉制御 ---
    const toggleMenu = (isActive, focus = true) => {
        siteNav.classList.toggle('is-active', isActive);
        navToggle.setAttribute('aria-expanded', isActive);
        body.classList.toggle('no-scroll', isActive);
        navToggle.setAttribute('aria-label', isActive ? 'メニューを閉じる' : 'メニューを開く');
        
        if (isActive && firstNavLink && focus) {
            firstNavLink.focus();
        }
    };

    // --- 3. イベントリスナーの設定 ---
    navToggle.addEventListener('click', () => {
        const isActive = !siteNav.classList.contains('is-active');
        toggleMenu(isActive);
        log(`Menu toggled: ${isActive ? 'Opened' : 'Closed'}`);
    });

    siteNav.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            toggleMenu(false, false); 
            log("Menu closed after navigation link clicked.");
        });
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && siteNav.classList.contains('is-active')) {
            toggleMenu(false);
            navToggle.focus();
            log("Menu closed via Esc key.");
        }
    });

    // --- 4. リサイズ時の状態整合 ---
    const mediaQuery = window.matchMedia('(min-width: 1024px)');
    
    const handleResize = (e) => {
        if (e.matches) {
            if (siteNav.classList.contains('is-active')) {
                toggleMenu(false, false);
                log("Menu state reset due to resize.");
            }
        }
    };

    mediaQuery.addEventListener('change', handleResize);
    handleResize(mediaQuery);

    // --- 5. note RSS 読み込みと表示 ---
    const rssContainer = document.getElementById('note-rss');
    if (rssContainer) {
        const rssUrl = 'https://note.com/noted_pipit7032/rss';
        const apiUrl = `https://api.rss2json.com/v1/api.json?rss_url=${encodeURIComponent(rssUrl)}`;

        fetch(apiUrl)
            .then(response => {
                if (!response.ok) throw new Error('Network response was not ok');
                return response.json();
            })
            .then(data => {
                if (data.status === 'ok') {
                    let html = '<ul class="note-list">';
                    data.items.slice(0, 5).forEach(item => {
                        const date = new Date(item.pubDate).toLocaleDateString('ja-JP');
                        html += `
                            <li class="note-item">
                                <span class="note-date">${date}</span>
                                <a href="${item.link}" target="_blank" rel="noopener noreferrer" class="note-title">
                                    ${item.title}
                                </a>
                            </li>`;
                    });
                    html += '</ul>';
                    rssContainer.innerHTML = html;
                    log("note RSS loaded successfully.");
                } else {
                    throw new Error('RSS conversion failed');
                }
            })
            .catch(err => {
                log(`RSS読み込み失敗: ${err.message}`, 'warn');
                rssContainer.innerHTML = '<p>記事は note にて公開しています。</p>';
            });
    }

    log("main.js loaded successfully.");
});