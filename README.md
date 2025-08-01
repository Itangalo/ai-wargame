# ai-wargame

Tool for automating scenario-based war-gaming using LLMs as actors and
as the game master. Models are accessed through [OpenRouter](https://openrouter.ai/)
so any supported LLM can be plugged in.

## Running a Scenario

1. Create a scenario folder under `scenarios/` with a `config.yaml`
   describing the initial world state, metrics to track, each actor and
the game master. See `scenarios/example/config.yaml` for a template.
2. Export your `OPENROUTER_API_KEY`.
3. Run the scenario for a number of rounds:

```bash
python run.py scenarios/example --rounds 1
```

After each round a Markdown log is written under `scenarios/<name>/logs`
containing the initial world state for that round, actions by each actor
and the updated world state as decided by the game master.

## Requirements

- Python 3.10+
- `openai` Python client (for OpenRouter API)
- `pyyaml`

Install dependencies with:

```bash
pip install -r requirements.txt
```
