import streamlit as st
from query_data import get_answer  # expects get_answer(query, book_id)
import time
import random

ALICE_QUESTIONS = [
    "What is the story of Alice in Wonderland about?",
    "Who are the main characters in Alice in Wonderland?",
    "Describe the Mad Hatter's tea party.",
    "What happens in the Queen of Hearts' court?",
    "What is the symbolism behind the rabbit hole?",
    "How does Alice change throughout her journey?",
    "What role does the Cheshire Cat play in the story?",
    "Explain the riddle 'Why is a raven like a writing desk?'",
    "What does the White Rabbit represent?",
    "How does Carroll use nonsense and wordplay?",
]

JUNGLE_QUESTIONS = [
    "Who is Mowgli and what makes him special?",
    "Describe the character of Shere Khan.",
    "How is Mowgli raised by wolves?",
    "What is the significance of fire (the Red Flower)?",
    "Summarize the story of Rikki-Tikki-Tavi.",
    "What is the Law of the Jungle?",
    "How does Baloo teach Mowgli about life?",
    "What role does Bagheera play as Mowgli's mentor?",
    "Why does Shere Khan fear and hate humans?",
    "What lessons does Mowgli learn from his animal friends?",
]

BOOK_EMOJIS = {
    "alice": ["🎩", "🐰", "🫖", "🌹", "♠️", "♥️", "♣️", "♦️", "🍄", "🦋"],
    "jungle": ["🐅", "🐺", "🐻", "🐍", "🌿", "🌳", "🔥", "🏹", "🌙", "⭐"]
}

def inject_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    .block-container { 
        padding-top: 2rem; 
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    .main-header {
        text-align: center;
        margin-bottom: 3rem;
        animation: fadeInDown 0.8s ease-out;
    }
    
    .app-title {
        font-weight: 800;
        font-size: clamp(2.2rem, 5vw, 3.5rem);
        background: linear-gradient(135deg, #fff 0%, #f8f9ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 20px rgba(255,255,255,0.1);
    }
    
    .app-subtitle {
        font-size: 1.3rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 400;
        margin-bottom: 1rem;
    }
    
    .floating-emojis {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
        z-index: 0;
    }
    
    .emoji {
        position: absolute;
        font-size: 2rem;
        opacity: 0.1;
        animation: float 20s infinite linear;
    }
    
    @keyframes float {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 0.1; }
        90% { opacity: 0.1; }
        100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .search-container {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 600px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        animation: slideInUp 0.6s ease-out;
        position: relative;
        z-index: 10;
    }
    
    .search-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 20px;
        pointer-events: none;
    }
    
    .question-input input {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 15px !important;
        color: #2d3748 !important;
        font-size: 1.1rem !important;
        padding: 18px 20px !important;
        box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.1) !important;
        transition: all 0.3s ease !important;
        font-weight: 500 !important;
    }
    
    .question-input input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1), inset 0 2px 10px rgba(0, 0, 0, 0.1) !important;
        transform: translateY(-2px) !important;
    }
    
    .stForm button {
        font-size: 1.1rem !important;
        padding: 0.8rem 2rem;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white !important;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        margin-top: 1rem;
        position: relative;
        overflow: hidden;
    }
    
    .stForm button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
        animation: pulse 2s infinite;
    }
    
    .books-section {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
        animation: slideInUp 0.8s ease-out;
    }
    
    .book-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .book-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
    }
    
    .book-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
        border-radius: 20px;
        pointer-events: none;
    }
    
    .book-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        position: relative;
        z-index: 2;
    }
    
    .alice-title {
        background: linear-gradient(135deg, #ff6b9d 0%, #c44569 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .jungle-title {
        background: linear-gradient(135deg, #2ed573 0%, #17a085 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .question-grid {
        display: grid;
        gap: 0.8rem;
        position: relative;
        z-index: 2;
    }
    
    .question-btn {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        color: white !important;
        padding: 1rem 1.2rem !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        text-align: left !important;
        backdrop-filter: blur(10px) !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .question-btn:hover {
        background: rgba(255, 255, 255, 0.2) !important;
        transform: translateX(5px) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1) !important;
    }
    
    .answer-container {
        margin: 3rem auto;
        max-width: 800px;
        animation: slideInUp 0.6s ease-out;
    }
    
    .answer-box {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2.5rem;
        color: #2d3748;
        font-size: 1.1rem;
        line-height: 1.7;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        position: relative;
        font-weight: 400;
    }
    
    .answer-box::before {
        content: '💭';
        position: absolute;
        top: -10px;
        left: 30px;
        font-size: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.5rem;
        border-radius: 50%;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .sources-section {
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 2px solid rgba(102, 126, 234, 0.1);
    }
    
    .sources-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .source-item {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 8px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.5rem;
        color: #4a5568;
        font-weight: 500;
        border-left: 4px solid #667eea;
    }
    
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.1rem;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 2rem auto;
        max-width: 500px;
        animation: slideInUp 0.6s ease-out;
    }
    
    .footer {
        text-align: center;
        margin-top: 4rem;
        padding: 2rem;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.9rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: spin 1s ease-in-out infinite;
        margin-right: 0.5rem;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    .stats-bar {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .stat-item {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border-radius: 15px;
        padding: 1rem 1.5rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.2);
        min-width: 120px;
    }
    
    .stat-number {
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
        display: block;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 0.25rem;
    }
    
    @media (max-width: 768px) {
        .books-section {
            grid-template-columns: 1fr;
            gap: 1.5rem;
        }
        
        .search-container {
            margin: 1rem;
            padding: 1.5rem;
        }
        
        .book-card {
            padding: 1.5rem;
        }
        
        .stats-bar {
            gap: 1rem;
        }
        
        .stat-item {
            min-width: 100px;
            padding: 0.8rem 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_floating_emojis():
    """Create floating emoji animation"""
    all_emojis = BOOK_EMOJIS["alice"] + BOOK_EMOJIS["jungle"]
    selected_emojis = random.sample(all_emojis, min(8, len(all_emojis)))
    
    emoji_html = "<div class='floating-emojis'>"
    for i, emoji in enumerate(selected_emojis):
        left = random.randint(0, 100)
        delay = random.randint(0, 20)
        emoji_html += f"""
        <div class='emoji' style='left: {left}%; animation-delay: {delay}s;'>
            {emoji}
        </div>
        """
    emoji_html += "</div>"
    
    st.markdown(emoji_html, unsafe_allow_html=True)

def render_book_card(title, questions, book_id, emoji, gradient_class):
    """Render a book card with questions"""
    st.markdown(f"""
    <div class='book-card'>
        <div class='book-title {gradient_class}'>
            <span style='font-size: 2rem; margin-right: 0.5rem;'>{emoji}</span>
            {title}
        </div>
        <div class='question-grid'>
    """, unsafe_allow_html=True)
    
    for i, question in enumerate(questions):
        if st.button(
            question, 
            key=f"{book_id}_{i}", 
            help=f"Ask about {title}",
            use_container_width=True
        ):
            st.session_state.query = question
            st.session_state.run_query = True
            st.session_state.active_book = book_id
            st.rerun()
    
    st.markdown("</div></div>", unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Literary AI Explorer",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    inject_styles()
    create_floating_emojis()
    
    # Initialize session state
    if 'query' not in st.session_state: 
        st.session_state.query = ""
    if 'last_query' not in st.session_state: 
        st.session_state.last_query = ""
    if 'run_query' not in st.session_state: 
        st.session_state.run_query = False
    if 'active_book' not in st.session_state: 
        st.session_state.active_book = None
    if 'query_count' not in st.session_state: 
        st.session_state.query_count = 0
    
    # Header
    st.markdown("""
    <div class='main-header'>
        <h1 class='app-title'>Literary AI Explorer</h1>
        <p class='app-subtitle'>Discover the magic of classic literature through AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats bar
    st.markdown(f"""
    <div class='stats-bar'>
        <div class='stat-item'>
            <span class='stat-number'>{len(ALICE_QUESTIONS + JUNGLE_QUESTIONS)}</span>
            <div class='stat-label'>Sample Questions</div>
        </div>
        <div class='stat-item'>
            <span class='stat-number'>2</span>
            <div class='stat-label'>Classic Books</div>
        </div>
        <div class='stat-item'>
            <span class='stat-number'>{st.session_state.query_count}</span>
            <div class='stat-label'>Your Queries</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Search container
    with st.container():
        st.markdown("<div class='search-container'>", unsafe_allow_html=True)
        
        with st.form(key="question_form"):
            user_input = st.text_input(
                "Ask anything about Alice in Wonderland or The Jungle Book:",
                value=st.session_state.query,
                key="question_input",
                label_visibility="collapsed",
                placeholder="What deeper meanings can we find in Alice's adventures?",
                help="✨ Ask any question about characters, themes, symbolism, or plot details"
            )
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                ask_btn = st.form_submit_button("🔍 Explore", use_container_width=True)
                
            if ask_btn and user_input.strip():
                st.session_state.query = user_input
                st.session_state.run_query = True
                st.session_state.active_book = None
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Book cards section
    st.markdown("<div class='books-section'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_book_card(
            "Alice in Wonderland", 
            ALICE_QUESTIONS, 
            "alice", 
            "🎩", 
            "alice-title"
        )
    
    with col2:
        render_book_card(
            "The Jungle Book", 
            JUNGLE_QUESTIONS, 
            "jungle", 
            "🐅", 
            "jungle-title"
        )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Process query
    query = st.session_state.query.strip()
    run = st.session_state.run_query
    last_query = st.session_state.last_query
    active_book = st.session_state.active_book
    
    if run and query and (query != last_query):
        # Determine book
        book_id = active_book
        if not book_id:
            # Enhanced book detection
            jungle_keywords = ["mowgli", "jungle", "baloo", "shere", "bagheera", "rikki", "wolf", "wolves", "fire", "red flower", "law of jungle"]
            alice_keywords = ["alice", "wonderland", "hatter", "queen", "hearts", "rabbit", "cheshire", "cat", "tea party", "mushroom"]
            
            query_lower = query.lower()
            jungle_score = sum(1 for word in jungle_keywords if word in query_lower)
            alice_score = sum(1 for word in alice_keywords if word in query_lower)
            
            book_id = "jungle" if jungle_score > alice_score else "alice"
        
        # Show loading animation
        with st.container():
            st.markdown("<div class='answer-container'>", unsafe_allow_html=True)
            loading_placeholder = st.empty()
            loading_placeholder.markdown("""
            <div class='answer-box' style='text-align: center; padding: 2rem;'>
                <div class='loading-spinner'></div>
                <span style='color: #667eea; font-weight: 600;'>Exploring the literary depths...</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Simulate processing time for better UX
        time.sleep(1)
        
        try:
            # Get the answer
            answer, sources = get_answer(query, book_id)
            
            # Update session state
            st.session_state.last_query = query
            st.session_state.run_query = False
            st.session_state.query_count += 1
            
            # Clear loading and show results
            loading_placeholder.empty()
            
            # Display answer
            st.markdown(f"""
            <div class='answer-box'>
                <strong style='color: #667eea; font-size: 1.2rem; display: block; margin-bottom: 1rem;'>
                    📖 Your Question: "{query}"
                </strong>
                {answer}
            """, unsafe_allow_html=True)
            
            # Display sources if available
            if sources:
                st.markdown("""
                <div class='sources-section'>
                    <div class='sources-title'>
                        📚 Sources Referenced
                    </div>
                """, unsafe_allow_html=True)
                
                for src in sources:
                    src_name = src.metadata.get("source", "Unknown source")
                    st.markdown(f"""
                    <div class='source-item'>
                        📄 {src_name}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
            
        except Exception as e:
            loading_placeholder.empty()
            st.markdown(f"""
            <div class='answer-box' style='border-left: 4px solid #e53e3e;'>
                <strong style='color: #e53e3e;'>⚠️ Error:</strong><br>
                Sorry, I encountered an issue while processing your question. Please try again or rephrase your query.
                <br><br>
                <small style='color: #666; font-style: italic;'>Technical details: {str(e)}</small>
            </div>
            """, unsafe_allow_html=True)
    
    elif not query:
        # Empty state
        st.markdown("""
        <div class='empty-state'>
            <div style='font-size: 3rem; margin-bottom: 1rem;'>📚✨</div>
            <strong>Ready to explore?</strong><br>
            Ask any question above or choose from our curated collection of sample questions.<br>
            <small style='opacity: 0.8; margin-top: 1rem; display: block;'>
                Discover hidden meanings, character insights, and literary themes!
            </small>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class='footer'>
        <div style='margin-bottom: 1rem;'>
            <strong>Literary AI Explorer</strong> - Powered by Advanced Language Models
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
