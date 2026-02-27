# Import required libraries
import streamlit as st              # Streamlit dashboard banane ke liye
import sqlite3                      # SQLite database connect karne ke liye
import pandas as pd                 # Data handle karne ke liye
import matplotlib.pyplot as plt     # Charts banane ke liye
import io                           # Data ko memory me excel file banane ke liye


# -------- Function: Convert DataFrame to Excel for Download --------
def convert_df_to_excel(df):
    # Ye function dataframe ko excel format me convert karta hai
    # taki user dashboard se file download kar sake
    output = io.BytesIO()  # memory me temporary excel file banane ke liye

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)  # dataframe ko excel file me likh diya

    return output.getvalue()  # excel file binary format me return hogi


# -------- Streamlit Page Configuration --------
st.set_page_config(page_title="Job Application Tracker", layout="wide")

# Dashboard ka main title
st.title("Job Application Tracker Dashboard")


# -------- Database Functions --------

def load_data():
    # Ye function database se saara data load karta hai
    # aur latest applications ko upar sort karta hai
    conn = sqlite3.connect("applications.db")

    df = pd.read_sql_query(
        "SELECT * FROM applications ORDER BY date_applied DESC", conn
    )

    conn.close()  # database connection close
    return df


def update_status(app_id, new_status):
    # Ye function kisi application ka status update karta hai
    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE applications SET status = ? WHERE id = ?",
        (new_status, app_id)
    )

    conn.commit()  # changes save
    conn.close()

def delete_application(app_id):
    # ye function database se ek specific application delete karega
    conn = sqlite3.connect("applications.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM applications WHERE id = ?",
        (app_id,)
    )

    conn.commit()   # changes save
    conn.close()    # connection close

# -------- Load Application Data --------
df = load_data()

# date_applied column ko datetime format me convert kar rahe hain
df["date_applied"] = pd.to_datetime(df["date_applied"])

# calculate kar rahe hain kitne din ho gaye apply kiye hue
df["days_since_applied"] = (pd.Timestamp.today() - df["date_applied"]).dt.days

# agar status "Applied" hai aur 10 din se zyada ho gaye
# to follow up needed flag true ho jayega
df["follow_up_needed"] = (
    (df["status"] == "Applied") &
    (df["days_since_applied"] > 10)
)

# agar database empty hai to warning show karenge
if df.empty:
    st.warning("No applications logged yet.")
    st.stop()


# -------- Download Excel Section --------
st.subheader("Download Applications")

# dataframe ko excel format me convert kiya
excel_file = convert_df_to_excel(df)

# streamlit download button
st.download_button(
    label="Download Excel File",
    data=excel_file,
    file_name="job_applications.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


# -------- Key Metrics Section --------
st.subheader("Application Metrics")

# important metrics calculate kar rahe hain
total_apps = len(df)
interviews = len(df[df["status"] == "Interview"])
offers = len(df[df["status"] == "Offer"])

# interview conversion rate calculate
conversion_rate = (interviews / total_apps * 100) if total_apps > 0 else 0

# dashboard me 4 columns bana rahe hain
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Applications", total_apps)
col2.metric("Interviews", interviews)
col3.metric("Offers", offers)
col4.metric("Interview Conversion %", f"{conversion_rate:.2f}%")

# -------- Follow-Up Recommendation Section --------

st.subheader("Applications Needing Follow-Up")

# yaha hum un applications ko filter kar rahe hain
# jinka status abhi bhi "Applied" hai aur 10 din se zyada ho gaye hain

followups = df[df["follow_up_needed"] == True]

# agar koi follow-up required nahi hai
if followups.empty:

    # user ko inform karenge ki sab applications recent hain
    st.info("No applications currently require follow-up")

else:

    # sirf important columns show karenge
    followups_display = followups[[
        "company",
        "role",
        "days_since_applied",
        "status"
    ]]

    # table show kar rahe hain dashboard me
    st.dataframe(
        followups_display,
        use_container_width=True
    )

# -------- Sidebar Filters --------
st.sidebar.header("Filters")

# status filter dropdown
status_filter = st.sidebar.selectbox(
    "Filter by Status",
    ["All"] + list(df["status"].unique())
)

# company search box
company_search = st.sidebar.text_input("Search Company")

# filtered dataframe banaya
filtered_df = df.copy()

# agar specific status select hua hai to filter lagayenge
if status_filter != "All":
    filtered_df = filtered_df[filtered_df["status"] == status_filter]

# company name search filter
if company_search:
    filtered_df = filtered_df[
        filtered_df["company"].str.contains(company_search, case=False)
    ]


# -------- Display Applications Table --------
st.subheader("Applications")

# follow up needed rows ko highlight karne ke liye function
def highlight_followups(row):
    if row["follow_up_needed"]:
        return ["background-color: #ffcccc"] * len(row)
    return [""] * len(row)

# dataframe styling apply
styled_df = filtered_df.style.apply(highlight_followups, axis=1)

# dashboard me table show
st.dataframe(styled_df, use_container_width=True)


# -------- Status Distribution Chart --------
st.subheader("Status Distribution")

# har status ka count nikal rahe hain
status_counts = df["status"].value_counts()

# bar chart bana rahe hain
fig1, ax1 = plt.subplots()
status_counts.plot(kind="bar", ax=ax1)

ax1.set_ylabel("Number of Applications")
ax1.set_xlabel("Status")

# chart streamlit me display
st.pyplot(fig1)


# -------- Weekly Applications Chart --------
st.subheader("Applications Over Time")

# week wise applications count kar rahe hain
apps_per_week = df.resample("W", on="date_applied").size()

# weekly trend line chart
fig2, ax2 = plt.subplots()
apps_per_week.plot(kind="line", marker="o", ax=ax2)

ax2.set_ylabel("Applications")
ax2.set_xlabel("Week")

# chart display
st.pyplot(fig2)


# -------- Status Update Section --------
st.subheader("Update Application Status")

# saare application IDs list me le rahe hain
app_ids = df["id"].tolist()

# user dropdown se application select karega
selected_id = st.selectbox("Select Application ID", app_ids)

# new status select karne ka dropdown
new_status = st.selectbox(
    "New Status",
    ["Applied", "OA", "Interview", "Offer", "Rejected"]
)

# button click hone par database update hoga
if st.button("Update Status"):
    update_status(selected_id, new_status)
    st.success("Status Updated")
# -------- Delete Application Section --------
st.subheader("Delete Application")

# user dropdown se application choose karega
delete_id = st.selectbox("Select Application ID to Delete", app_ids)

# delete button
if st.button("Delete Application"):
    delete_application(delete_id)
    st.success("Application deleted successfully")

    # dashboard refresh karne ke liye rerun
    st.rerun()