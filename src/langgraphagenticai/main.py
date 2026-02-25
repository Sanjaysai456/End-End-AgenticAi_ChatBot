import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit


def load_langgraph_agenticai_app():
    """
    Main entry point for LangGraph AgenticAI Streamlit application.
    """

    # Load UI
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()

    if not user_input:
        st.error("Failed to load user input from the UI.")
        return

    # Handle user input
    if st.session_state.IsFetchButtonClicked:
        user_message = st.session_state.timeframe
    else:
        user_message = st.chat_input("Enter your message:")

    if not user_message:
        return

    try:
        # Initialize LLM
        llm_config = GroqLLM(user_controls_input=user_input)
        model = llm_config.get_llm_model()

        if not model:
            st.error("LLM model initialization failed.")
            return

        # Get selected use case
        usecase = user_input.get("selected_usecase")

        if not usecase:
            st.error("No use case selected.")
            return

        # Build Graph
        graph_builder = GraphBuilder(model)
        graph = graph_builder.setup_graph(usecase)

        # Display Result
        DisplayResultStreamlit(
            usecase,
            graph,
            user_message
        ).display_result_on_ui()

    except Exception as e:
        st.error(f"Application error: {e}")