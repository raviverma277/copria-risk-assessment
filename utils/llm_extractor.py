import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
print("Loaded OpenAI Key:", os.getenv("OPENAI_API_KEY"))

def extract_risk_profile_from_text(text, schema_fields):
    # Flatten all fields from schema
    fields = [field for section in schema_fields.values() for field in section]

    # Generate JSON example template
    json_template = {field: "" for field in fields}
    formatted_template = json.dumps(json_template, indent=2)

    prompt = f"""
You are a commercial property insurance assistant. Extract risk-related information from the submission text and map it to the required fields.

IMPORTANT: The text may use different terminology than the exact field names. Use your judgment to map the information correctly.

### Fields to extract:
{fields}

### Field Mapping Examples:
- "Address" or "Property Address" → "Property Address"
- "Year Built" or "constructed in [year]" → "Year Built" 
- "Construction Type" or "built using [material]" → "Construction Type"
- "Number of Stories" or "single-story", "two-story" → "Number of Stories"
- "Hazardous Materials" or "flammable materials", "hazardous" → "Hazardous Materials (Y/N)"
- "Sprinkler System" or "sprinklers" → "Sprinkler System (Y/N)"
- "Fire Alarm" or "fire alarms", "basic fire alarms" → "Fire Alarm (Y/N)"
- "Total TIV" or "total insured value" → "Total TIV"
- "Prior Claims" or "claims" → "Prior Claims (Y/N)"
- "Total Loss Amount" or "loss amounting to" → "Total Loss Amount"
- "Flood Zone" or "Zone AE", "Zone X" → "Flood Zone (e.g., Zone X, AE)"
- "Earthquake" or "seismic" → "Earthquake Exposure (Low/Moderate/High or ShakeMap Zone)"

### Critical Instructions:
1. For "Fire Alarm (Y/N)": If text mentions ANY fire alarms (including "basic fire alarms"), set to "Yes"
2. For "Hazardous Materials (Y/N)": If text mentions flammable materials, hazardous materials, or dangerous substances, set to "Yes"
3. For "Flood Zone": If text mentions "Zone AE", "Zone X", or any flood zone, extract the zone type
4. For "Sprinkler System (Y/N)": If text mentions "no sprinkler system" or "no sprinklers", set to "No"
5. Extract information even if the terminology doesn't exactly match
6. For Y/N fields, use "Yes" or "No" based on the presence/absence of the feature
7. For missing information, use empty string ""
8. Return valid JSON format

### Example JSON output:
{formatted_template}

### Submission Text:
{text}
"""

    try:
        # Use the new OpenAI API format
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=1000,
        )
        extracted = response.choices[0].message.content

        # Parse response into JSON
        return json.loads(extracted)

    except Exception as e:
        print(f"LLM extraction error: {str(e)}")
        return {"error": f"LLM extraction failed: {str(e)}"}
