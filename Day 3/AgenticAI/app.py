from langchain_community.llms import Ollama
from langchain_classic.agents import initialize_agent
from langchain_classic.agents import Tool
from langchain_classic.agents import AgentType
import math
import datetime
import requests


# -----------------------------
# LOCAL LLM
# -----------------------------
llm = Ollama(model="gemma4")


# -----------------------------
# TOOL 1 : Calculator
# -----------------------------
def calculator_tool(query):
    try:
        result = eval(query)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


# -----------------------------
# TOOL 2 : Square Root
# -----------------------------
def sqrt_tool(query):
    try:
        number = float(query)
        return str(math.sqrt(number))
    except Exception as e:
        return f"Error: {str(e)}"


# -----------------------------
# TOOL 3 : Current Datetime
# -----------------------------
def datetime_tool(query):
    try:
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return f"Error: {str(e)}"


# -----------------------------
# TOOL 4 : Weather Forecast
# -----------------------------
def weather_tool(city):
    try:
        city = city.strip()
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
        geo_resp = requests.get(geo_url).json()
        if not geo_resp.get("results"):
            return f"Could not find coordinates for city: {city}"
        
        result = geo_resp["results"][0]
        lat, lon = result["latitude"], result["longitude"]
        name = result["name"]
        country = result.get("country", "")
        
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_resp = requests.get(weather_url).json()
        
        current = weather_resp.get("current_weather", {})
        temp = current.get("temperature")
        windspeed = current.get("windspeed")
        
        return f"Current weather in {name}, {country}: Temperature is {temp}°C, Windspeed is {windspeed} km/h."
    except Exception as e:
        return f"Error fetching weather: {str(e)}"


# -----------------------------
# TOOL 5 : Wikipedia Search
# -----------------------------
def wikipedia_tool(query):
    try:
        url = "https://en.wikipedia.org/w/api.php"
        headers = {"User-Agent": "GenAINotebookAgent/1.0 (harinikesh@example.com)"}
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srsearch": query,
            "utf8": 1,
            "formatversion": 2
        }
        resp = requests.get(url, params=params, headers=headers).json()
        search_results = resp.get("query", {}).get("search", [])
        if not search_results:
            return f"No Wikipedia page found for query: {query}"
        
        top_result = search_results[0]
        title = top_result["title"]
        snippet = top_result["snippet"].replace('<span class="searchmatch">', '').replace('</span>', '')
        
        summary_params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": title,
            "formatversion": 2
        }
        summary_resp = requests.get(url, params=summary_params, headers=headers).json()
        pages = summary_resp.get("query", {}).get("pages", [])
        if pages:
            extract = pages[0].get("extract", "")
            if extract:
                return f"Wikipedia Summary for '{title}': {extract[:500]}..."
        
        return f"Wikipedia snippet for '{title}': {snippet}..."
    except Exception as e:
        return f"Error fetching Wikipedia data: {str(e)}"


# -----------------------------
# TOOLS LIST
# -----------------------------
tools = [
    Tool(
        name="Calculator",
        func=calculator_tool,
        description="Useful for mathematical calculations. Input must be a valid math expression."
    ),

    Tool(
        name="SquareRoot",
        func=sqrt_tool,
        description="Useful for square root calculations. Input must be a number."
    ),

    Tool(
        name="CurrentDateTime",
        func=datetime_tool,
        description="Useful for getting the current date and time. Input can be anything (ignored)."
    ),

    Tool(
        name="WeatherForecast",
        func=weather_tool,
        description="Useful for getting real-time weather details of a city. Input must be the city name."
    ),

    Tool(
        name="WikipediaSearch",
        func=wikipedia_tool,
        description="Useful for looking up factual information or definitions about various topics on Wikipedia. Input must be a search term."
    )
]


# -----------------------------
# AGENT
# -----------------------------
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)


# -----------------------------
# USER QUERY
# -----------------------------
query = input("Ask Something: ")

response = agent.run(query)

print("\nFINAL ANSWER:")
print(response)
