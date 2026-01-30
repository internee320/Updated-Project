import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- 1. PAGE CONFIG ---
st.set_page_config(
    page_title="Email Dashboard", 
    page_icon="📧", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. CSS: DEFAULT DARK THEME & PRO ANIMATIONS ---
st.markdown("""
<style>
    /* --- IMPORTS --- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* --- VARIABLES (DEFAULT: DARK THEME) --- */
    :root {
        --primary: #818cf8;      /* Light Indigo */
        --secondary: #c084fc;    /* Purple */
        --accent: #38bdf8;
        
        /* Defaulting to Dark Colors */
        --bg-body: #0f172a;       /* Slate 900 (Dark Background) */
        --surface: #1e293b;       /* Slate 800 (Cards) */
        --surface-light: #334155; /* Slate 700 (Inputs) */
        --border: #334155;
        --text-main: #f8fafc;     /* Slate 50 (Light Text) */
        --text-light: #94a3b8;
        
        /* Dark Theme Shadows */
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.5);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.7);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.7);
        --shadow-glow: 0 0 0 10px rgba(129, 140, 248, 0.4);
    }

    /* --- LIGHT MODE OVERRIDE (System Preference) --- */
    @media (prefers-color-scheme: light) {
        :root {
            --bg-body: #f8fafc;       /* Slate 50 */
            --surface: #ffffff;
            --surface-light: #f1f5f9;
            --border: #e2e8f0;
            --text-main: #0f172a;     /* Slate 900 (Dark Text) */
            --text-light: #475569;
            
            /* Light Theme Shadows */
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.1);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.15);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
            --shadow-glow: 0 0 0 10px rgba(79, 70, 229, 0.5);
        }
    }

    /* --- GLOBAL --- */
    body {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-body);
        color: var(--text-main);
        transition: background-color 0.5s;
    }
    
    footer {visibility: hidden;}

    /* --- ANIMATIONS --- */
    /* Breathing Header */
    @keyframes breathe {
        0% { opacity: 0.8; transform: scale(0.98); }
        50% { opacity: 1; transform: scale(1); }
        100% { opacity: 0.8; transform: scale(0.98); }
    }

    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    @keyframes popIn {
        0% { opacity: 0; transform: scale(0.9); }
        60% { transform: scale(1.02); }
        100% { opacity: 1; transform: scale(1); }
    }

    @keyframes pulseGlow {
        0% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }
        50% { box-shadow: 0 0 0 15px rgba(99, 102, 241, 0); }
        100% { box-shadow: 0 0 0 0 rgba(99, 102, 241, 0.4); }
    }

    .main .block-container {
        padding-top: 2.5rem;
    }

    /* --- COMPONENTS --- */
    .glass-deck {
        background: rgba(15, 23, 42, 0.6); /* Darker glass for default dark theme */
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 40px;
        box-shadow: var(--shadow-lg);
        transition: all 0.4s ease;
    }
    .glass-deck:hover {
        border-color: var(--primary);
    }

    /* --- CARDS --- */
    .card {
        background-color: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 24px;
        box-shadow: var(--shadow-md);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .card:hover {
        transform: translateY(-6px);
        border-color: var(--primary);
        box-shadow: var(--shadow-glow);
    }

    /* --- INPUTS (Adapt to Dark/Light Theme) --- */
    div[data-testid="stTextInput"] > div > div > input, 
    .stTextInput input,
    input {
        background-color: var(--surface-light) !important;
        color: var(--text-main) !important;
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        padding: 14px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        -webkit-text-fill-color: var(--text-main) !important;
    }
    div[data-testid="stTextInput"] > div > div > input:focus, 
    .stTextInput input:focus,
    input:focus {
        border-color: var(--primary) !important;
        box-shadow: var(--shadow-glow) !important;
        outline: none !important;
    }
    
    /* Text Area */
    div[data-testid="stTextArea"] > div > div > textarea,
    .stTextArea textarea,
    textarea {
        background-color: var(--surface-light) !important;
        color: var(--text-main) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 14px !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        -webkit-text-fill-color: var(--text-main) !important;
    }

    /* --- BUTTONS --- */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s;
        border: none;
        box-shadow: var(--shadow-sm);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-glow);
    }
    .stButton > button[kind="primary"] {
        background-color: var(--primary) !important;
        color: #ffffff !important;
        animation: pulseGlow 2s infinite;
    }

    /* --- METRICS --- */
    .metric-val {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
        animation: popIn 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    }
    .metric-lbl {
        color: var(--text-light);
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    /* --- HEADER SHIMMER (Breathing + Gradient) --- */
    .shimmer-text {
        background: linear-gradient(120deg, var(--primary), var(--secondary), var(--primary));
        background-size: 200% auto;
        color: transparent;
        -webkit-background-clip: text;
        background-clip: text;
        animation: shimmer 5s linear infinite, breathe 5s ease-in-out infinite alternate;
    }

    /* --- EXPANDER --- */
    .streamlit-expanderHeader {
        background-color: var(--surface) !important;
        color: var(--text-main) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
        font-weight: 700;
        margin-bottom: 15px;
        box-shadow: var(--shadow-md);
        transition: all 0.2s;
        padding: 10px 20px;
    }
    .streamlit-expanderHeader:hover {
        border-color: var(--primary) !important;
        transform: translateY(-1px);
    }
    .streamlit-expanderHeader:focus,
    .streamlit-expanderHeader:active {
        background-color: var(--surface-light) !important;
        border-color: var(--primary) !important;
        box-shadow: var(--shadow-glow);
        color: var(--text-main) !important;
    }

    /* Hide Sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. DATA LOGIC ---
@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    df.columns = [c.strip().lower() for c in df.columns]
    
    if 'sender' not in df.columns:
        df['sender'] = df.get('email', df.get('username', 'Unknown'))
    if 'department' not in df.columns:
        df['department'] = 'General'
    if 'date' not in df.columns:
        df['date'] = pd.to_datetime(datetime.now())
    else:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Priority Logic
    if 'priority' not in df.columns:
        def get_prio(text):
            t = str(text).lower()
            spam_kws = ['lottery', 'winner', 'cash prize', 'click here', 'congratulations', 'free money', 'car', 'gift card']
            if any(kw in t for kw in spam_kws):
                return "Spam"
            if any(k in t for k in ['urgent', 'critical', 'deadline', 'alert']):
                return "High"
            elif any(k in t for k in ['invoice', 'reminder', 'meeting']):
                return "Medium"
            return "Normal"
        df['priority'] = (df['subject'].astype(str) + " " + df['body'].astype(str)).apply(get_prio)
        
    if 'cluster' not in df.columns:
        def get_cluster(text):
            t = str(text).lower()
            if any(k in t for k in ['server', 'login', 'tech', 'bug', 'security']):
                return "Tech"
            elif any(k in t for k in ['hr', 'lunch', 'event', 'policy']):
                return "HR"
            elif any(k in t for k in ['invoice', 'finance', 'pay', 'budget']):
                return "Finance"
            return "General"
        df['cluster'] = (df['subject'].astype(str) + " " + df['body'].astype(str)).apply(get_cluster)
        
    return df

# --- 4. STATE MANAGEMENT ---
if 'df' not in st.session_state:
    st.session_state.df = None
if 'filter_prio' not in st.session_state:
    st.session_state.filter_prio = 'All'

# --- 5. MAIN APP INTERFACE ---

# Header with Title Change & Breathing Animation
st.markdown("""
<div style='text-align:center; margin-bottom: 40px;'>
    <h1 class='shimmer-text' style='font-size: 3.5rem; font-weight: 800; margin: 0; letter-spacing: -2px;'>📧 Email Dashboard</h1>
    <p style='color: var(--text-light); font-weight: 500; font-size: 1.1rem; margin-top: 10px;'>Professional Analytics Platform</p>
</div>
""", unsafe_allow_html=True)

# --- UPLOAD ---
uploaded_file = st.file_uploader("Upload CSV Data", type=['csv'], label_visibility="collapsed")

# --- FILTER DECK ---
st.markdown("<div class='glass-deck'>", unsafe_allow_html=True)

# 4 Search Fields
s1, s2, s3, s4 = st.columns(4)
with s1:
    search_user = st.text_input("Sender", placeholder="Username...", label_visibility="collapsed")
with s2:
    search_dept = st.text_input("Department", placeholder="Dept...", label_visibility="collapsed")
with s3:
    search_subj = st.text_input("Subject Keyword", placeholder="In subject...", label_visibility="collapsed")
with s4:
    search_body = st.text_input("Body Keyword", placeholder="In body...", label_visibility="collapsed")

st.markdown("<div style='margin: 30px 0 15px 0; font-size: 0.9rem; font-weight: 700; color: var(--text-main); text-transform: uppercase;'>Filter By Priority</div>", unsafe_allow_html=True)

prio_btn_cols = st.columns(5)
prios = ['All', 'High', 'Medium', 'Normal', 'Spam']
current_prio = st.session_state.filter_prio

for i, p in enumerate(prios):
    with prio_btn_cols[i]:
        btn_type = "primary" if current_prio == p else "secondary"
        if st.button(p, key=f"prio_{p}", use_container_width=True, type=btn_type):
            st.session_state.filter_prio = p
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# --- LOGIC SECTION ---

if uploaded_file:
    st.session_state.df = load_data(uploaded_file)

df = st.session_state.df

if df is None:
    st.info("👋 Please upload a CSV file to visualize data.")
    st.stop()

# --- FILTERING ---
mask = pd.Series([True] * len(df))
if search_user: mask &= df['sender'].astype(str).str.lower().str.contains(search_user.lower(), na=False)
if search_dept: mask &= df['department'].astype(str).str.lower().str.contains(search_dept.lower(), na=False)
if search_subj: mask &= df['subject'].astype(str).str.lower().str.contains(search_subj.lower(), na=False)
if search_body: mask &= df['body'].astype(str).str.lower().str.contains(search_body.lower(), na=False)
if st.session_state.filter_prio != 'All': mask &= (df['priority'].astype(str) == st.session_state.filter_prio)

filtered_df = df[mask].reset_index(drop=True)

# --- METRICS ROW ---
m1, m2, m3, m4 = st.columns(4)

def render_metric(container, count, label, index):
    delay = index * 0.1
    container.markdown(f"""
    <div class='card' style='text-align:center; animation: popIn 0.6s ease-out {delay}s backwards;'>
        <div class='metric-val'>{count}</div>
        <div class='metric-lbl'>{label}</div>
    </div>
    """, unsafe_allow_html=True)

render_metric(m1, len(filtered_df), "Total", 0)
render_metric(m2, len(filtered_df[filtered_df['priority']=='High']), "High", 1)
render_metric(m3, len(filtered_df[filtered_df['priority']=='Spam']), "Spam", 2)
render_metric(m4, filtered_df['cluster'].nunique(), "Topics", 3)

# --- CHARTS ROW ---
c1, c2 = st.columns([2, 1])

@st.cache_data
def get_charts(df):
    df_c = df.copy()
    df_c['date'] = pd.to_datetime(df_c['date'], errors='coerce')
    df_c = df_c.dropna(subset=['date'])
    grp = df_c.groupby(df_c['date'].dt.date).size().reset_index(name='Count')
    
    fig1 = px.bar(grp, x='date', y='Count', template="simple_white", color='Count', color_continuous_scale='Viridis')
    fig1.update_traces(hovertemplate='<b>%{x}</b><br>Count: %{y}')
    fig1.update_layout(
        margin=dict(l=0, r=0, t=30, b=0), height=320,
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode='x unified'
    )
    
    cl_counts = df['cluster'].value_counts().reset_index()
    cl_counts.columns = ['Cluster', 'Count']
    fig2 = px.pie(cl_counts, values='Count', names='Cluster', template="simple_white", hole=0.6, color_discrete_sequence=px.colors.qualitative.Pastel)
    fig2.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=320, plot_bgcolor='rgba(0,0,0,0)', showlegend=True)
    return fig1, fig2

with c1:
    st.markdown("### Volume")
    fig1, _ = get_charts(filtered_df)
    st.plotly_chart(fig1, use_container_width=True, key="v1")

with c2:
    st.markdown("### Distribution")
    _, fig2 = get_charts(filtered_df)
    st.plotly_chart(fig2, use_container_width=True, key="v2")

# --- EMAIL LIST ---
st.markdown("### Inbox")

def summarize_text(text):
    if not text: return "No content."
    sentences = text.replace('\n', ' ').split('. ')
    summary = '. '.join(sentences[:3])
    if len(summary) > 150:
        summary = summary[:150] + "..."
    return summary

delay = 0.1
for idx, row in filtered_df.iterrows():
    p_color = "#818cf8" # Light Indigo (High)
    if row['priority'] == 'Spam': p_color = "#f59e0b" # Orange
    if row['priority'] == 'Normal': p_color = "#38bdf8" # Blue
    if row['priority'] == 'Medium': p_color = "#c084fc" # Purple
    
    st.markdown(f"""
    <style>
        #mail_{idx} {{
            animation: slideInUp 0.5s ease-out {delay}s backwards;
            border-left: 5px solid {p_color};
        }}
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<div id='mail_{idx}' class='card'>", unsafe_allow_html=True)
    
    with st.expander(f"**{row['subject']}** — *{row['sender']}*"):
        badge_html = f"""
        <div style='margin-bottom:15px;'>
            <span style='background:{p_color}20; color:{p_color}; padding:6px 12px; border-radius:8px; font-size:0.8rem; font-weight:700;'>{row['priority']}</span>
            <span style='background:var(--surface-light); color:var(--text-light); padding:6px 12px; border-radius:8px; font-size:0.8rem; font-weight:600; margin-left:8px;'>{row['department']}</span>
        </div>
        """
        st.markdown(badge_html, unsafe_allow_html=True)
        
        st.text_area("Email Body", str(row['body']), height=100, disabled=True, key=f"b_{idx}")
        
        if st.button("✨ Summarize Email", key=f"act_{idx}", use_container_width=True):
            summary = summarize_text(str(row['body']))
            st.success(f"**Summary:** {summary}")
                
    st.markdown("</div>", unsafe_allow_html=True)
    delay += 0.05

if filtered_df.empty:
    st.info("No emails found matching your filters.")