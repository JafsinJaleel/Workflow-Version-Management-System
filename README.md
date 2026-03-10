

# Workflow Version Management System

A **Workflow Version Management System** built using **Python (Flask), MySQL, HTML, CSS, and JavaScript** that allows users to create, manage, and track versions of workflows.
Each workflow consists of multiple **stages**, and every modification creates a **new version** while preserving the previous ones.

This system allows users to:

* Create workflows with multiple stages
* Update workflows while maintaining version history
* View workflow version history
* Compare two versions of a workflow
* Track workflow changes over time

---

# Project Features

* Create new workflows
* Add multiple workflow stages
* Automatic version generation when workflow is updated
* Version history tracking
* Compare workflow versions
* Delete workflows
* Simple dashboard interface

---

# Technology Stack

Backend:

* Python
* Flask

Database:

* MySQL

Frontend:

* HTML
* CSS
* JavaScript

Libraries Used:

* json
* difflib

---

# Setup Instructions

## 1 Install Python

Make sure **Python 3.8 or higher** is installed.

Check installation:

```bash
python --version
```

---

## 2 Clone the Repository

```bash
git clone https://github.com/JafsinJaleel/Workflow-Version-Management-System
cd workflow-versioning-system
```

---

## 3 Create Virtual Environment

```bash
python -m venv .venv
```

Activate virtual environment:

Windows

```bash
.venv\Scripts\activate
```

Mac/Linux

```bash
source .venv/bin/activate
```

---

## 4 Install Dependencies

```bash
pip install flask mysql-connector-python
```

---

## 5 Configure Database

Create a **MySQL database**.

Example:

```sql
CREATE DATABASE workflow_db;
```

---

### Create workflows table

```sql
CREATE TABLE workflows (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    current_version INT DEFAULT 1
);
```

---

### Create workflow_versions table

```sql
CREATE TABLE workflow_versions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    workflow_id INT,
    version_number INT,
    configuration JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 6 Configure Database Connection

Create file **db_config.py**

Example:

```python
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="workflow_db"
    )
```

---

## 7 Run the Application

```bash
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

# Versioning Approach

This project implements a **workflow versioning strategy** where every modification creates a new workflow version.

Key concepts:

### Workflow

Represents the main process with a name and description.

### Version

Every workflow modification creates a new version stored in the **workflow_versions** table.

### Configuration

Workflow stages are stored as **JSON configuration**.

Example:

```
{
 "stages": ["Draft", "Manager Review", "Archive"]
}
```

If stages are updated:

```
{
 "stages": ["Draft", "Manager Review", "Director Approval", "Archive"]
}
```

A new version is created.

### Version Tracking

The **current_version** field in the workflows table stores the latest version.

Version history is preserved for auditing and comparison.

---

# API Routes

## Dashboard

```
GET /
```

Displays all workflows in the system.

---

## Create Workflow Page

```
GET /create
```

Displays form to create a new workflow.

---

## Create Workflow

```
POST /create-workflow
```

Creates a new workflow and stores **version 1**.

Parameters:

* name
* description
* stages

---

## Edit Workflow

```
GET /edit/<id>
```

Displays edit page for selected workflow.

---

## Update Workflow

```
POST /update/<id>
```

Creates a **new workflow version** when stages are updated.

---

## Delete Workflow

```
GET /delete/<id>
```

Deletes workflow and all its versions.

---

## View Workflow History

```
GET /history/<workflow_id>
```

Displays all versions of a workflow with:

* Version Number
* Stages
* Creation Date

---

## Compare Workflow Versions

```
POST /compare/<workflow_id>
```

Compares two workflow versions and highlights differences.

Uses Python **difflib** to detect changes between stages.

Example result:

```
- Director Approval
+ Archive
```

---

# Database Schema

### Workflows

| Field           | Type    |
| --------------- | ------- |
| id              | INT     |
| name            | VARCHAR |
| description     | TEXT    |
| current_version | INT     |

---

### Workflow_Versions

| Field          | Type      |
| -------------- | --------- |
| id             | INT       |
| workflow_id    | INT       |
| version_number | INT       |
| configuration  | JSON      |
| created_at     | TIMESTAMP |

---

# Development Assumptions

The following assumptions were made during development:

1. Each workflow contains a sequence of **stages**.

2. Stages are stored in **JSON format** for flexibility.

3. Every update creates a **new version instead of modifying existing data**.

4. Users can compare any two versions of the same workflow.

5. Workflow deletion removes all related versions.

6. The system assumes **single-user usage** and does not include authentication.

7. The application runs on **local MySQL database**.

---

# Future Improvements

Possible Enhancements:

* User authentication
* Role-based workflow approvals
* Workflow rollback feature
* Visual workflow diagram
* REST API integration
* Deployment using Docker or Cloud


