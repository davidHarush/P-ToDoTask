
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
- Sqlalchemy

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


## Setup Instructions

### Prerequisites

- Python 3.x
- pip (Python package installer)

### Clone the repository:

```bash
git clone https://github.com/your-username/task-management-app.git
```

### Setting up the Python environment

Create a virtual environment:
```bash
python3 -m venv venv
```

Activate the virtual environment:
```bash
source venv/bin/activate
```

### Installing the required packages

Install the required packages:
```bash
pip install -r requirements.txt
```

### Running the application

Run the Flask server:
```bash
python app.py
```

Run the Streamlit application:
```bash
streamlit run dashboard.py
```



![Task Management App](media/Screenshot%202024-06-27%20at%2021.59.18.png)

