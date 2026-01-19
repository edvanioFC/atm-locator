# Project Report: ATM Locator Application

## 1. Overview

This project is an ATM Locator application designed to help users find nearby ATMs. It provides functionalities for user management, ATM information management, and location-based services.

**Core Functionalities:**
*   **User Authentication and Authorization:** Secure user registration, login, logout, and password management. Includes administrative functionalities.
*   **ATM Management:** Creation, retrieval, update, and deletion (CRUD) of ATM information.
*   **Location Services:** Ability to locate ATMs, potentially using geolocation features (requires HTTPS).
*   **Email Notifications:** Password reset and other transactional emails.

## 2. Technology Stack

The application is built using the following key technologies:

*   **Backend Framework:** Flask (Python) - A lightweight web framework for building the application's core logic and APIs.
*   **Database:** PostgreSQL - A powerful, open-source relational database system.
*   **Object-Relational Mapper (ORM):** Flask-SQLAlchemy - An extension for Flask that adds SQLAlchemy support, simplifying database interactions.
*   **Database Migrations:** Alembic with Flask-Migrate - Used for managing and applying database schema changes.
*   **Authentication:** Flask-Login - Provides user session management, making it easy to handle user logins, logouts, and session protection.
*   **Email Services:** Flask-Mail - An extension for sending emails, utilized for features like password recovery.
*   **Data Validation:** Pydantic - Used for data parsing and validation, ensuring data integrity for incoming requests and database operations.
*   **Environment Management:** python-dotenv - Loads environment variables from a `.env` file, facilitating configuration management across different environments.
*   **Frontend Technologies:**
    *   HTML (Jinja2 Templates)
    *   CSS
    *   JavaScript (for dynamic client-side interactions, including map functionalities).

## 3. Project Structure

The project follows a modular structure, organizing code logically into distinct directories:

*   **`/` (Root Directory):**
    *   `config.py`: Centralized configuration settings for development and production environments.
    *   `run.py`: Application entry point, responsible for initializing the Flask app, applying database migrations, and creating default administrative users.
    *   `requirements.txt`: Lists all Python dependencies required by the project.
    *   `Dockerfile`: Defines the Docker image for containerizing the application.
    *   `entrypoint.sh`, `setup.sh`, `Makefile`, `README.md`, `LICENSE`, `.gitignore`: Other project setup and documentation files.
*   **`app/`:** The core application package.
    *   `__init__.py`: Initializes the Flask application and registers blueprints.
    *   `models/`: Contains SQLAlchemy models (`atm.py`, `user.py`) defining the database schema for ATMs and users.
    *   `routes/`: Houses the blueprint definitions for various API endpoints and web routes:
        *   `admin.py`: Routes for administrative tasks (e.g., managing ATMs, users).
        *   `auth.py`: Routes for user authentication (registration, login, logout, password reset).
        *   `main.py`: General application routes, likely including the main ATM search and display.
    *   `schemas/`: Pydantic schemas (`atm_schema.py`, `user_schema.py`) for validating data related to ATMs and users.
    *   `static/`: Stores static assets such as CSS stylesheets, JavaScript files (e.g., `map.js` for location features), and uploaded images (`uploads/`).
    *   `templates/`: Contains Jinja2 HTML templates for rendering web pages (e.g., `login.html`, `user_dashboard.html`, `admin_dashboard.html`).
    *   `utils/`: Utility functions and helper modules.
*   **`migrations/`:** Contains Alembic scripts for managing database schema evolution.

## 4. Key Modules and Features

### 4.1 User Management

*   **Authentication:** Utilizes Flask-Login for secure user sessions.
*   **Authorization:** Differentiates between regular users and administrative users.
*   **Registration & Login:** Users can create new accounts and log in securely.
*   **Password Reset:** Functionality to reset forgotten passwords via email (Flask-Mail).
*   **Pydantic Validation:** User input during registration and login is validated using Pydantic schemas.

### 4.2 ATM Management

*   **Database Models:** `atm.py` defines the structure for ATM data storage.
*   **CRUD Operations:** Routes within `admin.py` and potentially `main.py` handle creating, reading, updating, and deleting ATM records.
*   **Data Validation:** ATM data is validated using Pydantic schemas (`atm_schema.py`).
*   **Image Uploads:** The `app/static/uploads` directory and `MAX_CONTENT_LENGTH` configuration suggest support for uploading images related to ATMs.

### 4.3 Location Services (Geolocation)

*   **`map.js`:** A dedicated JavaScript file suggests client-side logic for displaying and interacting with maps.
*   **HTTPS Requirement:** The `run.py` script explicitly warns about geolocation features requiring HTTPS, indicating its importance for this functionality.

### 4.4 Email Functionality

*   **Flask-Mail:** Integrated for sending emails, primarily for features like password recovery.
*   **Configurable:** Email server settings are configurable via environment variables in `config.py`.

### 4.5 Configuration Management

*   **Environment Variables:** Sensitive information and environment-specific settings are managed through environment variables (`.env` file support).
*   **Development & Production Profiles:** Separate configuration classes (`DevelopmentConfig`, `ProductionConfig`) allow for easy switching between different application environments.

This report provides a high-level overview of the ATM Locator application, its underlying technologies, structure, and key features.
