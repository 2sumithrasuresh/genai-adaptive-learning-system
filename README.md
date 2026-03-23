# Adaptive Explanations Engine

An intelligent GenAI-powered learning system that dynamically adapts explanations based on student responses.
The system evaluates answers, identifies misconceptions, and personalizes explanations using Retrieval-Augmented Generation (RAG), self-evaluation, and transferable teaching strategies.

---

## Features

- **Adaptive Learning**
  - Adjusts difficulty based on student performance
  - Identifies conceptual vs partial understanding

- **RAG-Based Knowledge Retrieval**
  - Retrieves relevant content from structured learning material
  - Ensures accurate and context-aware explanations

- **Self-Evaluation Engine**
  - Scores explanations based on clarity and effectiveness
  - Learns which teaching strategies work best

- **Transfer Learning**
  - Reuses effective explanation strategies across subjects
  - Enables scalability beyond a single domain

---

## How It Works

1. User selects a topic
2. System generates a question
3. Student submits an answer
4. Answer is evaluated using LLM
5. Relevant content is retrieved (RAG)
6. Explanation is generated and adapted
7. System scores its own explanation
8. Strategy is updated for future iterations

---

## Project Structure

```bash
src/
├── adaptive/ # Adaptive learning engine
├── rag/ # Retrieval-Augmented Generation system
├── meta/ # Self-evaluation and strategy learning
├── content/ # Learning materials
├── llm/ # LLM client interface
├── prompts/ # Prompt templates
├── pipeline/ # Main orchestration logic
```

---

## Tech Stack

- **Language:** Python
- **Frontend (planned):** React
- **LLM Integration:** OpenAI / compatible APIs
- **Vector Database:** FAISS / Chroma (planned)
- **Backend:** Python-based pipeline

---

## 🛠️ Setup & Installation

### Prerequisites

- Python 3.10+
- LLM API Key (e.g., OpenAI)

### Installation

```bash
git clone https://github.com/your-username/adaptive-explanations-engine.git
cd adaptive-explanations-engine
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

---

## Future Improvements

- Persistent student modeling (database integration)
- Advanced semantic chunking for RAG
- UI dashboard for learning visualization
- Multi-user support
- Performance benchmarking across subjects

---

## Contributors

<a href="https://github.com/2sumithrasuresh">
  <img src="https://github.com/2sumithrasuresh.png" width="20px;" />
  Sumithra Suresh
</a>
<br/>
<a href="https://github.com/spandhana-2128">
  <img src="https://github.com/spandhana-2128.png" width="20px;" />
   Spandhana K S
</a>
<br/>
<a href="https://github.com/Tevin-ph">
  <img src="https://github.com/Tevin-ph.png" width="20px;" />
  Tevin Philip
</a>

---

## Project Vision
To move beyond static AI tutoring and build a system that learns how to teach better over time, adapting not just to content, but to the learner.

