"""
Idea Factory - Frontend
Streamlit interface for the Idea Factory app
"""

import streamlit as st
import requests
import os
from anthropic import Anthropic

# Page config for mobile optimization
st.set_page_config(
    page_title="Idea Factory",
    page_icon="💡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-friendly UI
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
        border-left: 4px solid #4CAF50;
    }

    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .idea-card {
            background-color: #262730;
            border-left-color: #66BB6A;
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

# Initialize session state
if 'ideas' not in st.session_state:
    st.session_state.ideas = []
if 'selected_idea' not in st.session_state:
    st.session_state.selected_idea = None
if 'refined_plan' not in st.session_state:
    st.session_state.refined_plan = None
if 'visualization' not in st.session_state:
    st.session_state.visualization = None
if 'topic' not in st.session_state:
    st.session_state.topic = ""

# Initialize Anthropic client (for direct API calls instead of backend)
client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


def generate_ideas(topic):
    """Generate ideas using Claude API directly"""
    try:
        with st.spinner("🧠 Generating novel ideas..."):
            prompt = f"""Generate 10 creative, actionable ideas combining {topic}.
Each idea should be unique, specific, and formatted as a bullet point.
Avoid generic suggestions. Focus on novel cross-disciplinary approaches.

Format each idea as:
- [Idea title]: [Brief description]

Be creative and think outside the box!"""

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = message.content[0].text
            ideas = [line.strip() for line in response_text.split('\n') if line.strip().startswith('-')]

            if not ideas:
                ideas = response_text.split('\n')
                ideas = [idea.strip() for idea in ideas if idea.strip()]

            return ideas[:10]
    except Exception as e:
        st.error(f"Error generating ideas: {str(e)}")
        return []


def refine_idea(idea):
    """Refine an idea into a detailed plan"""
    try:
        with st.spinner("✨ Refining your idea..."):
            prompt = f"""Refine the following idea into a detailed plan: "{idea}".

Output a markdown table with columns: Task | Challenges | Resources.
Include 3-5 tasks, 2-3 challenges per task, and specific resources/tools.

Make it actionable and practical."""

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return message.content[0].text
    except Exception as e:
        st.error(f"Error refining idea: {str(e)}")
        return None


def create_visualization(ideas, topic):
    """Create a Mermaid.js visualization"""
    try:
        with st.spinner("🎨 Creating visualization..."):
            ideas_text = "\n".join(ideas)

            prompt = f"""Format the following ideas into a Mermaid.js mind map:

{ideas_text}

Root node: {topic}

Create a clean mind map using mermaid syntax. Output ONLY the mermaid code block without any explanation.

Format it as:

```mermaid
mindmap
  root(({topic}))
    Category1
      idea1
      idea2
    Category2
      idea3
      idea4
```

Make it visually organized and clear."""

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            return message.content[0].text
    except Exception as e:
        st.error(f"Error creating visualization: {str(e)}")
        return None


# Header
st.title("💡 Idea Factory")
st.markdown("**Generate novel, cross-disciplinary ideas and refine them into actionable plans**")
st.markdown("---")

# Navigation
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Home", "📋 Results", "🔧 Refinement", "🎨 Visualization"])

# Tab 1: Home - Input
with tab1:
    st.header("Generate Ideas")
    st.markdown("Combine any topics or concepts to generate creative, actionable ideas!")

    topic = st.text_input(
        "Enter your topic (e.g., 'quantum physics + storytelling')",
        value=st.session_state.topic,
        placeholder="artificial intelligence + gardening",
        help="Combine different concepts with '+' for cross-disciplinary ideas"
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button("✨ Generate Ideas", type="primary", use_container_width=True):
            if topic:
                st.session_state.topic = topic
                ideas = generate_ideas(topic)
                if ideas:
                    st.session_state.ideas = ideas
                    st.session_state.selected_idea = None
                    st.session_state.refined_plan = None
                    st.session_state.visualization = None
                    st.success(f"Generated {len(ideas)} ideas! Check the Results tab.")
            else:
                st.warning("Please enter a topic first!")

    with col2:
        if st.button("🔄 Clear", use_container_width=True):
            st.session_state.ideas = []
            st.session_state.selected_idea = None
            st.session_state.refined_plan = None
            st.session_state.visualization = None
            st.session_state.topic = ""
            st.rerun()

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
                ideas = generate_ideas(example)
                if ideas:
                    st.session_state.ideas = ideas
                    st.success("Ideas generated! Check the Results tab.")

# Tab 2: Results - Display Ideas
with tab2:
    st.header("Generated Ideas")

    if st.session_state.ideas:
        st.markdown(f"**Topic:** {st.session_state.topic}")
        st.markdown("---")

        for idx, idea in enumerate(st.session_state.ideas):
            with st.container():
                col1, col2 = st.columns([5, 1])
                with col1:
                    st.markdown(f"**{idx + 1}.** {idea}")
                with col2:
                    if st.button("🔧 Refine", key=f"refine_{idx}", use_container_width=True):
                        st.session_state.selected_idea = idea
                        plan = refine_idea(idea)
                        if plan:
                            st.session_state.refined_plan = plan
                            st.success("Idea refined! Check the Refinement tab.")
                st.markdown("---")

        # Export options
        st.markdown("### 📤 Export Ideas")
        ideas_text = "\n".join([f"{i+1}. {idea}" for i, idea in enumerate(st.session_state.ideas)])
        st.download_button(
            "💾 Download as Text",
            ideas_text,
            file_name=f"ideas_{st.session_state.topic.replace(' ', '_')}.txt",
            use_container_width=True
        )
    else:
        st.info("No ideas generated yet. Go to the Home tab to get started!")

# Tab 3: Refinement - Show Detailed Plan
with tab3:
    st.header("Idea Refinement")

    if st.session_state.refined_plan:
        st.markdown(f"**Selected Idea:** {st.session_state.selected_idea}")
        st.markdown("---")
        st.markdown(st.session_state.refined_plan)

        # Export refined plan
        st.markdown("### 📤 Export Plan")
        st.download_button(
            "💾 Download Plan",
            st.session_state.refined_plan,
            file_name=f"plan_{st.session_state.selected_idea[:30].replace(' ', '_')}.md",
            use_container_width=True
        )
    elif st.session_state.ideas:
        st.info("Select an idea from the Results tab to refine it into a detailed plan!")
    else:
        st.info("No ideas available. Generate ideas first from the Home tab!")

# Tab 4: Visualization - Mind Map
with tab4:
    st.header("Idea Visualization")

    if st.session_state.ideas:
        if st.button("🎨 Create Mind Map", type="primary", use_container_width=True):
            viz = create_visualization(st.session_state.ideas, st.session_state.topic)
            if viz:
                st.session_state.visualization = viz

        if st.session_state.visualization:
            st.markdown("### Mind Map")

            # Extract mermaid code if wrapped in code block
            viz_text = st.session_state.visualization
            if "```mermaid" in viz_text:
                start = viz_text.find("```mermaid") + 10
                end = viz_text.find("```", start)
                viz_text = viz_text[start:end].strip()

            # Display using mermaid
            st.code(viz_text, language="mermaid")

            # Also show as text for copying
            with st.expander("📋 View Mermaid Code"):
                st.code(viz_text, language="markdown")
    else:
        st.info("No ideas available. Generate ideas first from the Home tab!")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Built with ❤️ using Streamlit and Claude AI"
    "</div>",
    unsafe_allow_html=True
)
