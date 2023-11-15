import random
import sqlite3

from faker import Faker

connect = sqlite3.connect('data.db')
cursor = connect.cursor()

fake = Faker() #création de la variable Faker


nb_data = 15 #défini nombre de fausses données


for i in range(nb_data): #insertion donnée dans table Utilisateur
        user_id = int

        cursor.execute(
            "INSERT INTO User (UserID, Username, FirstName, LastName, Email, Password) VALUES (?, ?, ?, ?, ?, ?)",
            (i+1, fake.user_name(), fake.first_name(), fake.last_name(), fake.email(), fake.password())
        )

for i in range(nb_data): #insertion donnée dans table addresse
        cursor.execute(
            "INSERT INTO Address (AddressID, UserID, StreetAddress, City, StateProvince, PostalCode, Country) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (i+1, i+1, fake.street_address(), fake.city(), fake.state(), fake.postalcode(), fake.country())
        )

for _ in range(nb_data): #insertion donnée dans table produit
     
          cursor.execute(
              "INSERT INTO Product (ProductName, Description, Price, Category) VALUES (?, ?, ?, ?)",
              (fake.word(ext_word_list=["Product", "Item", "Goods"]), fake.sentence(), round(random.uniform(1, 300), 2), fake.word(ext_word_list=["Electronics", "Cosmetics", "Clothing", "Furniture", "Books", "Shoes", "Cleaning Products", "Beverage", "Food"]))
          )

for user_id in range(1, nb_data + 1): #insertion donnée dans table cart
          product_id = random.randint(1, nb_data)
          quantity = random.randint(1, 5)

          cursor.execute(
              "INSERT INTO Cart (UserID, ProductID, Quantity) VALUES (?, ?, ?)",
             (user_id, product_id, quantity)
          )

for _ in range(nb_data): #insertion donnée dans table command
          user_id = random.randint(1, nb_data)
          order_date = fake.date_time_this_decade(before_now=True, after_now=False)
          shipping_address_id = random.randint(1, nb_data)

          cursor.execute(
              "INSERT INTO Command (UserID, OrderDate, ShippingAddressID) VALUES (?, ?, ?)",
              (user_id, order_date, shipping_address_id)
          )

for _ in range(nb_data): #insertion donnée dans table invoices
                  command_id = random.randint(1, nb_data)
                  invoice_date = fake.date_between(start_date='-365d', end_date='today')
                  total_amount = round(random.uniform(1, 1000), 2)
                  payment_status = fake.random_element(elements=('Paid', 'Unpaid', 'Pending'))

                  insert_query = "INSERT INTO Invoices (CommandID, InvoiceDate, TotalAmount, PaymentStatus) VALUES (?, ?, ?, ?)"
                  data = (command_id, invoice_date, total_amount, payment_status)
                  cursor.execute(insert_query, data)
                
                
def generate_unique_payment_id(): #fonction de créeayion d'identité unique
    payment_id = random.randint(1, nb_data)
    while True:
        cursor.execute("SELECT COUNT(*) FROM Payment WHERE PaymentID = ?", (payment_id,))
        count = cursor.fetchone()[0]
        if count == 0:
            return payment_id
        else:
            payment_id = random.randint(1, nb_data)                
                
# Insert data into the Payment table
for _ in range(nb_data):
    payment_id = generate_unique_payment_id()
    user_id = random.randint(1, nb_data)
    payment_method = fake.credit_card_provider()
    card_number = fake.credit_card_number()
    expiration_date = fake.credit_card_expire()

    insert_query = "INSERT INTO Payment (PaymentID, UserID, PaymentMethod, CardNumber, ExpirationDate) VALUES (?, ?, ?, ?, ?)"
    data = (payment_id, user_id, payment_method, card_number, expiration_date)
    cursor.execute(insert_query, data)

def generate_unique_photo_id(): #fonction de créeayion d'identité unique
    photo_id = random.randint(1, nb_data)
    while True:
        cursor.execute("SELECT COUNT(*) FROM Photo WHERE PhotoID = ?", (photo_id,))
        count = cursor.fetchone()[0]
        if count == 0:
            return photo_id
        else:
            photo_id = random.randint(1, nb_data)

# Insert data into the Photo table
for _ in range(nb_data):
    photo_id = generate_unique_photo_id()
    user_id = random.randint(1, nb_data)
    product_id = random.randint(1, nb_data)
    file_path = fake.file_path(depth=3, category='image', extension='jpg')
    caption = fake.sentence()
    upload_date = fake.date_time_this_decade(before_now=True, after_now=False)

    insert_query = "INSERT INTO Photo (PhotoID, UserID, ProductID, FilePath, Caption, UploadDate) VALUES (?, ?, ?, ?, ?, ?)"
    data = (photo_id, user_id, product_id, file_path, caption, upload_date)
    cursor.execute(insert_query, data)

def generate_unique_rate_id(): #fonction de créeayion d'identité unique
    rate_id = random.randint(1, nb_data)
    while True:
        cursor.execute("SELECT COUNT(*) FROM Rate WHERE RateID = ?", (rate_id,))
        count = cursor.fetchone()[0]
        if count == 0:
            return rate_id
        else:
            rate_id = random.randint(1, nb_data)

# Insert data into the Rate table
for _ in range(nb_data):
    rate_id = generate_unique_rate_id()
    user_id = random.randint(1, nb_data)
    product_id = random.randint(1, nb_data)
    rating_value = random.randint(1, 5)
    review = fake.sentence()
    date = fake.date_time_this_decade(before_now=True, after_now=False)

    insert_query = "INSERT INTO Rate (RateID, UserID, ProductID, RatingValue, Review, Date) VALUES (?, ?, ?, ?, ?, ?)"
    data = (rate_id, user_id, product_id, rating_value, review, date)
    cursor.execute(insert_query, data)                
                
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';") #liste toutes les tables
# table_names = cursor.fetchall()

    
# for table_name in table_names: #parcours toutes les tables & supprime toutes les lignes
#              table_name = table_name[0]  
#              cursor.execute(f"DELETE FROM {table_name};")


connect.commit() #sauvegarde données
connect.close() #fermeture connection de db
