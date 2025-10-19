from national_agentic_ai_hackathon_2025_backend._debug import Logger
from national_agentic_ai_hackathon_2025_backend.agents_workflow.orchestrator_agent.orchestrator_instructions import get_orchestrator_instructions
from national_agentic_ai_hackathon_2025_backend.agents_workflow.orchestrator_agent.output_type import OrchestratorOutputType

from agents import Agent , Runner 

class OrchestratorAgent(Agent):
    def __init__(self,context):
        self.context=context
        super().__init__(
            name="Orchestrator Agent",
            instructions=get_orchestrator_instructions,
            tools=self._get_all_tools(),
            output_type=OrchestratorOutputType
        )

    async def run(self, raw_message: str) -> OrchestratorOutputType:
        Logger.info(f"Orchestrator Agent received message: {raw_message}")
        try:
            result = await Runner.run(self, raw_message, context=self.context)
            return result.final_output

        except Exception as e:
            Logger.error(f"Error running Orchestrator agent: {e}")
            return "Sorry, I am unable to process your critical request at the moment."

    def _get_all_tools(self):
        return []