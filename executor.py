import mysql.connector
import os
import shutil

# Connect to the MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="base_from_gamers_4_gamers"
)
cursor = conn.cursor()

# Disable foreign key checks
cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

# Drop existing tables
tables = [
    "store_product",
    "store_category",
    "store_order",
    "store_orderitem",
    "store_profile",
    "store_profile_favorites"
]

for table in tables:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

# Re-enable foreign key checks
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

# Commit the changes
conn.commit()

# Close the connection
cursor.close()
conn.close()

# Remove migration files
migration_folder = 'D:/Pycharm/from_gamers_4_gamers/store/migrations'
for file in os.listdir(migration_folder):
    file_path = os.path.join(migration_folder, file)
    try:
        if os.path.isfile(file_path) and file != '__init__.py':
            os.remove(file_path)
        elif os.path.isdir(file_path) and file == '__pycache__':
            shutil.rmtree(file_path)
    except Exception as e:
        print(f"Failed to delete {file_path}. Reason: {e}")

# Re-run the migrations
os.system("python manage.py makemigrations store")
os.system("python manage.py migrate")
