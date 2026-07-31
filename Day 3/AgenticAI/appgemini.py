import google.generativeai as genai
import math
import datetime
import requests


# --------------------------------
# CONFIGURE API
# --------------------------------
genai.configure(api_key="YOUR_API_KEY")


# --------------------------------
# LOAD MODEL
# --------------------------------
model = genai.GenerativeModel("gemini-1.5-flash")


# --------------------------------
# TOOLS
# --------------------------------
def calculator(query):
    try:
        return str(eval(query))
    except Exception as e:
        return str(e)


def square_root(query):
    try:
        return str(math.sqrt(float(query)))
    except Exception as e:
        return str(e)


def datetime_tool(query):
    try:
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        return f"Error: {str(e)}"


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



# --------------------------------
# SIMPLE AGENT LOOP
# --------------------------------
while True:

    user = input("\nAsk: ")

    prompt = f"""
    You are an AI agent.

    Available tools:
    1. calculator
    2. square_root

    User query:
    {user}

    Decide:
    - Which tool to use
    - What input to pass
    """

    response = model.generate_content(prompt)

    answer = response.text

    print("\nAgent Thinking:")
    print(answer)
