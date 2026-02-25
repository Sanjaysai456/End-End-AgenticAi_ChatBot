import streamlit as st
import os
from dotenv import load_dotenv
from src.langgraphagenticai.ui.uiconfigfile import Config

# Load environment variables
load_dotenv()

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(
            page_title="🤖 " + self.config.get_page_title(),
            layout="wide"
        )

        st.header("🤖 " + self.config.get_page_title())

        st.session_state.timeframe = ''
        st.session_state.IsFetchButtonClicked = False

        with st.sidebar:

            # Get options from config
            llm_options = self.config.get_llm_options()
            usecase_options = self.config.get_usecase_options()

            # LLM selection
            self.user_controls["selected_llm"] = st.selectbox(
                "Select LLM",
                llm_options
            )

            # If Groq selected
            if self.user_controls["selected_llm"] == 'Groq':

                model_options = self.config.get_groq_model_options()

                self.user_controls["selected_groq_model"] = st.selectbox(
                    "Select Model",
                    model_options
                )

                # Load GROQ key from .env
                groq_key = os.getenv("GROQ_API_KEY")

                if not groq_key:
                    st.error("❌ GROQ_API_KEY not found in .env file")
                else:
                    os.environ["GROQ_API_KEY"] = groq_key

            # Usecase selection
            self.user_controls["selected_usecase"] = st.selectbox(
                "Select Usecases",
                usecase_options
            )

            # If web-based usecases
            if self.user_controls["selected_usecase"] in ["Chatbot With Web", "AI News"]:

                tavily_key = os.getenv("TAVILY_API_KEY")

                if not tavily_key:
                    st.error("❌ TAVILY_API_KEY not found in .env file")
                else:
                    os.environ["TAVILY_API_KEY"] = tavily_key

            # AI News Section
            if self.user_controls['selected_usecase'] == "AI News":

                st.subheader("📰 AI_News_Explorer")

                time_frame = st.selectbox(
                    "📅 Select Time Frame",
                    ["Daily", "Weekly", "Monthly"],
                    index=0
                )

                if st.button("🔍 Fetch Latest AI News", use_container_width=True):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame

        return self.user_controls