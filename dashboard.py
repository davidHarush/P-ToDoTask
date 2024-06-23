import streamlit as st
import requests
import pandas as pd
from datetime import date

API_URL = "http://127.0.0.1:5000/tasks"

def fetch_tasks():
    """
    Fetches the list of tasks from the Flask API.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching tasks: {e}")
        return []

def add_task(task):
    """
    Adds a new task by sending a POST request to the Flask API.
    """
    try:
        response = requests.post(API_URL, json=task)
        response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"Error adding task: {e}")

def update_task(task_id, task):
    """
    Updates an existing task by sending a PUT request to the Flask API.
    """
    try:
        response = requests.put(f"{API_URL}/{task_id}", json=task)
        response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"Error updating task: {e}")

def delete_task(task_id):
    """
    Deletes an existing task by sending a DELETE request to the Flask API.
    """
    try:
        response = requests.delete(f"{API_URL}/{task_id}")
        response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"Error deleting task: {e}")

# Set page configuration
st.set_page_config(page_title="Task Management Dashboard", layout="wide")

# Add custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f0f5;
        padding: 20px;
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: white;
    }
    [data-testid=stSidebar] {
        background-color: #d1e7dd;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
    }
    .stTable {
        background-color: #ffffff;
    }
    .css-pxxe24 {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Task Management Dashboard")

# Fetch tasks
tasks = fetch_tasks()

# Sidebar for adding a new task
st.sidebar.header("Add New Task")

with st.sidebar.form("add_task_form"):
    task_title = st.text_input(label="Task Title", placeholder='')
    task_due_date = st.date_input("Due Date", value=date.today())
    add_task_button = st.form_submit_button(label="Add Task")

if add_task_button and task_title:
    add_task({"title": task_title, "completed": False, "description": "", "due_date": task_due_date.isoformat()})
    st.sidebar.success("Task added successfully!")
    st.experimental_rerun()

# Sidebar for editing a task
if 'selected_task' in st.session_state:
    st.sidebar.header("Edit Task")

    selected_task_id = st.session_state.selected_task_id
    selected_task = st.session_state.selected_task

    with st.sidebar.form("edit_task_form"):
        new_title = st.text_input("New Task Title", value=selected_task["title"], placeholder="")
        new_description = st.text_area("Description", value=selected_task.get("description", ""))
        new_due_date = st.date_input("Due Date", value=pd.to_datetime(selected_task.get("due_date", date.today().isoformat())))
        completed = st.checkbox("Completed", value=selected_task.get("completed"))
        update_task_button = st.form_submit_button(label="Update Task")

    if update_task_button:
        update_task(selected_task_id, {"title": new_title, "description": new_description, "completed": completed, "due_date": new_due_date.isoformat()})
        st.sidebar.success("Task updated successfully!")
        del st.session_state.selected_task  # Clear the selection after updating
        del st.session_state.selected_task_id
        st.experimental_rerun()

    with st.sidebar.form("delete_task_form"):
        delete_task_button = st.form_submit_button(label="Delete Task")

    if delete_task_button:
        delete_task(selected_task_id)
        st.sidebar.success("Task deleted successfully!")
        del st.session_state.selected_task  # Clear the selection after deleting
        del st.session_state.selected_task_id
        st.experimental_rerun()

else:
    # Sidebar for statistics
    st.sidebar.header("Statistics")
    st.sidebar.write(f"Total Tasks: {len(tasks)}")
    st.sidebar.write(f"Completed Tasks: {len([task for task in tasks if task.get('completed')])}")
    st.sidebar.write(f"Uncompleted Tasks: {len([task for task in tasks if not task.get('completed')])}")

    # Late Tasks
    late_tasks = [task for task in tasks if not task.get("completed") and pd.to_datetime(task.get("due_date")) < pd.Timestamp(date.today())]
    if late_tasks and len(late_tasks) > 0:
        st.sidebar.markdown(f"<span style='color:red;'>Late Tasks: {len(late_tasks)}</span>", unsafe_allow_html=True)

# Main area for displaying tasks
st.markdown("<hr>", unsafe_allow_html=True)

task_df = pd.DataFrame(tasks)
if not task_df.empty:
    task_df.index += 1
    task_df["Completed"] = task_df["completed"].apply(lambda x: "Completed" if x else "Uncompleted")

    # Adding Edit button to each row
    for i, row in task_df.iterrows():
        col1, col2, col3, col4, col5 = st.columns([2, 5, 2, 2, 2])  # Adjust the width ratio as needed
        with col1:
            st.write(row["title"])
        with col2:
            st.write(row.get("description", "No description provided"))
        with col3:
            st.write(row["Completed"])
        with col4:
            due_date = pd.to_datetime(row.get("due_date"))
            if due_date < pd.Timestamp(date.today()):
                st.markdown(f"<span style='color:red;'>{due_date.date()}</span>", unsafe_allow_html=True)
            else:
                st.write(due_date.date())
        with col5:
            if st.button("Edit", key=f"edit_{row['id']}"):
                st.session_state.selected_task_id = row['id']  # Use the task ID
                st.session_state.selected_task = row.to_dict()  # Use the row as a dictionary
                st.experimental_rerun()  # Rerun to reflect the changes

        # Add a horizontal line after each task
        st.markdown("<hr>", unsafe_allow_html=True)

else:
    st.write("No tasks available.")
