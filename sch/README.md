Appointment Scheduler
=====================

The goal of this project is to create a simple RESTful HTTP API for scheduling
and retrieving appointments.

### Instructions

Clone this repository from GitHub and create a branch with your name in it.
You should do all of your work on this branch and push it to GitHub when
you are finished.

Create a simple webserver connected to a database, which exposes a RESTful
API serving JSON over HTTP to schedule and retrieve appointments.
You may use whatever database and Python web framework you prefer,
although for a project of this size and scope we recommend using SQLite
for your database and Flask with SQLAlchemy as an ORM.

The key features are:
- Appointments can be created, and are persisted to an appointments table in the database.
    - The schema for this table is up to you, but it must somehow specify the date, time and length of the appointment, and have a unique ID.
- Appointments can be be retrieved by ID.
- All appointments can be listed.

The specification of routes and data formats is intentionally open-ended;
where not specified, do what you think best.

### Stretch Goals

Some features you can add if you have time, of varying scope and in no particular order:
- Add tests.
- Allow requests with "start_datetime" and "end_datetime" params to retreive only appointments which overlap with the time interval specified therein.
- Add users who own appointments, and implement access controls for these users.

Keep in mind that quality is more important than quantity and we will be
impressed if you do any of these.
