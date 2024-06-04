README
## Automated Commercial Real Estate Rental Management System

### Project Overview
This project is an Automated Information System (AIS) designed to manage the rental of commercial real estate. The system is built to streamline and automate the processes associated with renting commercial spaces, including tenant registration, lease management, payment tracking, and reporting.

### Features
- **Tenant Management**: Add, update, and delete tenant information.
- **Lease Management**: Create, update, and manage lease agreements.
- **Payment Tracking**: Record and track rental payments and other related expenses.
- **Reporting**: Generate various financial reports, including payment summaries and occupancy status.
- **Security**: Ensure data security with user authentication and access control.
- **Real-Time Access**: Access the system and its data from any device with an internet connection.

### Technologies Used
- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: PostgreSQL
- **Others**: Chart.js for data visualization

### Installation and Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/RentSoft.git
   cd RentSoft
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database:**
   - Ensure PostgreSQL is installed and running.
   - Create a database and a user with the necessary permissions.
   - Update the `DATABASES` configuration in `settings.py` with your database details.

5. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

### Usage
- **Accessing the Application:**
  Open a web browser and navigate to `http://127.0.0.1:8000`.

- **Logging In:**
  Use the superuser credentials created during setup to log in.

- **Managing Data:**
  - Add and manage tenants, properties, leases, and payments through the admin interface.
  - Use the navigation menu to access different sections of the system.



---

This project was created as a part of a course at Kazan National Research Technical University named after A.N. Tupolev (KAI) by students Danilaeva S.D. and Trifonov S.A., supervised by Senior Lecturer A. Yu. Alexandrov.

### Acknowledgments
- Thanks to the course "Design and Architecture of Software Systems" for providing the foundation for this project.
