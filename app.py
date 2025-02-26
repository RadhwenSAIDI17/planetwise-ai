import streamlit as st
from src.config import load_config, load_models_and_data
from src.workflow import build_workflow
from src.agents import AirQualityAPI

load_config()

# Set Streamlit page configuration
st.set_page_config(
    page_title="AI Assistant for Sustainable Development",
    page_icon=":earth_africa:",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Load models and data
@st.cache_resource
def get_resources():
    return load_models_and_data()


embedding_model, retriever, llm = get_resources()

import os

open_weather_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
air_quality_api = AirQualityAPI(api_key=open_weather_api_key)

# Build the workflow graph
app_workflow = build_workflow(retriever, llm, air_quality_api)


def main():
    st.title("🌍 AI Assistant for Sustainable Development")
    st.write(
        "Ask a question and let the AI assistant provide you with relevant information."
    )

    question = st.text_input("💬 Enter your question:", key="question_input")

    if question:
        inputs = {"question": question}
        with st.spinner("🤖 Processing your question..."):
            for output in app_workflow.stream(inputs):
                agent = list(output.keys())[0]
                response = output[agent]["documents"]
                if agent == "retrieve_internal":
                    st.subheader("📚 Information from Internal Documents")
                    st.markdown(response)
                elif agent == "fetch_air_quality":
                    st.subheader("🌤️ Air Quality Information")
                    st.markdown(response)
                elif agent == "visualize_data":
                    st.subheader("🗺️ CO₂ Emissions in France")
                    from src.agents import fig

                    if fig is not None:
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.warning("The map could not be generated.")
                    st.markdown(response)


if __name__ == "__main__":
    main()
