from national_agentic_ai_hackathon_2025_backend.context.global_context import GlobalContext
from national_agentic_ai_hackathon_2025_backend.agents_workflow.guidance_agent.agent import GuidanceAgent
from national_agentic_ai_hackathon_2025_backend.agents_workflow.orchestrator_agent.agent import OrchestratorAgent
from national_agentic_ai_hackathon_2025_backend.agents_workflow.police_agent.agent import PoliceAgent
from national_agentic_ai_hackathon_2025_backend.agents_workflow.medical_agent.agent import MedicalAgent
from national_agentic_ai_hackathon_2025_backend.agents_workflow.degraded_performer_agent.agent import DegradedPerformerAgent
from national_agentic_ai_hackathon_2025_backend.agents_workflow.catastrophic_agent.agent import CatastrophicAgent
from national_agentic_ai_hackathon_2025_backend.utils._helpers import should_enable_degraded_mode
from national_agentic_ai_hackathon_2025_backend._debug import Logger

class WorkFlow:
    def __init__(self, status = None) -> None:
        self.enable_degraded = should_enable_degraded_mode(status)

    async def execute_workflow(self, message: str, context: GlobalContext):
        Logger.info(f"Starting workflow execution for message: {message}")
        
        if self.enable_degraded:
            Logger.warning("System is in degraded mode. Using DegradedPerformerAgent.")
            degraded_agent = DegradedPerformerAgent(context)
            return await degraded_agent.run(message)
            
        guidance_agent = GuidanceAgent(context)
        Logger.info("Running GuidanceAgent...")
        agent_output = await guidance_agent.run(message)
        Logger.info(f"GuidanceAgent output: {agent_output}")

        if not agent_output.is_critical:
            Logger.info("Message is not critical. Returning guidance agent response.")
            return agent_output.response

        Logger.info("Message is critical. Escalating to OrchestratorAgent.")
        orchestrator_agent = OrchestratorAgent(context)
        agent_output = await orchestrator_agent.run(message)
        Logger.info(f"OrchestratorAgent output: {agent_output}")

        if agent_output.request_type == "police":
            Logger.info("Request type is police. Running PoliceAgent.")
            police_agent = PoliceAgent(context)
            agent_output = await police_agent.run(message)
            Logger.info(f"PoliceAgent output: {agent_output}")
            return agent_output

        elif agent_output.request_type == "medical":
            Logger.info("Request type is medical. Running MedicalAgent.")
            medical_agent = MedicalAgent(context)
            agent_output = await medical_agent.run(message)
            Logger.info(f"MedicalAgent output: {agent_output}")
            return agent_output

        elif agent_output.request_type == "catastrophic":
            Logger.info("Request type is catastrophic. Running CatastrophicAgent.")
            catastrophic_agent = CatastrophicAgent(context)
            agent_output = await catastrophic_agent.run(message)
            Logger.info(f"MedicalAgent output: {agent_output}")
            return agent_output
        
        else: 
            Logger.error(f"Unknown request type: {agent_output.request_type}. Returning error message.")
            return "Something went wrong"