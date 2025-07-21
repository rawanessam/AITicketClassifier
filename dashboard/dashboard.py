import streamlit as st
import json
import pandas as pd
import altair as alt
from pathlib import Path
from dotenv import load_dotenv
import os 

load_dotenv()

config = os.getenv("CONFIG_FILE")
src_path = os.getcwd()
### Process config file
config_dict = json.loads(open(f"../{config}").read())

DB_PATH = config_dict["DB_path"]
print(DB_PATH)
# ---- Load ticket data ----
@st.cache_data
def load_data(json_path):
    if not Path(json_path).exists():
        return []
    with open(json_path, "r") as f:
        return json.load(f)

# ---- Parse ticket data into DataFrame ----
def tickets_to_df(tickets):
    records = []
    for ticket in tickets:
        data = {
            "ticket_id": ticket["ticket_id"],
            "first_name": ticket["user_data"]["data"]["first_name"],
            "last_name": ticket["user_data"]["data"]["last_name"],
            "email": ticket["user_data"]["data"]["email"],
            "description": ticket["user_data"]["data"]["issue_description"],
            "category": ticket["llm_response"]["category"],
            "urgency_score": ticket["llm_response"]["urgency_score"],
        }
        records.append(data)
    return pd.DataFrame(records)

# ---- Main Dashboard ----
def main():
    st.title("🛠️ IT Support Ticket Dashboard")

    json_path = "../"+DB_PATH  # adjust as needed
    print(json_path)
    tickets = load_data(json_path)

    if not tickets:
        st.warning("No ticket data found.")
        return

    df = tickets_to_df(tickets)

    # Metrics
    total_tickets = len(df)
    missing_urgency = df['urgency_score'].isnull().sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Tickets", total_tickets)
    col2.metric("Missing Urgency Score", missing_urgency)

    # Category Distribution
    st.subheader("📊 Tickets by Category")
    category_chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("category:N", title="Category"),
            y=alt.Y("count():Q", title="Number of Tickets"),
            tooltip=["category", "count()"]
        )
        .properties(width=600, height=300)
    )
    st.altair_chart(category_chart)

    # Recent Tickets
    st.subheader("🧾 Recent Tickets")
    st.dataframe(df.sort_values("ticket_id", ascending=False).head(5))

if __name__ == "__main__":
    main()
