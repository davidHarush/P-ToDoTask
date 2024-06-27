# Task Management Application

This project is a task management application built with Flask for the backend and Streamlit for the frontend. The application allows users to manage their tasks with features like adding, updating, and deleting tasks. User authentication is handled via email-based registration.

## Features

- User authentication using email
- Add new tasks
- View all tasks
- Update tasks
- Delete tasks
- View task statistics (total tasks, completed tasks, uncompleted tasks, late tasks)

## Technologies Used

- Flask
- Streamlit
- Pandas
- Requests

## Architecture

The project is divided into two main parts:

1. **Backend (Server)**: 
   - Built with Flask.
   - Handles user authentication and task management.
   - Exposes RESTful APIs for the frontend to interact with.

2. **Frontend (Client)**: 
   - Built with Streamlit.
   - Provides a user-friendly interface for managing tasks.
   - Interacts with the backend through HTTP requests.

This is my first Python project, and it was a great learning experience to build a full-stack application from scratch.

## Setup Instructions

### Prerequisites

- Python 3.x
- pip (Python package installer)



Clone the repository:

```bash
git clone https://github.com/your-username/task-management-app.git
cd task-management-app
```



Run the Flask server and the Streamlit app:
```bash
python app.py
streamlit run dashboard.py
```

