# pyright: reportMissingImports=false, reportUndefinedVariable=false
import asyncio
from pyscript import document,when, fetch



# 1. KNOWLEDGE BASE (Hash Map / Dictionary)
raw_responses = {
    ("hello", "hi", "hey"): "Hello! Welcome in Burhan.",
    ("aoa", "salam"): "WAS, Welcome in burhan, how may i help you",
    ("namaskar",): "Namastay! welcome in burhan",
    ("musalman", "Who are Muslims?", "Muslims?"): "people who followed Prophet Muhammad (S.A.W)",
    ("pillars of islam", "islamic pillars", "arkan e islam", "what are the pilars of Islam"): "Islam have 5 pillars: Shahadah, Salah, Zakat, Sawm, aur Hajj.",
    ("hindus","who are hindus", "hindus?"): "Hindus are people who religiously practice Hinduism",
    ("hindus important book", "which book followed by hindus"): "Bhagvad Gita, Ramayan",
    ("christians important book","which book followed by christians"): "Bible",
    ("christianity", "who are christians", "christians?" ): "A person who follows Prophet Jesus.",
    ("who is saad", "about saad", "saad kaun hai"): "Saad is computer science student in AUST (Pakistan)",
    ("pakistan", "what is pakistan", "Pakistan kya hai"): "A beautiful country and hospitable people. Located in South asia",
    ("india", "what is India", "india kya hai"): "where nature meets its destination. Located in south asia",
    ("india and pakistan", "indo pak", "pakistan india"): "neighbouring country and divided by the British policy (Divide and rule)",
    ("How are you", "kaisay ho",): "I am the AI made by Saad. I have no physical existence",
    ("who are you", "tum kon ho", "kon ho tum"): "I am the rule based chatbot of decodelabs. Made by Saad",
    ("help", "menu", "options"): "You can write question or press quit, to finish this chat. Try 'weather karachi' for a single city, or 'weather all' for 10 Pakistan + 10 India cities at once."
}
 
 
# 2. DICTIONARY FLATTENING
responses = {}
for triggers, reply in raw_responses.items():
    for word in triggers:
        responses[word] = reply
 
exit_commands = ["exit", "bye", "quit", "allah hafiz"]
 
# 3. WEATHER MODULE — 10 Pakistan + 10 India cities
# lat/lon fixed hain taake koi geocoding call na karni pade (fast + reliable)
# "fallback" static estimate hai jo tab use hoga jab live fetch fail ho jaye (no internet / API down)
CITY_DATA = {
    # ---- Pakistan ----
    "karachi":     {"lat": 24.8607, "lon": 67.0011, "country": "PK", "fallback": "30°C, Humid & Sunny"},
    "lahore":      {"lat": 31.5497, "lon": 74.3436, "country": "PK", "fallback": "37°C, Hazy"},
    "islamabad":   {"lat": 33.6844, "lon": 73.0479, "country": "PK", "fallback": "32°C, Partly Cloudy"},
    "rawalpindi":  {"lat": 33.5651, "lon": 73.0169, "country": "PK", "fallback": "30°C, Partly Cloudy"},
    "faisalabad":  {"lat": 31.4180, "lon": 73.0790, "country": "PK", "fallback": "36°C, Clear"},
    "multan":      {"lat": 30.1575, "lon": 71.5249, "country": "PK", "fallback": "38°C, Hot & Dry"},
    "peshawar":    {"lat": 34.0151, "lon": 71.5249, "country": "PK", "fallback": "34°C, Clear"},
   "abbottabad": {"lat": 34.1463, "lon": 73.2116, "country": "PK", "fallback": "22°C, Cool & Pleasant"},
    "gujranwala":  {"lat": 32.1877, "lon": 74.1945, "country": "PK", "fallback": "34°C, Hazy"},
    # ---- India ----
    "delhi":       {"lat": 28.6139, "lon": 77.2090, "country": "IN", "fallback": "36°C, Hazy Sunshine"},
    "mumbai":      {"lat": 19.0760, "lon": 72.8777, "country": "IN", "fallback": "31°C, Humid"},
    "bangalore":   {"lat": 12.9716, "lon": 77.5946, "country": "IN", "fallback": "26°C, Pleasant"},
    "kolkata":     {"lat": 22.5726, "lon": 88.3639, "country": "IN", "fallback": "33°C, Humid"},
    "chennai":     {"lat": 13.0827, "lon": 80.2707, "country": "IN", "fallback": "34°C, Hot & Humid"},
    "pune":        {"lat": 18.5204, "lon": 73.8567, "country": "IN", "fallback": "28°C, Pleasant"},
    "jaipur":      {"lat": 26.9124, "lon": 75.7873, "country": "IN", "fallback": "37°C, Dry Heat"},
    "ahmedabad":   {"lat": 23.0225, "lon": 72.5714, "country": "IN", "fallback": "38°C, Hot"},
    "hyderabad":   {"lat": 17.3850, "lon": 78.4867, "country": "IN", "fallback": "32°C, Partly Cloudy"},
    "lucknow":     {"lat": 26.8467, "lon": 80.9462, "country": "IN", "fallback": "35°C, Hazy"},
}
 
# Open-Meteo "weathercode" ka simplified mapping
WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Rain showers", 81: "Moderate showers", 82: "Violent showers",
    95: "Thunderstorm",
}
 
 
async def get_weather_reply(city_key):
    """Live weather fetch karta hai. Fail ho jaye tu static fallback deta hai."""
    city = CITY_DATA[city_key]
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={city['lat']}&longitude={city['lon']}&current_weather=true"
        )
        response = await fetch(url)
        data = await response.json()
        cw = data["current_weather"]
        temp = cw["temperature"]
        wind = cw["windspeed"]
        condition = WEATHER_CODES.get(cw["weathercode"], "Unknown conditions")
        return f"{city_key.title()} ({city['country']}): {temp}°C, {condition}, wind {wind} km/h — live"
    except Exception:
        return f"{city_key.title()} ({city['country']}): {city['fallback']} — offline estimate"
 
 
async def get_all_weather_reply():
    """LOOP: saari 20 cities (10 PK + 10 IN) ka weather ek sath fetch karta hai."""
    tasks = [get_weather_reply(city) for city in CITY_DATA]
    results = await asyncio.gather(*tasks)
 
    pk_lines = [r for city, r in zip(CITY_DATA, results) if CITY_DATA[city]["country"] == "PK"]
    in_lines = [r for city, r in zip(CITY_DATA, results) if CITY_DATA[city]["country"] == "IN"]
 
    html = "<b>🇵🇰 Pakistan</b><br>" + "<br>".join(pk_lines)
    html += "<br><br><b>🇮🇳 India</b><br>" + "<br>".join(in_lines)
    return html
 
 
chat_box = document.getElementById("chat-history")
user_input_field = document.getElementById("user-input")
 
 
def append_user_message(text):
    chat_box.innerHTML += f"""
    <div class="row row-user">
      <div class="bubble bubble-user">{text}</div>
    </div>
    """
    chat_box.scrollTop = chat_box.scrollHeight
 
 
def append_bot_message(text, matched_key):
    if matched_key:
        tag_html = f'<div class="match-tag">matched: "{matched_key}"</div>'
    else:
        tag_html = '<div class="match-tag match-tag-none">no pattern matched</div>'
 
    chat_box.innerHTML += f"""
    <div class="row row-bot">
      <div class="bubble bubble-bot">
        {text}
        {tag_html}
      </div>
    </div>
    """
    chat_box.scrollTop = chat_box.scrollHeight
 
 
def show_typing():
    chat_box.innerHTML += """
    <div class="row row-bot" id="typing-row">
      <div class="bubble bubble-bot typing"><span></span><span></span><span></span></div>
    </div>
    """
    chat_box.scrollTop = chat_box.scrollHeight
 
 
def hide_typing():
    row = document.getElementById("typing-row")
    if row:
        row.remove()
 
 
async def process_input():
    raw_input = user_input_field.value
 
    # Agar user ne khali 'Send' daba diya toh kuch mat karo
    if not raw_input.strip():
        return
 
    append_user_message(raw_input)
    user_input_field.value = ""
 
    # Sanitization
    clean_input = raw_input.lower().strip().replace("?", "").replace(".", "")
 
    show_typing()
 
    # ---- WEATHER INTENT ----
    if clean_input in ("weather all", "mausam sab", "weather sab", "sab shehar", "all weather"):
        reply = await get_all_weather_reply()
        hide_typing()
        append_bot_message(reply, "weather: all (loop over 20 cities)")
        return
 
    if clean_input.startswith("weather ") or clean_input.startswith("mausam "):
        city_query = clean_input.split(" ", 1)[1].strip()
        if city_query in CITY_DATA:
            reply = await get_weather_reply(city_query)
            hide_typing()
            append_bot_message(reply, f"weather: {city_query}")
        else:
            hide_typing()
            cities_list = ", ".join(CITY_DATA.keys())
            append_bot_message(f"Ye city list mein nahi hai. Try: {cities_list}", None)
        return
 
    # ---- NORMAL RULE-BASED FLOW ----
    await asyncio.sleep(0.5)
    hide_typing()
 
    if clean_input in exit_commands:
        append_bot_message("Session ended. Thanks for using BURHAN! Please close the tab.", clean_input)
    elif clean_input in responses:
        append_bot_message(responses[clean_input], clean_input)
    else:
        append_bot_message(
            "Error: I don't know what you are saying, please type help for more assistance.",
            None
        )
 
 
@when("click", "#send-btn")
async def on_send_click(event):
    await process_input()
 
 
@when("keydown", "#user-input")
async def on_enter_key(event):
    if event.key == "Enter":
        await process_input()
 