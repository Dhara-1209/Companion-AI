import streamlit as st
import requests
import time
from typing import List, Dict, Any
import os
import json
from pathlib import Path
import re

def format_assistant_response(content: str) -> str:
    """Format assistant response for better readability with bullet points and line breaks."""
    # Remove asterisks from the content first
    content = re.sub(r'\*+', '', content)
    
    # Split content into paragraphs
    paragraphs = content.split('\n\n')
    formatted_paragraphs = []
    
    for paragraph in paragraphs:
        # Clean up the paragraph
        paragraph = paragraph.strip()
        if not paragraph:
            continue
            
        # Check if this is a list or steps
        if any(paragraph.startswith(prefix) for prefix in ['1.', '2.', '3.', '4.', '5.', '•', '-', '*']):
            # This is already a list, format it as HTML list
            lines = paragraph.split('\n')
            list_items = []
            for line in lines:
                line = line.strip()
                if line:
                    # Remove existing bullet points and numbers
                    clean_line = re.sub(r'^[\d\.\-\*\•]\s*', '', line)
                    list_items.append(f"<li>{clean_line}</li>")
            if list_items:
                formatted_paragraphs.append(f"<ul>{''.join(list_items)}</ul>")
        else:
            # Check if this paragraph contains numbered steps or bullet points inline
            if re.search(r'\d+\.\s+|[\•\-\*]\s+', paragraph):
                # Split by numbers or bullet points and create a list
                parts = re.split(r'(\d+\.\s+|[\•\-\*]\s+)', paragraph)
                list_items = []
                current_item = ""
                
                for part in parts:
                    if re.match(r'\d+\.\s+|[\•\-\*]\s+', part):
                        if current_item.strip():
                            list_items.append(f"<li>{current_item.strip()}</li>")
                        current_item = ""
                    else:
                        current_item += part
                
                if current_item.strip():
                    list_items.append(f"<li>{current_item.strip()}</li>")
                
                if list_items:
                    formatted_paragraphs.append(f"<ul>{''.join(list_items)}</ul>")
            else:
                # Regular paragraph
                formatted_paragraphs.append(f"<p>{paragraph}</p>")
    
    # Join all formatted paragraphs
    formatted_content = '<div class="answer-content">' + ''.join(formatted_paragraphs) + '</div>'
    return formatted_content

# Page configuration
st.set_page_config(
    page_title="CompanionAI - Appliance Assistant",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, professional styling
st.markdown("""
<style>
    /* Main app styling */
    .main > div {
        padding-top: 2rem;
        color: #ffffff !important;  /* Make main text white */
    }
    
    /* Global text color override */
    .stMarkdown, .stText, .stSelectbox label, div[data-testid="stMarkdownContainer"] {
        color: #ffffff !important;
    }
    
    /* Sidebar text styling */
    .css-1d391kg, .css-1lcbmhc {
        color: #ffffff !important;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Chat container styling */
    .chat-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Sample query buttons */
    .sample-query {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        margin: 0.25rem;
        cursor: pointer;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    }
    
    .sample-query:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.5);
    }
    
    /* Safety alerts */
    .safety-alert {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        border: 2px solid #ff6b6b;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #d63031;
        font-weight: bold;
        box-shadow: 0 4px 20px rgba(255, 107, 107, 0.2);
    }
    
    /* Success alerts */
    .success-alert {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border: 2px solid #00b894;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #00695c;
        box-shadow: 0 4px 20px rgba(0, 184, 148, 0.2);
    }
    
    /* Answer box styling */
    .answer-box {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-left: 5px solid #fd79a8;
        padding: 1.5rem;
        margin: 1rem 0;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(253, 121, 168, 0.2);
    }
    
    /* Citation box */
    .citation-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 4px solid #2196f3;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(33, 150, 243, 0.2);
    }
    
    /* Input styling - Dark theme */
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;  /* Blue-purple gradient */
        border: 2px solid #74b9ff !important;
        border-radius: 25px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #74b9ff !important;
        box-shadow: 0 0 0 3px rgba(116, 185, 255, 0.4) !important;
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%) !important;  /* Brighter blue on focus */
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #f8f9fa !important;
    }
    
    /* Chat input styling */
    .stChatInput > div > div > input {
        background: linear-gradient(135deg, #e84393 0%, #fd79a8 100%) !important;  /* Pink gradient */
        border: 2px solid #fd79a8 !important;
        border-radius: 25px !important;
        color: white !important;
        padding: 1rem !important;
    }
    
    .stChatInput > div > div > input:focus {
        background: linear-gradient(135deg, #fd79a8 0%, #fdcb6e 100%) !important;  /* Pink-orange on focus */
        border-color: #fdcb6e !important;
        box-shadow: 0 0 0 3px rgba(253, 203, 110, 0.4) !important;
    }
    
    .stChatInput > div > div > input::placeholder {
        color: #f8f9fa !important;
    }
    
    /* Feedback buttons styling */
    .feedback-container {
        display: flex;
        gap: 10px;
        margin: 15px 0;
        justify-content: center;
    }
    
    .feedback-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 8px 16px;
        cursor: pointer;
        font-size: 0.9rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 3px 10px rgba(102, 126, 234, 0.3);
        min-width: 100px;
    }
    
    .feedback-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.5);
    }
    
    .feedback-btn.helpful {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        box-shadow: 0 3px 10px rgba(0, 184, 148, 0.3);
    }
    
    .feedback-btn.helpful:hover {
        box-shadow: 0 5px 15px rgba(0, 184, 148, 0.5);
    }
    
    .feedback-btn.not-helpful {
        background: linear-gradient(135deg, #e17055 0%, #fd79a8 100%);
        box-shadow: 0 3px 10px rgba(225, 112, 85, 0.3);
    }
    
    .feedback-btn.not-helpful:hover {
        box-shadow: 0 5px 15px rgba(225, 112, 85, 0.5);
    }
    
    /* Answer formatting */
    .answer-content {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        color: #ecf0f1;
        line-height: 1.6;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .answer-content h1, .answer-content h2, .answer-content h3 {
        color: #667eea !important;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    
    .answer-content ul, .answer-content ol {
        margin: 10px 0;
        padding-left: 20px;
    }
    
    .answer-content li {
        margin: 8px 0;
        line-height: 1.5;
    }
    
    .answer-content strong {
        color: #667eea;
        font-weight: 600;
    }
    
    .answer-content em {
        color: #bdc3c7;
        font-style: italic;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Feedback button specific styling */
    div[data-testid="column"] .stButton > button {
        font-size: 14px;
        padding: 8px 16px;
        min-height: 38px;
        width: 100%;
        border-radius: 20px;
    }
    
    /* Helpful button (green) */
    div[data-testid="column"]:nth-child(1) .stButton > button {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        box-shadow: 0 4px 15px rgba(39, 174, 96, 0.3);
    }
    
    div[data-testid="column"]:nth-child(1) .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(39, 174, 96, 0.4);
        transform: translateY(-2px);
    }
    
    /* Not helpful button (orange/red) */
    div[data-testid="column"]:nth-child(2) .stButton > button {
        background: linear-gradient(135deg, #e74c3c 0%, #f39c12 100%);
        box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
    }
    
    div[data-testid="column"]:nth-child(2) .stButton > button:hover {
        box-shadow: 0 6px 20px rgba(231, 76, 60, 0.4);
        transform: translateY(-2px);
    }
    
    /* Answer content styling */
    .answer-content {
        font-size: 16px;
        line-height: 1.6;
        color: #ffffff !important;  /* Make text white for better visibility */
    }
    
    .answer-content p {
        margin-bottom: 16px;
        text-align: justify;
        color: #ffffff !important;  /* Ensure paragraphs are white */
    }
    
    .answer-content ul {
        margin: 16px 0;
        padding-left: 20px;
    }
    
    .answer-content li {
        margin-bottom: 8px;
        list-style-type: disc;
        color: #ffffff !important;  /* Make list items white */
    }
    
    .answer-content li::marker {
        color: #74b9ff;  /* Light blue bullets for contrast */
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;  /* Purple gradient like buttons */
        border-radius: 25px !important;
        border: none !important;
        color: white !important;
        padding: 0.25rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .stSelectbox > div > div:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stSelectbox > div > div > select {
        background: transparent !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    .stSelectbox > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600 !important;
    }
    
    /* Metrics styling */
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 0.5rem 0;
    }
</style>""", unsafe_allow_html=True)

# Predefined brand/model suggestions
BRAND_MODEL_SUGGESTIONS = {
    "Samsung": ["WF42H5200", "WF45K6500AV", "RF23J9011SR", "DV45K6200EW", "MS23K3513AK"],
    "LG": ["MS2595DIS", "WM3488HW", "LRFVS3006S", "DLGX3471V", "LMC0975ST"],
    "Whirlpool": ["WOS51EC0HS", "WFW92HEFW", "WRS325SDHZ", "WED92HEFW", "WMH31017HZ"],
    "Bosch": ["BGL72294", "WAT28401UC", "B36CL80ENS", "WTG86401UC", "HMV8053U"],
    "Philips": ["HR7761", "HD9641/96", "HR1855/00", "HD9220/20", "HR2371/05"],
    "GE": ["GFW650SSNWW", "GNE27JSMSS", "GFD65ESSNWW", "JVM6175SKSS"],
    "KitchenAid": ["KSMSFTA", "KSEG700ESS", "KDFE104HPS", "KMCC5015GSS"],
    "Frigidaire": ["FFCE2238LS", "FGGH3047VF", "FFBD2406NS", "FGMV176NTF"]
}

# Sample queries for different appliances
SAMPLE_QUERIES = {
    "Washing Machine": [
        "E3 error code on my washing machine",
        "Washing machine not draining water",
        "Loud noise during spin cycle",
        "Door won't unlock after cycle",
        "Water not filling properly"
    ],
    "Oven": [
        "Oven not heating to correct temperature", 
        "F1 error code displayed",
        "Gas oven won't ignite",
        "Uneven cooking in oven",
        "Self-cleaning cycle not working"
    ],
    "Vacuum Cleaner": [
        "Vacuum has no suction power",
        "Vacuum overheating and shutting off",
        "Brush not spinning on vacuum",
        "Strange smell from vacuum",
        "Vacuum leaves dirt behind"
    ],
    "Microwave": [
        "Microwave not heating food",
        "Turntable not rotating",
        "Sparking inside microwave",
        "Door won't close properly",
        "Digital display not working"
    ],
    "Dishwasher": [
        "Dishes not getting clean",
        "Water pooling at bottom",
        "Dishwasher won't start cycle",
        "White spots on glassware",
        "Strange odor from dishwasher"
    ],
    "Mixer": [
        "Mixer not working at all speeds",
        "Strange grinding noise",
        "Bowl attachment won't lock",
        "Mixer overheating during use",
        "Beater hitting the bowl"
    ]
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_citations" not in st.session_state:
    st.session_state.show_citations = True
if "feedback_data" not in st.session_state:
    st.session_state.feedback_data = []

def display_safety_alert(safety_level: str, safety_message: str):
    """Display safety alerts with appropriate styling"""
    if safety_level in ["emergency", "danger"]:
        st.markdown(f"""
        <div class="safety-alert">
            ⚠️ SAFETY ALERT - {safety_level.upper()}<br>
            {safety_message}
        </div>
        """, unsafe_allow_html=True)
    elif safety_level == "caution":
        st.warning(f"⚠️ Caution: {safety_message}")

def get_brand_model_suggestions(brand: str) -> List[str]:
    """Get model suggestions for a given brand"""
    return BRAND_MODEL_SUGGESTIONS.get(brand, [])

def call_api(query: str, brand: str = None, model: str = None) -> Dict[str, Any]:
    """Call the CompanionAI API"""
    try:
        # Use the restructured backend API
        api_url = "http://localhost:8000/answer"
        
        payload = {
            "query": query,
            "brand": brand,
            "model": model,
            "k": 10
        }
        
        response = requests.post(api_url, json=payload, timeout=60)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "answer": f"API Error: {response.status_code}",
                "safety_flag": False,
                "safety_level": "safe",
                "sources": [],
                "processing_time": 0
            }
    except Exception as e:
        return {
            "answer": f"Connection Error: {str(e)}",
            "safety_flag": False,
            "safety_level": "safe", 
            "sources": [],
            "processing_time": 0
        }

def save_feedback(query: str, response: str, helpful: bool):
    """Save user feedback"""
    feedback = {
        "timestamp": time.time(),
        "query": query,
        "response": response,
        "helpful": helpful
    }
    st.session_state.feedback_data.append(feedback)
    
    # Save to file for persistence
    feedback_file = Path("data/feedback.jsonl")
    feedback_file.parent.mkdir(exist_ok=True)
    
    with open(feedback_file, "a") as f:
        f.write(json.dumps(feedback) + "\n")

def upload_manual():
    """Handle manual upload"""
    st.header("📁 Upload Appliance Manuals")
    
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload appliance manuals to expand the knowledge base"
    )
    
    if uploaded_files:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processing {uploaded_file.name}...")
            
            # Simulate processing (replace with actual API call)
            time.sleep(1)
            
            # Update progress
            progress = (i + 1) / len(uploaded_files)
            progress_bar.progress(progress)
        
        status_text.text("Upload complete!")
        st.success(f"Successfully processed {len(uploaded_files)} manual(s)")

def main_chat_interface():
    """Main chat interface with enhanced styling"""
    
    # Modern header
    st.markdown("""
    <div class="main-header">
        <h1>� CompanionAI - Intelligent Appliance Assistant</h1>
        <p>AI-powered appliance troubleshooting with safety-first approach</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced sidebar controls
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Brand selection with better styling
        brand = st.selectbox(
            "🏷️ Appliance Brand",
            [""] + list(BRAND_MODEL_SUGGESTIONS.keys()),
            help="Select your appliance brand for more accurate results"
        )
        
        # Model selection
        model = ""
        if brand:
            models = get_brand_model_suggestions(brand)
            model = st.selectbox(
                "📱 Model Number", 
                [""] + models,
                help="Choose your specific model if available"
            )
        
        # Citation toggle
        st.session_state.show_citations = st.checkbox(
            "📚 Show Source Citations", 
            value=st.session_state.show_citations,
            help="Display manual references with responses"
        )
        
        # Enhanced sample queries with better organization
        st.markdown("### 💡 Try These Questions")
        
        # Appliance type selector for relevant examples
        appliance_type = st.selectbox(
            "Select Appliance Type",
            list(SAMPLE_QUERIES.keys()),
            help="Choose your appliance type for relevant examples"
        )
        
        st.markdown("**Click any question to try it:**")
        for i, sample_query in enumerate(SAMPLE_QUERIES[appliance_type][:4]):
            if st.button(f"🔸 {sample_query}", key=f"sample_{appliance_type}_{i}", use_container_width=True):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": sample_query})
                
                # Get AI response
                with st.spinner("🤖 Analyzing your issue..."):
                    start_time = time.time()
                    response = call_api(sample_query, brand, model)
                    processing_time = time.time() - start_time
                
                # Store response
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["answer"],
                    "metadata": {
                        "safety_flag": response.get("safety_flag", False),
                        "safety_level": response.get("safety_level", "safe"),
                        "safety_message": response.get("safety_message"),
                        "sources": response.get("sources", []),
                        "processing_time": processing_time
                    }
                })
                st.rerun()
        
        # Quick action buttons
        st.markdown("### ⚡ Emergency & Quick Help")
        if st.button("🚨 Safety Emergency", key="emergency", type="primary", use_container_width=True):
            emergency_query = "I smell gas from my appliance and there are strange noises"
            st.session_state.messages.append({"role": "user", "content": emergency_query})
            with st.spinner("🚨 Emergency safety analysis..."):
                response = call_api(emergency_query, brand, model)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["answer"],
                    "metadata": {
                        "safety_flag": response.get("safety_flag", False),
                        "safety_level": response.get("safety_level", "safe"),
                        "safety_message": response.get("safety_message"),
                        "sources": response.get("sources", []),
                        "processing_time": 0
                    }
                })
            st.rerun()
    
    
    # Quick action buttons for common issues
    st.markdown("### 🚀 Quick Diagnosis")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔧 Won't Start", use_container_width=True):
            quick_query = "My appliance won't turn on or start"
            st.session_state.messages.append({"role": "user", "content": quick_query})
            with st.spinner("🔍 Analyzing power issues..."):
                response = call_api(quick_query, brand, model)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["answer"],
                    "metadata": {"safety_flag": response.get("safety_flag", False), "safety_level": response.get("safety_level", "safe"), "sources": response.get("sources", []), "processing_time": 0}
                })
            st.rerun()
    
    with col2:
        if st.button("⚠️ Error Code", use_container_width=True):
            error_query = "Error code displayed on my appliance screen"
            st.session_state.messages.append({"role": "user", "content": error_query})
            with st.spinner("🔍 Decoding error..."):
                response = call_api(error_query, brand, model)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["answer"], 
                    "metadata": {"safety_flag": response.get("safety_flag", False), "safety_level": response.get("safety_level", "safe"), "sources": response.get("sources", []), "processing_time": 0}
                })
            st.rerun()
    
    with col3:
        if st.button("🔊 Strange Noise", use_container_width=True):
            noise_query = "My appliance is making unusual or loud noises"
            st.session_state.messages.append({"role": "user", "content": noise_query})
            with st.spinner("🔍 Diagnosing sounds..."):
                response = call_api(noise_query, brand, model)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["answer"],
                    "metadata": {"safety_flag": response.get("safety_flag", False), "safety_level": response.get("safety_level", "safe"), "sources": response.get("sources", []), "processing_time": 0}
                })
            st.rerun()
    
    with col4:
        if st.button("🌡️ Temperature", use_container_width=True):
            temp_query = "Temperature or heating issues with my appliance"
            st.session_state.messages.append({"role": "user", "content": temp_query})
            with st.spinner("🔍 Checking thermal systems..."):
                response = call_api(temp_query, brand, model)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response["answer"],
                    "metadata": {"safety_flag": response.get("safety_flag", False), "safety_level": response.get("safety_level", "safe"), "sources": response.get("sources", []), "processing_time": 0}
                })
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat messages display
    for msg_idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            # Format assistant responses with better line breaks and bullet points
            if message["role"] == "assistant":
                content = message["content"]
                
                # Format the content for better readability
                formatted_content = format_assistant_response(content)
                st.markdown(formatted_content, unsafe_allow_html=True)
            else:
                st.write(message["content"])
            
            # Show additional info for assistant messages
            if message["role"] == "assistant" and "metadata" in message:
                metadata = message["metadata"]
                
                # Safety alerts
                if metadata.get("safety_flag"):
                    display_safety_alert(
                        metadata.get("safety_level", "caution"),
                        metadata.get("safety_message", "Safety concern detected")
                    )
                
                # Citations
                if st.session_state.show_citations and metadata.get("sources"):
                    with st.expander("📚 Sources & Citations"):
                        for i, source in enumerate(metadata["sources"]):
                            st.markdown(f"""
                            <div class="citation-box">
                                <strong>Source {i+1}:</strong> {source.get('filename', 'Unknown')}<br>
                                <strong>Page:</strong> {source.get('page', 'N/A')}<br>
                                <strong>Relevance:</strong> {source.get('relevance_score', 0):.2f}
                            </div>
                            """, unsafe_allow_html=True)
                
                # Feedback buttons with unique keys
                col1, col2, col3 = st.columns([2, 2, 6])
                with col1:
                    if st.button("👍 Helpful", key=f"helpful_{msg_idx}"):
                        if msg_idx > 0:  # Make sure there's a previous user message
                            save_feedback(
                                st.session_state.messages[msg_idx-1]["content"],
                                message["content"],
                                True
                            )
                            st.success("Thank you for your feedback!")
                
                with col2:
                    if st.button("👎 Not Helpful", key=f"not_helpful_{msg_idx}"):
                        if msg_idx > 0:  # Make sure there's a previous user message
                            save_feedback(
                                st.session_state.messages[msg_idx-1]["content"],
                                message["content"],
                                False
                            )
                            st.info("Thank you for your feedback. We'll improve!")
    
    # Chat input
    if prompt := st.chat_input("Ask about your appliance issue..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                start_time = time.time()
                response = call_api(prompt, brand, model)
                processing_time = time.time() - start_time
            
            # Display response
            st.write(response["answer"])
            
            # Store response with metadata
            st.session_state.messages.append({
                "role": "assistant",
                "content": response["answer"],
                "metadata": {
                    "safety_flag": response.get("safety_flag", False),
                    "safety_level": response.get("safety_level", "safe"),
                    "safety_message": response.get("safety_message"),
                    "sources": response.get("sources", []),
                    "processing_time": processing_time
                }
            })
            
            # Show performance metrics
            st.caption(f"⚡ Response time: {processing_time:.2f}s | Sources: {len(response.get('sources', []))}")

def main():
    """Main application"""
    
    # Navigation tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat Assistant", "📁 Upload Manuals", "📊 Analytics"])
    
    with tab1:
        main_chat_interface()
    
    with tab2:
        upload_manual()
    
    with tab3:
        st.header("📊 System Analytics")
        
        # Performance metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Queries", len(st.session_state.messages) // 2)
        
        with col2:
            if st.session_state.feedback_data:
                helpful_count = sum(1 for f in st.session_state.feedback_data if f["helpful"])
                satisfaction_rate = helpful_count / len(st.session_state.feedback_data) * 100
                st.metric("User Satisfaction", f"{satisfaction_rate:.1f}%")
            else:
                st.metric("User Satisfaction", "N/A")
        
        with col3:
            st.metric("System Status", "🟢 Online")
        
        # Feedback summary
        if st.session_state.feedback_data:
            st.subheader("Recent Feedback")
            for feedback in st.session_state.feedback_data[-5:]:
                emoji = "👍" if feedback["helpful"] else "👎"
                st.write(f"{emoji} {feedback['query'][:50]}...")

if __name__ == "__main__":
    main()