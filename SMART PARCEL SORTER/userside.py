import datetime
import random
import json
import os
from typing import List, Dict, Optional

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
        parcel.location = data.get("location", "origin")
        if data.get("delivery_date"):
            parcel.delivery_date = datetime.datetime.fromisoformat(data["delivery_date"])
        return parcel
        
    def __str__(self):
        return f"Parcel {self.tracking_number} - {self.weight}kg to {self.destination} ({self.status})"

class TrackingService:
    def __init__(self):
        self.tracking_history = {}
        
    def generate_tracking_number(self) -> str:
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_suffix = random.randint(1000, 9999)
        return f"PKG{timestamp}{random_suffix}"
        
    def log_tracking_event(self, tracking_number: str, event: str):
        if tracking_number not in self.tracking_history:
            self.tracking_history[tracking_number] = []
            
        event_record = {
            "timestamp": datetime.datetime.now(),
            "event": event
        }
        self.tracking_history[tracking_number].append(event_record)
        
    def get_tracking_history(self, tracking_number: str) -> List[Dict]:
        return self.tracking_history.get(tracking_number, [])

class ParcelTracker:
    def __init__(self):
        self.parcels = []
        self.tracking_service = TrackingService()
        self.load_parcels()
        
    def load_parcels(self):
        """Load parcels from JSON file (shared with adminside)"""
        try:
            if os.path.exists("parcels.json"):
                with open("parcels.json", "r") as f:
                    data = json.load(f)
                    self.parcels = [Parcel.from_dict(parcel_data) for parcel_data in data]
        except Exception as e:
            print(f"Error loading parcels: {e}")
            self.parcels = []
            
    def save_parcels(self):
        """Save parcels to JSON file (shared with adminside)"""
        try:
            data = [parcel.to_dict() for parcel in self.parcels]
            with open("parcels.json", "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving parcels: {e}")
        
    def add_parcel(self, weight: float, destination: str, sender: str, recipient: str, priority: str = "normal") -> Parcel:
        parcel = Parcel(weight, destination, sender, recipient, priority)
        tracking_number = self.tracking_service.generate_tracking_number()
        parcel.set_tracking_number(tracking_number)
        self.parcels.append(parcel)
        self.tracking_service.log_tracking_event(tracking_number, "Parcel created and registered")
        self.save_parcels()
        return parcel
        
    def track_parcel(self, tracking_number: str) -> Optional[Dict]:
        # Reload parcels to get latest updates from admin side
        self.load_parcels()
        parcel = next((p for p in self.parcels if p.tracking_number == tracking_number), None)
        if not parcel:
            return None
            
        return {
            "parcel": parcel,
            "history": self.tracking_service.get_tracking_history(tracking_number)
        }
        
    def get_all_parcels(self) -> List[Parcel]:
        # Reload parcels to get latest updates from admin side
        self.load_parcels()
        return self.parcels

class ParcelApp:
    def __init__(self):
        self.tracker = ParcelTracker()
        
    def display_menu(self):
        print("\n" + "="*50)
        print("PARCEL TRACKING SYSTEM")
        print("="*50)
        print("1. Add New Parcel")
        print("2. Track Parcel")
        print("3. View All Parcels")
        print("4. Exit")
        print("-"*50)
        
    def add_parcel_ui(self):
        print("\nADD NEW PARCEL")
        print("-"*25)
        
        try:
            weight = float(input("Weight (kg): "))
            destination = input("Destination: ")
            sender = input("Sender: ")
            recipient = input("Recipient: ")
            
            print("\nPriority:")
            print("1. urgent")
            print("2. high") 
            print("3. normal")
            print("4. low")
            
            priority_choice = input("Priority (1-4, default 3): ").strip()
            priority_map = {"1": "urgent", "2": "high", "3": "normal", "4": "low"}
            priority = priority_map.get(priority_choice, "normal")
            
            parcel = self.tracker.add_parcel(weight, destination, sender, recipient, priority)
            print(f"\nParcel registered successfully!")
            print(f"Tracking Number: {parcel.tracking_number}")
            print(f"\nThanks for choosing us!")
            print(f"Your parcel is in good hands and will reach {destination} safely!")
            
        except ValueError:
            print("Invalid input. Please try again.")
            
    def track_parcel_ui(self):
        print("\nTRACK PARCEL")
        print("-"*25)
        
        tracking_number = input("Enter tracking number: ").strip()
        result = self.tracker.track_parcel(tracking_number)
        
        if result:
            parcel = result["parcel"]
            history = result["history"]
            
            print(f"\nParcel Details:")
            print(f"Tracking: {parcel.tracking_number}")
            print(f"Weight: {parcel.weight}kg")
            print(f"To: {parcel.destination}")
            print(f"From: {parcel.sender}")
            print(f"For: {parcel.recipient}")
            print(f"Priority: {parcel.priority}")
            print(f"Status: {parcel.status}")
            print(f"Location: {parcel.location}")
            
            if parcel.delivery_date:
                print(f"Expected Delivery: {parcel.delivery_date.strftime('%Y-%m-%d')}")
            else:
                print("Expected Delivery: Not set")
            
            print(f"\nJourney:")
            for event in history:
                timestamp = event["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
                print(f"  {timestamp}: {event['event']}")
        else:
            print("Parcel not found")
            
    def view_all_parcels_ui(self):
        print(f"\nALL PARCELS ({len(self.tracker.parcels)} total)")
        print("-"*60)
        
        if not self.tracker.parcels:
            print("No parcels in system")
            return
            
        for parcel in self.tracker.parcels:
            print(f"{parcel.tracking_number} | {parcel.weight}kg | {parcel.destination} | {parcel.priority} | {parcel.status} | {parcel.location}")
        
    def run(self):
        print("Welcome to Parcel Tracking System!")
        
        while True:
            self.display_menu()
            choice = input("Choose (1-4): ").strip()
            
            if choice == "1":
                self.add_parcel_ui()
            elif choice == "2":
                self.track_parcel_ui()
                input("\nPress Enter to continue...")
            elif choice == "3":
                self.view_all_parcels_ui()
                input("\nPress Enter to continue...")
            elif choice == "4":
                print("\nThanks for using Parcel Tracking System!")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    app = ParcelApp()
    app.run()
