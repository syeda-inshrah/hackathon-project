from national_agentic_ai_hackathon_2025_backend._debug import Logger
from national_agentic_ai_hackathon_2025_backend.agents_workflow.police_agent.police_instruction import get_police_instructions
from national_agentic_ai_hackathon_2025_backend.tools.RAG.police import police_facility_tool
from national_agentic_ai_hackathon_2025_backend.tools.location.get_location import get_location_info
from national_agentic_ai_hackathon_2025_backend.tools.location.get_nearest_location import get_nearest_place
from agents import Agent , Runner

class PoliceAgent(Agent):
    def __init__(self,context):
        self.context=context
        super().__init__(
            name="Police Agent",
            instructions=get_police_instructions,
            tools=self._get_all_tools()
        )

    async def run(self, raw_message: str):
        Logger.info(f"Police Agent received message: {raw_message}")
        try:
            result = await Runner.run(self, raw_message, context=self.context)
            return result.final_output

        except Exception as e:
            Logger.error(f"Error running medical agent: {e}")
            return "Sorry, I am unable to process your police request at the moment."

    def _get_all_tools(self):
        return [
            police_facility_tool(self.context),
            get_location_info,
            get_nearest_place
        ]
