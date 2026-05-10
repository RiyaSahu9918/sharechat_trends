INDEX_HTML = """<!doctype html>
<html lang="hi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ShareChat Trends Prototype</title>
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #09090b;
      --bg-card: #18181b;
      --bg-hover: #27272a;
      --text-main: #f4f4f5;
      --text-muted: #a1a1aa;
      --accent: #3b82f6;
      --accent-hover: #2563eb;
      --border: #3f3f46;
      --gradient-start: #3b82f6;
      --gradient-end: #8b5cf6;
      --danger: #ef4444;
      --success: #22c55e;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body { 
      font-family: 'Inter', sans-serif; 
      background: var(--bg-dark); 
      color: var(--text-main); 
      -webkit-font-smoothing: antialiased;
    }
    
    .app-container {
      max-width: 480px;
      margin: 0 auto;
      min-height: 100vh;
      background: var(--bg-dark);
      position: relative;
      box-shadow: 0 0 40px rgba(0,0,0,0.5);
    }
    
    .header {
      position: sticky;
      top: 0;
      background: rgba(9, 9, 11, 0.85);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      padding: 16px 20px;
      border-bottom: 1px solid rgba(63, 63, 70, 0.4);
      z-index: 50;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .header-title {
      font-size: 22px;
      font-weight: 800;
      background: linear-gradient(135deg, var(--text-main), var(--text-muted));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    
    .header-subtitle {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 4px;
      font-weight: 500;
    }
    
    .content-area {
      padding: 16px;
    }
    
    .btn-refresh {
      width: 100%;
      background: linear-gradient(135deg, var(--gradient-start), var(--gradient-end));
      color: white;
      border: none;
      padding: 14px;
      border-radius: 12px;
      font-size: 15px;
      font-weight: 600;
      cursor: pointer;
      margin-bottom: 20px;
      transition: opacity 0.2s, transform 0.1s;
      box-shadow: 0 4px 14px rgba(59, 130, 246, 0.3);
    }
    
    .btn-refresh:active {
      transform: scale(0.98);
    }
    
    .btn-icon {
      background: transparent;
      color: var(--text-main);
      border: none;
      cursor: pointer;
      padding: 8px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .btn-icon:hover {
      background: var(--bg-hover);
    }

    .trend-card {
      background: var(--bg-card);
      border: 1px solid rgba(63, 63, 70, 0.3);
      border-radius: 16px;
      padding: 16px;
      margin-bottom: 16px;
      cursor: pointer;
      transition: all 0.2s ease;
      position: relative;
      overflow: hidden;
    }
    
    .trend-card:hover {
      background: var(--bg-hover);
      border-color: rgba(63, 63, 70, 0.8);
      transform: translateY(-2px);
    }
    
    .trend-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 10px;
    }
    
    .rank-badge {
      font-size: 14px;
      font-weight: 800;
      color: var(--accent);
      background: rgba(59, 130, 246, 0.1);
      padding: 4px 10px;
      border-radius: 8px;
    }
    
    .category-chip {
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      font-weight: 700;
      color: var(--text-muted);
      background: rgba(255, 255, 255, 0.05);
      padding: 4px 8px;
      border-radius: 6px;
    }
    
    .trend-title {
      font-size: 18px;
      font-weight: 700;
      margin-bottom: 6px;
      line-height: 1.3;
    }
    
    .trend-desc {
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.5;
      margin-bottom: 12px;
    }
    
    .trend-metrics {
      display: flex;
      gap: 16px;
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .metric {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 13px;
      color: var(--text-muted);
      font-weight: 500;
    }
    
    .metric.heat {
      color: #fb923c;
    }
    
    /* Detail View Styles */
    .detail-hero {
      padding: 24px 20px;
      background: linear-gradient(180deg, rgba(59,130,246,0.1) 0%, var(--bg-dark) 100%);
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .detail-title {
      font-size: 26px;
      font-weight: 800;
      margin-bottom: 12px;
      line-height: 1.2;
    }
    
    .ai-summary {
      margin: 20px 16px;
      padding: 16px;
      background: linear-gradient(145deg, rgba(139, 92, 246, 0.15), rgba(59, 130, 246, 0.05));
      border: 1px solid rgba(139, 92, 246, 0.3);
      border-radius: 16px;
      position: relative;
    }
    
    .ai-summary::before {
      content: '✨ AI Summary';
      font-size: 12px;
      font-weight: 700;
      color: #a78bfa;
      display: block;
      margin-bottom: 8px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    
    .ai-summary p {
      font-size: 15px;
      line-height: 1.6;
      color: #e2e8f0;
    }
    
    .stats-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      padding: 0 16px;
      margin-bottom: 24px;
    }
    
    .stat-card {
      background: var(--bg-card);
      padding: 16px;
      border-radius: 12px;
      border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .stat-value {
      font-size: 20px;
      font-weight: 700;
      margin-bottom: 4px;
    }
    
    .stat-label {
      font-size: 12px;
      color: var(--text-muted);
      font-weight: 500;
    }
    
    .post-card {
      margin: 0 16px 16px 16px;
      background: var(--bg-card);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 16px;
      padding: 16px;
    }
    
    .post-header {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 12px;
    }
    
    .avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: linear-gradient(135deg, #4ade80, #3b82f6);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: bold;
      color: white;
    }
    
    .author-name {
      font-weight: 600;
      font-size: 15px;
    }
    
    .post-time {
      font-size: 12px;
      color: var(--text-muted);
    }
    
    .post-content {
      font-size: 15px;
      line-height: 1.5;
      margin-bottom: 16px;
    }
    
    .post-actions {
      display: flex;
      justify-content: space-between;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      padding-top: 12px;
    }
    
    .action-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 14px;
      font-weight: 500;
      display: flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
    }
    
    .action-btn:hover {
      color: var(--text-main);
    }
    
    .loader {
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 40px;
    }
    
    .spinner {
      width: 32px;
      height: 32px;
      border: 3px solid rgba(255,255,255,0.1);
      border-radius: 50%;
      border-top-color: var(--accent);
      animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
  </style>
</head>
<body>
  <div id="root"></div>

  <script type="text/babel">
    const { useState, useEffect } = React;

    // Minimal SVG Icons
    const Icons = {
      Flame: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M8.5 14.5A2.5 2.5 0 0011 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 11-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 002.5 2.5z"/></svg>,
      Eye: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>,
      Search: () => <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>,
      Back: () => <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>,
      Heart: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>,
      Message: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>,
      Share: () => <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>
    };

    function App() {
      const [view, setView] = useState('feed');
      const [trends, setTrends] = useState([]);
      const [activeTrendId, setActiveTrendId] = useState(null);
      const [activeTrendData, setActiveTrendData] = useState(null);
      const [loading, setLoading] = useState(true);
      const [lastUpdated, setLastUpdated] = useState('');

      const fetchTrends = async () => {
        setLoading(true);
        try {
          // Adjust API endpoint port depending on where Python is running
          const response = await fetch('/api/trends?limit=10');
          const data = await response.json();
          setTrends(data);
          setLastUpdated(new Date().toLocaleTimeString('hi-IN'));
        } catch (e) {
          console.error("Error fetching trends", e);
        }
        setLoading(false);
      };

      const handleRegenerate = async () => {
        setLoading(true);
        try {
          await fetch('/api/trends/generate', { method: 'POST' });
          await fetchTrends();
        } catch (e) {
          console.error("Error regenerating trends", e);
        }
      };

      const openDetail = async (id) => {
        setView('detail');
        setLoading(true);
        try {
          const response = await fetch(`/api/trends/${id}`);
          const data = await response.json();
          setActiveTrendData(data);
        } catch (e) {
          console.error("Error fetching detail", e);
        }
        setLoading(false);
      };

      useEffect(() => {
        fetchTrends();
      }, []);

      const formatNumber = (num) => {
        if (num >= 100000) return (num / 100000).toFixed(1) + 'M';
        if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
        return num;
      };

      if (view === 'detail') {
        return (
          <div className="app-container">
            <div className="header">
              <button className="btn-icon" onClick={() => { setView('feed'); setActiveTrendData(null); }}>
                <Icons.Back />
              </button>
              <div style={{fontWeight: 600}}>ट्रेंड डिटेल</div>
              <div style={{width: 40}}></div>
            </div>
            
            {loading || !activeTrendData ? (
              <div className="loader"><div className="spinner"></div></div>
            ) : (
              <div style={{paddingBottom: 40}}>
                <div className="detail-hero">
                  <div className="category-chip" style={{display: 'inline-block', marginBottom: 12}}>
                    {activeTrendData.category}
                  </div>
                  <h1 className="detail-title">{activeTrendData.title_hi}</h1>
                  <p className="trend-desc">{activeTrendData.description_hi}</p>
                </div>
                
                <div className="ai-summary">
                  <p>{activeTrendData.summary_hi}</p>
                </div>

                <div className="stats-grid">
                  <div className="stat-card">
                    <div className="stat-value">{formatNumber(activeTrendData.daily_active_users_clicks)}</div>
                    <div className="stat-label">डेली क्लिक्स</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value">{formatNumber(activeTrendData.views)}</div>
                    <div className="stat-label">कुल व्यूज</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value">{activeTrendData.mobile_os_type.split(':')[0]}</div>
                    <div className="stat-label">प्रमुख OS</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-value">{activeTrendData.heat_score}</div>
                    <div className="stat-label">हीट स्कोर</div>
                  </div>
                </div>

                <h3 style={{margin: '24px 16px 16px', fontSize: 18}}>संबंधित पोस्ट्स</h3>
                
                {activeTrendData.posts.map(post => (
                  <div className="post-card" key={post.id}>
                    <div className="post-header">
                      <div className="avatar">{post.author_name.charAt(0).toUpperCase()}</div>
                      <div>
                        <div className="author-name">@{post.author_name}</div>
                        <div className="post-time">2 घंटे पहले</div>
                      </div>
                    </div>
                    <div className="post-content">
                      {post.content_text} <span style={{color: 'var(--accent)'}}>{activeTrendData.tag}</span>
                    </div>
                    <div className="post-actions">
                      <button className="action-btn"><Icons.Heart /> {formatNumber(post.likes)}</button>
                      <button className="action-btn"><Icons.Message /> {formatNumber(post.comments)}</button>
                      <button className="action-btn"><Icons.Share /> {formatNumber(post.shares)}</button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        );
      }

      return (
        <div className="app-container">
          <div className="header">
            <div>
              <div className="header-title">ट्रेंडिंग नाउ</div>
              <div className="header-subtitle">अपडेटेड: {lastUpdated}</div>
            </div>
            <div className="avatar" style={{width: 32, height: 32, fontSize: 12}}>U</div>
          </div>
          
          <div className="content-area">
            <button className="btn-refresh" onClick={handleRegenerate} disabled={loading}>
              {loading ? 'रिफ्रेशिंग...' : 'नए ट्रेंड्स रिफ्रेश करें'}
            </button>
            
            {loading ? (
              <div className="loader"><div className="spinner"></div></div>
            ) : (
              <div>
                {trends.map((t) => (
                  <div className="trend-card" key={t.id} onClick={() => openDetail(t.id)}>
                    <div className="trend-header">
                      <div className="rank-badge">#{t.rank}</div>
                      <div className="category-chip">{t.category}</div>
                    </div>
                    <div className="trend-title">{t.tag}</div>
                    <div className="trend-desc">{t.title_hi}</div>
                    
                    <div className="trend-metrics">
                      <div className="metric heat">
                        <Icons.Flame /> {t.heat_score}
                      </div>
                      <div className="metric">
                        <Icons.Eye /> {formatNumber(t.views)}
                      </div>
                      <div className="metric">
                        <Icons.Search /> {formatNumber(t.searches_in_last_30mins)}/hr
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      );
    }

    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<App />);
  </script>
</body>
</html>
"""
