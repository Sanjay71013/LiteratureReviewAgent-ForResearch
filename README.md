# LiteratureReviewAgent-ForResearch

**LiteratureReviewAgent-ForResearch** is a modular, multi-agent system designed to streamline academic research workflows. It automates tasks such as literature discovery, summarization, and synthesis by leveraging specialized agents that interact through industry-standard protocols like Model Context Protocol (MCP) and Agent-to-Agent (A2A).

---

## 🧠 Overview

This system integrates various autonomous agents to perform distinct research-related functions:

* **Literature Discovery Agent**: Searches and retrieves relevant academic papers from sources like arXiv.
* **Summarization Agent**: Generates concise summaries of academic papers.
* **Web Browsing Agent**: Navigates and extracts information from web sources.
* **Synthesis Agent**: Combines insights from multiple papers to provide comprehensive overviews.
* **Critique Agent**: Evaluates the quality and relevance of retrieved literature.

These agents collaborate using standardized communication protocols to ensure interoperability and scalability.

---

## 🧩 Architecture

The system employs a layered architecture:

* **Agent Layer**: Comprises specialized agents, each responsible for a specific task.
* **Communication Layer**: Facilitates interaction between agents using A2A for peer-to-peer communication and MCP for tool and data access.
* **Tool Integration Layer**: Connects agents to external tools and data sources via MCP, enabling access to APIs and databases.

This architecture promotes modularity, allowing for easy addition or modification of agents and tools.

---

## 🔗 Protocols

### Model Context Protocol (MCP)

MCP provides a standardized interface for agents to access external tools and data sources. It ensures secure and structured communication, facilitating tasks like data retrieval and processing.

### Agent-to-Agent (A2A)

A2A enables direct communication between agents, allowing them to delegate tasks and share information efficiently. This protocol supports dynamic collaboration and task management across heterogeneous agent systems.
---

## ⚙️ Features

* **Modular Design**: Easily add or remove agents based on research needs.
* **Scalability**: Supports concurrent processing of multiple research tasks.
* **Interoperability**: Agents can be developed in different programming languages, thanks to standardized protocols.
* **Security**: Implements authentication and authorization mechanisms to protect data and agent interactions.
* **Extensibility**: Facilitates integration with new tools and data sources as research requirements evolve.

---

## 🚀 Getting Started

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Sanjay71013/LiteratureReviewAgent-ForResearch.git
   cd LiteratureReviewAgent-ForResearch
   ```



2. **Install Dependencies**:

   ```bash
   uv install -r requirements.txt
   ```



3. **env file**:
   
   Create a `.env` file to add your API keys for using LLMs.

4. **Run the System**:

   ```bash
   python main.py
   ```



---

## 📚 Use Case Example

A researcher seeks to understand recent advancements in multi-agent systems.

1. **Literature Discovery Agent**: Queries arXiv for relevant papers.
2. **Summarization Agent**: Generates summaries of the retrieved papers.
3. **Synthesis Agent**: Combines summaries to provide an overview of current trends.
4. **Critique Agent**: Evaluates the significance and quality of the findings.

This collaborative process delivers a comprehensive and concise literature review.
