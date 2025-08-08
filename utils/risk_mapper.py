
def generate_risk_profile(submission, schema):
    profile = {}

    # Initialize all fields from schema with default values
    for section_fields in schema.values():
        for field in section_fields:
            profile[field] = ""

    # Helper function to extract nested values
    def get_nested_value(data, key_path):
        """Extract value from nested dictionary using dot notation or direct key"""
        if key_path in data:
            return data[key_path]
        
        # Try to find in nested structures
        for key, value in data.items():
            if isinstance(value, dict):
                if key_path in value:
                    return value[key_path]
                # Recursively search nested dicts
                nested_result = get_nested_value(value, key_path)
                if nested_result is not None:
                    return nested_result
        return None

    # Map submission data to profile - PRIORITIZE LLM EXTRACTION
    for section_fields in schema.values():
        for field in section_fields:
            value = submission.get(field) or get_nested_value(submission, field)
            if value is not None and value != "":
                profile[field] = value

    # Only apply risk mapper logic if LLM didn't extract the value
    year_built = int(submission.get("Year Built", 0))
    if not profile.get("Roof > 20 yrs"):
        profile["Roof > 20 yrs"] = "Yes" if year_built and 2025 - year_built > 20 else "No"
    
    # Handle Total TIV from various possible sources
    if not profile.get("Total TIV"):
        total_tiv = (submission.get("Total Insured Value (USD)") or 
                     submission.get("Total TIV") or 
                     get_nested_value(submission, "Total Insured Value (USD)"))
        profile["Total TIV"] = str(total_tiv) if total_tiv else ""

    # Handle fire protection logic ONLY if LLM didn't extract these values
    if not profile.get("Sprinkler System (Y/N)"):
        fire_prot = (submission.get("Fire Protection", "") or 
                     get_nested_value(submission, "Fire Protection") or "").lower()
        
        # Also check COPE.Protection if available
        cope_protection = get_nested_value(submission, "Protection")
        if cope_protection:
            fire_prot += " " + cope_protection.lower()
        
        profile["Sprinkler System (Y/N)"] = "Yes" if "sprinkler" in fire_prot else "No"

    if not profile.get("Fire Alarm (Y/N)"):
        fire_prot = (submission.get("Fire Protection", "") or 
                     get_nested_value(submission, "Fire Protection") or "").lower()
        
        cope_protection = get_nested_value(submission, "Protection")
        if cope_protection:
            fire_prot += " " + cope_protection.lower()
        
        profile["Fire Alarm (Y/N)"] = "Yes" if "alarm" in fire_prot or "fire alarm" in fire_prot else "No"

    # Handle natural hazard exposure ONLY if LLM didn't extract
    if not profile.get("Flood Zone (e.g., Zone X, AE)"):
        hazard = (submission.get("Natural Hazard Exposure", "") or 
                  get_nested_value(submission, "Natural Hazard Exposure") or "").lower()
        
        if "zone ae" in hazard:
            profile["Flood Zone (e.g., Zone X, AE)"] = "AE"
        elif "zone x" in hazard:
            profile["Flood Zone (e.g., Zone X, AE)"] = "X"
        else:
            profile["Flood Zone (e.g., Zone X, AE)"] = "Unknown"

    # Handle earthquake exposure ONLY if LLM didn't extract
    if not profile.get("Earthquake Exposure (Low/Moderate/High or ShakeMap Zone)"):
        hazard = (submission.get("Natural Hazard Exposure", "") or 
                  get_nested_value(submission, "Natural Hazard Exposure") or "").lower()
        
        if "earthquake" in hazard and "high" in hazard:
            profile["Earthquake Exposure (Low/Moderate/High or ShakeMap Zone)"] = "High"
        elif "earthquake" in hazard and "moderate" in hazard:
            profile["Earthquake Exposure (Low/Moderate/High or ShakeMap Zone)"] = "Moderate"
        else:
            profile["Earthquake Exposure (Low/Moderate/High or ShakeMap Zone)"] = "Low"

    # Handle wildfire risk ONLY if LLM didn't extract
    if not profile.get("Wildfire Risk (Low/Moderate/High or ISO Class)"):
        hazard = (submission.get("Natural Hazard Exposure", "") or 
                  get_nested_value(submission, "Natural Hazard Exposure") or "").lower()
        
        if "wildfire" in hazard and "high" in hazard:
            profile["Wildfire Risk (Low/Moderate/High or ISO Class)"] = "High"
        elif "wildfire" in hazard and "moderate" in hazard:
            profile["Wildfire Risk (Low/Moderate/High or ISO Class)"] = "Moderate"
        else:
            profile["Wildfire Risk (Low/Moderate/High or ISO Class)"] = "Low"

    # Set default values for required fields if not present
    if not profile.get("Prior Claims (Y/N)"):
        profile["Prior Claims (Y/N)"] = submission.get("Prior Claims (Y/N)", "No")
    if not profile.get("Total Loss Amount"):
        profile["Total Loss Amount"] = submission.get("Total Loss Amount", "0")
    if not profile.get("Number of Stories"):
        profile["Number of Stories"] = submission.get("Number of Stories", "1")
    
    # Handle construction type from various sources
    if not profile.get("Construction Type"):
        construction = (submission.get("Construction Type") or 
                       get_nested_value(submission, "Construction") or 
                       submission.get("COPE", {}).get("Construction") or "")
        profile["Construction Type"] = construction

    # Handle occupancy type
    if not profile.get("Occupancy Type"):
        occupancy = (submission.get("Occupancy Type") or 
                     get_nested_value(submission, "Occupancy") or "")
        profile["Occupancy Type"] = occupancy

    # Handle hazardous materials ONLY if LLM didn't extract
    if not profile.get("Hazardous Materials (Y/N)"):
        risk_factors = submission.get("Risk Factors", "").lower()
        profile["Hazardous Materials (Y/N)"] = "Yes" if "hazardous" in risk_factors or "lithium" in risk_factors else "No"

    return profile
