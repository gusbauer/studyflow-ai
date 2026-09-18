# StudyFlow AI

#### Video Demo: https://www.youtube.com/watch?v=fCKaODqcTMA

## Description

StudyFlow AI is a web application designed to help students organize their academic tasks and manage their study time more effectively. I developed this project as my final project for CS50x 2026.

The application combines task management, user authentication, statistics, calendar organization, and an AI-assisted study planning feature in a single web application.

Users can register for an account and log in to access their own private workspace. Each user can create tasks containing information such as a title, subject, description, priority, due date, and estimated completion time. Tasks can later be viewed, edited, marked as completed, or deleted.

The main objective of StudyFlow AI is to provide students with more than a simple to-do list. The application uses deadlines, priorities, estimated study times, statistics, and calendar visualization to give users a clearer overview of their academic workload.

An additional feature of the project is the integration with the OpenAI API. The application can send information about a user's pending tasks to an AI service in order to generate a personalized study plan when API access and credits are available.

## Features

### User Authentication

StudyFlow AI includes a complete authentication system. Users can register, log in, and log out of the application. Passwords are stored securely using password hashing instead of storing the original passwords.

Flask-Login is used to manage user sessions and protect pages that should only be accessible to authenticated users.

### Task Management

Users can create and manage academic tasks. Each task can contain:

- Title
- Subject
- Description
- Priority
- Due date
- Estimated study time
- Completion status

The application supports the main CRUD operations: creating, reading, updating, and deleting tasks.

Tasks can also be marked as completed without deleting them, allowing the application to calculate statistics about the user's progress.

### Priority and Urgency

Tasks are not treated equally. StudyFlow AI considers their priority and due date to determine how urgent they are.

The application distinguishes between tasks that are overdue, due today, approaching their deadline, or scheduled further into the future. This helps students identify the work that requires their attention first.

### Dashboard

The dashboard gives the user a quick overview of their academic workload.

It displays information such as the number of tasks, completed tasks, pending tasks, and high-priority tasks. Statistics and graphical elements make it easier to understand progress without having to inspect every task individually.

### Calendar

StudyFlow AI includes a calendar view that organizes tasks according to their deadlines.

This provides a different way to visualize academic work. Instead of only viewing tasks as a list, users can see when assignments and study activities are due and understand how their workload is distributed over time.

### AI Study Plan

The application contains an AI-assisted study planning feature using the OpenAI API.

Pending tasks can be analyzed according to information including their subject, priority, deadline, and estimated completion time. This information is used to request a personalized study plan from the AI service.

The OpenAI integration is separated from the routes through `ai_service.py`. This design keeps the external API logic independent from the HTTP request handling.

An OpenAI API key is never stored directly in the source code. It is loaded from an environment variable. Generating a plan requires a valid OpenAI API key with available API credits.

## Technologies

The backend of StudyFlow AI was developed using Python and Flask.

The main technologies used in the project are:

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- SQLite
- HTML5
- CSS3
- JavaScript
- Bootstrap
- Chart.js
- FullCalendar
- Jinja2
- OpenAI API
- python-dotenv
- Git and GitHub

SQLite was selected because it provides a simple relational database that works well for a project of this size without requiring a separate database server.

SQLAlchemy provides an abstraction layer between the Python application and the database.

## Project Structure

The project is divided into different files and directories to keep responsibilities separated.

### `app.py`

This is the main entry point of the application. It creates and configures the Flask application, initializes the extensions, registers the different blueprints, configures Flask-Login, and defines error handlers.

### `config.py`

This file contains the application's configuration. It loads environment variables and defines settings such as the secret key, database location, and OpenAI configuration.

### `extensions.py`

This file initializes extensions that are shared by different parts of the application, including SQLAlchemy, Flask-Login, and CSRF protection.

Keeping these extensions in a separate file helps avoid circular imports.

### `models.py`

This file defines the database models.

The `User` model represents registered users, while the `Task` model represents academic tasks. Tasks belong to individual users.

The Task model also contains methods used to calculate information such as priority labels, overdue status, days remaining until a deadline, and urgency.

### `forms.py`

This file contains the forms used by the application and their validation rules.

### `routes/`

The `routes` directory separates the application's endpoints into Flask blueprints.

`auth.py` manages registration, login, and logout.

`tasks.py` manages task creation, editing, deletion, completion, task details, and calendar-related functionality.

`dashboard.py` manages the dashboard and the information displayed in its statistics.

`ai.py` manages the pages and requests associated with AI study-plan generation.

### `services/`

The services directory contains business logic that does not need to be directly inside the route files.

`ai_service.py` communicates with the OpenAI API and creates the prompt used to generate a study plan.

`statistics_service.py` contains logic used to calculate information for the dashboard.

`task_service.py` contains task-related business logic.

Separating this logic from the routes makes the application easier to understand and maintain.

### `templates/`

This directory contains the Jinja2 HTML templates used to generate the application's pages.

It includes templates for authentication, the dashboard, task management, the calendar, the AI study plan, and error pages.

### `static/`

This directory contains the application's static resources, including CSS and JavaScript.

The CSS defines the visual design of StudyFlow AI, while JavaScript is used for interactive behavior in the interface.

### `instance/studyflow.db`

During local development, SQLite stores the application's data in this database file.

The local database itself is excluded from version control so that personal development data is not uploaded to the repository.

### `create_db.py`

This script can be used to create the database and required tables for the application.

### `requirements.txt`

This file lists the Python dependencies required to run StudyFlow AI.

### `.env.example`

This file documents the environment variables expected by the application without containing real passwords, secret keys, or API credentials.

## Design Decisions

One of the main design decisions was to divide the application into Flask blueprints instead of placing every route inside `app.py`.

As the project grew, authentication, task management, dashboard statistics, calendar functionality, and AI functionality became separate areas of responsibility. Blueprints make this structure clearer and make future changes easier.

I also decided to separate some business logic into services. For example, communication with OpenAI is handled by `ai_service.py` instead of directly inside the AI route. This reduces the responsibilities of the route and makes the project more modular.

SQLite was chosen as the database because the application does not require a separate database server. It is lightweight and appropriate for a personal task-management application while still allowing me to use relational database concepts learned during CS50.

For security, passwords are hashed rather than stored as plain text. Forms use CSRF protection, authenticated routes are protected, and sensitive values such as the Flask secret key and OpenAI API key are loaded from environment variables.

I also chose to provide both a task list and a calendar. A list is useful for managing individual tasks, while the calendar provides a better overview of deadlines over time.

Finally, the AI functionality was implemented as an additional planning tool rather than replacing the normal task-management system. The core application continues to work without OpenAI API access. When API access is available, AI can use the existing task information to provide an additional personalized study plan.

## Installation

Clone the repository:

```bash
git clone https://github.com/gusbauer/StudyFlow-AI.git
cd StudyFlow-AI
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file based on `.env.example` and configure the required environment variables.

For example:

```env
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
```

A real API key should never be committed to the repository.

Create the database:

```bash
python create_db.py
```

Run the application:

```bash
python app.py
```

The Flask development server will then provide the local address where StudyFlow AI can be opened in a web browser.

## Security

StudyFlow AI implements several security measures.

User passwords are hashed before being stored in the database. Flask-Login is used to control authenticated sessions, and Flask-WTF provides CSRF protection for forms.

Secret configuration values are stored using environment variables. The `.env` file is excluded from Git, and `.env.example` contains only placeholders.

The local SQLite database and virtual environment are also excluded from version control.

## AI Assistance

AI tools, including ChatGPT, were used during the development of this project as a programming assistant to help explain concepts, debug errors, and suggest possible implementation approaches.

The generated suggestions were reviewed, adapted, integrated, and tested as part of the development process.

## Future Improvements

There are several features that could be added in future versions of StudyFlow AI.

Possible improvements include notifications before deadlines, more advanced study statistics, recurring tasks, additional calendar functionality, improved AI-generated schedules, and deployment to a public web server.

The current version focuses on providing a complete foundation that combines authentication, persistent task management, dashboard statistics, deadline visualization, and AI-assisted study planning.
