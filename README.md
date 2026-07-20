# 🔌 MCP Server & Client Integration

A hands-on project demonstrating how to build and connect **Model Context Protocol (MCP)** servers with an AI-powered client using **LangChain** and **LangGraph**. This project showcases two different MCP transport mechanisms — **stdio** and **streamable HTTP** — wired together through a unified **ReAct agent**.

> **💡 Note:** This is a **reference implementation** focused on showing how to configure and connect MCP servers to a client. The weather server returns dummy data — in a real-world scenario, you would integrate it with a weather API (e.g., [OpenWeatherMap](https://openweathermap.org/api), [WeatherAPI](https://www.weatherapi.com/), or [Tomorrow.io](https://www.tomorrow.io/)) to fetch live weather information.

---

## 📐 Architecture

```
┌───────────────────────────────────────────────────────┐
│                    client.py                          │
│           (LangGraph ReAct Agent + Groq LLM)          │
│                                                       │
│   ┌─────────────────────┐  ┌────────────────────────┐ │
│   │  Math Server (stdio) │  │ Weather Server (HTTP)  │ │
│   │   mathserver.py      │  │   weather.py           │ │
│   └─────────────────────┘  └────────────────────────┘ │
└───────────────────────────────────────────────────────┘
```

| Component         | File             | Transport        | Description                                  |
|-------------------|------------------|------------------|----------------------------------------------|
| **Math Server**   | `mathserver.py`  | `stdio`          | Arithmetic operations (add, subtract, etc.)  |
| **Weather Server**| `weather.py`     | `streamable-http`| Returns weather info for a given city        |
| **Client / Agent**| `client.py`      | —                | ReAct agent that discovers and calls tools   |

---

## 🛠️ Tech Stack

- **[MCP (Model Context Protocol)](https://modelcontextprotocol.io/)** — Open protocol for tool/resource sharing between LLMs and external services
- **[LangChain](https://www.langchain.com/)** — Framework for building LLM-powered applications
- **[LangGraph](https://langchain-ai.github.io/langgraph/)** — Agent orchestration with `create_react_agent`
- **[Groq](https://groq.com/)** — Ultra-fast LLM inference (using `qwen/qwen3.6-27b`)
- **[FastMCP](https://github.com/jlowin/fastmcp)** — High-level Python framework for building MCP servers
- **Python 3.14+**

---

## 📂 Project Structure

```
mcp-server-integration/
├── client.py           # MCP client with LangGraph ReAct agent
├── mathserver.py       # MCP server — math tools (stdio transport)
├── weather.py          # MCP server — weather tool (streamable HTTP)
├── main.py             # Default entry point
├── requirements.txt    # Python dependencies
├── pyproject.toml      # Project metadata (uv)
├── .env                # Environment variables (not tracked by git)
├── .gitignore          # Git ignore rules
└── .python-version     # Python version pin
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/zees007/mcp-server-and-client-configuration.git
cd mcp-server-and-client-configuration
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or, if using **uv**:

```bash
uv sync
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> **Note:** Get your free API key from [console.groq.com](https://console.groq.com/).

---

## 🚀 Usage

### Step 1 — Start the Weather Server

The Weather MCP server uses **streamable HTTP** transport, so it needs to be running before the client connects.

```bash
python weather.py
```

This starts the server at `http://localhost:8000/mcp`.

### Step 2 — Run the Client

In a **new terminal** (with the virtual environment activated), run:

```bash
python client.py
```

The client will:

1. Spawn the **Math MCP server** as a subprocess (stdio transport — no manual startup needed)
2. Connect to the already-running **Weather MCP server** over HTTP
3. Discover all available tools from both servers
4. Create a **ReAct agent** powered by Groq's LLM
5. Execute sample queries and print the results

### Example Output

```
The square root of 16 is 4.
The weather in New York is sunny.
```

---

## 🔧 MCP Servers in Detail

### Math Server (`mathserver.py`) — stdio Transport

Runs as a **child process** spawned by the client. Communicates over standard input/output.

| Tool       | Description              | Example               |
|------------|--------------------------|------------------------|
| `add`      | Add two numbers          | `add(2, 3)` → `5`     |
| `subtract` | Subtract two numbers     | `subtract(10, 4)` → `6` |
| `multiply` | Multiply two numbers     | `multiply(3, 7)` → `21` |
| `divide`   | Divide two numbers       | `divide(20, 5)` → `4`  |
| `power`    | Raise to a power         | `power(2, 8)` → `256`  |
| `modulo`   | Modulo operation         | `modulo(10, 3)` → `1`  |

### Weather Server (`weather.py`) — Streamable HTTP Transport

Runs as a **standalone HTTP server**. Must be started separately before the client.

| Tool          | Description                      | Example                                  |
|---------------|----------------------------------|------------------------------------------|
| `get_weather` | Get weather for a given city     | `get_weather("Tokyo")` → `"The weather in Tokyo is sunny"` |

> **🌐 Real-World Integration:** The current weather server returns hardcoded dummy responses. To get real weather data, you can easily extend the `get_weather` tool by integrating any weather API (such as OpenWeatherMap, WeatherAPI, or Tomorrow.io). Simply make an HTTP request inside the tool function and return the actual weather data — the MCP server/client architecture remains exactly the same.

---

## 🧠 How the Client Works

The client ([client.py](client.py)) uses **LangChain MCP Adapters** to connect to multiple MCP servers simultaneously:

```python
client = MultiServerMCPClient(
    {
        "math": {                                    # stdio — spawned automatically
            "command": "python",
            "args": ["mathserver.py"],
            "transport": "stdio"
        },
        "weather": {                                 # HTTP — must be running
            "url": "http://localhost:8000/mcp",
            "transport": "streamable-http"
        }
    }
)
```

It then builds a **ReAct agent** with LangGraph that can reason about which tools to call:

```python
tools = await client.get_tools()
model = ChatGroq(model="qwen/qwen3.6-27b")
agent = create_react_agent(model, tools)
```

---

## 📦 Dependencies

| Package                   | Purpose                                  |
|---------------------------|------------------------------------------|
| `mcp`                     | MCP protocol SDK for building servers    |
| `langchain-mcp-adapters`  | Connects LangChain agents to MCP servers |
| `langchain-groq`          | Groq LLM integration for LangChain      |
| `langgraph`               | Agent orchestration framework            |
| `python-dotenv`           | Loads environment variables from `.env`  |

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

<h1 align="center">❤️ Support & Engagement ❤️</h1>

<p align="center">
If you find this project helpful, please consider supporting it in the following ways:
</p>

⭐ If you find this project helpful, please give it a **star** on [GitHub](https://github.com/zees007/mcp-server-and-client-configuration)!

⭐ If you find this article informative and beneficial, please consider showing your appreciation by giving it a clap 👏👏👏, highlight it and replying on my story. Feel free to share this article with your peers. Your support and knowledge sharing within the developer community are highly valued.

⭐ Please share on social media

⭐ Follow me on: [Medium](https://medium.com/@mhmdzeeshan) || [LinkedIn](https://www.linkedin.com/in/zeeshan-adil-a94b3867/) || [X (Formerly Twitter)](https://x.com/DevZeesCraft)

⭐ Check out my work, projects, and more on my [Linktree](https://linktr.ee/zees007)

⭐ [Check out my other articles on Medium](https://medium.com/@mhmdzeeshan)

⭐ [Subscribe to my newsletter 📧](https://medium.com/@mhmdzeeshan/subscribe), so that you don't miss out on my latest articles.

⭐ If you enjoyed my article, please consider [buying me a coffee ❤️](https://buymeacoffee.com/mhmdzeeshan) and stay tuned to more articles about Java, technologies and AI. 🧑‍💻

---

## 👨‍💻 Author

**Zeeshan**

🌍 Full-stack AI Developer | Python | Java | Spring Boot | Flutter | Agentic AI | RAG | LangChain | Generative AI
