# Importing necessary packages
import os
import json
import matplotlib.pyplot as plt
from requests import get
import sys

# Color printing functions
def prCyan(skk): print("\033[96m {}\033[00m".format(skk))
def prYellow(skk): print("\033[93m {}\033[00m".format(skk))
def prGreen(skk): print("\033[92m {}\033[00m".format(skk))
def prRed(skk): print("\033[91m {}\033[00m".format(skk))

# Global Data Store
ip_store = []

# Function to fetch IP details using "http://ip-api.com/json/"
def fetch_ip_details(ip=None):
    """Fetch details for a specific IP or the user's IP."""
    url = f"http://ip-api.com/json/{ip}" if ip else "http://ip-api.com/json/"
    try:
        response = get(url)
        response.raise_for_status()
        data = response.json()
        if data["status"] != "success":
            prRed(f"Error fetching details: {data.get('message', 'Unknown Error')}")
            return None
        return {
            "ip": data.get("query", "N/A"),
            "city": data.get("city", "N/A"),
            "region": data.get("regionName", "N/A"),
            "country": data.get("country", "N/A"),
            "latitude": data.get("lat", "N/A"),
            "longitude": data.get("lon", "N/A"),
            "isp": data.get("isp", "N/A"),
            "timezone": data.get("timezone", "N/A"),
        }
    except Exception as e:
        prRed(f"Error: {e}")
        return None

# Function to store IP details
def store_ip_data(data):
    """Add IP details to the global store."""
    ip_store.append(data)
    prGreen(f"Stored IP data successfully: {data['ip']}")

# Function to delete IP details
def delete_ip_data(ip):
    """Delete IP data from the store."""
    global ip_store
    for entry in ip_store:
        if entry["ip"] == ip:
            ip_store.remove(entry)
            prRed(f"Deleted data for IP: {ip}")
            return
    prRed(f"No data found for IP: {ip}")

# Function to update IP details
def update_ip_data(ip, field, new_value):
    """Update a specific field for a stored IP."""
    for entry in ip_store:
        if entry["ip"] == ip:
            if field in entry:
                entry[field] = new_value
                prGreen(f"Updated {field} for IP {ip} to {new_value}")
                return
            else:
                prRed(f"Invalid field: {field}")
                return
    prRed(f"No data found for IP: {ip}")

# Function to arrange data
def arrange_ip_data(by_field):
    """Sort the IP store by a specific field."""
    global ip_store
    try:
        ip_store.sort(key=lambda x: x.get(by_field, ""))
        prGreen(f"Data arranged by {by_field}")
    except Exception as e:
        prRed(f"Error while arranging data: {e}")

# Function to display data graphically
def display_graphical_data():
    """Display stored IP data graphically."""
    if not ip_store:
        prRed("No data available for graphical representation.")
        return
    labels = [entry['ip'] for entry in ip_store]
    countries = [entry['country'] for entry in ip_store]
    plt.figure(figsize=(10, 5))
    plt.bar(labels, countries, color='skyblue')
    plt.xlabel("IP Addresses")
    plt.ylabel("Countries")
    plt.title("IP Addresses and their Countries")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

# Function to save data to a file
def save_stored_data(filename="ip_data.json"):
    """Save stored data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(ip_store, file, indent=4)
    prGreen(f"Data successfully saved to {filename}.")

# Function to load data from a file
def load_stored_data(filename="ip_data.json"):
    """Load stored data from a JSON file."""
    global ip_store
    if os.path.exists(filename):
        with open(filename, "r") as file:
            ip_store = json.load(file)
        prGreen(f"Data successfully loaded from {filename}.")
    else:
        prRed(f"No stored data found in {filename}.")

# Main menu
def main():
    """Main function to interact with the user."""
    while True:
        prCyan("\n========== IP Tracker ==========")
        prGreen("1. Fetch IP Details")
        prGreen("2. Store IP Details")
        prGreen("3. Delete IP Details")
        prGreen("4. Update IP Details")
        prGreen("5. Arrange Data")
        prGreen("6. Show Data in Graphic Format")
        prGreen("7. Save Data to File")
        prGreen("8. Load Data from File")
        prGreen("9. Exit")
        
        option = input("\nSelect an option: ").strip()
        
        if option == "1":
            ip = input("Enter IP (leave blank for your IP): ").strip()
            details = fetch_ip_details(ip)
            if details:
                prYellow(details)
        
        elif option == "2":
            ip = input("Enter IP (leave blank for your IP): ").strip()
            details = fetch_ip_details(ip)
            if details:
                store_ip_data(details)
        
        elif option == "3":
            ip = input("Enter IP to delete: ").strip()
            delete_ip_data(ip)
        
        elif option == "4":
            ip = input("Enter IP to update: ").strip()
            field = input("Enter field to update (e.g., city, region): ").strip()
            value = input("Enter new value: ").strip()
            update_ip_data(ip, field, value)
        
        elif option == "5":
            field = input("Enter field to arrange by (e.g., city, country): ").strip()
            arrange_ip_data(field)
        
        elif option == "6":
            display_graphical_data()
        
        elif option == "7":
            save_stored_data()
        
        elif option == "8":
            load_stored_data()
        
        elif option == "9":
            prRed("Exiting... Thank you!")
            break
        
        else:
            prRed("Invalid option. Please try again.")

# Run the program
if __name__ == "__main__":
    main()
