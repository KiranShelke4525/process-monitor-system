# process-monitor-system


## Project Structure

process-monitor/
├── agent/ # Example agent scripts to send data
├── backend/ # Django backend project
│ ├── backend_app/ # Django app
│ │ ├── templates/
│ │ │ └── backend_app/index.html
│ │ ├── models.py
│ │ ├── views.py
│ │ └── urls.py
│ ├── backend/
│ │ └── settings.py
│ └── manage.py
├── requirements.txt
└── README.md


---


## Setup and Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/KiranShelke4525/process-monitor-system.git
cd process-monitor
2. Create a virtual environment

python -m venv venv
3. Activate the virtual environment
Windows


venv\Scripts\activate
Linux/macOS

source venv/bin/activate
4. Install dependencies

pip install -r requirements.txt
Backend Setup
5. Run migrations

python backend/manage.py makemigrations
python backend/manage.py migrate
6. Create superuser (optional, for admin access)

python backend/manage.py createsuperuser
7. Run the backend server

python backend/manage.py runserver
Open http://127.0.0.1:8000/ in your browser.

System dashboard is available at http://127.0.0.1:8000/api/monitor

Agent Setup
Open the agent script in agent/ folder.

Update the backend URL and API key:


API_URL = "http://127.0.0.1:8000/api/agent/ingest/"
API_KEY = "your_api_key_here"
Run the agent:
# DATABASE SETTING 
set your db setting 

python agent/agent.py
The agent sends system info and running processes to the backend.

API Endpoints
Endpoint	Method	Description
/api/agent/ingest/	POST	Send system + process data
/api/agent/latest/	GET	Get latest system info
/api/agent/system/<id>/	GET	Get processes for a specific system

Notes
Make sure your API key exists in the ApiKey table in the database.

Dashboard auto-refreshes every 1 minute for system info.

Processes refresh manually via the "Refresh Processes" button.

Add .gitignore for venv/ and other unnecessary files.

If using Windows, Git CRLF warnings are normal and can be ignored.
