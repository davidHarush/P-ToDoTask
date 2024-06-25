from datetime import date

import pandas as pd
import requests
import streamlit as st

API_URL = "http://127.0.0.1:5000"


def fetch_tasks(headers):
    try:
        response = requests.get(f"{API_URL}/tasks", headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching tasks: {e}")
        return []


def add_task(task, headers):
    try:
        response = requests.post(f"{API_URL}/tasks", json=task, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"Error adding task: {e}")


def update_task(task_id, task, headers):
    try:
        response = requests.put(f"{API_URL}/tasks/{task_id}", json=task, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"Error updating task: {e}")


def delete_task(task_id, headers):
    try:
        response = requests.delete(f"{API_URL}/tasks/{task_id}", headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        st.error(f"Error deleting task: {e}")


def authenticate_user(email):
    try:
        response = requests.post(f"{API_URL}/register", json={"email": email})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error authenticating user: {e}")
        return None


st.set_page_config(page_title="Task Management Dashboard", layout="wide")

st.sidebar.header("User Authentication")
with st.sidebar.form(key='login_form'):
    email = st.text_input("Enter your email", value="", placeholder="your-email@example.com")
    login_button = st.form_submit_button(label="Login")

if login_button:
    if email:
        user = authenticate_user(email)
        if user:
            st.session_state.user = user
            st.sidebar.success(f"Logged in as {email}")
    else:
        st.sidebar.error("Please enter your email")

if 'user' in st.session_state:
    st.title(f"Task Management Dashboard for {st.session_state.user['email']}")

    headers = {'X-User-Email': st.session_state.user['email']}
    tasks = fetch_tasks(headers=headers)

    if 'selected_task' not in st.session_state:
        st.sidebar.header("Add New Task")

        with st.sidebar.form("add_task_form"):
            task_title = st.text_input(label="Task Title", placeholder='')
            task_due_date = st.date_input("Due Date", value=date.today())
            add_task_button = st.form_submit_button(label="Add Task")

        if add_task_button and task_title:
            add_task(
                {"title": task_title, "completed": False, "description": "", "due_date": task_due_date.isoformat()},
                headers=headers)
            st.sidebar.success("Task added successfully!")
            st.experimental_rerun()

        # Sidebar for statistics
        st.sidebar.header("Statistics")
        st.sidebar.write(f"Total Tasks: {len(tasks)}")
        st.sidebar.write(f"Completed Tasks: {len([task for task in tasks if task.get('completed')])}")
        st.sidebar.write(f"Uncompleted Tasks: {len([task for task in tasks if not task.get('completed')])}")

        # Late Tasks
        late_tasks = [task for task in tasks if
                      not task.get("completed") and pd.to_datetime(task.get("due_date")) < pd.Timestamp(date.today())]
        if late_tasks and len(late_tasks) > 0:
            st.sidebar.markdown(f"<span style='color:red;'>Late Tasks: {len(late_tasks)}</span>",
                                unsafe_allow_html=True)

    task_df = pd.DataFrame(tasks)
    if not task_df.empty:
        task_df.index += 1
        task_df["Completed"] = task_df["completed"].apply(lambda x: "Completed" if x else "Uncompleted")

        for i, row in task_df.iterrows():
            col1, col2, col3, col4, col5 = st.columns([2, 5, 2, 2, 2])
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
                    st.session_state.selected_task_id = row['id']
                    st.session_state.selected_task = row.to_dict()
                    st.experimental_rerun()

            st.markdown("<hr>", unsafe_allow_html=True)
    else:
        st.write("No tasks available.")

    if 'selected_task' in st.session_state:
        st.sidebar.header("Edit Task")

        selected_task_id = st.session_state.selected_task_id
        selected_task = st.session_state.selected_task

        with st.sidebar.form("edit_task_form"):
            new_title = st.text_input("New Task Title", value=selected_task["title"], placeholder="")
            new_description = st.text_area("Description", value=selected_task.get("description", ""))
            new_due_date = st.date_input("Due Date",
                                         value=pd.to_datetime(selected_task.get("due_date", date.today().isoformat())))
            completed = st.checkbox("Completed", value=selected_task.get("completed"))
            update_task_button = st.form_submit_button(label="Update Task")

        if update_task_button:
            update_task(selected_task_id, {"title": new_title, "description": new_description, "completed": completed,
                                           "due_date": new_due_date.isoformat()}, headers=headers)
            st.sidebar.success("Task updated successfully!")
            del st.session_state.selected_task
            del st.session_state.selected_task_id
            st.experimental_rerun()

        with st.sidebar.form("delete_task_form"):
            delete_task_button = st.form_submit_button(label="Delete Task")

        if delete_task_button:
            delete_task(selected_task_id, headers=headers)
            st.sidebar.success("Task deleted successfully!")
            del st.session_state.selected_task
            del st.session_state.selected_task_id
            st.experimental_rerun()

else:
    st.write("Please log in to manage your tasks.")
