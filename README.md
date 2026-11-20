# AI Research Assistant with LangChain Tool Calling

## Why this project

Learn how a language model decides when to call a tool.
Build tools for calculations, web search, keyword extraction, and research summaries.
See how a single request can trigger several tool calls before the agent answers.
Run the same notebook with Gemini or OpenAI by switching the model configuration.

## Run the demo

1. Install Python and open a terminal in the repository root. Create a virtual environment and activate it.

   ```powershell
   # Windows PowerShell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   ```bash
   # macOS or Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install the dependencies.

   ```sh
   python -m pip install -r requirements.txt
   ```

3. Create a `.env` file in the repository root. Set the variable for the provider you plan to use. The empty assignments below show the variable names.

   ```dotenv
   GEMINI_API_KEY=
   OPENAI_API_KEY=
   ```

   The repository ignores `.env`. Keep credentials there and clear notebook outputs before sharing the notebook.

4. In [config/config.yaml](config/config.yaml), set `llm.provider` to `gemini` or `openai`. Set the corresponding `llm.gemini.model_name` or `llm.openai.model_name` to a model your account can use that supports tool calling. The loader reads this nested configuration.

5. Start Jupyter from the notebook directory.

   ```sh
   cd notebooks
   jupyter notebook tool_calling_demo.ipynb
   ```

   In Jupyter or VS Code, open [tool_calling_demo.ipynb](notebooks/tool_calling_demo.ipynb), select the Python kernel from the virtual environment, and run the cells in order. The connection check sends one prompt to the configured model before the tool examples start. The notebook expects its working directory to be `notebooks/`.

   If DuckDuckGo rate-limits the search cell, retry later. You can continue with the calculation, keyword extraction, and summary examples while search is unavailable. If you change an installed dependency, restart the kernel before rerunning the cells.

## Topics covered

- Creating custom tools with `@tool` and using a prebuilt community search tool.
- Testing tools directly with `.invoke()` before registering them with an agent.
- Building a chat prompt with system instructions, user input, and an agent scratchpad.
- Running one or more tool calls with `AgentExecutor` and inspecting the trace with `verbose=True`.
- Loading YAML configuration and selecting a model provider with credentials from the environment.

## Architecture

```text
config/config.yaml and .env
           |
           v
     load_llm() --> Gemini or OpenAI
                           |
                           v
User request --> AgentExecutor --> Model chooses a tool or answers
                      ^                     |
                      |                     v
                      +--------- Tool result returns to the model
```

The notebook assembles the prompt, model, and tool list. The system prompt describes when to use each tool. The scratchpad carries tool calls and their results between model turns. The executor continues until the model produces a final answer. A calculation can take one tool call, while a request for recent information may involve search followed by synthesis.

## Tools and examples

After running the tool setup cells, invoke these tools directly to see what each returns.

| Tool | Try in the notebook | When to use it |
| --- | --- | --- |
| `calculator` | `calculator.invoke("125 * 8")` returns `"1000"`. | Calculate the total for 125 items at 8 per item. |
| `search_tool` | `search_tool.invoke("What is Agentic AI?")` | Find web snippets for an unfamiliar or changing topic. |
| `keyword_extractor` | `keyword_extractor.invoke("LangGraph coordinates agents and tools in a stateful workflow.")` | Generate search terms or tags from a research note. |
| `research_summary_tool` | `research_summary_tool.invoke("LangGraph")` | Draft a short overview before reading the documentation. |

The calculator uses Python's `eval()`. Run that example only with trusted arithmetic input. The keyword and summary tools call the configured model. They do not fetch web pages themselves.

After creating the agent executor, try a calculation and a request that calls for more than one tool. Inspect the verbose output to see which tools the model actually picks.

```python
answer = agent_executor.invoke({"input": "What is 125 * 75?"})
print(answer["output"])

answer = agent_executor.invoke({
    "input": (
        "Extract keywords from this note, then summarize its topic. "
        "LangGraph coordinates stateful workflows that use agents and tools."
    )
})
print(answer["output"])
```

## Main imports

| Import | How the project uses it |
| --- | --- |
| `langchain_core.tools.tool` | Wraps a function such as `calculator` as an invokable tool. The function's signature and docstring describe its inputs and purpose. |
| `langchain_core.prompts.ChatPromptTemplate` | Combines the system instructions, `{input}`, and `{agent_scratchpad}` into messages for the model. |
| `langchain.agents.create_tool_calling_agent` | Connects the model, prompt, and tool list so the model can request a tool call. |
| `langchain.agents.AgentExecutor` | Runs requested tools and feeds the results back into the agent. |
| `langchain_community.tools.DuckDuckGoSearchRun` | Supplies the web search tool. This project uses `duckduckgo-search` and a compatible `primp` version through `requirements.txt`. |
| `langchain_google_genai.ChatGoogleGenerativeAI` and `langchain_openai.ChatOpenAI` | Let the same notebook call either Gemini or OpenAI through `load_llm()`. |
| `dotenv.load_dotenv` and `os.getenv` | Load provider keys from `.env` and read the selected key from the environment. |
| `yaml.safe_load` and `pathlib.Path` | Locate and read the project's YAML configuration. The notebook also uses `Path` and `sys.path` to import the shared loaders. |

## Project files

| File | Purpose |
| --- | --- |
| [notebooks/tool_calling_demo.ipynb](notebooks/tool_calling_demo.ipynb) | Runs the model check, standalone tool examples, and agent examples. |
| [src/utils/config_loader.py](src/utils/config_loader.py) | Reads the model settings from `config/config.yaml`. |
| [src/utils/model_loader.py](src/utils/model_loader.py) | Builds the selected Gemini or OpenAI chat model. |
| [requirements.txt](requirements.txt) | Lists the notebook and runtime dependencies. |
| [template.py](template.py) | Creates the project scaffold. The demo tools and agent are defined in the notebook. |
