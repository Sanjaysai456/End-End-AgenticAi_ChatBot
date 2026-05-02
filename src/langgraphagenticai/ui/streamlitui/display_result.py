import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        print(user_message)

        if usecase == "Multi-Agent System":
            
            with st.chat_message("user"):
                st.write(user_message)

            initial_state = {"messages": [HumanMessage(content=user_message)]}

            with st.spinner("Agent is thinking... ⏳"):
                res = graph.invoke(initial_state)

            intent = res.get("intent", "basic")

            if intent == "ai_news":
                try:
                    frequency = res.get("frequency", "daily").lower()
                    if not frequency:
                        frequency = "daily"
                    AI_NEWS_PATH = f"./AINews/{frequency}_summary.md"
                    with open(AI_NEWS_PATH, "r", encoding='utf-8') as file:
                        markdown_content = file.read()
                    
                    with st.chat_message("assistant"):
                        st.markdown(markdown_content, unsafe_allow_html=True)

                except FileNotFoundError:
                    st.error(f"News Not Generated or File not found: {AI_NEWS_PATH}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
            else:
                # For basic chat and web search
                for message in reversed(res["messages"]):
                    if isinstance(message, AIMessage) and message.content:
                        with st.chat_message("assistant"):
                            st.write(message.content)
                        break