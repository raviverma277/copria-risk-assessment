
def apply_red_flag_rules(profile, rules):
    red_flags = []
    for rule in rules:
        try:
            field = rule["field"]
            condition = rule["condition"]
            # Use 'description' instead of 'message' to match the JSON structure
            message = rule.get("description", rule.get("message", "Red flag detected"))
            
            # Handle different condition types
            if ">" in condition and " and " not in condition:
                threshold = float(condition.split(">")[-1])
                field_value = profile.get(field, 0)
                # Handle non-numeric values for Number of Stories
                if field == "Number of Stories" and isinstance(field_value, str):
                    # Extract numeric value from strings like "Single-story", "Two-story", etc.
                    import re
                    numbers = re.findall(r'\d+', field_value)
                    if numbers:
                        field_value = float(numbers[0])
                    else:
                        # Map common text values to numbers
                        field_value = 1 if "single" in field_value.lower() else 0
                
                if float(field_value) > threshold:
                    red_flags.append(message)
            elif "<" in condition and " and " not in condition:
                threshold = float(condition.split("<")[-1])
                field_value = profile.get(field, 0)
                # Handle non-numeric values for Number of Stories
                if field == "Number of Stories" and isinstance(field_value, str):
                    import re
                    numbers = re.findall(r'\d+', field_value)
                    if numbers:
                        field_value = float(numbers[0])
                    else:
                        field_value = 1 if "single" in field_value.lower() else 0
                
                if float(field_value) < threshold:
                    red_flags.append(message)
            elif "==" in condition and " and " not in condition:
                # Fix the parsing to properly extract the expected value
                parts = condition.split("==")
                if len(parts) == 2:
                    expected = parts[1].strip().strip('"').strip("'")
                    profile_value = str(profile.get(field, "")).strip()
                    
                    if profile_value.lower() == expected.lower():
                        red_flags.append(message)
            elif "contains" in condition.lower():
                # Handle contains conditions like "contains 'AE' or 'VE' or 'A'"
                contains_parts = condition.lower().split("contains")[-1].strip()
                # Extract quoted strings
                import re
                quoted_values = re.findall(r"'([^']*)'", contains_parts)
                field_value = str(profile.get(field, "")).lower()
                if any(value.lower() in field_value for value in quoted_values):
                    red_flags.append(message)
            elif " and " in condition.lower():
                # Handle compound conditions like "Prior Claims == 'Yes' and Total Loss Amount > 100000"
                parts = condition.lower().split(" and ")
                all_conditions_met = True
                for part in parts:
                    part = part.strip()
                    if "==" in part:
                        # Extract field name and expected value
                        field_name = part.split("==")[0].strip()
                        expected = part.split("==")[-1].strip('"').strip("'")
                        if str(profile.get(field_name, "")).strip().lower() != expected.lower():
                            all_conditions_met = False
                            break
                    elif ">" in part:
                        # Extract field name and threshold
                        field_name = part.split(">")[0].strip()
                        threshold_str = part.split(">")[-1].strip()
                        try:
                            threshold = float(threshold_str)
                            field_value = profile.get(field_name, 0)
                            # Handle non-numeric values for Number of Stories
                            if field_name == "Number of Stories" and isinstance(field_value, str):
                                import re
                                numbers = re.findall(r'\d+', field_value)
                                if numbers:
                                    field_value = float(numbers[0])
                                else:
                                    field_value = 1 if "single" in field_value.lower() else 0
                            
                            if float(field_value) <= threshold:
                                all_conditions_met = False
                                break
                        except ValueError:
                            all_conditions_met = False
                            break
                if all_conditions_met:
                    red_flags.append(message)
        except Exception as e:
            print(f"Rule error for {field}: {e}")
    profile["Red Flags"] = red_flags
    return profile
