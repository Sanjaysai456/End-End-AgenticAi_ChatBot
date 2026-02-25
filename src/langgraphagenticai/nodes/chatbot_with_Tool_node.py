from src.langgraphagenticai.state.state import State

class ChatbotWithToolNode:
    """
    Chatbot logic enhanced with tool integration.
    """

    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a response.
        """

        # Directly pass full message history
        llm_response = self.llm.invoke(state["messages"])

        return {"messages": [llm_response]}

    def create_chatbot(self, tools):
        """
        Returns a chatbot node function with tool binding.
        """

        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            response = llm_with_tools.invoke(state["messages"])
            return {"messages": [response]}

        return chatbot_node