from dotenv import load_dotenv
from livekit import agents
from .support_agent import support_agent_entrypoint
from .transfer_agent import transfer_agent_entrypoint

load_dotenv()

async def main_entrypoint(ctx: agents.JobContext):
    room_name = ctx.room.name
    
    if "consult" in room_name or "specialist" in room_name:
        await transfer_agent_entrypoint(ctx)
    else:
        await support_agent_entrypoint(ctx)

if __name__ == "__main__":
    print("🚀 Starting LiveKit agent service...")
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=main_entrypoint))
