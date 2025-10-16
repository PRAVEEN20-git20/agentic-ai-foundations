# Hello Advisor - Quick Start Guide

Get up and running with Hello Advisor in under 5 minutes! 🚀

## Installation

1. **Navigate to the day1 directory:**
   ```bash
   cd day1
   ```

2. **Verify Python version (3.8+ required):**
   ```bash
   python3 --version
   ```

3. **No additional dependencies needed!** Hello Advisor uses only Python standard library.

## Running the Agent

### Option 1: Interactive CLI (Recommended)

Start chatting with Hello Advisor:

```bash
python3 cli.py
```

Or if you made it executable:

```bash
./cli.py
```

### Option 2: View Examples

See example usage patterns:

```bash
python3 example_usage.py
```

### Option 3: Run Tests

Verify everything works:

```bash
python3 test_agent.py
```

### Option 4: Use Programmatically

```python
from hello_advisor import HelloAdvisor

agent = HelloAdvisor()
response = agent.process_input("Hello!")
print(response)
```

## What to Try

Once in the interactive CLI, try these:

1. **Say hello:**
   ```
   Hello!
   ```

2. **Tell it your name:**
   ```
   My name is [Your Name]
   ```

3. **Ask for a joke:**
   ```
   Tell me a programming joke
   ```

4. **Check what it remembers:**
   ```
   What do you know about me?
   ```

5. **Get session stats:**
   ```
   summary
   ```

6. **Ask for help:**
   ```
   help
   ```

7. **Exit when done:**
   ```
   exit
   ```

## Special CLI Commands

- `help` - Show available commands
- `summary` - Display session statistics
- `export` - Export memory state
- `clear` - Clear screen
- `exit`, `quit`, `q` - End session

## Understanding the Agent

### The Three Pillars

1. **🤖 Autonomy:** The agent decides how to respond without explicit programming for every case
2. **🧠 Memory:** Remembers your name, conversation history, and topics discussed
3. **💭 Reasoning:** Analyzes your input to understand intent and provide contextual responses

### What Makes It "Agentic"?

Unlike a simple if-else chatbot, Hello Advisor:
- Analyzes intent from natural language patterns
- Maintains state across interactions
- Makes decisions based on context and history
- Personalizes responses using memory
- Tracks and summarizes conversation metadata

## Next Steps

1. **Read the full README:** `README.md` for detailed documentation
2. **Explore the code:** Start with `hello_advisor.py` to see the agent logic
3. **Customize:** Add new intents, jokes, or capabilities
4. **Extend:** Integrate with LLM APIs for more sophisticated responses

## Troubleshooting

### "python: command not found"
Use `python3` instead of `python`

### Import errors
Make sure you're in the `day1` directory when running scripts

### Need help?
Run `python3 cli.py` and type `help` to see what the agent can do

---

**Happy chatting! 🤖✨**

For detailed documentation, see [README.md](README.md)

