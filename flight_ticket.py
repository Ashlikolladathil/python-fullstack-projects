import sqlite3
from datetime import datetime

# ==========================================
#     FLIGHT TICKET BOOKING SYSTEM
# ==========================================

DB_NAME = "flight_booking.db"


class Database:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.insert_default_admin()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin(
            username TEXT PRIMARY KEY,
            password TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS flights(
            flight_no TEXT PRIMARY KEY,
            source TEXT,
            destination TEXT,
            route TEXT,
            flight_type TEXT,
            status TEXT,
            flight_date TEXT,
            departure_time TEXT,
            arrival_time TEXT,
            duration TEXT,
            fare INTEGER,
            seats INTEGER
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings(
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_no TEXT,
            booking_date TEXT,
            passenger_name TEXT,
            age INTEGER,
            travel_class TEXT,
            seat_type TEXT,
            meal TEXT,
            luggage INTEGER,
            flight_no TEXT,
            total_fare INTEGER
        )
        """)

        self.conn.commit()

    def insert_default_admin(self):

        self.cursor.execute(
            "SELECT * FROM admin WHERE username=?",
            ("admin",)
        )

        if self.cursor.fetchone() is None:

            self.cursor.execute(
                "INSERT INTO admin VALUES(?,?)",
                ("admin", "1234")
            )

            self.conn.commit()

    def close(self):
        self.conn.close()

class Person:

    def __init__(self, name, age=0):
        self.name = name
        self.age = age


class User(Person):

    def __init__(self, username, password):
        super().__init__(username)
        self.username = username
        self.password = password

    def login(self, db):

        print("\n========== ADMIN LOGIN ==========")

        uname = input("Username : ")
        pwd = input("Password : ")

        db.cursor.execute(
            "SELECT * FROM admin WHERE username=? AND password=?",
            (uname, pwd)
        )

        if db.cursor.fetchone():

            print("\nLogin Successful!\n")
            return True

        print("\nInvalid Username or Password")
        return False


class Flight:

    def __init__(self,
                 flight_no,
                 source,
                 destination,
                 route,
                 flight_type,
                 status,
                 flight_date,
                 departure_time,
                 arrival_time,
                 duration,
                 fare,
                 seats):

        self.flight_no = flight_no
        self.source = source
        self.destination = destination
        self.route = route
        self.flight_type = flight_type
        self.status = status
        self.flight_date = flight_date
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.duration = duration
        self.fare = fare
        self.seats = seats

    def display(self):

        print("-------------------------------------------")
        print("Flight Number :", self.flight_no)
        print("Route         :", self.source, "->", self.destination)
        print("Type          :", self.flight_type)
        print("Status        :", self.status)
        print("Date          :", self.flight_date)
        print("Departure     :", self.departure_time)
        print("Arrival       :", self.arrival_time)
        print("Duration      :", self.duration)
        print("Fare          : ₹", self.fare)
        print("Seats Left    :", self.seats)
        print("-------------------------------------------")


class Passenger(Person):

    def __init__(self,
                 name,
                 age,
                 travel_class,
                 seat_type,
                 meal,
                 luggage):

        super().__init__(name, age)

        self.travel_class = travel_class
        self.seat_type = seat_type
        self.meal = meal
        self.luggage = luggage

class Booking:

    def __init__(self,
                 passenger,
                 flight_no,
                 total_fare):

        self.ticket_no = "FT" + datetime.now().strftime("%Y%m%d%H%M%S")
        self.booking_date = datetime.now().strftime("%d-%m-%Y")

        self.passenger = passenger
        self.flight_no = flight_no
        self.total_fare = total_fare

class FlightBookingSystem:

    def __init__(self):
        self.db = Database()
        self.load_default_flights()


    def load_default_flights(self):

        self.db.cursor.execute("SELECT COUNT(*) FROM flights")
        count = self.db.cursor.fetchone()[0]

        if count == 0:

            flights = [

                ("AI101","Delhi","Mumbai",
                 "Delhi -> Mumbai",
                 "Direct",
                 "On Time",
                 "15-08-2026",
                 "09:30 AM",
                 "11:45 AM",
                 "2 Hours 15 Minutes",
                 5000,
                 5),

                ("6E202","Kochi","Bangalore",
                 "Kochi -> Coimbatore -> Bangalore",
                 "Connecting",
                 "Delayed",
                 "16-08-2026",
                 "10:00 AM",
                 "12:15 PM",
                 "2 Hours 15 Minutes",
                 3500,
                 4),

                ("UK303","Chennai","Hyderabad",
                 "Chennai -> Hyderabad",
                 "Direct",
                 "On Time",
                 "17-08-2026",
                 "03:00 PM",
                 "04:30 PM",
                 "1 Hour 30 Minutes",
                 4200,
                 6)

            ]

            self.db.cursor.executemany(
                "INSERT INTO flights VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                flights
            )

            self.db.conn.commit()

    
    def show_flights(self):

        self.db.cursor.execute("SELECT * FROM flights")

        flights = self.db.cursor.fetchall()

        if len(flights) == 0:
            print("\nNo Flights Available.")
            return

        print("\n========== AVAILABLE FLIGHTS ==========")

        for f in flights:

            print("----------------------------------------")
            print("Flight Number :", f[0])
            print("Source        :", f[1])
            print("Destination   :", f[2])
            print("Route         :", f[3])
            print("Type          :", f[4])
            print("Status        :", f[5])
            print("Date          :", f[6])
            print("Departure     :", f[7])
            print("Arrival       :", f[8])
            print("Duration      :", f[9])
            print("Fare          : ₹", f[10])
            print("Seats Left    :", f[11])
            print("----------------------------------------")

    
    def search_flight(self):

        source = input("Enter Source City : ")
        destination = input("Enter Destination City : ")

        self.db.cursor.execute(
            """
            SELECT * FROM flights
            WHERE source=? AND destination=?
            """,
            (source, destination)
        )

        data = self.db.cursor.fetchall()

        if len(data) == 0:
            print("\nNo Flight Found.")
            return

        print("\nFlight Found\n")

        for f in data:

            print("----------------------------------------")
            print("Flight Number :", f[0])
            print("Source        :", f[1])
            print("Destination   :", f[2])
            print("Fare          : ₹", f[10])
            print("Seats Left    :", f[11])
            print("----------------------------------------")

    
    def add_flight(self):

        print("\n====== ADD NEW FLIGHT ======")

        flight_no = input("Flight Number : ")
        source = input("Source : ")
        destination = input("Destination : ")
        route = input("Route : ")
        flight_type = input("Type : ")
        status = input("Status : ")
        flight_date = input("Date : ")
        departure = input("Departure Time : ")
        arrival = input("Arrival Time : ")
        duration = input("Duration : ")
        fare = int(input("Fare : "))
        seats = int(input("Seats : "))

        self.db.cursor.execute(
            """
            INSERT INTO flights
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                flight_no,
                source,
                destination,
                route,
                flight_type,
                status,
                flight_date,
                departure,
                arrival,
                duration,
                fare,
                seats
            )
        )

        self.db.conn.commit()

        print("\nFlight Added Successfully.")

    
    def update_status(self):

        flight_no = input("Enter Flight Number : ")

        print("\n1. On Time")
        print("2. Delayed")
        print("3. Boarding")
        print("4. Cancelled")

        ch = input("Choose : ")

        status = "On Time"

        if ch == "2":
            status = "Delayed"
        elif ch == "3":
            status = "Boarding"
        elif ch == "4":
            status = "Cancelled"

        self.db.cursor.execute(
            """
            UPDATE flights
            SET status=?
            WHERE flight_no=?
            """,
            (status, flight_no)
        )

        self.db.conn.commit()

        print("\nStatus Updated Successfully.")

    
    def delete_flight(self):

        flight_no = input("Enter Flight Number : ")

        self.db.cursor.execute(
            "DELETE FROM flights WHERE flight_no=?",
            (flight_no,)
        )

        self.db.conn.commit()

        print("\nFlight Deleted Successfully")



    def book_ticket(self):
        self.show_flights()

        flight_no = input("\nEnter Flight Number : ")

        self.db.cursor.execute(
            "SELECT * FROM flights WHERE flight_no=?",
            (flight_no,)
            )

        flight = self.db.cursor.fetchone()

        if flight is None:
            print("\nFlight Not Found.")
            return

        if flight[11] <= 0:
            print("\nSorry! No Seats Available.")
            return

        print("\n===== PASSENGER DETAILS =====")

        name = input("Passenger Name : ")
        age = int(input("Age : "))

        print("\nTravel Class")
        print("1. First Class (+3000)")
        print("2. Business Class (+1500)")
        print("3. Economy Class")

        ch = input("Choice : ")

        class_charge = 0

        if ch == "1":
            travel_class = "First Class"
            class_charge = 3000
        elif ch == "2":
            travel_class = "Business Class"
            class_charge = 1500
        else:
            travel_class = "Economy Class"

        print("\nSeat Preference")
        print("1. Window")
        print("2. Middle")
        print("3. Aisle")

        seat = input("Choice : ")

        if seat == "1":
            seat_type = "Window"
        elif seat == "2":
            seat_type = "Middle"
        else:
            seat_type = "Aisle"

        print("\nMeal Preference")
        print("1. Vegetarian (+200)")
        print("2. Non-Vegetarian (+300)")
        print("3. Vegan (+250)")
        print("4. No Meal")

        meal_choice = input("Choice : ")

        meal_charge = 0

        if meal_choice == "1":
            meal = "Vegetarian"
            meal_charge = 200
        elif meal_choice == "2":
            meal = "Non-Vegetarian"
            meal_charge = 300
        elif meal_choice == "3":
            meal = "Vegan"
            meal_charge = 250
        else:
            meal = "No Meal"

        luggage = int(input("Enter Luggage Weight (kg): "))

        luggage_charge = 0

        if luggage > 15:
            luggage_charge = (luggage - 15) * 100

        total = flight[10] + class_charge + meal_charge + luggage_charge

        ticket_no = "FT" + datetime.now().strftime("%Y%m%d%H%M%S")
        booking_date = datetime.now().strftime("%d-%m-%Y")

        self.db.cursor.execute("""
                               INSERT INTO bookings(
                                 ticket_no,
                                 booking_date,
                                 passenger_name,
                                 age,
                                 travel_class,
                                 seat_type,
                                 meal,
                                 luggage,
                                 flight_no,
                                 total_fare
                              )
                             VALUES(?,?,?,?,?,?,?,?,?,?)
                            """, 
                            (
                                 ticket_no,
                                 booking_date,
                                 name,
                                 age,
                                 travel_class,
                                 seat_type,
                                 meal,
                                 luggage,
                                 flight_no,
                                 total
                            ))

        self.db.cursor.execute("""
                               UPDATE flights
                               SET seats = seats - 1
                               WHERE flight_no=?
                              """,
                                (flight_no,)
                               )

        self.db.conn.commit()

        print("\n====================================")
        print("          FLIGHT TICKET")
        print("====================================")
        print("Ticket Number :", ticket_no)
        print("Booking Date  :", booking_date)
        print("Passenger     :", name)
        print("Age           :", age)
        print("Flight Number :", flight_no)
        print("From          :", flight[1])
        print("To            :", flight[2])
        print("Travel Class  :", travel_class)
        print("Seat          :", seat_type)
        print("Meal          :", meal)
        print("Luggage       :", luggage, "kg")
        print("Total Fare    : ₹", total)
        print("====================================")



    def view_bookings(self):
        
        self.db.cursor.execute("SELECT * FROM bookings")

        data = self.db.cursor.fetchall()

        if len(data) == 0:
            print("\nNo Bookings Found.")
            return

        print("\n========== BOOKINGS ==========")

        for b in data:
            print("--------------------------------")
            print("Booking ID :", b[0])
            print("Ticket No  :", b[1])
            print("Passenger  :", b[3])
            print("Flight No  :", b[9])
            print("Class      :", b[5])
            print("Seat       :", b[6])
            print("Meal       :", b[7])
            print("Fare       : ₹", b[10])
            print("--------------------------------")

    def cancel_ticket(self):
        booking_id = int(input("Enter Booking ID : "))
        self.db.cursor.execute(
            "SELECT flight_no FROM bookings WHERE booking_id=?",
            (booking_id,)
            )

        booking = self.db.cursor.fetchone()

        if booking is None:
            print("\nBooking Not Found.")
            return

        flight_no = booking[0]

    # Restore seat
        self.db.cursor.execute("""
                               UPDATE flights
                               SET seats = seats + 1
                               WHERE flight_no=?
                               """,
                              (flight_no,)
                               )

    # Delete booking
        self.db.cursor.execute(
            "DELETE FROM bookings WHERE booking_id=?",
            (booking_id,)
            )

        self.db.conn.commit()

        print("\nTicket Cancelled Successfully.")



    def modify_booking(self):
        booking_id = int(input("Enter Booking ID : "))

        self.db.cursor.execute("""
                               SELECT travel_class,
                               meal,
                               luggage
                               FROM bookings
                               WHERE booking_id=?
                               """,
                               (booking_id,)
                                )

        booking = self.db.cursor.fetchone()

        if booking is None:
            print("\nBooking Not Found.")
            return

        print("\n===== MODIFY BOOKING =====")

        print("1. First Class")
        print("2. Business Class")
        print("3. Economy Class")

        ch = input("Select Class : ")

        class_charge = 0

        if ch == "1":
            travel_class = "First Class"
            class_charge = 3000

        elif ch == "2":
            travel_class = "Business Class"
            class_charge = 1500

        else:
            travel_class = "Economy Class"

        print("\nMeal")

        print("1. Vegetarian")
        print("2. Non-Vegetarian")
        print("3. Vegan")
        print("4. No Meal")

        meal_choice = input("Choice : ")

        meal_charge = 0

        if meal_choice == "1":
            meal = "Vegetarian"
            meal_charge = 200

        elif meal_choice == "2":
            meal = "Non-Vegetarian"
            meal_charge = 300

        elif meal_choice == "3":
            meal = "Vegan"
            meal_charge = 250

        else:
            meal = "No Meal"

        luggage = int(input("Enter Luggage Weight : "))

        luggage_charge = 0

        if luggage > 15:
            luggage_charge = (luggage - 15) * 100

        self.db.cursor.execute("""
                               SELECT flights.fare
                               FROM bookings
                               JOIN flights
                               ON bookings.flight_no = flights.flight_no
                               WHERE booking_id=?
                               """,
                               (booking_id,)
                             )

        base_fare = self.db.cursor.fetchone()[0]

        total = base_fare + class_charge + meal_charge + luggage_charge

        self.db.cursor.execute("""
                               UPDATE bookings
                               SET travel_class=?,
                               meal=?,
                               luggage=?,
                               total_fare=?
                               WHERE booking_id=?
                               """,
                             (
                              travel_class,
                              meal,
                              luggage,
                              total,
                              booking_id
                             )
                             )

        self.db.conn.commit()

        print("\nBooking Updated Successfully.")

        print("\n========= PAYMENT SUMMARY =========")
        print("Updated Fare : ₹", total)


    def passenger_menu(self):
        
        while True:
            
            print("\n=================================")
            print("      PASSENGER MENU")
            print("=================================")
            print("1. View Flights")
            print("2. Search Flight")
            print("3. Book Ticket")
            print("4. View Bookings")
            print("5. Modify Booking")
            print("6. Cancel Ticket")
            print("7. Back")

            choice = input("Enter Choice : ")

            if choice == "1":
                self.show_flights()

            elif choice == "2":
                self.search_flight()

            elif choice == "3":
                self.book_ticket()

            elif choice == "4":
                self.view_bookings()

            elif choice == "5":
                self.modify_booking()

            elif choice == "6":
                self.cancel_ticket()

            elif choice == "7":
                break

            else:
                print("Invalid Choice")


    def admin_menu(self):
        
        while True:
            
            print("\n=================================")
            print("         ADMIN MENU")
            print("=================================")
            print("1. View Flights")
            print("2. Add Flight")
            print("3. Delete Flight")
            print("4. Update Flight Status")
            print("5. View Bookings")
            print("6. Back")

            choice = input("Enter Choice : ")

            if choice == "1":
                self.show_flights()

            elif choice == "2":
                self.add_flight()

            elif choice == "3":
                self.delete_flight()

            elif choice == "4":
                self.update_status()

            elif choice == "5":
                self.view_bookings()

            elif choice == "6":
                break

            else:
                print("Invalid Choice")

    def run(self):

        admin = User("admin", "1234")

        while True:

            print("\n=================================")
            print("   FLIGHT BOOKING MANAGEMENT")
            print("=================================")
            print("1. Passenger")
            print("2. Admin")
            print("3. Exit")

            choice = input("Enter Choice : ")

            if choice == "1":

                self.passenger_menu()

            elif choice == "2":

                if admin.login(self.db):

                    self.admin_menu()

            elif choice == "3":

                self.db.close()

                print("\nThank You For Using Flight Booking System.")
                break

            else:

                print("Invalid Choice")

if __name__ == "__main__":

    system = FlightBookingSystem()

    system.run()
