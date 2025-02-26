# 🌍 PlanetWise AI

PlanetWise AI is an AI-powered assistant designed to provide valuable insights into sustainable development. It leverages state-of-the-art technologies to deliver accurate and actionable information. The project showcases cutting-edge AI techniques, including:

- **Retrieval-Augmented Generation (RAG):** Combines powerful language models with a search engine that retrieves relevant information from internal PDF documents for context-aware Q&A.
- **LangGraph Workflow Orchestration:** Uses LangGraph to create a dynamic and modular workflow, enabling seamless interaction between different agents (retrievers, models, and APIs) with flexibility and scalability.

## 🚀 Key Features & Strengths

- **Document Processing:** Extracts useful information from internal PDF documents to provide structured answers.
- **CO₂ Emissions Visualization:** Generates interactive maps of CO₂ emissions in France, highlighting regional environmental data clearly.
- **Air Quality Data Integration:** Retrieves real-time air quality data from OpenWeatherMap API, enabling easy monitoring of pollution levels.
- **Workflow Explanation:** Provides a clear explanation of the project’s architecture and the interactions between various components.

## 📁 Documentation & Presentation

For detailed insights into the project, please refer to the presentation file:

- [PlanetWise AI Presentation](docs/PlanetWise_AI_Presentation.pptx)  
  This file includes:
  - An overview of the project
  - Key features and strengths
  - A detailed explanation of the workflow

## 🎥 Video Demonstration

A short video demonstration is also provided in the repository to illustrate the application's functionalities in action.

- [PlanetWise AI Demo Video](docs/PlanetWise_AI_Demo.mp4)

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