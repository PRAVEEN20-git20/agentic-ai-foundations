# Document Q&A Agent - Quick Start Guide

Get up and running with the Document Q&A Agent in 5 minutes!

---

## ⚡ Super Quick Start

```bash
# 1. Install dependencies
cd day2
pip install -r requirements.txt

# 2. Set up API key
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-your-key-here

# 3. Run the demo
python demo.py

# 4. Try the interactive CLI
python cli.py
```

---

## 📝 5-Minute Tutorial

### Step 1: Setup (1 minute)

```bash
# Navigate to day2 directory
cd day2

# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Key (1 minute)

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Don't have an API key?** Get one at [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### Step 3: Run the Demo (1 minute)

```bash
python demo.py
```

This shows you all the features without needing any documents.

### Step 4: Load Your First Document (1 minute)

Start the interactive CLI:

```bash
python cli.py
```

Load a PDF (replace with your own):

```
You: load path/to/your/document.pdf
```

### Step 5: Ask Questions! (1 minute)

```
You: What is this document about?
You: What are the main points?
You: Summarize the key findings
```

---

## 🎯 Common Use Cases

### Academic Research

```bash
python cli.py
> load research_paper.pdf
> What is the main contribution of this paper?
> What methodology did the authors use?
> What were the results?
```

### Business Documents

```bash
python cli.py
> load quarterly_report.pdf
> What were the key financial highlights?
> What are the main risks mentioned?
> Summarize the outlook section
```

### Legal Documents

```bash
python cli.py
> load contract.pdf
> What are the key terms of this agreement?
> What are the termination conditions?
> Summarize the liability clauses
```

### Technical Documentation

```bash
python cli.py
> load api_documentation.pdf
> How do I authenticate API requests?
> What are the rate limits?
> Explain the error codes
```

---

## 🔧 Programmatic Usage

For Python scripts:

```python
from doc_qa_agent import DocumentQAAgent

# Initialize
agent = DocumentQAAgent()

# Load document
agent.load_document("my_document.pdf")

# Ask questions
result = agent.ask("What are the main topics?")
print(result['answer'])

# View sources
for source in result['sources']:
    print(f"- {source['source']} (Page {source['page']})")
```

---

## 💡 Pro Tips

### Tip 1: Save Vector Stores

Don't re-process documents every time:

```
You: load big_document.pdf
[wait for processing...]
You: save my_docs
✓ Vector store 'my_docs' saved successfully

# Next session:
You: loadstore my_docs
✓ Vector store 'my_docs' loaded successfully
You: [Ask questions immediately!]
```

### Tip 2: Load Multiple Documents

Search across multiple files:

```
You: load doc1.pdf doc2.pdf doc3.pdf
[processes all documents]
You: Compare the findings across all three documents
```

### Tip 3: Check Status

See what's loaded:

```
You: status

📊 Agent Status
🔹 Documents loaded: 3
🔹 Total chunks: 142
🔹 Queries processed: 7
```

### Tip 4: Better Questions

Get better answers with specific questions:

❌ "Tell me about this"  
✅ "What is the main argument in section 3?"

❌ "What's in here?"  
✅ "What methodology did the researchers use for data collection?"

### Tip 5: View Sources

Always check the sources:

```python
result = agent.ask("Your question")
print(result['answer'])
print(f"Confidence: {result['confidence']}")

for source in result['sources']:
    print(f"- {source['source']} (Page {source['page']}, {source['similarity']*100:.0f}% relevant)")
```

---

## 🐛 Troubleshooting

### Problem: "OPENAI_API_KEY not set"

**Solution**: Create a `.env` file with your API key:

```bash
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### Problem: "No text could be extracted from PDF"

**Solution**: Your PDF might be image-based (scanned). Try:
1. Use a text-based PDF instead
2. OCR the PDF first (future enhancement)

### Problem: "ModuleNotFoundError: No module named 'openai'"

**Solution**: Install dependencies:

```bash
pip install -r requirements.txt
```

### Problem: Agent gives wrong answers

**Solutions**:
1. Check if the information is actually in the document
2. Try rephrasing your question more specifically
3. Load the correct document
4. Check the sources to see what context was used

### Problem: Slow performance

**Solutions**:
1. Save vector stores after first load
2. Reduce document size
3. Use smaller embedding model
4. Adjust chunk_size and chunk_overlap

---

## 📚 Next Steps

1. **Read the full README**: `README.md` for detailed documentation
2. **Run examples**: `python example_usage.py` for code examples
3. **Explore the code**: Check out the modular architecture
4. **Customize**: Adjust chunk sizes and models for your needs
5. **Extend**: Add new features like OCR or web interface

---

## 🆘 Need Help?

- Check `README.md` for detailed documentation
- Run `python demo.py` to see all features
- In the CLI, type `help` for commands
- Check the troubleshooting section above

---

## 🎉 You're Ready!

You now have a powerful document Q&A system. Some things to try:

- Load your research papers
- Query your business documents
- Search through technical manuals
- Analyze legal contracts
- Process meeting notes

**Happy querying! 📚🚀**

