# Stub module for langchain.agents
class AgentExecutor:
    def __init__(self, agent, tools, verbose=False):
        self.agent = agent
        self.tools = tools
        self.verbose = verbose

    def invoke(self, input_dict):
        """Stub invocation returning a fixed response"""
        return {"output": "stub-response"}
