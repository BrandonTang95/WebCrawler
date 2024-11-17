
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re


class FacultyParser:
    def __init__(self, db_name, source_collection, target_collection):
        self.mongo_client = MongoClient("mongodb://localhost:27017/")
        self.db = self.mongo_client[db_name]
        self.source_collection = self.db[source_collection]
        self.target_collection = self.db[target_collection]



    def get_permanent_faculty_page(self):
        # Locate the Permanent Faculty page HTML from the source collection
        faculty_page = self.source_collection.find_one({"url": {"$regex": "permanent-faculty"}})
        if not faculty_page:
            print("Permanent Faculty page not found in database!")
            return None
        return faculty_page["html"]



    def clean_value(self, value):
        """Clean extracted values to remove unwanted characters."""
        return value.lstrip(":").strip() if value else None



    def clean_phone(self, phone):
        """Sanitize phone numbers by removing invalid characters."""
        if phone:
            # Remove unexpected characters like extra colons, spaces, or non-digit content
            phone = re.sub(r"[^0-9\-\(\)\s]", "", phone).strip()
            return phone if phone else None
        return None



    def parse_faculty_data(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        faculty_data = []

        # Find all div elements with the class "clearfix"
        faculty_divs = soup.find_all("div", class_="clearfix")
        print(f"Found {len(faculty_divs)} faculty entries.")

        for div in faculty_divs:
            try:
                # Extract the name
                name_tag = div.find("h2")
                name = name_tag.text.strip() if name_tag else None
                if not name:
                    print(f"Skipping entry: Missing name in div: {div}")
                    continue

                print(f"Extracted Name: {name}")

                # Extract other details
                details = div.find("p")
                title, office, phone, email, website = None, None, None, None, None

                if details:
                    for line in details.children:
                        if line.name == "strong":
                            label = line.text.strip(":").strip().lower()
                            value = line.next_sibling.strip() if line.next_sibling else None

                            if "title" in label:
                                title = self.clean_value(value)
                            elif "office" in label:
                                office = self.clean_value(value)
                            elif "phone" in label:
                                phone = self.clean_phone(value)
                            elif "email" in label:
                                email_tag = line.find_next("a", href=lambda x: x and "mailto:" in x)
                                email = self.clean_value(email_tag["href"].replace("mailto:", "")) if email_tag else None
                            elif "web" in label:
                                website_tag = line.find_next("a", href=lambda x: x and "http" in x)
                                website = self.clean_value(website_tag["href"]) if website_tag else None
                            else:
                                print(f"Unrecognized label: {label}")

                    # Print debug statements for extracted fields
                    print(f"Extracted Details - Title: {title}, Office: {office}, Phone: {phone}, Email: {email}, Website: {website}")

                # Handle missing data with warnings
                if not title:
                    print(f"Warning: Missing title for faculty: {name}")
                if not email:
                    print(f"Warning: Missing email for faculty: {name}")
                if not website:
                    print(f"Warning: Missing website for faculty: {name}")

                # Create faculty entry
                faculty_entry = {
                    "name": name,
                    "title": title if title else "Unknown Title",
                    "office": office if office else "Unknown Office",
                    "phone": phone if phone else "Unknown Phone",
                    "email": email if email else "No Email Provided",
                    "website": website if website else "No Website Provided",
                }
                faculty_data.append(faculty_entry)
                print(f"Appended data: {faculty_entry}")

            except Exception as e:
                print(f"Error parsing faculty data: {e}")
                continue

        print(f"Total faculty entries extracted: {len(faculty_data)}")
        return faculty_data



    def store_professors_data(self, faculty_data):
        if not faculty_data:
            print("No faculty data to store!")
            return

        # Clear the target collection
        self.target_collection.delete_many({})
        self.target_collection.insert_many(faculty_data)
        print(f"Stored {len(faculty_data)} faculty members in the database.")



    def run(self):
        print("Retrieving Permanent Faculty page...")
        html = self.get_permanent_faculty_page()
        if not html:
            return

        print("Parsing faculty data...")
        faculty_data = self.parse_faculty_data(html)

        print(f"Faculty data extracted: {faculty_data}")

        print("Storing faculty data in MongoDB...")
        self.store_professors_data(faculty_data)



if __name__ == "__main__":
    DB_NAME = "webcrawler"
    SOURCE_COLLECTION = "pages"
    TARGET_COLLECTION = "professors"

    parser = FacultyParser(DB_NAME, SOURCE_COLLECTION, TARGET_COLLECTION)
    parser.run()
