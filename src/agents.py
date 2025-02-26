import re
import requests
import pandas as pd
import plotly.express as px
from typing import TypedDict, List
from langchain.schema import Document

# Global figure to store the generated plot
fig = None


# Define the GraphState type
class GraphState(TypedDict):
    question: str
    documents: List[Document]


def retrieve_internal(state: GraphState, retriever, llm):
    """Agent to retrieve information from internal documents."""
    question = state["question"]
    documents = retriever.invoke(question)
    if documents:
        context = "\n\n".join(doc.page_content for doc in documents[:3])
        prompt = f"""Analyze the following documents and answer the question in a structured way.
Documents:
{context}
Question: {question}
Expected format:
1. Summary
2. Key Points
3. Recommendations"""
        response = llm.invoke(prompt)
        if hasattr(response, "content"):
            formatted_response = response.content.strip()
        elif isinstance(response, str):
            formatted_response = response.strip()
        else:
            formatted_response = "Error formatting the response."
        return {"documents": formatted_response}
    return {"documents": "No relevant documents found."}


def visualize_data(state: GraphState):
    """Agent to generate and return a CO₂ emissions map."""
    global fig
    try:
        csv_file = "data/emissions_co2_france.csv"
        df = pd.read_csv(csv_file)
        fig = px.scatter_map(
            df,
            lat="Latitude",
            lon="Longitude",
            size="CO2_Emissions",
            color="Emissions_Per_Capita",
            hover_name="Region",
            hover_data={
                "Population": ":,",
                "CO2_Emissions": True,
                "Emissions_Per_Capita": ":.2f",
                "Sector": True,
                "Description": True,
            },
            color_continuous_scale="YlOrRd",
            title="Detailed Map of CO₂ Emissions in France",
            size_max=50,
            map_style="carto-positron",
            zoom=5.5,
            center={"lat": 46.603354, "lon": 1.888334},
        )
        fig.update_layout(
            title_font=dict(size=24, color="darkblue"),
            font=dict(family="Arial", size=14),
            margin={"r": 0, "t": 50, "l": 0, "b": 0},
            coloraxis_colorbar=dict(
                title="Emissions per Capita (kt)",
                tickvals=[
                    df["Emissions_Per_Capita"].min(),
                    df["Emissions_Per_Capita"].max() / 2,
                    df["Emissions_Per_Capita"].max(),
                ],
                ticktext=["Low", "Medium", "High"],
            ),
            height=600,
        )
        return {"documents": "Interactive CO₂ emissions map generated successfully."}
    except Exception as e:
        return {"documents": f"Error generating the map: {str(e)}"}


class AirQualityAPI:
    """Helper class for fetching air quality data using the OpenWeatherMap API."""

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://api.openweathermap.org/data/2.5/air_pollution"
        self.geo_url = "http://api.openweathermap.org/geo/1.0/direct"

    def get_coordinates(self, city_name):
        params = {"q": city_name, "appid": self.api_key, "limit": 1}
        response = requests.get(self.geo_url, params=params)
        if response.status_code == 200 and response.json():
            data = response.json()[0]
            return data["lat"], data["lon"]
        return None, None

    def get_air_quality(self, lat, lon):
        params = {"lat": lat, "lon": lon, "appid": self.api_key}
        response = requests.get(self.base_url, params=params)
        return response.json() if response.status_code == 200 else None


def fetch_air_quality(state: GraphState, llm, air_quality_api):
    """Agent to fetch air quality data using the OpenWeatherMap API."""
    question = state["question"]
    extraction_prompt = f"Extract only the city name from this question: {question}"
    response = llm.invoke(extraction_prompt)
    if hasattr(response, "content"):
        city = response.content.strip()
    elif isinstance(response, str):
        city = response.strip()
    else:
        raise ValueError("Unexpected response format from LLM.")
    city = re.sub(r"[^\w\s]", "", city).strip()
    if not city:
        city = "Paris"  # Fallback default
    lat, lon = air_quality_api.get_coordinates(city)
    if lat is None or lon is None:
        return {"documents": f"Unable to find coordinates for city: {city}"}
    air_data = air_quality_api.get_air_quality(lat, lon)
    if air_data:
        aqi = air_data["list"][0]["main"]["aqi"]
        components = air_data["list"][0]["components"]
        summary = (
            f"## Air Quality in {city}\n"
            f"- **Air Quality Index (AQI)**: {aqi}\n"
            f"- **Pollutant Levels**:\n"
            f"  - Carbon Monoxide (CO): {components['co']} µg/m³\n"
            f"  - Nitrogen Dioxide (NO2): {components['no2']} µg/m³\n"
            f"  - Ozone (O3): {components['o3']} µg/m³\n"
            f"  - Fine Particles (PM2.5): {components['pm2_5']} µg/m³\n"
            f"  - Fine Particles (PM10): {components['pm10']} µg/m³\n\n"
            f"The Air Quality Index of {aqi} indicates that the air quality in {city} is satisfactory."
        )
        return {"documents": summary}
    return {"documents": "Unable to retrieve air quality data."}
