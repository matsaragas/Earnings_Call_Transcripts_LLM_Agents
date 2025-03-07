import operator
from typing import Annotated, List, Tuple, Union
from typing_extensions import TypedDict
from pydantic import BaseModel, Field
from langgraph.prebuilt import create_react_agent
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END

class PlanExecute(TypedDict):
    input: str
    plan: List[str]
    past_steps: Annotated[List[Tuple], operator.add]
    response: str


class Plan(BaseModel):
    """Plan to follow in future"""

    steps: List[str] = Field(
        description="different steps to follow, should be in sorted order"
    )


class Response(BaseModel):
    """Response to user."""

    response: str


class Act(BaseModel):
    """Action to perform."""

    action: Union[Response, Plan] = Field(
        description="Action to perform. If you want to respond to user, use Response. "
                    "If you need to further use tools to get the answer, use Plan."
    )


def create_plan_execute(agent):
    llm = agent.model
    tools = [agent.contextualqa]
    prompt = "You are a helpful assistant capable to compare earning information between companies."
    agent_executor = create_react_agent(llm, tools, prompt=prompt)
    planner_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """For the given objective, come up with a simple step by step plan. \
    This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
    The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.""",
            ),
            ("placeholder", "{messages}"),
        ]
    )

    replanner_prompt = ChatPromptTemplate.from_template(
        """For the given objective, come up with a simple step by step plan.
        This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
        The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.
        Your objective was this:
        {input}
        
        Your original plan was this:
        {plan}
        
        You have currently done the follow steps:
        {past_steps}
        
        Update your plan accordingly. If no more steps are needed and you can return to the user, then respond with that. Otherwise, fill out the plan. Only add steps to the plan that still NEED to be done. Do not return previously done steps as part of the plan."""
    )
    planner = planner_prompt | llm.with_structured_output(Plan)
    replanner = replanner_prompt | llm.with_structured_output(Act)
    agent_executor = create_react_agent(llm, tools, prompt=prompt)

    async def execute_step(state: PlanExecute):
        plan = state["plan"]
        plan_str = "\n".join(f"{i+1}. {step}" for i, step in enumerate(plan))
        task = plan[0]
        task_formatted = f"""For the following plan: {plan_str}\n\nYou are tasked with executing step {1}, {task}."""
        agent_response = await agent_executor.ainvoke(
            {"messages": [("user", task_formatted)]}
        )
        return {
            "past_steps": [(task, agent_response["messages"][-1].content)],
        }

    async def plan_step(state: PlanExecute):
        plan = await planner.ainvoke({"messages": [("user", state["input"])]})
        return {"plan": plan.steps}

    async def replan_step(state: PlanExecute):
        output = await replanner.ainvoke(state)
        if isinstance(output.action, Response):
            return {"response": output.action.response}
        else:
            return {"plan": output.action.steps}

    def should_end(state: PlanExecute):
        if "response" in state and state["response"]:
            return END
        else:
            return "agent"

    return (
        execute_step,
        plan_step,
        replan_step,
        should_end
    )
