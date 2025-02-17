from config import Settings
from langgraph.graph import START, END, StateGraph
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from core.plan_execute import PlanExecute, create_plan_execute
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.vectorstores import FAISS
from typing import Dict


# embeddings = OpenAIEmbeddings(
#     model="text-embedding-ada-002",
#     api_key=Settings.api_key)
# vector_store = FAISS.load_local("vectorize" + "/" + "nvidia",
#                                 embeddings,
#                                 allow_dangerous_deserialization=True)
#
# print(vector_store)


class Agent:
    def __init__(self,
                 model_name: str,
                 embeddings_name: str) -> None:
        self.model_name = model_name
        self.embeddings_name = embeddings_name
        self.model = self.setupmodel(self.model_name)
        self.embeddings = self.setupembeddings(self.embeddings_name)
        self.workflow = self.compile_workflow()


    def compile_workflow(self) -> StateGraph:

        (execute_step,
         plan_step,
         replan_step,
         should_end) = create_plan_execute(self)

        workflow = StateGraph(PlanExecute)
        workflow.add_node("planner", plan_step)
        workflow.add_node("agent", execute_step)
        workflow.add_node("replan", replan_step)
        workflow.add_edge(START, "planner")
        workflow.add_edge("planner", "agent")
        workflow.add_conditional_edges(
            "replan",
            should_end,
            ["agent", END]
        )

        return workflow.compile()

    def setupmodel(self, model_name):

        model = ChatOpenAI(model=model_name,
                           temperature=0,
                           api_key=Settings.api_key)
        return model

    def setupembeddings(self, embeddings_name):
        embeddings = OpenAIEmbeddings(
            model=embeddings_name,
            api_key=Settings.api_key)
        return embeddings

    @staticmethod
    def parse_retriever_input(params: Dict):
        return params["messages"][-1].content

    def contextualqa(self, earnings_question: str, company_name: str) -> str:

        """
        Identifies the relevant context in the earning call transcripts to the user question

        This tool searches in the earnings calls transcript documents and extract financial information
        such as net income, REvenue, EBITDA and etc.

        Parameters:
        - earnings_question: The questions asked by the user
        - the company for which we need to answer the question. Company names should always be lowercase

        Returns:
        - A string with the context that contain the answer to the earnings question.
        """
        vector_store = FAISS.load_local(Settings.VECTOR_DIR + "/" + company_name,
                                        self.embeddings,
                                        allow_dangerous_deserialization=True)
        retriever = vector_store.as_retriever()
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", Settings.SYSTEM_TEMPLATE),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        qa_chain = create_stuff_documents_chain(self.model, qa_prompt)
        retrieval_chain = RunnablePassthrough.assign(
            context=self.parse_retriever_input | retriever).assign(answer=qa_chain)
        response = retrieval_chain.invoke(
            {
                "messages": [HumanMessage(content=earnings_question)]
            }
        )
        return response["answer"]








