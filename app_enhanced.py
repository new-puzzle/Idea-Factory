"""
Idea Factory - Ultimate Edition
Combines the original Visualization/UI flow with the new Database and Advanced Prompts.
"""

import streamlit as st
import os
import sqlite3
from datetime import datetime
from anthropic import Anthropic

# --- 1. CONFIGURATION & STYLES ---
st.set_page_config(
    page_title="Idea Factory",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for mobile-friendly UI and Cards
st.markdown("""
<style>
    /* Mobile-optimized styles */
    .stButton > button {
        width: 100%;
        padding: 1rem;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 10px;
        margin: 0.5rem 0;
    }

    .stTextInput > div > div > input {
        font-size: 1.1rem;
        padding: 0.8rem;
    }

    /* Card-like containers for ideas */
    .idea-card {
        background-color: #f0f2f6;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 5px solid #FF4B4B;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .idea-card {
            background-color: #262730;
            border-left-color: #FF4B4B;
        }
    }

    /* Responsive text */
    h1 {
        font-size: 2rem !important;
    }

    h2 {
        font-size: 1.5rem !important;
    }

    h3 {
        font-size: 1.2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. DATABASE HANDLER (The Memory) ---
def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect('ideas.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            category TEXT,
            content TEXT,
            refined_plan TEXT,
            created_at TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

conn = init_db()

def save_to_history(topic, category, content, plan=None):
    """Save item to DB"""
    c = conn.cursor()
    # Check duplicates
    c.execute("SELECT id FROM ideas WHERE content = ?", (content,))
    if not c.fetchone():
        c.execute('''
            INSERT INTO ideas (topic, category, content, refined_plan, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (topic, category, content, plan, datetime.now()))
        conn.commit()
        return True
    return False

def delete_from_history(idea_id):
    c = conn.cursor()
    c.execute("DELETE FROM ideas WHERE id = ?", (idea_id,))
    conn.commit()

def get_history_items(category_filter=None):
    c = conn.cursor()
    if category_filter and category_filter != "All":
        c.execute("SELECT * FROM ideas WHERE category = ? ORDER BY created_at DESC", (category_filter,))
    else:
        c.execute("SELECT * FROM ideas ORDER BY created_at DESC")
    return c.fetchall()

# --- 3. AI ENGINE (The Brains) ---
# Initialize Anthropic
api_key = os.environ.get("ANTHROPIC_API_KEY")
# Fallback for local testing if needed, though env var is best practice
if not api_key:
    # st.error("🚨 ANTHROPIC_API_KEY not found. Please set it in your environment variables.")
    # st.stop()
    pass 

# Initialize client (Handle missing key gracefully if possible, or fail)
try:
    client = Anthropic(api_key=api_key)
except:
    client = None

def get_category_config(category):
    """Returns Persona and Examples"""
    configs = {
        "work": {
            "role": "You are a Y-Combinator Startup Advisor.",
            "focus": "Market viability, scalability, and business models.",
            "good": "Topic: 'AI + Agri' -> Idea: 'CropVision API': SaaS using drone imagery...",
            "bad": "Topic: 'AI + Agri' -> Idea: 'Use AI to farm': Robots planting seeds..."
        },
        "learning": {
            "role": "You are an Educational Psychologist.",
            "focus": "Retention, engagement, and active recall.",
            "good": "Topic: 'History + VR' -> Idea: 'The Empathy Engine': VR roleplay...",
            "bad": "Topic: 'History + VR' -> Idea: 'VR Museum': Look at statues..."
        },
        "creative": {
            "role": "You are an Avant-Garde Art Director.",
            "focus": "Novelty, aesthetic impact, and breaking conventions.",
            "good": "Topic: 'Music + Arch' -> Idea: 'Resonant Brutalism': Walls moving with sound...",
            "bad": "Topic: 'Music + Arch' -> Idea: 'Guitar Building': Shaped like guitar..."
        },
        "task": {
            "role": "You are a Senior Project Manager.",
            "focus": "Speed, resource optimization, and efficiency.",
            "good": "Topic: 'Clean + Game' -> Idea: 'Dust-Buster AR': Gamified cleaning...",
            "bad": "Topic: 'Clean + Game' -> Idea: 'Cleaning Points': Get points..."
        },
        "general": {
            "role": "You are a Polymath Futurist.",
            "focus": "Unexpected intersections and cross-pollination.",
            "good": "Topic: 'Cook + Chem' -> Idea: 'Edible pH': Sauce changing color...",
            "bad": "Topic: 'Cook + Chem' -> Idea: 'Science Cook': Using beakers..."
        }
    }
    return configs.get(category, configs["general"])

def generate_ideas(topic, category):
    if not client:
        st.error("Anthropic API Key missing.")
        return []
        
    try:
        with st.spinner(f"🧠 Generating ideas via {category} persona..."):
            cfg = get_category_config(category)
            prompt = f"""
{cfg['role']}
Generate 5 high-quality, actionable ideas combining: {topic}.
FOCUS: {cfg['focus']}

GOOD EXAMPLE: {cfg['good']}
BAD EXAMPLE: {cfg['bad']}

CONSTRAINTS:
1. Specific mechanism of action required.
2. No generic buzzwords.
3. Format: - Idea Title: Description
"""
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            text = message.content[0].text
            # Robust parsing
            ideas = [line.strip()[1:].strip() for line in text.split('\n') if line.strip().startswith('-')]
            if not ideas: ideas = [l.strip() for l in text.split('\n') if len(l) > 10]
            return ideas[:5]
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return []

def refine_idea(idea, category):
    if not client: return None
    try:
        with st.spinner("✨ Creating strategic plan..."):
            cfg = get_category_config(category)
            prompt = f"""
{cfg['role']}
Critique and plan this idea: "{idea}"
Output a Markdown table: Phase | Critical Task | The Trap (Risk) | Resource
Follow with a paragraph: "The Secret Sauce".
"""
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def create_visualization(ideas, topic):
    if not client: return None
    try:
        with st.spinner("🎨 creating mind map..."):
            ideas_text = "\n".join(ideas)
            prompt = f"""
Format these ideas into a Mermaid.js mind map.
Root node: {topic}
Output ONLY the mermaid code block.
Format:
mindmap
  root(({topic}))
    Idea1
    Idea2
    
Ideas to map:
{ideas_text}
"""
            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# --- 4. MAIN APP LOGIC ---

# Initialize Session State
if 'ideas' not in st.session_state: st.session_state.ideas = []
if 'selected_idea' not in st.session_state: st.session_state.selected_idea = None
if 'refined_plan' not in st.session_state: st.session_state.refined_plan = None
if 'visualization' not in st.session_state: st.session_state.visualization = None
if 'topic' not in st.session_state: st.session_state.topic = ""
if 'category' not in st.session_state: st.session_state.category = "general"

# Sidebar History
with st.sidebar:
    st.header("📚 History")
    cat_filter = st.selectbox("Filter", ["All", "work", "learning", "creative", "task", "general"])
    history = get_history_items(cat_filter)
    
    if not history:
        st.caption("No saved ideas yet.")
        
    for item in history:
        # item: id, topic, category, content, plan, date
        db_id, db_topic, db_cat, db_content, db_plan, db_date = item
        title = db_content.split(":")[0] if ":" in db_content else db_content[:20]
        
        with st.expander(f"{title}"):
            st.caption(f"{db_topic} | {db_cat}")
            if st.button("📂 Load", key=f"load_{db_id}"):
                st.session_state.ideas = [db_content] # Load as single idea list
                st.session_state.topic = db_topic
                st.session_state.category = db_cat
                st.session_state.selected_idea = db_content
                st.session_state.refined_plan = db_plan
                st.toast("Loaded into Results tab!", icon="✅")
            
            if st.button("🗑️ Delete", key=f"del_{db_id}"):
                delete_from_history(db_id)
                st.rerun()

# Main Header
st.title("💡 Idea Factory")
st.markdown("**Generate, Refine, and Visualize ideas with AI Experts.**")

# Navigation Tabs (RESTORED 4 TABS)
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📋 Results", "🔧 Refinement", "🎨 Visualization"])

# Tab 1: Generator
with tab1:
    col1, col2 = st.columns([3,1])
    with col1:
        topic_input = st.text_input("Topic", value=st.session_state.topic, placeholder="e.g. AI + Gardening")
    with col2:
        cat_input = st.selectbox("Persona", ["general", "work", "learning", "creative", "task"], 
                               index=["general", "work", "learning", "creative", "task"].index(st.session_state.category))
    
    if st.button("✨ Generate Ideas", type="primary"):
        if topic_input:
            st.session_state.topic = topic_input
            st.session_state.category = cat_input
            ideas = generate_ideas(topic_input, cat_input)
            if ideas:
                st.session_state.ideas = ideas
                st.session_state.visualization = None # Reset viz for new batch
                st.success(f"Generated {len(ideas)} ideas! Check Results tab.")
        else:
            st.warning("Enter a topic first.")
    
    # Quick examples
    st.markdown("### 💭 Example Topics")
    examples = [
        "blockchain + education",
        "psychology + game design",
        "renewable energy + fashion",
        "virtual reality + meditation"
    ]

    cols = st.columns(2)
    for idx, example in enumerate(examples):
        with cols[idx % 2]:
            if st.button(f"📌 {example}", key=f"ex_{idx}", use_container_width=True):
                st.session_state.topic = example
                st.session_state.category = cat_input
                ideas = generate_ideas(example, cat_input)
                if ideas:
                    st.session_state.ideas = ideas
                    st.session_state.visualization = None
                    st.success(f"Generated {len(ideas)} ideas! Check Results tab.")

# Tab 2: Results (With Save functionality)
with tab2:
    if st.session_state.ideas:
        st.markdown(f"### Ideas for: {st.session_state.topic}")
        for idx, idea in enumerate(st.session_state.ideas):
            with st.container():
                st.markdown(f"<div class='idea-card'>{idea}</div>", unsafe_allow_html=True)
                c1, c2 = st.columns([1, 4])
                with c1:
                    if st.button("💾 Save", key=f"save_{idx}"):
                        if save_to_history(st.session_state.topic, st.session_state.category, idea, st.session_state.refined_plan):
                            st.toast("Saved!", icon="💾")
                        else:
                            st.toast("Already saved.", icon="⚠️")
                with c2:
                    if st.button("Refine ➤", key=f"ref_{idx}"):
                        st.session_state.selected_idea = idea
                        plan = refine_idea(idea, st.session_state.category)
                        if plan:
                            st.session_state.refined_plan = plan
                            st.success("Refined! Check Refinement tab.")
    else:
        st.info("Generate ideas in the Home tab first.")

# Tab 3: Refinement
with tab3:
    if st.session_state.refined_plan:
        st.markdown(f"### Strategic Plan: {st.session_state.selected_idea}")
        st.markdown(st.session_state.refined_plan)
        st.download_button("Download Plan", st.session_state.refined_plan, "plan.md")
    elif st.session_state.selected_idea:
        st.warning("Idea selected but no plan generated. Click 'Refine' in Results tab.")
    else:
        st.info("Select an idea to refine first.")

# Tab 4: Visualization (RESTORED)
with tab4:
    st.header("Mind Map")
    if st.session_state.ideas:
        if st.button("🎨 Generate Mind Map", key="gen_viz"):
            viz = create_visualization(st.session_state.ideas, st.session_state.topic)
            if viz:
                st.session_state.visualization = viz
        
        if st.session_state.visualization:
            # Clean code block
            viz_text = st.session_state.visualization
            if "```mermaid" in viz_text:
                start = viz_text.find("```mermaid") + 10
                end = viz_text.find("```", start)
                viz_text = viz_text[start:end].strip()
            elif "```" in viz_text:
                start = viz_text.find("```") + 3
                end = viz_text.find("```", start)
                viz_text = viz_text[start:end].strip()
                
            st.code(viz_text, language="mermaid")
    else:
        st.info("Generate ideas first to create a visualization.")