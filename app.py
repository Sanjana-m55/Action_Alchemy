import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from pymongo import MongoClient
import pandas as pd
import winsound
import time
from datetime import datetime
import numpy as np

# App Modes Definition
APP_MODES = {
    "Command Center": "Main dashboard and overview of features🪶",
    "Architect Goal": "Create new tasks and goals🪛",
    "Explore Horizons": "View all existing tasks⚒️👩🏻‍🏭",
    "Calibrate Mission": "Edit existing tasks🤺",
    "Conquer Milestone": "Mark tasks as completed🤺",
    "Dissolve Mission": "Delete existing tasks🗑️",
    "Map Constellation": "Visualize task analytics📊",
    "Leaderboard": "View user rankings🏆"
}

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["habitthreads"]

# Streamlit App Setup
st.title("ActionAlchemy - Your productivity, our magical formula 🔮🪄")

# Session Management
if "user" not in st.session_state:
    st.session_state["user"] = None

def create_task_analytics_dashboard(tasks):
    """Create an analytics dashboard with various visualizations"""
    st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    # Calculate metrics
    completed = len([task for task in tasks if task["status"] == "completed"])
    pending = len([task for task in tasks if task["status"] == "pending"])
    
    # Metrics Display
    cols = st.columns(3)
    metrics = [
        ("🎯 Completed Tasks", completed),
        ("⏳ Pending Tasks", pending),
        ("✨ Completion Rate", f"{(completed/(completed+pending)*100 if completed+pending>0 else 0):.1f}%")
    ]
    
    for col, (label, value) in zip(cols, metrics):
        with col:
            st.markdown(f'<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f"### {label}")
            st.markdown(f'<p class="big-font">{value}</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # 3D Donut Chart
    fig_donut = go.Figure(data=[go.Pie(
        labels=['Completed', 'Pending'],
        values=[completed, pending],
        hole=.6,
        marker_colors=['#00CC96', '#EF553B']
    )])
    
    fig_donut.update_layout(
        title="Task Distribution",
        showlegend=True,
        width=400,
        height=400,
        scene=dict(camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)))
    )

    # Progress Monitor (ECG-like)
    def generate_ecg_data(num_points=100):
        t = np.linspace(0, 4*np.pi, num_points)
        baseline = np.sin(t) * 0.2
        peaks = np.zeros(num_points)
        peak_positions = np.random.randint(0, num_points-3, 5)
        for pos in peak_positions:
            peaks[pos:pos+3] = np.array([0.8, 1, 0.8])
        return t, baseline + peaks

    t, y = generate_ecg_data()
    fig_progress = go.Figure()
    fig_progress.add_trace(go.Scatter(
        x=t, y=y,
        mode='lines',
        line=dict(color='#1f77b4', width=2),
        name='Progress'
    ))
    
    fig_progress.update_layout(
        title='Real-time Progress Monitor',
        xaxis_title='Time',
        yaxis_title='Activity',
        showlegend=False,
        width=800,
        height=300
    )

    # Task Completion Trend
    dates = pd.date_range(end=datetime.now(), periods=10).tolist()
    completion_trend = [np.random.randint(5, 15) for _ in range(10)]
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(
        x=dates,
        y=completion_trend,
        marker_color='#17BECF',
        name='Completed Tasks'
    ))
    
    fig_trend.update_layout(
        title='Task Completion Trend',
        xaxis_title='Date',
        yaxis_title='Number of Tasks',
        width=800,
        height=400
    )

    # Display visualizations
    st.plotly_chart(fig_donut)
    st.plotly_chart(fig_progress)
    st.plotly_chart(fig_trend)

    if st.button('Refresh Dashboard'):
        st.rerun()

def main():
    """Main application logic"""
    # Login/Signup Interface
    if st.session_state["user"] is None:
        st.markdown("<h2 style='text-align: center;'>Welcome to ActionAlchemy</h2>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center;'>Please login or signup to continue 🚀</h4>", unsafe_allow_html=True)

        login_tab, signup_tab = st.tabs(["Login", "Signup"])
        
        with login_tab:
            st.subheader("Login to your account")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login"):
                user = db.users.find_one({"email": email, "password": password})
                if user:
                    st.success(f"Welcome back, {user['name']}! 🎉")
                    st.session_state["user"] = user
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        with signup_tab:
            st.subheader("Create a new account")
            name = st.text_input("Name", key="signup_name")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")

            if st.button("Signup"):
                if db.users.find_one({"email": email}):
                    st.error("Email already registered")
                else:
                    db.users.insert_one({"name": name, "email": email, "password": password})
                    st.success("Account created successfully!")

    else:
        # Sidebar Navigation
        st.sidebar.header(f"Welcome, {st.session_state['user']['name']}! 🎀🎗️")
        if st.sidebar.button("Logout"):
            st.session_state["user"] = None
            st.rerun()

        app_mode = st.sidebar.selectbox("Choose an action", list(APP_MODES.keys()))

        # Mode handlers
        if app_mode == "Command Center":
            st.write("Welcome to ActionAlchemy🚀")
            st.write("Track habits, visualize goals, and maintain progress📊📶")
            
            st.markdown("### Explore Our Features 🪄")
            for mode, desc in APP_MODES.items():
                if mode != "Command Center":
                    st.markdown(f"""
                    <div style='border:2px solid #6c63ff; border-radius:10px; padding:15px; margin:10px;
                        background-color:#222831; color:#eeeeee; text-align:center;'>
                        <h4>{mode}</h4>
                        <p>{desc}</p>
                    </div>
                    """, unsafe_allow_html=True)

        elif app_mode == "Architect Goal":
            st.subheader("Create New Task 🤹🏻‍♂️")
            task_id = st.text_input("Task ID (unique)")
            task_name = st.text_input("Task Name")
            task_description = st.text_area("Description")
            task_deadline = st.date_input("Deadline")
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            linked_goal = st.text_input("Linked Goal (Optional)")

            if st.button("Create Task"):
                if all([task_id, task_name, task_description]):
                    if not db.tasks.find_one({"task_id": task_id, "user_email": st.session_state["user"]["email"]}):
                        task = {
                            "task_id": task_id,
                            "name": task_name,
                            "description": task_description,
                            "deadline": str(task_deadline),
                            "priority": priority,
                            "linked_goal": linked_goal,
                            "status": "pending",
                            "streak": 0,
                            "created_at": str(datetime.now()),
                            "user_email": st.session_state["user"]["email"]
                        }
                        db.tasks.insert_one(task)
                        st.success(f"Task '{task_name}' created! 🎉")
                    else:
                        st.error("Task ID already exists")
                else:
                    st.error("Please fill all required fields")

        elif app_mode == "Explore Horizons":
            st.subheader("View All Tasks 🔭")
            tasks = list(db.tasks.find({"user_email": st.session_state["user"]["email"]}, {"_id": 0}))
            if tasks:
                st.write(pd.DataFrame(tasks))
            else:
                st.info("No tasks found")

        elif app_mode == "Calibrate Mission":
            st.subheader("Edit Task ✍🏻")
            task_id = st.text_input("Enter Task ID")
            task = db.tasks.find_one({"task_id": task_id, "user_email": st.session_state["user"]["email"]})
            
            if task:
                task_name = st.text_input("Task Name", task["name"])
                task_description = st.text_area("Description", task["description"])
                task_deadline = st.date_input("Deadline", datetime.strptime(task["deadline"], "%Y-%m-%d"))
                priority = st.selectbox("Priority", ["Low", "Medium", "High"], 
                                     index=["Low", "Medium", "High"].index(task["priority"]))
                linked_goal = st.text_input("Linked Goal", task["linked_goal"])

                if st.button("Save Changes"):
                    db.tasks.update_one(
                        {"task_id": task_id},
                        {"$set": {
                            "name": task_name,
                            "description": task_description,
                            "deadline": str(task_deadline),
                            "priority": priority,
                            "linked_goal": linked_goal
                        }}
                    )
                    st.success("Task updated! 🎉")
            else:
                st.error("Task not found")

        elif app_mode == "Conquer Milestone":
            st.subheader("Complete Task ✅")
            task_id = st.text_input("Enter Task ID")
            task = db.tasks.find_one({"task_id": task_id, "user_email": st.session_state["user"]["email"]})
            
            if task:
                if task["status"] == "pending":
                    deadline = datetime.strptime(task["deadline"], "%Y-%m-%d")
                    if deadline >= datetime.now():
                        if st.button("Mark as Completed"):
                            db.tasks.update_one(
                                {"task_id": task_id},
                                {"$set": {"status": "completed", "streak": task["streak"] + 1}}
                            )
                            winsound.Beep(1000, 1000)
                            st.balloons()
                            st.success(f"Task '{task['name']}' completed! 🎉")
                    else:
                        st.warning("Task deadline has passed")
                else:
                    st.info("Task already completed")
            else:
                st.error("Task not found")

        elif app_mode == "Dissolve Mission":
            st.subheader("Delete Task 🚮")
            task_id = st.text_input("Enter Task ID")
            task = db.tasks.find_one({"task_id": task_id, "user_email": st.session_state["user"]["email"]})
            
            if task:
                if st.button("Delete Task"):
                    db.tasks.delete_one({"task_id": task_id})
                    st.success(f"Task '{task['name']}' deleted")
            else:
                st.error("Task not found")

        elif app_mode == "Map Constellation":
            st.subheader("Task Analytics 🔍")
            tasks = list(db.tasks.find({"user_email": st.session_state["user"]["email"]}, {"_id": 0}))
            if tasks:
                create_task_analytics_dashboard(tasks)
            else:
                st.info("No tasks available for visualization")

        elif app_mode == "Leaderboard":
            st.subheader("Leaderboard 🏆")
            leaderboard_data = []
            for user in db.users.find():
                completed_tasks = list(db.tasks.find({"user_email": user["email"], "status": "completed"}))
                total_streak = sum(task["streak"] for task in completed_tasks)
                leaderboard_data.append({"name": user["name"], "streak": total_streak})
            
            if leaderboard_data:
                st.write(pd.DataFrame(leaderboard_data).sort_values("streak", ascending=False))
            else:
                st.info("No data available for leaderboard")

if __name__ == "__main__":
    main()