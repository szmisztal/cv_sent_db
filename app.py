from db_utils import SQLite


class App:
    def __init__(self):
        self.db = SQLite("cv_sent_db.db")
        self.is_running = False
        self.commands = {
            "1": "add offer to db (position, company name, date)",
            "2": "update offer",
            "3": "show all offers",
            "4": "show only active or refused offers",
            "5": "count offers",
            "6": "delete offer (position, company name)",
            "7": "search for company in offers",
            "8": "stop app"
        }

    def read_dict(self, dict):
        print("--------")
        for key, value in dict.items():
            print(f"{key}: {value}")
        print("--------")

    def offers_table_template(self, offers):
        print("--------")
        print("ID:\t | \tPOSITION:\t | \tCOMPANY NAME:\t | \tDATE:\t | \tSTATUS:")
        for offer in offers:
            print(f"{offer[0]} | {offer[1]} | {offer[2]} | {offer[3]} | {offer[4]}")

    def add_offer_to_db(self):
        position = input("Position: ")
        company_name = input("Company name: ")
        date = input("Date (yyyy.mm.dd): ")
        self.db.insert_to_db(position, company_name, date)
        print("Offer added successfully")

    def update_offer(self):
        offer_id = input("Which offer do you want to update: ")
        int_offer_id = int(offer_id)
        commands = {
            "1": "Position",
            "2": "Company name",
            "3": "Date",
            "4": "Status"
        }
        self.read_dict(commands)
        option = input("What would you want to update: ")
        if option == "1":
            new_position = input("New position: ")
            self.db.update_offer(int_offer_id, "position", new_position)
            print("Offer updated successfully")
        elif option == "2":
            new_company_name = input("New company name: ")
            self.db.update_offer(int_offer_id, "company_name", new_company_name)
            print("Offer updated successfully")
        elif option == "3":
            new_data = input("New data (yyyy.mm.dd): ")
            self.db.update_offer(int_offer_id, "post_date", new_data)
            print("Offer updated successfully")
        elif option == "4":
            new_status = input("New status: ")
            self.db.update_offer(int_offer_id, "status", new_status)
            print("Offer updated successfully")
        else:
            print("Unknown command")

    def show_all_offers(self):
        commands = {
            "1": "Order by ID",
            "2": "Order by date"
        }
        self.read_dict(commands)
        option = input("How want you to order these offers ?: ")
        if option == "1":
            all_offers = self.db.show_all_offers("offer_id")
        elif option == "2":
            all_offers = self.db.show_all_offers("post_date")
        else:
            print("Unknown command")
        self.offers_table_template(all_offers)

    def show_active_or_refused_offers(self):
        commands = {
            "1": "Only active",
            "2": "Only refused"
        }
        self.read_dict(commands)
        active_or_not_input = input("Which offers want you to see ?: ")
        commands_2 = {
            "1": "Order by ID",
            "2": "Order by date"
        }
        self.read_dict(commands_2)
        order_input = input("How want you to order these offers ?: ")
        if active_or_not_input == "1" and order_input == "1":
            offers = self.db.show_filtered_offers("ACTIVE", "offer_id")
        elif active_or_not_input == "1" and order_input == "2":
            offers = self.db.show_filtered_offers("ACTIVE", "post_date")
        elif active_or_not_input == "2" and order_input == "1":
            offers = self.db.show_filtered_offers("REFUSED", "offer_id")
        elif active_or_not_input == "2" and order_input == "2":
            offers = self.db.show_filtered_offers("REFUSED", "post_date")
        else:
            print("Unknown command")
        self.offers_table_template(offers)

    def count_offers(self):
        number_of_offers = self.db.count_offers()
        print(f"Number of offers: {number_of_offers}")

    def delete_offer(self):
        offer_id = input("Which offer do you want to delete ?: ")
        int_offer_id = int(offer_id)
        self.db.delete_offer(int_offer_id)
        print("Offer deleted successfully")

    def search_for_company(self):
        company_name = input("Type searching company name: ")
        offers = self.db.look_for_a_company(company_name)
        if offers == None:
            print("There`s no offers with this company name")
        else:
            self.offers_table_template(offers)

    def start(self):
        self.is_running = True
        print("Hello !")
        while self.is_running == True:
            self.read_dict(self.commands)
            try:
                command_input = input("TYPE: ")
                if command_input == "1":
                    self.add_offer_to_db()
                elif command_input == "2":
                    self.update_offer()
                elif command_input == "3":
                    self.show_all_offers()
                elif command_input == "4":
                    self.show_active_or_refused_offers()
                elif command_input == "5":
                    self.count_offers()
                elif command_input == "6":
                    self.delete_offer()
                elif command_input == "7":
                    self.search_for_company()
                elif command_input == "8":
                    print("Bye !")
                    self.is_running = False
                else:
                    print("Unknown command")
            except Exception as e:
                print(e)


app = App()
app.start()
