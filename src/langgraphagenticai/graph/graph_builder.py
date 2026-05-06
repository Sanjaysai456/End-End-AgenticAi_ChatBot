from langgraph.graph import StateGraph
from src.langgraphagenticai.state.state import State
from langgraph.graph import START,END
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraphagenticai.tools.search_tool import get_tools,create_tool_node
from langgraph.prebuilt import tools_condition,ToolNode
from src.langgraphagenticai.nodes.chatbot_with_Tool_node import ChatbotWithToolNode
from src.langgraphagenticai.nodes.ai_news_node import AINewsNode
from src.langgraphagenticai.nodes.medical_rag_node import MedicalRAGNode


class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class 
        and integrates it into the graph. The chatbot node is set as both the 
        entry and exit point of the graph.
        """

        self.basic_chatbot_node=BasicChatbotNode(self.llm)

        self.graph_builder.add_node("chatbot",self.basic_chatbot_node.process)
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_edge("chatbot",END)

    def chatbot_with_tools_build_graph(self):
        """
        Builds an advanced chatbot graph with tool integration.
        This method creates a chatbot graph that includes both a chatbot node 
        and a tool node. It defines tools, initializes the chatbot with tool 
        capabilities, and sets up conditional and direct edges between nodes. 
        The chatbot node is set as the entry point.
        """
        ## Define the tool and tool node
        tools=get_tools()
        tool_node=create_tool_node(tools)

        ## Define the LLM
        llm=self.llm

        ## Define the chatbot node

        obj_chatbot_with_node=ChatbotWithToolNode(llm)
        chatbot_node=obj_chatbot_with_node.create_chatbot(tools)
        ## Add nodes
        self.graph_builder.add_node("chatbot",chatbot_node)
        self.graph_builder.add_node("tools",tool_node)
        # Define conditional and direct edges
        self.graph_builder.add_edge(START,"chatbot")
        self.graph_builder.add_conditional_edges("chatbot",tools_condition)
        self.graph_builder.add_edge("tools","chatbot")


    def ai_news_builder_graph(self):

        ai_news_node=AINewsNode(self.llm)

        ## added the nodes

        self.graph_builder.add_node("fetch_news",ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news",ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result",ai_news_node.save_result)

        #added the edges

        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news","summarize_news")
        self.graph_builder.add_edge("summarize_news","save_result")
        self.graph_builder.add_edge("save_result", END)


       



    def multi_agent_build_graph(self):
        """
        Builds the unified Multi-Agent router graph.
        """
        from src.langgraphagenticai.nodes.router_node import RouterNode

        router = RouterNode(self.llm)
        basic_chatbot = BasicChatbotNode(self.llm)
        
        tools = get_tools()
        tool_node = create_tool_node(tools)
        obj_chatbot_with_node = ChatbotWithToolNode(self.llm)
        chatbot_with_web = obj_chatbot_with_node.create_chatbot(tools)
        
        ai_news_node = AINewsNode(self.llm)

        # Medical RAG agent — shared singleton so FAISS index stays in memory
        medical_rag_node = MedicalRAGNode(self.llm)

        # Add nodes
        self.graph_builder.add_node("router", router.process)
        self.graph_builder.add_node("basic_chat", basic_chatbot.process)
        self.graph_builder.add_node("web_search_chatbot", chatbot_with_web)
        self.graph_builder.add_node("tools", tool_node)
        self.graph_builder.add_node("fetch_news", ai_news_node.fetch_news)
        self.graph_builder.add_node("summarize_news", ai_news_node.summarize_news)
        self.graph_builder.add_node("save_result", ai_news_node.save_result)
        self.graph_builder.add_node("medical_rag", medical_rag_node.process)

        # Router entry and conditional edges
        self.graph_builder.set_entry_point("router")
        
        def route_intent(state: State):
            return state.get("intent", "basic")

        self.graph_builder.add_conditional_edges(
            "router",
            route_intent,
            {
                "basic": "basic_chat",
                "web_search": "web_search_chatbot",
                "ai_news": "fetch_news",
                "medical": "medical_rag",
            }
        )

        # Basic Chat edge
        self.graph_builder.add_edge("basic_chat", END)

        # Web Search edges
        self.graph_builder.add_conditional_edges("web_search_chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "web_search_chatbot")

        # AI News edges
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("save_result", END)

        # Medical RAG edge
        self.graph_builder.add_edge("medical_rag", END)


    def setup_graph(self, usecase: str):
        """
        Sets up the graph for the selected use case.
        """
        if usecase == "Basic Chatbot":
            self.basic_chatbot_build_graph()
        elif usecase == "Chatbot With Web":
            self.chatbot_with_tools_build_graph()
        elif usecase == "AI News":
            self.ai_news_builder_graph()
        elif usecase == "Multi-Agent System":
            self.multi_agent_build_graph()

        return self.graph_builder.compile()
