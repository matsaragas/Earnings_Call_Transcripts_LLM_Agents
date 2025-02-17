import asyncio

from core.controller import Controller

controller = Controller()
message = "what was the difference in the total revenue between Nvidia and Lyft in 2020?"
asyncio.run(controller.process_questions(message))
