import google.generativeai as genai
import pandas as pd
import re
import os

# 🔐 SET YOUR API KEY HERE
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

def analyze_description(description):
    prompt = f"""Classify this ticket description. Is it related to DisputeApp access issue?
Description: "{description}"
Respond in JSON format with keys:
- access_issue: Yes or No
- email: Extracted email if access issue, otherwise "NA"
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

def extract_from_response(response):
    try:
        match = re.search(r'"access_issue"\s*:\s*"?(Yes|No)"?', response, re.IGNORECASE)
        email_match = re.search(r'"email"\s*:\s*"([^"]+)"', response)
        access_issue = match.group(1) if match else "Unknown"
        email = email_match.group(1) if email_match else "NA"
        return access_issue, email
    except Exception:
        return "Unknown", "NA"

def load_feedback():
    if os.path.exists("feedback.csv") and os.path.getsize("feedback.csv") > 0:
        return pd.read_csv("feedback.csv")
    return pd.DataFrame(columns=["ticket_number", "correct_access_issue", "correct_email"])

def main():
    df = pd.read_csv("incidents.csv")
    feedback_df = load_feedback()
    results = []

    for _, row in df.iterrows():
        ticket = row["ticket_number"]
        description = row["description"]

        # Check if we have feedback
        fb_row = feedback_df[feedback_df["ticket_number"] == ticket]
        if not fb_row.empty:
            access_issue = fb_row.iloc[0]["correct_access_issue"]
            email = fb_row.iloc[0]["correct_email"]
        else:
            response = analyze_description(description)
            access_issue, email = extract_from_response(response)

        results.append({
            "ticket_number": ticket,
            "access_issue": access_issue,
            "email": email
        })

    pd.DataFrame(results).to_csv("review.csv", index=False)
    print("Analysis saved to review.csv")

if __name__ == "__main__":
    main()
