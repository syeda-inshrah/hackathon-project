from national_agentic_ai_hackathon_2025_backend._debug import Logger
from national_agentic_ai_hackathon_2025_backend.agents_workflow.catastrophic_agent.instructions import get_catastrophic_instructions

from agents import Agent, Runner


class CatastrophicAgent(Agent):
    def __init__(self, context):
        self.context = context
        super().__init__(
            name="Catastrophic Agent",
            instructions=get_catastrophic_instructions,
            tools=self._get_all_tools()
        )

    async def run(self, raw_message: str) -> str:
        Logger.warning(f"Catastrophic Agent activated for message: {raw_message}")
        try:
            result = await Runner.run(self, raw_message, context=self.context)
            return result.final_output

        except Exception as e:
            Logger.error(f"Error running catastrophic agent: {e}")
            # Even in catastrophic mode, provide emergency contacts
            return """🚨 SYSTEM IN CATASTROPHIC MODE 🚨

Due to severe technical difficulties, I cannot process your request normally. However, for emergencies:

IMMEDIATE EMERGENCY CONTACTS:
- Medical Emergency: Call 1122
- Police Emergency: Call 15
- Women Helpline: 1099
- Child Protection: 1098

If this is a life-threatening emergency, please call the appropriate number immediately. The system will be restored as soon as possible."""

    def _get_all_tools(self):
        return []
