from config import Settings
from core.utils import Utility
from core.agent import Agent

class Controller:

    def __init__(self):
        self.threads = None

    def get_thread(self):
        self.threads = {
            "agent": Agent(model_name=Settings.MODEL_NAME,
                           embeddings_name=Settings.EMBEDDING_NAME
                           )}
        return self.threads

    async def process_questions(self, message):

        thread_data = self.get_thread()
        agent = thread_data['agent']
        inputs = {"input": message}
        config = {"recursion_limit": 20}
        async for event in agent.workflow.astream(inputs, config=config):
            for k, v in event.items():
                if k != "__end__":
                    print(v)




