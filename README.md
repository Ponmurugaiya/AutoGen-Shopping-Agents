# AutoGen multi-agent shopping search system

This project demonstrates a **multi-agent shopping search system** using [Microsoft AutoGen AgentChat](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/) to simulate product search and recommendation with persistent memory.

The system consists of three agents:

* **UserAgent** → Handles user queries and extracts intent/entities.
* **SearchAgent** → Searches across multiple stores (Amazon, Flipkart, eBay).
* **AggregatorAgent** → Aggregates and filters results based on user intent.

---

## Project Structure

```
AutoGen_Project/
│── main.py                 # Entry point (simulation runner)
│── config.py               # Configuration (folders, product DB path)
│── memory.py               # PersistentMemory class
│── utils.py                # Helper functions (search, intent parsing, aggregation)
│── agents/
│   ├── __init__.py
│   ├── user_agent.py       # UserAgent
│   ├── search_agent.py     # SearchAgent
│   └── aggregator_agent.py # AggregatorAgent
│── data/
│   └── products.json       # Product database
│── AutoGen_Memory/         # Persistent memory storage (auto-created)
│── requirements.txt        # Python dependencies
```

---

## Setup & Installation

### 1. Clone Repository

```bash
git clone https://github.com/Ponmurugaiya/AutoGen-Shopping-Agents.git
cd AutoGen-Shopping-Agents
```

### 2. Create Virtual Environment

It’s recommended to use a virtual environment:

```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install -U "autogen-agentchat"
```

> If you plan to use OpenAI or Azure OpenAI with AutoGen, install extensions:

```bash
pip install "autogen-ext[openai]"
pip install "autogen-ext[azure]"
```

---

## Product Database

The system reads product data from `data/products.json`.

Example format:

```json
{
  "Amazon": [
    {"name": "Running Shoes", "price": 50},
    {"name": "Sneakers", "price": 70}
  ],
  "Flipkart": [
    {"name": "Running Shoes", "price": 45},
    {"name": "Casual Shoes", "price": 65}
  ],
  "eBay": [
    {"name": "Running Shoes", "price": 48},
    {"name": "Sports Shoes", "price": 60}
  ]
}
```

---

## Running the Simulation

Run the main script:

```bash
python main.py
```

Expected output (example):

```
=== TURN 1: User Query: 'Running shoes' ===
[UserAgent] Query: 'Running shoes' | Intent: search | Entities: {}
[SearchAgent] Amazon results: [...]
[SearchAgent] Flipkart results: [...]
[SearchAgent] Search completed for query: Running shoes
[AggregatorAgent] Final Recommendations: [...]
[Main] Turn 1 aggregated results: [...]
```

---

## Features

* **Persistent Memory per Agent** → Stores query history and search results in `AutoGen_Memory/`.
* **Intent & Entity Extraction** → Supports filtering by price (`under $55`) and store (`only Amazon results`).
* **Parallel Searches** → Runs searches concurrently for better performance.
* **Aggregation** → Combines and filters top recommendations.

---

## Requirements

* Python **3.10+**
* [autogen-agentchat](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/)

Install all requirements with:

```bash
pip install -r requirements.txt
```
