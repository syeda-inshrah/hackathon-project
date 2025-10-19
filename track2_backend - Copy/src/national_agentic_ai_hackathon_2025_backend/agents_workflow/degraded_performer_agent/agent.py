from national_agentic_ai_hackathon_2025_backend._debug import Logger
from national_agentic_ai_hackathon_2025_backend.agents_workflow.degraded_performer_agent.instructions import get_degraded_performer_instructions
from national_agentic_ai_hackathon_2025_backend.tools.RAG.faqs import get_faqs
from agents import Agent , Runner 

class DegradedPerformerAgent(Agent):
    def __init__(self,context):
        self.context=context
        super().__init__(
            name="Degraded Performer Agent",
            instructions=get_degraded_performer_instructions,
            tools=self._get_all_tools()
        )

    async def run(self, raw_message: str) -> str:
        Logger.info(f"Degraded Performer Agent received message: {raw_message}")
        try:
            result = await Runner.run(self, raw_message, context=self.context)
            return result.final_output

        except Exception as e:
            Logger.error(f"Error running degraded performer agent: {e}")
            return "Sorry, I am unable to process your request at the moment due to system limitations."

    def _get_all_tools(self):
        return [
            get_faqs(self.context)
        ]