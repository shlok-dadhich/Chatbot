"""
frontend/styles.py
------------------
Global CSS injected once at app startup via st.markdown.
"""

CSS_STYLES = """
<style>
:root {
    --bg-primary:   #0d0f14;
    --bg-secondary: #13161e;
    --bg-card:      #1a1d27;
    --bg-hover:     #1f2335;
    --bg-active:    #252a3d;
    --text-primary: #e2e8f0;
    --text-muted:   #64748b;
    --border:       #1e2436;
    --border-light: #2a2f45;
    --active-bar:   #6c7fc4;
    --danger:       #e05c5c;
    --radius:       10px;
}

html, body { background: var(--bg-primary); color: var(--text-primary); }

#MainMenu, footer { display: none !important; visibility: hidden; }

/* Keep header/toolbar available so collapsed sidebar can always be reopened */
[data-testid="stHeader"] {
    background: transparent !important;
    border: none !important;
}
[data-testid="stToolbar"] {
    right: 0.5rem !important;
}

/* ── Sidebar ─────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--bg-secondary);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] h1 {
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    padding: 14px 8px 10px 8px !important;
}

/* Standard sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    text-align: left !important;
    justify-content: flex-start !important;
    background: transparent;
    border: 1px solid transparent;
    border-radius: var(--radius);
    padding: 9px 14px;
    color: var(--text-primary);
    font-size: 0.875rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    transition: background 0.15s, border-color 0.15s;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--bg-hover);
    border-color: var(--border-light);
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: var(--bg-active) !important;
    border-color: var(--active-bar) !important;
    color: #fff !important;
    font-weight: 600 !important;
    padding-left: 20px !important;
    box-shadow: inset 3px 0 0 var(--active-bar) !important;
}

/* Delete (🗑️) button — compact, danger-coloured */
button[data-testid="baseButton-secondary"].delete-btn {
    background: transparent !important;
    border: none !important;
    color: var(--danger) !important;
    padding: 4px 6px !important;
    min-width: unset !important;
    width: auto !important;
    font-size: 0.8rem !important;
    opacity: 0.55;
    transition: opacity 0.15s;
}
button[data-testid="baseButton-secondary"].delete-btn:hover {
    opacity: 1;
}

/* ── Chat header ─────────────────────────────────────────────────── */
.chat-header {
    background: var(--bg-secondary);
    border-bottom: 1px solid var(--border);
    padding: 10px 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 50px;
    margin-bottom: 2rem;
}
.chat-header h1 {
    font-size: 1.2rem;
    font-weight: 600;
    margin: 0;
    text-align: center;
}

/* ── Memory page ─────────────────────────────────────────────────── */
.memory-hero {
    background: linear-gradient(135deg, #1c2235 0%, #141925 100%);
    border: 1px solid var(--border-light);
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 14px;
}
.memory-hero h1 { margin: 0; font-size: 1.45rem; font-weight: 700; color: #f8fafc; }
.memory-hero p  { margin: 6px 0 0 0; color: #b5c1d8; font-size: 0.95rem; }

.memory-card {
    background: var(--bg-card);
    border: 1px solid var(--border-light);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
}
.memory-card .memory-index {
    color: #9db0d9; font-size: 0.78rem;
    margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.04em;
}
.memory-card .memory-text { color: var(--text-primary); font-size: 0.96rem; line-height: 1.45; }
.memory-category {
    display: inline-block;
    margin-left: 8px;
    padding: 2px 8px;
    border: 1px solid var(--border-light);
    border-radius: 999px;
    font-size: 0.72rem;
    color: #c7d3ec;
    text-transform: capitalize;
}

.memory-empty {
    border: 1px dashed #34415f;
    border-radius: 12px;
    padding: 24px 18px;
    text-align: center;
    color: #9caac8;
    background: rgba(27,33,49,0.45);
}
</style>
"""
