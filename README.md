# 🌍 PlanetWise AI

PlanetWise AI is an AI-powered assistant designed to provide valuable insights into sustainable development. It leverages state-of-the-art technologies to deliver accurate and actionable information. The project showcases cutting-edge AI techniques, including:

- **Retrieval-Augmented Generation (RAG):** Combines powerful language models with a search engine that retrieves relevant information from internal PDF documents, ensuring accurate and context-aware question answering.
- **LangGraph Workflow Orchestration:** Utilizes LangGraph to create a dynamic and modular workflow, enabling seamless interaction between different AI agents (retrievers, models, and APIs) while maintaining flexibility and scalability.

## 🚀 Key Features

- **Document Processing:** Extracts and processes information from internal PDF documents, providing structured and insightful answers to user queries.
- **CO₂ Emissions Visualization:** Generates interactive and detailed maps of CO₂ emissions in France, offering a clear view of regional environmental data.
- **Air Quality Data Integration:** Fetches real-time air quality data from the OpenWeatherMap API, making it easy to monitor pollution levels in specific locations.

## 🛠️ Installation Guide

Follow these steps to set up and run the project:

### 1️⃣ Install Dependencies
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt

### 2️⃣ Add API Keys
Set the following environment variables:
GROQ_API_KEY=your_groq_api_key
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key

### 3️⃣ Run the Application
streamlit run app.py