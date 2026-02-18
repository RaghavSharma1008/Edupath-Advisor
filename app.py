import streamlit as st
import pandas as pd
import os

# ----------------------
# Users CSV setup
# ----------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
USER_CSV = os.path.join(DATA_DIR, "users.csv")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# create users.csv if it doesn't exist
if not os.path.exists(USER_CSV):
    df_users = pd.DataFrame(columns=["username", "password"])
    df_users.to_csv(USER_CSV, index=False)

# ----------------------
# Session state defaults
# ----------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "page" not in st.session_state:
    st.session_state.page = "login"

# ----------------------
# Login / Signup functions
# ----------------------
def signup(username, password):
    df_users = pd.read_csv(USER_CSV)
    df_users["username"] = df_users["username"].str.strip()
    df_users["password"] = df_users["password"].astype(str).str.strip()

    if username.strip() in df_users["username"].values:
        st.warning("Username already exists! Try a different one.")
    else:
        df_users = pd.concat(
            [df_users, pd.DataFrame([[username.strip(), password.strip()]], columns=["username", "password"])],
            ignore_index=True)
        df_users.to_csv(USER_CSV, index=False)
        st.success("Signup successful! You can now log in.")


def login(username, password):
    df_users = pd.read_csv(USER_CSV)
    df_users["username"] = df_users["username"].str.strip()
    df_users["password"] = df_users["password"].astype(str).str.strip()

    if username.strip() in df_users["username"].values:
        user_pass = df_users[df_users["username"] == username.strip()]["password"].values[0]
        if password.strip() == user_pass:
            st.session_state.logged_in = True
            st.session_state.username = username.strip()
            st.session_state.page = "home"  # redirect to main app
            st.success(f"Logged in as {username.strip()}")
        else:
            st.error("Incorrect password!")
    else:
        st.error("Username not found! Please signup first.")


career_roadmap = {
    "Science": {
        "Engineer": ["12th Science", "Entrance Exam (JEE/State Exam)", "B.Tech in Engineering", "Internships", "Job / Higher Studies"],
        "Doctor": ["12th Science (PCB)", "NEET Exam", "MBBS / BDS / BAMS", "Residency / Internship", "Job / Specialization"]
    },
    "Commerce": {
        "Accountant": ["12th Commerce", "B.Com / BBA", "Internship / CA Coaching", "Job / CA Final Exam", "Professional Career"],
        "Business Analyst": ["12th Commerce", "B.Com / BBA / Economics", "Internship / Projects", "MBA / Analytics Certification", "Job / Career Growth"]
    },
    "Arts": {
        "Journalist": ["12th Arts", "Bachelor in Journalism / Mass Communication", "Internships / College Projects", "Entry-Level Job", "Senior Journalist / Editor"],
        "Designer": ["12th Arts", "Bachelor in Design / Fine Arts", "Portfolio & Internship", "Freelance / Job", "Senior Designer / Creative Head"]
    }
}


if not st.session_state.logged_in:
    st.set_page_config(page_title="EduPath Advisor - Login", layout="centered")
    st.title("🎓 EduPath Advisor - Login")

    tab = st.radio("Choose an option", ["Login", "Sign Up"])

    if tab == "Login":
        st.subheader("Login to your account")
        user = st.text_input("Username", key="login_user")
        passwd = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            if user and passwd:
                login(user, passwd)
            else:
                st.warning("Please enter both username and password.")

    elif tab == "Sign Up":
        st.subheader("Create a new account")
        new_user = st.text_input("New Username", key="signup_user")
        new_pass = st.text_input("New Password", type="password", key="signup_pass")
        if st.button("Sign Up"):
            if new_user and new_pass:
                signup(new_user, new_pass)
            else:
                st.warning("Please enter both username and password.")

if st.session_state.logged_in and st.session_state.page == "home":
    st.set_page_config(page_title="EduPath Advisor", layout="centered")
    st.title("🎓 EduPath Advisor")
    st.markdown("Your One-Stop Personalized Career & Education Guide")


    page = st.sidebar.radio("Navigate", ["Home", "Career Quiz", "Career Roadmap", "College Finder", "Dashboard", "Future Scope"])


    df = pd.read_csv("data/colleges.csv")

    if page == "Home":
        st.image("assets/logo.png", caption="EduPath Advisor")
        st.write("""
        Many students struggle to choose the right career path after 10th or 12th.
        EduPath Advisor helps you:
        - Discover your ideal stream based on interests  
        - Explore nearby government colleges  
        - Track courses, scholarships, and facilities  
        - (Coming soon) Get AI-based personalized guidance  
        """)

    # QUIZ SECTION
    elif page == "Career Quiz":
        st.subheader("Career Interest Quiz 🧩")

        q1 = st.radio("1. Which activity do you enjoy the most?",
                      ["Solving science experiments", "Managing money or business ideas", "Drawing or writing"])
        q2 = st.radio("2. Which subject interests you the most?",
                      ["Physics/Biology", "Economics/Accounts", "History/Literature"])
        q3 = st.radio("3. What kind of career excites you?",
                      ["Engineer/Doctor", "Entrepreneur/Analyst", "Journalist/Designer"])
        q4 = st.radio("4. How do you solve problems?",
                      ["Logical", "Numerical", "Creative"])

        if st.button("Submit"):
            answers = [q1, q2, q3, q4]
            science = sum("science" in a.lower() or "engineer" in a.lower() or "physics" in a.lower() for a in answers)
            commerce = sum("money" in a.lower() or "economics" in a.lower() or "business" in a.lower() for a in answers)
            arts = sum("drawing" in a.lower() or "creative" in a.lower() or "literature" in a.lower() for a in answers)

            result = max(("Science", science), ("Commerce", commerce), ("Arts", arts), key=lambda x: x[1])[0]

            st.success(f"You're best suited for the **{result}** stream!")
            st.session_state["stream"] = result

    elif page == "Career Roadmap":
        st.subheader("🛤️ Career Roadmap")
        # Use stream from quiz if available, else let user choose
        stream_choice = st.session_state.get("stream", None)
        if not stream_choice:
            stream_choice = st.selectbox("Choose your stream:", ["Science", "Commerce", "Arts"])
        else:
            st.info(f"Detected Stream from Quiz: **{stream_choice}**")

        # Show possible jobs
        st.write(f"### Popular Jobs for {stream_choice} stream:")
        jobs = list(career_roadmap[stream_choice].keys())
        selected_job = st.selectbox("Choose a job to see its roadmap:", jobs)

        # Show roadmap
        st.write(f"#### Roadmap to become a {selected_job}:")
        roadmap = career_roadmap[stream_choice][selected_job]
        for i, step in enumerate(roadmap, 1):
            st.write(f"{i}. {step}")


    elif page == "College Finder":
        st.subheader("🏫 Find Government Colleges")

        stream_choice = st.selectbox("Choose Stream", ["Science", "Commerce", "Arts"])
        city_choice = st.selectbox("Choose City", ["Gurdaspur", "Ferozepur", "Ludhiana", "Amritsar", "Pathankot"])

        filtered = df[(df["City"] == city_choice) & (df["Stream"] == stream_choice)]

        if st.button("Show Colleges"):
            if len(filtered) == 0:
                st.warning("No colleges found for this selection.")
            else:
                st.write(f"### Colleges offering {stream_choice} in {city_choice}:")
                st.table(filtered[["Name", "Facilities"]])


    elif page == "Dashboard":
        st.subheader("📊 Insights Dashboard")
        st.write("### Stream Distribution in Colleges")
        st.bar_chart(df["Stream"].value_counts())
        st.write("### Colleges per City")
        st.bar_chart(df["City"].value_counts())


    elif page == "Future Scope":
        st.subheader("🚀 Future Scope of EduPath Advisor")
        st.markdown("""
        In future versions, we plan to integrate:
        - **AI Chatbot** for instant student counseling  
        - **ML Model** for personalized course predictions  
        - **Real-time scholarship updates**  
        - **Integration with government APIs** for live admission tracking  
        """)
        st.info("Developed by Raghav")
