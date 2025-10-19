from national_agentic_ai_hackathon_2025_backend.database.police import PoliceFacilityDB
from national_agentic_ai_hackathon_2025_backend.handlers.vector_store import VectorStoreManager
from rich import print
import asyncio
import json

async def main():
    db = PoliceFacilityDB()
    vsm = VectorStoreManager()
    # Retrieve all police facilities
    facilities_result = await db.get_all_police_facility()
    if not facilities_result.get("success"):
        print(f"[red]Failed to fetch facilities: {facilities_result.get('error')}[/red]")
        return
    facilities = facilities_result.get("data", [])
    print(f"[green]Fetched {len(facilities)} police facilities.[/green]")
    print(facilities)
    # Create vector store with the fetched facilities
    data = vsm.create_vector_store("police_facility")
    for facility in facilities:
        file_data = vsm.upload_file(
            file_name=f"{facility['name'].replace(' ', '_').lower()}.txt",
            content=json.dumps(facility).encode("utf-8"),
        )
        vsm.add_file_to_vector_store(data['id'], file_data['id'])
    print(data)
    print("[blue]Vector store 'police_facility' created with facility data.[/blue]")

if __name__ == "__main__":
    asyncio.run(main())
