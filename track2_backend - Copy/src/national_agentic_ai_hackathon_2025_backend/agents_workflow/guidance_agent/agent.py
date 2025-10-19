from national_agentic_ai_hackathon_2025_backend._debug import Logger
from national_agentic_ai_hackathon_2025_backend.agents_workflow.guidance_agent.guidance_instruction import get_guidance_instructions
from national_agentic_ai_hackathon_2025_backend.agents_workflow.guidance_agent.output_type import GuidanceOutputType
from agents import Agent , Runner 

class GuidanceAgent(Agent):
    def __init__(self,context):
        self.context=context
        super().__init__(
            name="Guidance Agent",
            instructions=get_guidance_instructions,
            tools=self._get_all_tools(),
            output_type=GuidanceOutputType
        )

    async def run(self, raw_message: str) -> GuidanceOutputType:
        Logger.info(f"Medical Agent received message: {raw_message}")
        try:
            result = await Runner.run(self, raw_message, context=self.context)
            return result.final_output

        except Exception as e:
            Logger.error(f"Error running medical agent: {e}")
            return "Sorry, I am unable to process your medical request at the moment."

    def _get_all_tools(self):
        return []
