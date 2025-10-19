from national_agentic_ai_hackathon_2025_backend._debug import Logger
from national_agentic_ai_hackathon_2025_backend.agents_workflow.medical_agent.medical_instruction import get_medical_instructions
from national_agentic_ai_hackathon_2025_backend.tools.RAG.hospital import health_facility_tool
from national_agentic_ai_hackathon_2025_backend.tools.location.get_location import get_location_info
from national_agentic_ai_hackathon_2025_backend.tools.location.get_nearest_location import get_nearest_place
from national_agentic_ai_hackathon_2025_backend.agents_workflow.booking_agent.agent import BookingAgent
from agents import Agent, Runner 

class MedicalAgent(Agent):
    def __init__(self,context):
        self.context=context
        super().__init__(
            name="Medical Agent",
            instructions=get_medical_instructions,
            tools=self._get_all_tools()
        )

    async def run(self, raw_message: str):
        Logger.info(f"Medical Agent received message: {raw_message}")
        try:
            result = await Runner.run(self, raw_message, context=self.context)
            return result.final_output
        except Exception as e:
            Logger.error(f"Error running medical agent: {e}")
            return "Sorry, I am unable to process your medical request at the moment."

    def _get_all_tools(self):
        booking_agent = BookingAgent(self.context)
        return [
            health_facility_tool(self.context),
            get_location_info,
            get_nearest_place,
            booking_agent.as_tool(
                tool_description="Book appointments or make reservations at medical facilities.",
                tool_name="book_medical_appointment"
            )
        ]