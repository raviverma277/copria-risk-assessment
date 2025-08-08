
import streamlit as st
import json
import os
from dotenv import load_dotenv
from utils.risk_mapper import generate_risk_profile
from utils.red_flag_engine import apply_red_flag_rules
from utils.llm_extractor import extract_risk_profile_from_text
from utils.pdf_reader import extract_text_from_pdf

load_dotenv()

st.set_page_config(layout="wide")
st.title("🏢 CoPRIA - Commercial Property Risk Intelligence Assistant")

st.markdown("### Upload Input Files")
submissions_file = st.file_uploader("Upload Submissions JSON", type="json")
schema_file = st.file_uploader("Upload Risk Profile Schema JSON", type="json")
rules_file = st.file_uploader("Upload Red Flag Rules JSON", type="json")

st.markdown("---")
st.markdown("### Or Paste Raw Submission Text or Upload PDF")
submission_text = st.text_area("Paste submission text here", height=200)
pdf_file = st.file_uploader("Or Upload Submission PDF", type=["pdf"])

st.markdown("---")
st.markdown("### Generate Risk Profiles")

if st.button("Generate"):
    if not schema_file or not rules_file:
        st.error("Please upload both schema and red flag rules files.")
    else:
        schema = json.load(schema_file)
        rules = json.load(rules_file)

        if submission_text or pdf_file:
            text = submission_text
            if pdf_file:
                text = extract_text_from_pdf(pdf_file)

            extracted_data = extract_risk_profile_from_text(text, schema)
            risk_profile = generate_risk_profile(extracted_data, schema)
            profile_with_flags = apply_red_flag_rules(risk_profile, rules)

            # Display summary with red flags highlighted
            st.markdown("### 🔍 Risk Profile Summary")
            
            # Create columns for better layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📋 Property Information")
                if profile_with_flags.get("Property Name"):
                    st.write(f"**Property:** {profile_with_flags['Property Name']}")
                if profile_with_flags.get("Property Address"):
                    st.write(f"**Address:** {profile_with_flags['Property Address']}")
                if profile_with_flags.get("State"):
                    st.write(f"**State:** {profile_with_flags['State']}")
                if profile_with_flags.get("Year Built"):
                    st.write(f"**Year Built:** {profile_with_flags['Year Built']}")
                if profile_with_flags.get("Construction Type"):
                    st.write(f"**Construction:** {profile_with_flags['Construction Type']}")
                if profile_with_flags.get("Total TIV"):
                    st.write(f"**Total TIV:** {profile_with_flags['Total TIV']}")
            
            with col2:
                st.markdown("#### 🛡️ Safety & Protection")
                sprinkler = profile_with_flags.get("Sprinkler System (Y/N)", "Unknown")
                fire_alarm = profile_with_flags.get("Fire Alarm (Y/N)", "Unknown")
                hazardous = profile_with_flags.get("Hazardous Materials (Y/N)", "Unknown")
                
                # Color code the safety indicators
                sprinkler_color = "🔴" if sprinkler == "No" else "🟢"
                fire_alarm_color = "🔴" if fire_alarm == "No" else "🟢"
                hazardous_color = "🔴" if hazardous == "Yes" else "🟢"
                
                st.write(f"**Sprinkler System:** {sprinkler_color} {sprinkler}")
                st.write(f"**Fire Alarm:** {fire_alarm_color} {fire_alarm}")
                st.write(f"**Hazardous Materials:** {hazardous_color} {hazardous}")
                
                if profile_with_flags.get("Flood Zone (e.g., Zone X, AE)"):
                    flood_zone = profile_with_flags["Flood Zone (e.g., Zone X, AE)"]
                    flood_color = "🔴" if flood_zone in ["AE", "VE", "A"] else "🟢"
                    st.write(f"**Flood Zone:** {flood_color} {flood_zone}")
                
                if profile_with_flags.get("Earthquake Exposure (Low/Moderate/High or ShakeMap Zone)"):
                    earthquake = profile_with_flags["Earthquake Exposure (Low/Moderate/High or ShakeMap Zone)"]
                    earthquake_color = "🔴" if earthquake == "High" else "🟢"
                    st.write(f"**Earthquake Exposure:** {earthquake_color} {earthquake}")

            # Display red flags prominently
            red_flags = profile_with_flags.get("Red Flags", [])
            if red_flags:
                st.markdown("### 🔴 Risk Flags Identified")
                for i, flag in enumerate(red_flags, 1):
                    st.markdown(f"**{i}.** {flag}")
                
                st.markdown(f"**Total Risk Flags:** {len(red_flags)}")
            else:
                st.markdown("### ✅ No Risk Flags Identified")
                st.success("This property appears to have no significant risk flags based on the current assessment.")

            # Show detailed JSON in expander
            with st.expander("📄 View Detailed Risk Profile (JSON)"):
                st.json(profile_with_flags)

            # Save to output
            os.makedirs("output", exist_ok=True)
            with open("output/risk_profiles.json", "w") as f:
                json.dump([profile_with_flags], f, indent=2)

        elif submissions_file:
            submissions = json.load(submissions_file)
            profiles = []

            st.markdown("### 📊 Multiple Property Risk Assessment")
            
            # Process all submissions
            for i, submission in enumerate(submissions):
                risk_profile = generate_risk_profile(submission, schema)
                profile_with_flags = apply_red_flag_rules(risk_profile, rules)
                profiles.append(profile_with_flags)

            # Display summary for each property
            for i, profile in enumerate(profiles):
                st.markdown(f"---")
                st.markdown(f"#### 🏢 Property {i+1}: {profile.get('Property Name', 'Unknown')}")
                
                # Create columns for property info
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Property Details:**")
                    if profile.get("State"):
                        st.write(f"• Location: {profile['State']}")
                    if profile.get("Construction Type"):
                        st.write(f"• Construction: {profile['Construction Type']}")
                    if profile.get("Total TIV"):
                        st.write(f"• Total TIV: {profile['Total TIV']}")
                
                with col2:
                    st.markdown("**Safety Status:**")
                    sprinkler = profile.get("Sprinkler System (Y/N)", "Unknown")
                    fire_alarm = profile.get("Fire Alarm (Y/N)", "Unknown")
                    hazardous = profile.get("Hazardous Materials (Y/N)", "Unknown")
                    
                    sprinkler_color = "🔴" if sprinkler == "No" else "🟢"
                    fire_alarm_color = "🔴" if fire_alarm == "No" else "🟢"
                    hazardous_color = "🔴" if hazardous == "Yes" else "🟢"
                    
                    st.write(f"• Sprinklers: {sprinkler_color} {sprinkler}")
                    st.write(f"• Fire Alarm: {fire_alarm_color} {fire_alarm}")
                    st.write(f"• Hazardous: {hazardous_color} {hazardous}")
                
                # Display red flags for this property
                red_flags = profile.get("Red Flags", [])
                if red_flags:
                    st.markdown("**🔴 Risk Flags:**")
                    for flag in red_flags:
                        st.markdown(f"• {flag}")
                else:
                    st.markdown("**✅ No Risk Flags**")

            # Overall summary
            st.markdown("---")
            st.markdown("### 📈 Overall Assessment Summary")
            
            total_properties = len(profiles)
            total_flags = sum(len(profile.get("Red Flags", [])) for profile in profiles)
            properties_with_flags = sum(1 for profile in profiles if profile.get("Red Flags"))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Properties Assessed", total_properties)
            with col2:
                st.metric("Properties with Risk Flags", properties_with_flags)
            with col3:
                st.metric("Total Risk Flags", total_flags)
            
            # Flag breakdown
            if total_flags > 0:
                st.markdown("**Risk Flag Breakdown:**")
                flag_counts = {}
                for profile in profiles:
                    for flag in profile.get("Red Flags", []):
                        flag_counts[flag] = flag_counts.get(flag, 0) + 1
                
                for flag, count in flag_counts.items():
                    st.write(f"• {flag}: {count} occurrence(s)")

            # Save to output
            os.makedirs("output", exist_ok=True)
            with open("output/risk_profiles.json", "w") as f:
                json.dump(profiles, f, indent=2)

        else:
            st.warning("Please upload a submission file or paste/upload text.")
