import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from datetime import datetime, date

load_dotenv()

class AstrologyResponse(BaseModel):
    birth_chart: str
    personality: str
    career_education: str
    finance: str
    relationships: str
    health: str
    family: str
    career_jobs: str
    life_periods: str
    remedies: str

# Streamlit Page Config
st.set_page_config(
    page_title="AI Astrology Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling - Mystical Astrology Theme
st.markdown("""
    <style>
    /* Main Background - Dark Purple with Starry Effect */
    .stApp {
        background: linear-gradient(135deg, #1a0033 0%, #2d1b4e 50%, #1a0033 100%);
        background-attachment: fixed;
    }
    
    /* Header/Top Bar - Dark Purple */
    header {
        background-color: #1a0033 !important;
        border-bottom: 2px solid #D4A574 !important;
    }
    
    [data-testid="stHeader"] {
        background-color: #1a0033 !important;
    }
    
    .stToolbar {
        background-color: #1a0033 !important;
    }
    
    /* Header buttons - Black */
    [data-testid="stHeader"] button,
    .stToolbar button {
        background-color: transparent !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
    }
    
    [data-testid="stHeader"] button:hover,
    .stToolbar button:hover {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    /* Text in header */
    [data-testid="stHeader"] {
        color: #000000 !important;
    }
    
    [data-testid="stHeader"] span, 
    [data-testid="stHeader"] p {
        color: #000000 !important;
    }
    
    [data-testid="stHeader"] button {
        color: #000000 !important;
    }
    
    /* H1 - App Title */
    .stApp h1 {
        font-size: 42px;
        font-weight: 700;
        color: #D4A574;
        line-height: 1.4;
        margin-bottom: 10px;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
    }
    
    /* H2 - Section Title */
    .stApp h2 {
        font-size: 28px;
        font-weight: 600;
        color: #D4A574;
        line-height: 1.4;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* H3 - Card Title */
    .stApp h3 {
        font-size: 18px;
        font-weight: 600;
        color: #D4A574;
        line-height: 1.4;
    }
    
    /* Body Text */
    .stApp p, .stApp span, .stApp label {
        font-size: 14px;
        color: #E8D9C8;
        line-height: 1.6;
    }
    
    /* Markdown text */
    .stMarkdown {
        color: #E8D9C8;
    }
    
    /* Input Fields - Dark with Gold Border */
    .stTextInput > div > div > input {
        background-color: rgba(45, 27, 78, 0.7);
        color: #E8D9C8;
        border: 2px solid #D4A574;
        border-radius: 12px;
        padding: 12px 15px;
        font-size: 14px;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.3);
    }
    
    /* Date Input with Calendar Icon */
    input[type="date"] {
        background-color: rgba(45, 27, 78, 0.7) !important;
        color: #E8D9C8 !important;
        border: 2px solid #D4A574 !important;
        border-radius: 12px !important;
        padding: 12px 15px !important;
        font-size: 14px !important;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.3) !important;
    }
    
    input[type="date"]::-webkit-calendar-picker-indicator {
        cursor: pointer;
        background-color: #D4A574;
        border-radius: 4px;
        margin-right: 5px;
        opacity: 1;
    }
    
    input[type="date"]::-webkit-calendar-picker-indicator:hover {
        background-color: #FFD700;
    }
    
    input[type="date"]:focus {
        border-color: #FFD700 !important;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.3), 0 0 10px rgba(212, 165, 116, 0.3) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #B8A89C;
        opacity: 0.8;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #FFD700;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.3), 0 0 10px rgba(212, 165, 116, 0.3);
    }
    
    /* Buttons - Gold Theme */
    .stButton > button {
        background: linear-gradient(135deg, #D4A574 0%, #E8C896 100%);
        color: #000000;
        border: 2px solid #D4A574;
        border-radius: 50%;
        padding: 10px 15px;
        font-size: 18px;
        font-weight: 700;
        transition: all 0.3s ease;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 28px;
        box-shadow: 0 4px 12px rgba(212, 165, 116, 0.3);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #E8C896 0%, #FFD700 100%);
        color: #000000;
        box-shadow: 0 6px 16px rgba(212, 165, 116, 0.5);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Ensure all button variants are gold */
    button {
        background: linear-gradient(135deg, #D4A574 0%, #E8C896 100%) !important;
        color: #000000 !important;
        border: 2px solid #D4A574 !important;
        transition: all 0.3s ease !important;
    }
    
    button:hover {
        background: linear-gradient(135deg, #E8C896 0%, #FFD700 100%) !important;
        color: #000000 !important;
        box-shadow: 0 6px 16px rgba(212, 165, 116, 0.5) !important;
    }
    
    /* Ensure button text is always black */
    button span, button p, button div {
        color: #000000 !important;
    }
    
    /* Tabs - Gold Theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #D4A574;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(45, 27, 78, 0.6);
        color: #E8D9C8;
        border: 1px solid #D4A574;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 13px;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(212, 165, 116, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(212, 165, 116, 0.3);
        color: #D4A574;
        border: 2px solid #D4A574;
    }
    
    /* Info Boxes - Gold Theme */
    .stInfo {
        background-color: rgba(212, 165, 116, 0.1);
        border: 2px solid #D4A574;
        border-left: 4px solid #FFD700;
        color: #E8D9C8;
    }
    
    /* Success Messages - Gold */
    .stSuccess {
        background-color: rgba(212, 165, 116, 0.15);
        border: 2px solid #D4A574;
        border-left: 4px solid #FFD700;
        color: #D4A574;
    }
    
    /* Error Messages - Red */
    .stError {
        background-color: rgba(255, 107, 107, 0.2);
        border: 2px solid #FF6B6B;
        border-left: 4px solid #FF0000;
        color: #FF6B6B;
    }
    
    /* Warning Messages - Gold */
    .stWarning {
        background-color: rgba(212, 165, 116, 0.1);
        border: 2px solid #D4A574;
        border-left: 4px solid #FFD700;
        color: #D4A574;
    }
    
    /* Sidebar */
    .stSidebar {
        background: linear-gradient(135deg, #1a0033 0%, #2d1b4e 100%);
    }
    
    .stSidebar [data-testid="stSidebarContent"] {
        background: transparent;
    }
    
    .stSidebar h1, .stSidebar h2 {
        color: #D4A574;
    }
    
    .stSidebar p, .stSidebar span, .stSidebar label {
        color: #E8D9C8;
    }
    
    .stSidebar .stSelectbox > div > div {
        background-color: rgba(45, 27, 78, 0.7);
        border: 2px solid #D4A574;
        color: #E8D9C8;
    }
    
    /* Divider */
    hr {
        border-color: #D4A574 !important;
        background-color: #D4A574 !important;
    }
    
    [data-testid="stHorizontalBlock"] hr {
        border-color: #D4A574 !important;
        background-color: #D4A574 !important;
    }
    
    .stDivider {
        border-color: #D4A574 !important;
        background-color: #D4A574 !important;
    }
    
    /* Caption */
    .stCaption, .stMetricValue, .stMetricLabel {
        color: #E8D9C8;
    }
    
    /* Spinner text */
    .stSpinner {
        color: #D4A574;
    }
    </style>
""", unsafe_allow_html=True)

st.title("AI Astrology Assistant")
st.markdown("Discover your life guidance through advanced astrological analysis")

# Sidebar for LLM Selection
st.sidebar.header("Settings")
llm_choice = st.sidebar.selectbox(
    "Choose LLM:",
    ["Google Gemini", "OpenAI", "Anthropic Claude"]
)

# Initialize LLM based on selection
if llm_choice == "Google Gemini":
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
elif llm_choice == "OpenAI":
    llm = ChatOpenAI(model="gpt-4")
else:
    llm = ChatAnthropic(model="claude-3-sonnet-20240229")

st.sidebar.info(f"Using: **{llm_choice}**")

# Parser setup
parser = PydanticOutputParser(pydantic_object=AstrologyResponse)

# Prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an advanced AI Astrology Assistant with deep knowledge of traditional and modern astrology, including:
            - Vedic (Jyotisha) astrology
            - Western astrology
            - Planetary positions, houses, signs, aspects
            - Dashas / planetary periods (high-level)
            - Personality, career, relationships, health, finance, spirituality, and life trends

            Your task is to analyze a person's life based on the following inputs:
            1. Date of Birth (DD/MM/YYYY)
            2. Time of Birth (HH:MM with AM/PM or 24-hour format)
            3. Place of Birth (City, Country)

            You must:
            - Assume reasonable astronomical calculations if exact ephemeris data is not available
            - Clearly state when predictions are probabilistic or interpretative
            - Provide insights, not deterministic guarantees
            - Maintain a respectful, ethical, and neutral tone

            ---

            ### 🔍 Analysis Process
            1. Determine zodiac sign, ascendant (Lagna), and moon sign (approximate if needed)
            2. Analyze planetary influences on key houses:
            - 1st: Personality & life approach
            - 2nd: Wealth & family
            - 4th: Home & emotional security
            - 5th: Educational status & best fitted area for higher studies
            - 6th: Challenges & health tendencies, diseases
            - 7th: Relationships, marriage life ,count of children
            - 8th: Career & Jobs 
            - 9th: Last Part of life

            3. Consider planetary strengths, weaknesses, and notable combinations (yogas) at a conceptual level

            ---

            ### Output Structure

            Present the analysis using the following structured format:

            1. **Basic Birth Chart Overview**
            - Zodiac sign
            - Ascendant (Lagna)
            - Moon sign
            - Dominant elements (Fire, Earth, Air, Water)

            2. **Personality & Core Nature**
            - Psychological traits
            - Strengths
            - Weaknesses
            - Emotional tendencies

            3. **Career & Education**
            - Suitable career paths
            - what happeen with A/L results
            - what happen with O/L results
            - selected to the higher education or not
            - Academic strengths & weaknesses
            - Best fitted area for higher studies
            - Educational challenges

            4. **Finance & Wealth**
            - Earning patterns
            - earning sources
            - economical status of the family

            5. **Love, Marriage & Relationships**
            - Relationship nature
            - about the partner details
            - count of children
            - why delay Marriage if any
            - Marriage timing
            - how many marriages

            6. **Health & Well-being (medical)**
            - Energy levels
            - Stress patterns
            - diseases likely to be affected by
            - cancer risk analysis

            7. **Family & Social Life**
            - Family bonding
            - Social reputation
            - Support systems

            8. **Career & Jobs **
            - Job nature
            - Job changes timing
            - Career growth patterns
            - Job stability analysis
            - Job satisfaction tendencies
            - Job challenges
            - Job opportunities timing

            9. **Key Life Periods & Turning Points**
            - Early life trends
            - Mid-life focus
            - Later life themes

            10. **Guidance & Positive Remedies (Optional)**
            - Mindset shifts
            - Habits to strengthen positive planetary influences
            - Ethical, non-superstitious suggestions only

            ---

            ### ⚠️ Important Rules
            - Do NOT predict death, accidents, or exact dates of events
            - Do NOT claim absolute certainty
            - Always use language like:
            "indicates", "suggests", "tends to", "may experience"
            - Ensure outputs are insightful, structured, and human-friendly

            ---

            wrap the output in this format and provide no other text\n{format_instructions}""",
        ),
        ("human", "{query}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Initialize session state for AM/PM toggle
if "is_pm" not in st.session_state:
    st.session_state.is_pm = False

# Main content area
col1, col_time, col4, col5 = st.columns([2, 2.5, 2, 1])

with col1:
    birth_date = st.date_input(
        "Date of Birth",
        value=None,
        format="DD/MM/YYYY",
        min_value=date(1901, 1, 1),
        max_value=date.today()
    )
    date_of_birth = birth_date.strftime("%d/%m/%Y") if birth_date else ""

with col_time:
    time_col1, time_col2, time_col3 = st.columns([2, 0.6, 0.9])
    with time_col1:
        birth_time = st.time_input(
            "Time of Birth",
            value=None,
            step=60
        )
        time_input_only = birth_time.strftime("%H:%M") if birth_time else ""
    with time_col2:
        am_pm_status = "PM" if st.session_state.is_pm else "AM"
        st.markdown(f"<div style='display: flex; align-items: center; justify-content: center; height: 40px; margin-top: 30px; font-weight: bold; font-size: 16px;'>{am_pm_status}</div>", unsafe_allow_html=True)
    with time_col3:
        st.write("")  # Add spacing for alignment
        st.write("")  # Extra spacing for vertical alignment
        if st.button("AM/PM", use_container_width=True, key="am_pm_btn", help="AM to PM & PM to AM"):
            st.session_state.is_pm = not st.session_state.is_pm
            st.rerun()

# Combine time with AM/PM
am_pm_status = "PM" if st.session_state.is_pm else "AM"
time_of_birth = f"{time_input_only} {am_pm_status}" if time_input_only else ""

with col4:
    place_of_birth = st.text_input(
        "Place of Birth (City, Country)",
        placeholder="e.g., New York, USA"
    )

with col5:
    st.write("")  # Add spacing for alignment
    st.write("")  # Extra spacing for vertical alignment
    analyze_button = st.button("↑", use_container_width=False, key="analyze_btn", help="Generate Analysis")

# Process query
if analyze_button and date_of_birth and time_of_birth and place_of_birth:
    query = f"Date of Birth: {date_of_birth}\nTime of Birth: {time_of_birth}\nPlace of Birth: {place_of_birth}"
    
    with st.spinner("Analyzing your birth chart..."):
        try:
            chain = prompt | llm | parser
            response = chain.invoke({"query": query})
            
            # Display results
            st.success("Analysis complete!")
            
            # Create tabs for different aspects
            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
                "Birth Chart", 
                "Personality", 
                "Career & Education", 
                "Finance & Wealth",
                "Relationships",
                "Health",
                "Family & Social",
                "Career & Jobs",
                "Life Periods",
                "Guidance & Remedies"
            ])
            
            with tab1:
                st.markdown(response.birth_chart)
            
            with tab2:
                st.markdown(response.personality)
            
            with tab3:
                st.markdown(response.career_education)
            
            with tab4:
                st.markdown(response.finance)
            
            with tab5:
                st.markdown(response.relationships)
            
            with tab6:
                st.markdown(response.health)
            
            with tab7:
                st.markdown(response.family)
            
            with tab8:
                st.markdown(response.career_jobs)
            
            with tab9:
                st.markdown(response.life_periods)
            
            with tab10:
                st.markdown(response.remedies)
                    
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Please check your API keys and try again.")
elif analyze_button:
    st.warning("Please fill in all birth details to continue.")

# Footer
st.divider()
st.caption("Powered by Google Gemini - Ethical Astrological Guidance")
