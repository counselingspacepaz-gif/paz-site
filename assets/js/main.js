// サイト全体のJavaScriptロジック
document.addEventListener('DOMContentLoaded', () => {

    const navToggle = document.querySelector('.nav-toggle');
    const siteNav = document.querySelector('.site-nav');
    const body = document.body;

    // --- 1. ログ出力制御 (本番環境での抑制) ---
    // Canvas実行環境でのJEKYLL_ENVの定義がないため、ここでは厳密にチェック
    const isProduction = typeof JEKYLL_ENV !== 'undefined' && JEKYLL_ENV === 'production';
    
    /**
     * 環境に応じてログを出力する
     * @param {string} message - 出力するメッセージ
     * @param {'log'|'warn'} type - ログタイプ
     */
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
        return; // 要素がなければ処理を中断
    }
    
    const firstNavLink = siteNav.querySelector('ul a');

    // --- 2. ナビゲーション（ハンバーガーメニュー）の開閉制御 ---
    
    /**
     * メニューの状態をトグルし、関連するDOM属性とCSSクラスを制御する
     * @param {boolean} isActive - メニューを開く(true)か閉じる(false)か
     * @param {boolean} [focus=true] - 開く際に最初のリンクへフォーカスするか
     */
    const toggleMenu = (isActive, focus = true) => {
        // 1. クラスとARIA属性を更新
        siteNav.classList.toggle('is-active', isActive);
        navToggle.setAttribute('aria-expanded', isActive);

        // 2. スクロール停止の制御 (bodyにクラスを付け外し)
        body.classList.toggle('no-scroll', isActive);
        
        // 3. ARIAラベルを更新
        navToggle.setAttribute('aria-label', isActive ? 'メニューを閉じる' : 'メニューを開く');
        
        // 4. フォーカス管理: 開時に最初のリンクへ移動
        if (isActive && firstNavLink && focus) {
            firstNavLink.focus();
        }
    };

    // --- 3. イベントリスナーの設定 ---

    // トグルボタンのクリックイベント
    navToggle.addEventListener('click', () => {
        const isActive = !siteNav.classList.contains('is-active');
        toggleMenu(isActive);
        log(`Menu toggled: ${isActive ? 'Opened' : 'Closed'}`);
    });

    // メニュー項目クリックで閉じる (UX & A11y)
    siteNav.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            // リンクがクリックされたら必ず閉じる
            toggleMenu(false, false); 
            log("Menu closed after navigation link clicked.");
        });
    });

    // Escキーで閉じる (A11y/キーボード操作)
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && siteNav.classList.contains('is-active')) {
            toggleMenu(false);
            navToggle.focus(); // トグルボタンにフォーカスを戻す
            log("Menu closed via Esc key.");
        }
    });

    // --- 4. リサイズ時の状態整合（ブレークポイント監視） ---
    // 修正: @mediaの条件を直接値 (1024px) に変更
    const mediaQuery = window.matchMedia('(min-width: 1024px)');
    
    const handleResize = (e) => {
        // PCサイズになった場合
        if (e.matches) {
            // メニューが開いている状態であれば強制的に閉じる (不整合防止)
            if (siteNav.classList.contains('is-active')) {
                toggleMenu(false, false);
                log("Menu state reset due to resize crossing breakpoint (to desktop).");
            }
        }
    };

    // イベントリスナーを追加
    mediaQuery.addEventListener('change', handleResize);
    // 初回ロード時のチェックも実行
    handleResize(mediaQuery);

    log("main.js loaded successfully. (A11y and State Management complete)");
});