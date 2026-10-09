# Flight Ticket Booking System

A command-line flight ticket booking project built with Python, Object-Oriented Programming (OOP), and SQLite3.

## Features

### Passenger
- View available flights
- Search flights by source and destination
- Book tickets
- View bookings
- Modify travel class, meal, and luggage details
- Cancel tickets

### Admin
- Admin login
- View flights and bookings
- Add and delete flights
- Update flight status

### Technical concepts
- Python classes, objects, and inheritance
- SQLite3 database connectivity
- SQL `CREATE`, `INSERT`, `SELECT`, `UPDATE`, and `DELETE`
- Parameterized SQL queries
- Ticket and fare calculations

## Requirements

- Python 3.10 or newer (the project uses standard-library modules only)

SQLite3 is included with most standard Python installations, so no `pip install` command is normally required.

## Run the project

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

   ```bash
   python flight_ticket.py
   ```

The program creates `flight_booking.db` in the current working directory when it starts, and creates its tables if they do not already exist.

## Demo admin login

For this educational project, the default admin credentials are:

- Username: `admin`
- Password: `1234`

**Security note:** These are demonstration credentials. This console project stores the password as plain text and is not suitable for real-world deployment without security improvements. Do not reuse these credentials for any other account.

## Database and generated files

The SQLite database is created locally when the program runs. The `.gitignore` file excludes the generated database and Python cache files from GitHub by default. This prevents personal test bookings or local data from being uploaded accidentally.

## Project status

This is an educational command-line project. Test the booking, cancellation, modification, and admin flows before describing it as fully tested. It is not connected to a real airline or payment service.
