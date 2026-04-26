// Mock data and utility functions

// Authentication
function isLoggedIn() {
    const user = localStorage.getItem('user');
    if (!user) return false;
    const userData = JSON.parse(user);
    return userData.approved === true;
}

function initAuth() {
    const loginBtn = document.getElementById('loginBtn');
    const userInfo = document.getElementById('userInfo');
    const myGrammarLink = document.getElementById('myGrammarLink');
    const createBtn = document.getElementById('createBtn');

    if (isLoggedIn()) {
        const user = JSON.parse(localStorage.getItem('user'));
        if (loginBtn) loginBtn.style.display = 'none';
        if (userInfo) {
            userInfo.style.display = 'flex';
            document.getElementById('userEmail').textContent = user.email;
        }
        if (myGrammarLink) myGrammarLink.style.display = 'block';
        if (createBtn) createBtn.style.display = 'block';
    } else {
        if (loginBtn) loginBtn.style.display = 'block';
        if (userInfo) userInfo.style.display = 'none';
        if (myGrammarLink) myGrammarLink.style.display = 'none';
        if (createBtn) createBtn.style.display = 'none';
    }

    // Logout handler
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            localStorage.removeItem('user');
            window.location.href = 'index.html';
        });
    }

    // Login button handler
    if (loginBtn) {
        loginBtn.addEventListener('click', function() {
            window.location.href = 'login.html';
        });
    }
}

// Mock grammar data
function getRecommendedGrammar() {
    return [
        {
            id: 'g1',
            title: '～ている',
            meaning: '表示动作正在进行或状态的持续',
            level: 'N5',
            tags: ['动词', '进行时', '状态'],
            connection: '动词て形 + いる',
            context: '用于日常会话和书面语',
            examples: [
                { japanese: '今、勉強しています。', chinese: '现在正在学习。' },
                { japanese: '彼は東京に住んでいます。', chinese: '他住在东京。' }
            ]
        },
        {
            id: 'g2',
            title: '～ば～ほど',
            meaning: '越...越...',
            level: 'N3',
            tags: ['条件', '程度'],
            connection: '动词假定形 + ば + 同一动词辞书形 + ほど',
            context: '用于表达程度递增关系',
            examples: [
                { japanese: '勉強すればするほど、分かるようになります。', chinese: '越学习越明白。' },
                { japanese: '見れば見るほど、美しいと思います。', chinese: '越看越觉得美丽。' }
            ]
        },
        {
            id: 'g3',
            title: '～てしまう',
            meaning: '完全完成某动作，或表示遗憾',
            level: 'N4',
            tags: ['动词', '完成', '遗憾'],
            connection: '动词て形 + しまう',
            context: '口语中常缩略为～ちゃう/～じゃう',
            examples: [
                { japanese: '宿題を忘れてしまいました。', chinese: '忘记带作业了。（遗憾）' },
                { japanese: '全部食べてしまった。', chinese: '全部吃完了。（完成）' }
            ]
        }
    ];
}

function getGrammarById(id) {
    const allGrammar = getRecommendedGrammar();
    return allGrammar.find(g => g.id === id);
}

function searchGrammar(query) {
    const allGrammar = getRecommendedGrammar();
    const lowerQuery = query.toLowerCase();

    const bestMatch = allGrammar.find(g =>
        g.title.toLowerCase().includes(lowerQuery)
    );

    const similarCards = allGrammar.filter(g =>
        g.id !== bestMatch?.id &&
        (g.meaning.includes(query) || g.tags.some(t => t.includes(query)))
    ).slice(0, 3);

    return {
        best_match: bestMatch,
        similar_cards: similarCards,
        search_confidence: bestMatch ? 0.9 : 0.3,
        should_offer_ai_generation: !bestMatch
    };
}

function getSimilarGrammar(id) {
    const allGrammar = getRecommendedGrammar();
    return allGrammar.filter(g => g.id !== id).slice(0, 2);
}

function getPracticeQuestions(grammarId) {
    return [
        {
            question: '次の文の（　）に入る適切な言葉を選んでください。',
            options: ['している', 'します', 'した', 'しよう'],
            correctAnswer: 0,
            explanation: '「～ている」は動作の進行を表します。'
        },
        {
            question: '正しい文を選んでください。',
            options: [
                '彼は東京に住んています。',
                '彼は東京に住みています。',
                '彼は東京に住んでいます。',
                '彼は東京に住むています。'
            ],
            correctAnswer: 2,
            explanation: '「住む」の て形は「住んで」です。'
        }
    ];
}

function getFavorites() {
    const data = localStorage.getItem('favorites');
    return data ? JSON.parse(data) : [];
}

function saveFavorites(favorites) {
    localStorage.setItem('favorites', JSON.stringify(favorites));
}

function getRecentViews() {
    const data = localStorage.getItem('recent_views');
    return data ? JSON.parse(data) : [];
}

function saveRecentView(grammarId) {
    let views = getRecentViews();
    views = views.filter(v => v.id !== grammarId);
    views.unshift({ id: grammarId, timestamp: Date.now() });
    if (views.length > 20) views.length = 20;
    localStorage.setItem('recent_views', JSON.stringify(views));
}

function getCreatedGrammar() {
    const data = localStorage.getItem('created_grammar');
    return data ? JSON.parse(data) : [];
}

function saveCreatedGrammar(grammar) {
    const id = 'created_' + Date.now();
    grammar.id = id;
    grammar.createdTime = Date.now();

    let created = getCreatedGrammar();
    created.push(id);
    localStorage.setItem('created_grammar', JSON.stringify(created));

    return id;
}

function generateGrammarCard(grammarText, description) {
    return {
        title: grammarText,
        meaning: 'AI生成的含义说明',
        level: 'N3',
        connection: 'AI生成的接续方式',
        context: 'AI生成的语气和语境说明',
        examples: [
            { japanese: 'AI生成的例句1', chinese: '中文翻译1' },
            { japanese: 'AI生成的例句2', chinese: '中文翻译2' }
        ],
        tags: ['AI生成', '新文法'],
        questions: [
            { question: 'AI生成的选择题1' },
            { question: 'AI生成的选择题2' }
        ]
    };
}

function savePracticeResult(grammarId, correct, total) {
    const result = {
        grammarId: grammarId,
        correct: correct,
        total: total,
        timestamp: Date.now()
    };
    localStorage.setItem(`practice_result_${grammarId}_${Date.now()}`, JSON.stringify(result));
}
