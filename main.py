import asyncio
from config import MEMORY_FOLDER
from agents.user_agent import UserAgent
from agents.search_agent import SearchAgent
from agents.aggregator_agent import AggregatorAgent

# ----------------------------
# Simulation
# ----------------------------
simulated_queries = [
    "Running shoes",
    "Show cheaper than $55",
    "Only Amazon results"
]

async def run_fully_async_autogen():
    user_queue = asyncio.Queue()
    search_queue = asyncio.Queue()

    user_agent = UserAgent("UserAgent", "Handles user queries", f"{MEMORY_FOLDER}/user_agent_mem.json", user_queue)
    search_agent = SearchAgent("SearchAgent", "Performs product searches", f"{MEMORY_FOLDER}/search_agent_mem.json", user_queue, search_queue)
    aggregator_agent = AggregatorAgent("AggregatorAgent", "Aggregates results", f"{MEMORY_FOLDER}/aggregator_agent_mem.json")

    for turn, query in enumerate(simulated_queries, 1):
        print(f"\n=== TURN {turn}: User Query: '{query}' ===")

        user_task = asyncio.create_task(user_agent.on_messages([{"type":"text","content":query}]))
        search_task = asyncio.create_task(search_agent.on_messages([{"type":"text","content":query}]))

        user_result, search_results = await asyncio.gather(user_task, search_task)

        agg_results = await aggregator_agent.on_messages([{"type":"text","content":query}], user_agent.memory, search_results)
        print(f"[Main] Turn {turn} aggregated results: {agg_results}")

if __name__ == "__main__":
    asyncio.run(run_fully_async_autogen())
