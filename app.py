from db_utils import SQLite


class App:
    def __init__(self):
        self.db = SQLite("cv_sent_db.db")
        self.is_running = False
        self.commands = {
            "1": "add offer to db (position, company name, date)",
            "2": "update status (status, company name)",
            "3": "show all offers",
            "4": "count offers",
            "5": "delete offer (position, company name)",
            "6": "stop app"
        }

    def start(self):
        self.is_running = True
        while self.is_running == True:
            print("--------")
            for key, value in self.commands.items():
                print(f"{key}: {value}")
            print("--------")
            try:
                command_input = input("TYPE: ")
                if command_input == "1":
                    position = input("Position: ")
                    company_name = input("Company name: ")
                    date = input("Date (dd, mm, yyyy): ")
                    self.db.insert_to_db(position, company_name, date)
                    print("Offer added successfully")
                elif command_input == "2":
                    status = input("Status: ")
                    offer_id = input("Company name: ")
                    int_offer_id = int(offer_id)
                    self.db.update_status(status, int_offer_id)
                    print("Status updated successfully")
                elif command_input == "3":
                    all_offers = self.db.show_all_offers()
                    print("--------")
                    for offer in all_offers:
                        print(f"ID: {offer[0]}, POSITION: {offer[1]}, COMPANY NAME: {offer[2]}, DATE: {offer[3]}, STATUS: {offer[4]}")
                    print("--------")
                elif command_input == "4":
                    number_of_offers = self.db.show_all_offers()
                    print(number_of_offers)
                elif command_input == "5":
                    offer_id = input("Which offer do you want to delete ?: ")
                    int_offer_id = int(offer_id)
                    self.db.delete_offer(int_offer_id)
                    print("Offer deleted successfully")
                elif command_input == "6":
                    print("Bye !")
                    self.is_running = False
                else:
                    print("Unknown command")
            except Exception as e:
                print(e)

app = App()
app.start()
