from pdb import main

import customtkinter as ctk
import json

from tkinter import messagebox
from tkinter import ttk

# ==========================
# SETTINGS
# ==========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

DATA_FILE = "data.json"


# ==========================
# DATA FUNCTIONS
# ==========================

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except:
        return {}


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


users = load_data()


# ==========================
# MAIN APP
# ==========================

class VehicleCareApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("VehicleCare Tracker")
        self.geometry("1200x700")

        self.current_user = None

        self.show_login()

    # ==========================
    # LOGIN PAGE
    # ==========================

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_login(self):

        self.clear_window()

        frame = ctk.CTkFrame(self, width=500, height=500)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(
            frame,
            text="VEHICLECARE TRACKER",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=30)

        subtitle = ctk.CTkLabel(
            frame,
            text="Smart Vehicle Maintenance System",
            font=("Arial", 14)
        )
        subtitle.pack(pady=5)

        self.login_username = ctk.CTkEntry(
            frame,
            width=300,
            placeholder_text="Username"
        )
        self.login_username.pack(pady=15)

        self.login_password = ctk.CTkEntry(
            frame,
            width=300,
            show="*",
            placeholder_text="Password"
        )
        self.login_password.pack(pady=15)

        login_btn = ctk.CTkButton(
            frame,
            text="Login",
            width=300,
            command=self.login
        )
        login_btn.pack(pady=10)

        register_btn = ctk.CTkButton(
            frame,
            text="Register",
            width=300,
            fg_color="#1f6aa5",
            command=self.show_register
        )
        register_btn.pack(pady=10)

    # ==========================
    # REGISTER PAGE
    # ==========================

    def show_register(self):

        self.clear_window()

        frame = ctk.CTkFrame(self, width=500, height=500)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        title = ctk.CTkLabel(
            frame,
            text="CREATE ACCOUNT",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=30)

        self.reg_username = ctk.CTkEntry(
            frame,
            width=300,
            placeholder_text="Username"
        )
        self.reg_username.pack(pady=10)

        self.reg_password = ctk.CTkEntry(
            frame,
            width=300,
            show="*",
            placeholder_text="Password"
        )
        self.reg_password.pack(pady=10)

        register_btn = ctk.CTkButton(
            frame,
            text="Create Account",
            width=300,
            command=self.register
        )
        register_btn.pack(pady=20)

        back_btn = ctk.CTkButton(
            frame,
            text="Back",
            width=300,
            command=self.show_login
        )
        back_btn.pack()

    # ==========================
    # LOGIN LOGIC
    # ==========================

    def login(self):

        username = self.login_username.get().strip()
        password = self.login_password.get()

        if username in users:

            if users[username]["password"] == password:

                self.current_user = username

                self.show_dashboard()

                return

        messagebox.showerror(
            "Login Failed",
            "Invalid username or password."
        )

    # ==========================
    # REGISTER LOGIC
    # ==========================

    def register(self):

        username = self.reg_username.get().strip()
        password = self.reg_password.get()

        if username == "" or password == "":

            messagebox.showerror(
                "Error",
                "Fill all fields."
            )
            return

        if username in users:

            messagebox.showerror(
                "Error",
                "Username already exists."
            )
            return

        users[username] = {
            "password": password,
            "vehicles": {}
        }

        save_data(users)

        messagebox.showinfo(
            "Success",
            "Account created successfully!"
        )

        self.show_login()

    # ==========================
    # DASHBOARD
    # ==========================

    def show_dashboard(self):

        self.clear_window()

        # Sidebar
        sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        title = ctk.CTkLabel(
            sidebar,
            text="VEHICLECARE",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=30)

        dashboard_btn = ctk.CTkButton(
            sidebar,
            text="Dashboard"
        )
        dashboard_btn.pack(pady=10, padx=20)

        vehicles_btn = ctk.CTkButton(
            sidebar,
        text="🚗 Vehicles",
            command=self.show_vehicles
        )
        vehicles_btn.pack(pady=10, padx=20)

        services_btn = ctk.CTkButton(
            sidebar,
            text="🔧 Services",
            command=self.show_services
        )
        services_btn.pack(pady=10, padx=20)

        reminders_btn = ctk.CTkButton(
            sidebar,
            text="⏰ Reminders",
            command=self.show_reminders
        )
        reminders_btn.pack(pady=10, padx=20)

        logout_btn = ctk.CTkButton(
            sidebar,
            text="Logout",
            fg_color="red",
            command=self.show_login
        )
        logout_btn.pack(
            side="bottom",
            pady=20,
            padx=20
        )

        # Main Area
        main = ctk.CTkFrame(self)
        main.pack(
            side="right",
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        welcome = ctk.CTkLabel(
            main,
            text=f"Welcome, {self.current_user}",
            font=("Arial", 28, "bold")
        )

        welcome.pack(
            anchor="w",
            pady=20
        )

        vehicle_count = len(
            users[self.current_user]["vehicles"]
        )

        service_count = 0

        total_cost = 0

        for vehicle in users[self.current_user]["vehicles"].values():

            service_count += len(
                vehicle["maintenance"]
            )

            for service in vehicle["maintenance"]:

                total_cost += service["cost"]

            # Alerts count (not implemented yet) - default to 0 to avoid undefined variable
            reminders = self.get_reminders()

            alert_count = len(reminders)

        cards_frame = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            pady=20
        )

        self.create_card(
            cards_frame,
            "🚗 Vehicles",
            vehicle_count,
            0
        )

        self.create_card(
            cards_frame,
            "🔧 Services",
            service_count,
            1
        )

        self.create_card(
            cards_frame,
            "💰 Cost",
            f"{total_cost:,.0f}",
            2
        )

        self.create_card(
            cards_frame,
            "⚠ Alerts",
            alert_count,
            3
        )
        health_score = 100
        health_score -= 10
        health_score = max(0, health_score)
        self.create_card(
            cards_frame,
            "❤️ Health Score",
            f"{health_score}%",
            4
        )
        # AI Assistant
        self.create_ai_panel(main)
        # INSERT THE MAINTENANCE WIDGET HERE

        maintenance_box = ctk.CTkTextbox(
            main,
            height=180
        )

        maintenance_box.pack(
            fill="x",
            pady=20
        )

        maintenance_box.insert(
            "end",
            "UPCOMING MAINTENANCE\n\n"
        )

        vehicles = users[self.current_user]["vehicles"]

        for plate, vehicle in vehicles.items():

            last_oil = None

            for service in vehicle["maintenance"]:

                if service["type"] == "Oil Change":
                    last_oil = service["mileage"]

            if last_oil is not None:

                distance = vehicle["mileage"] - last_oil
                remaining = max(0, 5000 - distance)

                maintenance_box.insert(
                    "end",
                    f"{plate} → Oil Change in {remaining} km\n"
                )


    def create_ai_panel(self, parent):

        vehicles = users[self.current_user]["vehicles"]

        total_cost = 0
        service_count = 0
        recommendations = []

        reminders = self.get_reminders()

        alert_count = len(reminders)
  
        for plate, vehicle in vehicles.items():

            for service in vehicle["maintenance"]:

                total_cost += service["cost"]
                service_count += 1

        for reminder in reminders:

            if reminder["status"] == "OVERDUE":

                recommendations.append(
                    f"⚠ {reminder['plate']} is overdue by "
                    f"{reminder['distance']} km."
                )

            else:

                recommendations.append(
                    f"🔧 {reminder['plate']} will require "
                    f"an oil change in "
                    f"{reminder['distance']} km."
                )
                

        ai_frame = ctk.CTkFrame(parent)

        ai_frame.pack(
            fill="x",
            padx=10,
            pady=15
        )

        title = ctk.CTkLabel(
            ai_frame,
            text="🤖 VehicleCare AI Assistant",
            font=("Segoe UI", 20, "bold")
        )

        title.pack(
            anchor="w",
            padx=15,
            pady=(10, 5)
        )

        ai_box = ctk.CTkTextbox(
            ai_frame,
            height=180
        )

        ai_box.pack(
            fill="x",
            padx=15,
            pady=10
        )

        ai_box.insert(
            "end",
            "VEHICLE HEALTH INSIGHTS\n"
            "═══════════════════════════\n\n"
        )

        if len(vehicles) == 0:

            ai_box.insert(
                "end",
                "• No vehicles registered yet.\n"
                "• Register your first vehicle to start tracking maintenance.\n"
            )

        else:

            ai_box.insert(
                "end",
                f"• Vehicles managed: {len(vehicles)}\n"
            )

            ai_box.insert(
                "end",
                f"• Services recorded: {service_count}\n"
            )

            ai_box.insert(
                "end",
                f"• Maintenance spending: {total_cost:,.0f} RWF\n\n"
            )

            if alert_count == 0:

                ai_box.insert(
                    "end",
                    "✅ All vehicles appear to be in good maintenance condition.\n\n"
                )

            else:

                ai_box.insert(
                    "end",
                    f"⚠ {alert_count} vehicle(s) require attention.\n\n"
                )

            ai_box.insert(
                "end",
                "RECOMMENDATIONS\n"
                "────────────────────\n"
            )

            if recommendations:

                for recommendation in recommendations:

                    ai_box.insert(
                        "end",
                        recommendation + "\n"
                    )

            else:

                ai_box.insert(
                    "end",
                    "No maintenance recommendations at this time.\n"
                )

            if total_cost > 300000:

                ai_box.insert(
                    "end",
                    "\n💰 Maintenance expenses are becoming significant."
                )

            if service_count > 10:

                ai_box.insert(
                    "end",
                    "\n📊 Sufficient data available for future predictive maintenance analysis."
                )

        ai_box.configure(state="disabled")

    def get_reminders(self):

        reminders = []

        vehicles = users[self.current_user]["vehicles"]

        for plate, vehicle in vehicles.items():

            current_mileage = vehicle["mileage"]

            last_oil_change = None

            for service in vehicle["maintenance"]:

                if service["type"].lower() == "oil change":

                    last_oil_change = service["mileage"]

            if last_oil_change is not None:

                distance = current_mileage - last_oil_change

                if distance >= 5000:

                    reminders.append({
                        "plate": plate,
                        "status": "OVERDUE",
                        "distance": distance - 5000
                    })

                elif distance >= 4000:

                    reminders.append({
                        "plate": plate,
                        "status": "SOON",
                        "distance": 5000 - distance
                    })

        return reminders    

    # ==========================
    # CARD
    # ==========================

    def create_card(
        self,
        parent,
        title,
        value,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            width=250,
            height=150
        )

        card.grid(
            row=0,
            column=column,
            padx=20
        )

        label1 = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 18)
        )

        label1.pack(pady=20)

        label2 = ctk.CTkLabel(
            card,
            text=str(value),
            font=("Arial", 30, "bold")
        )

        label2.pack()
# ==========================
# START APP
# ==========================


    def show_vehicles(self):

        self.clear_window()

        # Sidebar
        sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        title = ctk.CTkLabel(
            sidebar,
            text="VEHICLECARE",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=30)

        dashboard_btn = ctk.CTkButton(
            sidebar,
            text="🏠 Dashboard",
            command=self.show_dashboard
        )

        dashboard_btn.pack(
            pady=10,
            padx=20
        )

        vehicle_btn = ctk.CTkButton(
            sidebar,
            text="🚗 Vehicles"
        )

        vehicle_btn.pack(
            pady=10,
            padx=20
        )

        logout_btn = ctk.CTkButton(
            sidebar,
            text="Logout",
            fg_color="red",
            command=self.show_login
        )

        logout_btn.pack(
            side="bottom",
            pady=20,
            padx=20
        )

        # Main Content

        main = ctk.CTkFrame(self)

        main.pack(
            side="right",
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        title = ctk.CTkLabel(
            main,
            text="Vehicle Management",
            font=("Arial", 28, "bold")
        )

        title.pack(anchor="w", pady=10)

        # Search

        search_frame = ctk.CTkFrame(main)

        search_frame.pack(
            fill="x",
            pady=10
        )

        self.search_entry = ctk.CTkEntry(
            search_frame,
            width=250,
            placeholder_text="Search plate..."
        )

        self.search_entry.pack(
            side="left",
            padx=10,
            pady=10
        )

        search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self.search_vehicle
        )

        search_btn.pack(
            side="left",
            padx=10
        )

        add_btn = ctk.CTkButton(
            search_frame,
            text="Add Vehicle",
            command=self.add_vehicle_window
        )

        add_btn.pack(
            side="right",
            padx=10
        )

        # Table

        table_frame = ctk.CTkFrame(main)

        table_frame.pack(
            fill="both",
            expand=True,
            pady=20
        )

        columns = (
            "Plate",
            "Model",
            "Mileage"
        )

        self.vehicle_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:

            self.vehicle_table.heading(
                col,
                text=col
            )

            self.vehicle_table.column(
                col,
                width=180
            )

        self.vehicle_table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.load_vehicle_table()

        delete_btn = ctk.CTkButton(
            main,
            text="Remove Selected Vehicle",
            fg_color="red",
            command=self.remove_selected_vehicle
        )

        delete_btn.pack(
            pady=10
        )
        update_btn = ctk.CTkButton(
            main,
            text="⛽ Update Mileage",
            command=self.update_mileage_window
        )

        update_btn.pack(
        pady=10
        )
    def load_vehicle_table(self):

        for row in self.vehicle_table.get_children():
            self.vehicle_table.delete(row)

        vehicles = users[self.current_user]["vehicles"]

        for plate, info in vehicles.items():

            self.vehicle_table.insert(
                "",
                "end",
                values=(
                    plate,
                    info["model"],
                    info["mileage"]
                )
            )
    def search_vehicle(self):

        plate = self.search_entry.get().upper()

        vehicles = users[self.current_user]["vehicles"]

        if plate in vehicles:

            vehicle = vehicles[plate]

            messagebox.showinfo(
                "Vehicle Found",
                f"Plate: {plate}\n"
                f"Model: {vehicle['model']}\n"
                f"Mileage: {vehicle['mileage']} km"
            )

        else:

            messagebox.showerror(
                "Not Found",
                "Vehicle not found."
            )
    def add_vehicle_window(self):

        window = ctk.CTkToplevel(self)

        window.title("Add Vehicle")

        window.geometry("400x300")

        plate_entry = ctk.CTkEntry(
            window,
            placeholder_text="Plate Number"
        )

        plate_entry.pack(
            pady=15,
            padx=20,
            fill="x"
        )

        model_entry = ctk.CTkEntry(
            window,
            placeholder_text="Model"
        )

        model_entry.pack(
            pady=15,
            padx=20,
            fill="x"
        )

        mileage_entry = ctk.CTkEntry(
            window,
            placeholder_text="Mileage"
        )

        mileage_entry.pack(
            pady=15,
            padx=20,
            fill="x"
        )

        def save_vehicle():

            plate = plate_entry.get().upper()

            model = model_entry.get()

            try:
                mileage = int(
                    mileage_entry.get()
                )
            except:
                messagebox.showerror(
                    "Error",
                    "Mileage must be a number."
                )
                return

            users[self.current_user]["vehicles"][plate] = {
                "model": model,
                "mileage": mileage,
                "maintenance": []
            }

            save_data(users)

            self.load_vehicle_table()

            window.destroy()

        save_btn = ctk.CTkButton(
            window,
            text="Save Vehicle",
            command=save_vehicle
        )

        save_btn.pack(
            pady=20
        )
    def remove_selected_vehicle(self):

        selected = self.vehicle_table.selection()

        if not selected:
            return

        values = self.vehicle_table.item(
            selected[0]
        )["values"]

        plate = values[0]

        confirm = messagebox.askyesno(
            "Confirm",
            f"Delete vehicle {plate}?"
        )

        if confirm:

            del users[self.current_user]["vehicles"][plate]

            save_data(users)

            self.load_vehicle_table()

    def show_services(self):

        self.clear_window()

        sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        ctk.CTkLabel(
            sidebar,
            text="VEHICLECARE",
            font=("Arial",22,"bold")
        ).pack(pady=30)

        ctk.CTkButton(
            sidebar,
            text="🏠 Dashboard",
            command=self.show_dashboard
        ).pack(pady=10,padx=20)

        ctk.CTkButton(
            sidebar,
            text="🚗 Vehicles",
            command=self.show_vehicles
        ).pack(pady=10,padx=20)

        ctk.CTkButton(
            sidebar,
            text="🔧 Services"
        ).pack(pady=10,padx=20)

        ctk.CTkButton(
            sidebar,
            text="⏰ Reminders",
            command=self.show_reminders
        ).pack(pady=10,padx=20)

        main = ctk.CTkFrame(self)

        main.pack(
            side="right",
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            main,
            text="Service Management",
            font=("Arial",28,"bold")
        ).pack(anchor="w")

        ctk.CTkButton(
            main,
            text="➕ Record Service",
            command=self.record_service_window
        ).pack(
            anchor="e",
            pady=10
        )

        columns = (
            "Plate",
            "Type",
            "Cost",
            "Mileage",
            "Date"
        )

        table_frame = ctk.CTkFrame(main)

        table_frame.pack(
            fill="both",
            expand=True
        )

        self.service_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.service_table.heading(
                col,
                text=col
            )

        self.service_table.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.load_service_table()

    def load_service_table(self):

        for row in self.service_table.get_children():
            self.service_table.delete(row)

        vehicles = users[self.current_user]["vehicles"]

        for plate, vehicle in vehicles.items():

            for service in vehicle["maintenance"]:

                self.service_table.insert(
                    "",
                    "end",
                    values=(
                        plate,
                        service["type"],
                        f"{service['cost']:,.0f}",
                        service["mileage"],
                        service.get("date", "")
                    )
                )

    def record_service_window(self):

        vehicles = users[self.current_user]["vehicles"]

        if not vehicles:

            messagebox.showerror(
                "Error",
                "No vehicles registered."
            )

            return

        window = ctk.CTkToplevel(self)

        window.geometry("450x450")

        window.title("Record Service")

        plate_menu = ctk.CTkOptionMenu(
            window,
            values=list(
                vehicles.keys()
            )
        )

        plate_menu.pack(
            pady=15,
            padx=20
        )

        service_menu = ctk.CTkOptionMenu(
            window,
            values=[
                "Oil Change",
                "Tire Change",
                "General Service"
            ]
        )

        service_menu.pack(
            pady=15,
            padx=20
        )

        cost_entry = ctk.CTkEntry(
            window,
            placeholder_text="Cost (RWF)"
        )

        cost_entry.pack(
            pady=15,
            padx=20
        )

        mileage_entry = ctk.CTkEntry(
            window,
            placeholder_text="Mileage"
        )

        mileage_entry.pack(
            pady=15,
            padx=20
        )

        def save_service():

            plate = plate_menu.get()

            try:
                cost = float(
                    cost_entry.get()
                )

                mileage = int(
                    mileage_entry.get()
                )

            except:

                messagebox.showerror(
                    "Error",
                    "Invalid values."
                )

                return

            from datetime import datetime

            service = {
                "type": service_menu.get(),
                "cost": cost,
                "mileage": mileage,
                "date": datetime.now().strftime("%d/%m/%Y")
            }

            users[self.current_user]["vehicles"][plate]["maintenance"].append(
                service
            )

            if mileage > users[self.current_user]["vehicles"][plate]["mileage"]:
                users[self.current_user]["vehicles"][plate]["mileage"] = mileage

            save_data(users)

            self.load_service_table()

            window.destroy()

        ctk.CTkButton(
            window,
            text="Save Service",
            command=save_service
        ).pack(
            pady=20
        )

    def show_reminders(self):

        self.clear_window()

        main = ctk.CTkFrame(self)

        main.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        ctk.CTkLabel(
            main,
            text="Maintenance Reminders",
            font=("Arial",28,"bold")
        ).pack(
            anchor="w",
            pady=10
        )
        reminders = self.get_reminders()

        textbox = ctk.CTkTextbox(
            main,
            width=800,
            height=400
        )
        textbox.pack(
            fill="both",
            expand=True,
            pady=10
        )

        if not reminders:
            textbox.insert(
                "0.0",
                "✅ All vehicles are in good condition."
            )
        else:
            for reminder in reminders:
                if reminder["status"] == "OVERDUE":
                    textbox.insert(
                        "end",
                        f"⚠ {reminder['plate']}\n"
                        f"Oil Change Overdue\n"
                        f"Overdue by {reminder['distance']} km\n\n"
                    )
                else:
                    textbox.insert(
                        "end",
                        f"🔧 {reminder['plate']}\n"
                        f"Oil Change Soon\n"
                        f"Remaining {reminder['distance']} km\n\n"
                    )

        textbox.configure(state="disabled")

    def update_mileage_window(self):

        selected = self.vehicle_table.selection()

        if not selected:
            return

        plate = self.vehicle_table.item(
            selected[0]
        )["values"][0]

        window = ctk.CTkToplevel(self)

        window.geometry("350x200")

        entry = ctk.CTkEntry(
            window,
            placeholder_text="New Mileage"
        )

        entry.pack(
            pady=20,
            padx=20
        )

        def save():

            try:
                mileage = int(
                    entry.get()
                )
            except:
                return

            users[self.current_user]["vehicles"][plate]["mileage"] = mileage

            save_data(users)

            self.load_vehicle_table()

            window.destroy()

        ctk.CTkButton(
            window,
            text="Save",
            command=save
        ).pack(
            pady=10
        )


    
app = VehicleCareApp()
app.mainloop()