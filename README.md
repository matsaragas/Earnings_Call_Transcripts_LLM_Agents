# QA on Earnings Calls Transcripts with LLM Agent

This notebook shows how to create a simple `plan-and-execute` style agent to perform multi-hop QA on earnings calls transcripts.


![Logo](notebooks/images/plan_orchestrator1.png)

This is similar to a typical [ReAct](https://arxiv.org/abs/2210.03629) style agent where you think one step at a time. The advantages of this `plan-and-execute`
style agent are:


1. Explicit long term planning, which even strong LLMS can struggle with
2. Ability to use smaller models for the execution step, only using larger/better/expensive models for the planning step



The framework proposed here is organized as follows:

1. The user submits a request to the `Orchestrator`. The request can be a simple questions (e.g., 'What is the capital of Spain?') or a request that requires careful planning and execution to answer.
2. If the users determins that the request requires planning, it sents the request to the `Planner`.
3. The `Planner` breaks down the request into a list of actionable tasks
4. Each task is then executed using a list of available `Tools`, which allow our agent to commnicate with the outside world and retrieve the necessary information to complete the task. The outside world may include the web, a repository of documents, a large collection of images, or any other structured or unstructured source of information and data.
5. `Tools` here refer to various mechanisms and functions that enable our agent to access the nessecary information, such as APIs, Retrieval-Augmented Generation (RAG) systems and etc.
6. Once all the tasks are executed, the final output is sent to `Replan`, which evaluates whether the result meets the requirements of the original request.
7. If the answer is not satisfactory, `Replan` will refine the task list and generate a new execution plan. This process may iterate multiple times until an appropriate answer is obtained.
8. Once `Replan` determines that the final answer is sufficient, it is communicated back to the user.