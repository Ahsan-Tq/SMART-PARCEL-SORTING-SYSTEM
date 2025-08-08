import datetime
import json
import os
from typing import List, Dict, Optional

# Admin credentials (in production, use secure database)
ADMIN_CREDENTIALS = {
    "admin": "admin123",
    "manager": "manager123"
}

class Parcel:
    def __init__(self, weight: float, destination: str, sender: str, recipient: str, priority: str = "normal"):
        self.weight = weight
        self.destination = destination
        self.sender = sender
        self.recipient = recipient
        self.priority = priority
        self.status = "pending"
        self.created_date = datetime.datetime.now()
        self.last_updated = datetime.datetime.now()
        self.tracking_number = None
        self.delivery_date = None
        self.location = "origin"
        
    def update_status(self, new_status: str):
        self.status = new_status
        self.last_updated = datetime.datetime.now()
        
    def set_tracking_number(self, tracking_number: str):
        self.tracking_number = tracking_number
        
    def set_delivery_date(self, delivery_date: datetime.datetime):
        self.delivery_date = delivery_date
        
    def set_location(self, location: str):
        self.location = location
        
    def to_dict(self):
        return {
            "weight": self.weight,
            "destination": self.destination,
            "sender": self.sender,
            "recipient": self.recipient,
            "priority": self.priority,
            "status": self.status,
            "created_date": self.created_date.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "tracking_number": self.tracking_number,
            "delivery_date": self.delivery_date.isoformat() if self.delivery_date else None,
            "location": self.location
        }
        
    @classmethod
    def from_dict(cls, data: Dict):
        parcel = cls(data["weight"], data["destination"], data["sender"], data["recipient"], data["priority"])
        parcel.status = data["status"]
        parcel.created_date = datetime.datetime.fromisoformat(data["created_date"])
        parcel.last_updated = datetime.datetime.fromisoformat(data["last_updated"])
        parcel.tracking_number = data["tracking_number"]
        parcel.location = data["location"]
        if data["delivery_date"]:
            parcel.delivery_date = datetime.datetime.fromisoformat(data["delivery_date"])
        return parcel
        
    def __str__(self):
        return f"Parcel {self.tracking_number} - {self.weight}kg to {self.destination} ({self.status})"

class ParcelManager:
    def __init__(self):
        self.parcels = []
        self.load_parcels()
        
    def load_parcels(self):
        """Load parcels from JSON file (shared with userside)"""
        try:
            if os.path.exists("parcels.json"):
                with open("parcels.json", "r") as f:
                    data = json.load(f)
                    self.parcels = [Parcel.from_dict(parcel_data) for parcel_data in data]
        except Exception as e:
            print(f"Error loading parcels: {e}")
            self.parcels = []
            
    def save_parcels(self):
        """Save parcels to JSON file (shared with userside)"""
        try:
            data = [parcel.to_dict() for parcel in self.parcels]
            with open("parcels.json", "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving parcels: {e}")
            
    def get_all_parcels(self) -> List[Parcel]:
        return self.parcels
        
    def get_parcel_by_tracking(self, tracking_number: str) -> Optional[Parcel]:
        return next((p for p in self.parcels if p.tracking_number == tracking_number), None)
        
    def update_parcel_status(self, tracking_number: str, new_status: str, location: str = None):
        parcel = self.get_parcel_by_tracking(tracking_number)
        if parcel:
            parcel.update_status(new_status)
            if location:
                parcel.set_location(location)
            self.save_parcels()
            return True
        return False
        
    def set_delivery_date(self, tracking_number: str, delivery_date: datetime.datetime):
        parcel = self.get_parcel_by_tracking(tracking_number)
        if parcel:
            parcel.set_delivery_date(delivery_date)
            self.save_parcels()
            return True
        return False
        
    def delete_parcel(self, tracking_number: str) -> bool:
        parcel = self.get_parcel_by_tracking(tracking_number)
        if parcel:
            self.parcels.remove(parcel)
            self.save_parcels()
            return True
        return False
        
    def check_heavy_parcels(self, threshold: float = 10.0) -> List[Parcel]:
        """Check for parcels heavier than threshold"""
        return [p for p in self.parcels if p.weight > threshold]

class AdminApp:
    def __init__(self):
        self.parcel_manager = ParcelManager()
        self.current_user = None
        
    def login(self) -> bool:
        print("\n" + "="*50)
        print("ADMIN LOGIN SYSTEM")
        print("="*50)
        
        max_attempts = 3
        for attempt in range(max_attempts):
            user_id = input("Admin ID: ").strip()
            password = input("Password: ").strip()
            
            if user_id in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[user_id] == password:
                self.current_user = user_id
                print(f"\nWelcome, {user_id}!")
                return True
            else:
                remaining = max_attempts - attempt - 1
                print(f"Invalid credentials. {remaining} attempts remaining.")
                
        print("Too many failed attempts. Exiting.")
        return False
        
    def display_menu(self):
        print("\n" + "="*50)
        print("ADMIN PARCEL MANAGEMENT SYSTEM")
        print("="*50)
        print("1. View All Parcels")
        print("2. Update Parcel Status")
        print("3. Set Delivery Date")
        print("4. Delete Parcel")
        print("5. Check Heavy Parcels")
        print("6. Search Parcel")
        print("7. Logout")
        print("8. Exit")
        print("-"*50)
        
    def view_all_parcels(self):
        print(f"\nALL PARCELS ({len(self.parcel_manager.parcels)} total)")
        print("-"*80)
        print(f"{'Tracking':<15} {'Weight':<8} {'Destination':<15} {'Status':<12} {'Location':<12} {'Priority':<8}")
        print("-"*80)
        
        if not self.parcel_manager.parcels:
            print("No parcels in system")
            return
            
        for parcel in self.parcel_manager.parcels:
            print(f"{parcel.tracking_number:<15} {parcel.weight:<8.1f} {parcel.destination:<15} {parcel.status:<12} {parcel.location:<12} {parcel.priority:<8}")
            
    def update_parcel_status(self):
        print("\nUPDATE PARCEL STATUS")
        print("-"*25)
        
        tracking_number = input("Enter tracking number: ").strip()
        parcel = self.parcel_manager.get_parcel_by_tracking(tracking_number)
        
        if not parcel:
            print("Parcel not found")
            return
            
        print(f"\nCurrent status: {parcel.status}")
        print(f"Current location: {parcel.location}")
        
        print("\nAvailable statuses:")
        print("1. pending")
        print("2. in_transit")
        print("3. at_main_centre")
        print("4. out_for_delivery")
        print("5. delivered")
        print("6. returned")
        
        status_choice = input("New status (1-6): ").strip()
        status_map = {
            "1": "pending",
            "2": "in_transit", 
            "3": "at_main_centre",
            "4": "out_for_delivery",
            "5": "delivered",
            "6": "returned"
        }
        
        new_status = status_map.get(status_choice)
        if not new_status:
            print("Invalid status choice")
            return
            
        location = input("Location (optional): ").strip() or None
        
        if self.parcel_manager.update_parcel_status(tracking_number, new_status, location):
            print(f"Status updated to: {new_status}")
        else:
            print("Failed to update status")
            
    def set_delivery_date(self):
        print("\nSET DELIVERY DATE")
        print("-"*25)
        
        tracking_number = input("Enter tracking number: ").strip()
        parcel = self.parcel_manager.get_parcel_by_tracking(tracking_number)
        
        if not parcel:
            print("Parcel not found")
            return
            
        try:
            date_str = input("Delivery date (YYYY-MM-DD): ").strip()
            delivery_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            
            if self.parcel_manager.set_delivery_date(tracking_number, delivery_date):
                print(f"Delivery date set to: {delivery_date.strftime('%Y-%m-%d')}")
            else:
                print("Failed to set delivery date")
        except ValueError:
            print("Invalid date format. Use YYYY-MM-DD")
            
    def delete_parcel(self):
        print("\nDELETE PARCEL")
        print("-"*25)
        
        tracking_number = input("Enter tracking number: ").strip()
        parcel = self.parcel_manager.get_parcel_by_tracking(tracking_number)
        
        if not parcel:
            print("Parcel not found")
            return
            
        print(f"\nParcel details:")
        print(f"Tracking: {parcel.tracking_number}")
        print(f"Weight: {parcel.weight}kg")
        print(f"Destination: {parcel.destination}")
        print(f"Status: {parcel.status}")
        
        confirm = input("\nAre you sure you want to delete this parcel? (yes/no): ").strip().lower()
        if confirm == "yes":
            if self.parcel_manager.delete_parcel(tracking_number):
                print("Parcel deleted successfully")
            else:
                print("Failed to delete parcel")
        else:
            print("Deletion cancelled")
            
    def check_heavy_parcels(self):
        print("\nCHECK HEAVY PARCELS")
        print("-"*25)
        
        try:
            threshold = float(input("Weight threshold (kg, default 10.0): ").strip() or "10.0")
        except ValueError:
            threshold = 10.0
            
        heavy_parcels = self.parcel_manager.check_heavy_parcels(threshold)
        
        if not heavy_parcels:
            print(f"No parcels heavier than {threshold}kg found")
            return
            
        print(f"\nHEAVY PARCELS (> {threshold}kg) - {len(heavy_parcels)} found")
        print("-"*80)
        print(f"{'Tracking':<15} {'Weight':<8} {'Destination':<15} {'Status':<12} {'Priority':<8}")
        print("-"*80)
        
        for parcel in heavy_parcels:
            print(f"{parcel.tracking_number:<15} {parcel.weight:<8.1f} {parcel.destination:<15} {parcel.status:<12} {parcel.priority:<8}")
            
    def search_parcel(self):
        print("\nSEARCH PARCEL")
        print("-"*25)
        
        tracking_number = input("Enter tracking number: ").strip()
        parcel = self.parcel_manager.get_parcel_by_tracking(tracking_number)
        
        if not parcel:
            print("Parcel not found")
            return
            
        print(f"\nParcel Details:")
        print(f"Tracking Number: {parcel.tracking_number}")
        print(f"Weight: {parcel.weight}kg")
        print(f"Destination: {parcel.destination}")
        print(f"Sender: {parcel.sender}")
        print(f"Recipient: {parcel.recipient}")
        print(f"Priority: {parcel.priority}")
        print(f"Status: {parcel.status}")
        print(f"Location: {parcel.location}")
        print(f"Created: {parcel.created_date.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Last Updated: {parcel.last_updated.strftime('%Y-%m-%d %H:%M:%S')}")
        if parcel.delivery_date:
            print(f"Delivery Date: {parcel.delivery_date.strftime('%Y-%m-%d')}")
        else:
            print("Delivery Date: Not set")
            
    def run(self):
        print("Welcome to Admin Parcel Management System!")
        
        if not self.login():
            return
            
        while True:
            self.display_menu()
            choice = input("Choose (1-8): ").strip()
            
            if choice == "1":
                self.view_all_parcels()
                input("\nPress Enter to continue...")
            elif choice == "2":
                self.update_parcel_status()
                input("\nPress Enter to continue...")
            elif choice == "3":
                self.set_delivery_date()
                input("\nPress Enter to continue...")
            elif choice == "4":
                self.delete_parcel()
                input("\nPress Enter to continue...")
            elif choice == "5":
                self.check_heavy_parcels()
                input("\nPress Enter to continue...")
            elif choice == "6":
                self.search_parcel()
                input("\nPress Enter to continue...")
            elif choice == "7":
                print(f"\nLogged out, {self.current_user}")
                self.current_user = None
                if not self.login():
                    break
            elif choice == "8":
                print("\nThanks for using Admin Parcel Management!")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    app = AdminApp()
    app.run()
