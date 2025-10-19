from national_agentic_ai_hackathon_2025_backend._debug import Logger
from national_agentic_ai_hackathon_2025_backend.agents_workflow.booking_agent.booking_instruction import get_booking_instructions
from national_agentic_ai_hackathon_2025_backend.tools.RAG.hospital import health_facility_tool
from national_agentic_ai_hackathon_2025_backend.tools.RAG.police import police_facility_tool
from national_agentic_ai_hackathon_2025_backend.tools.location.get_location import get_location_info
from national_agentic_ai_hackathon_2025_backend.tools.location.get_nearest_location import get_nearest_place
from national_agentic_ai_hackathon_2025_backend.tools.email.booking_email_tool import create_booking_email_tool
from agents import Agent , Runner 

class BookingAgent(Agent):
    def __init__(self,context):
        self.context=context
        super().__init__(
            name="Booking Agent",
            instructions=get_booking_instructions,
            tools=self._get_all_tools()
        )

    async def run(self, raw_message: str):
        Logger.info(f"Clinic Agent received message: {raw_message}")
        try:
            result = await Runner.run(self, raw_message, context=self.context)
            return result.final_output

        except Exception as e:
            Logger.error(f"Error running clinic agent: {e}")
            return "Sorry, I am unable to process your clinic request at the moment."

    def _get_all_tools(self):
        return [
            health_facility_tool(self.context),
            police_facility_tool(self.context),
            get_nearest_place,
            get_location_info,
            create_booking_email_tool(self.context),
        ]