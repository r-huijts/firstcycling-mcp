# FirstCycling MCP Server
[![Trust Score](https://archestra.ai/mcp-catalog/api/badge/quality/r-huijts/firstcycling-mcp)](https://archestra.ai/mcp-catalog/r-huijts__firstcycling-mcp)

This is a Model Context Protocol (MCP) server that provides professional cycling data from FirstCycling. It allows you to retrieve comprehensive information about professional cyclists, race results, race details, and historical cycling data.

## Features

This MCP server offers rich access to professional cycling data, providing tools for:

- Finding information about professional cyclists
- Retrieving race results and details
- Exploring historical race data
- Analyzing rider performance and career progression
- Accessing information about cycling teams and competitions

## Real-World Use Cases

With this MCP server, you can use Claude to:

### Rider Analysis

- **Performance Tracking**: "How has Tadej Pogačar performed in the Tour de France over the years?"
- **Career Progression**: "Show me the team history and career progression of Wout van Aert."
- **Specialization Analysis**: "What are Mathieu van der Poel's results in Monument classics?"
- **Victory Analysis**: "List all WorldTour victories for Jonas Vingegaard."
- **Historical Comparison**: "Compare the Grand Tour results of Primož Roglič and Jonas Vingegaard."

### Race Research

- **Recent Results**: "Show me the results of the 2023 Paris-Roubaix."
- **Historical Context**: "Who are the youngest and oldest winners of the Tour of Flanders?"
- **Team Analysis**: "Get the startlist for the 2023 Tour de France with detailed team information."
- **Race Statistics**: "Show me the victory table for Liège-Bastogne-Liège. Who has won it the most times?"
- **Stage Information**: "Can you show me the stage profiles for the 2023 Giro d'Italia?"

### Sports Journalism

- "Create a detailed profile of Remco Evenepoel for a cycling magazine article."
- "Write a preview for the upcoming Tour de France based on the recent results of top contenders like Tadej Pogačar and Jonas Vingegaard."
- "Analyze the evolution of Tom Pidcock's career based on his race results and team history."

### Cycling Education

- "Explain what makes the Monument classics special using data about their history and winners."
- "Create an educational summary about Grand Tours and their significance in professional cycling."
- "Describe the typical career progression of a professional cyclist using examples from the data."

## Requirements

- Python 3.10 or higher
- `uv` package manager (recommended)
- Dependencies as listed in `pyproject.toml`, including:
  - mcp
  - beautifulsoup4
  - lxml
  - pandas
  - slumber
  - and other packages for web scraping and data processing

## Setup

1. Clone this repository
2. Create and activate a virtual environment:
   ```
   uv venv
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```
   uv pip install -e .
   ```

## FirstCycling API

This server uses the [FirstCycling API](https://github.com/baronet2/FirstCyclingAPI), which has been integrated directly into the project. The API provides methods to fetch data from the FirstCycling website through web scraping.

## MCP Tools

The server exposes the following tools through the Model Context Protocol:

### Rider Information

| Tool | Description |
|------|-------------|
| `get_rider_info` | Get basic biographical information about a rider including nationality, birthdate, weight, height, and current team |
| `get_rider_best_results` | Retrieve a rider's best career results, sorted by importance |
| `get_rider_grand_tour_results` | Get a rider's results in Grand Tours (Tour de France, Giro d'Italia, Vuelta a España) |
| `get_rider_monument_results` | Retrieve a rider's results in cycling's Monument classics |
| `get_rider_team_and_ranking` | Get a rider's team history and UCI ranking evolution over time |
| `get_rider_race_history` | Retrieve a rider's complete race participation history, optionally filtered by year |
| `get_rider_one_day_races` | Get a rider's results in one-day races, optionally filtered by year |
| `get_rider_stage_races` | Get a rider's results in multi-day stage races, optionally filtered by year |
| `get_rider_teams` | Retrieve the complete team history of a rider throughout their career |
| `get_rider_victories` | Get a list of a rider's career victories, with optional filters for WorldTour or UCI races |

### Race Information

| Tool | Description |
|------|-------------|
| `get_race_results` | Retrieve results for a specific race edition by race ID and year |
| `get_race_overview` | Get general information about a race including history, records, and past winners |
| `get_race_stage_profiles` | Retrieve stage profiles and details for multi-stage races |
| `get_race_startlist` | Get the startlist for a specific race edition with detailed or basic team information |
| `get_race_victory_table` | Retrieve the all-time victory table for a race showing riders with most wins |
| `get_race_year_by_year` | Get year-by-year results for a race with optional classification filter |
| `get_race_youngest_oldest_winners` | Retrieve information about the youngest and oldest winners of a race |
| `get_race_stage_victories` | Get information about stage victories in multi-stage races |

### Search Tools

| Tool | Description |
|------|-------------|
| `search_rider` | Search for riders by name, returning their IDs and basic information |
| `search_race` | Search for races by name, returning their IDs and basic information |

## Usage

### Development Mode

You can test the server with MCP Inspector by running:

```
uv run mcp dev firstcycling.py
```

This will start the server and open the MCP Inspector in your browser, allowing you to test the available tools.

### Integration with Claude for Desktop

To integrate this server with Claude for Desktop:

1. Edit the Claude for Desktop config file, located at:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the server to your configuration:
   ```json
   {
     "mcpServers": {
       "firstcycling": {
         "command": "uv",
         "args": ["--directory", "/path/to/server/directory", "run", "firstcycling.py"]
       }
     }
   }
   ```

3. Restart Claude for Desktop

## License

MIT
