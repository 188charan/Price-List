import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

# Function to create a MySQL connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="bmgiwu7opiyq7grqp43g-mysql.services.clever-cloud.com",
            user="u9vthbpksygk4fsf",
            password="1xt1TYlaGbyzDkVGDoa4",
            database="bmgiwu7opiyq7grqp43g"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None
    
# Function to create pricelist table
def create_pricelist_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pricelist (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                buy_price INT,
                sell_price INT ,
                location VARCHAR(200)
            )
        """)
        connection.commit()
    except Error as e:
        st.error(f"Error creating login table: {e}")

#add item page 
def additem_page(connection):
    st.title("Welcome to :violet[PAVAN CYCLE STORES]")
    cursor = connection.cursor()
    item_name = st.text_input("Item Name")
    buy_price = st.number_input("Buy Price", min_value=1, step=1)
    selling_price = st.number_input("Selling Price", min_value=1, step=1)
    location = st.text_input("Location")

    if st.button("Add Item"):
        cursor.execute("INSERT INTO pricelist (name, buy_price, sell_price, location) VALUES (%s, %s, %s, %s)", (item_name, buy_price, selling_price, location))
        st.success("Item added successfully!")
    connection.commit()
     
    cursor = connection.cursor()
    st.header("Please enter the id to delete the item")
    id = st.number_input("Enter the id to delete :", step=1)
    if st.button("Delete"):
        cursor.execute("Delete from pricelist where id = %s", (id,))
        connection.commit()
        st.success("Item Deleted successfully!")
    connection.close()
    

def view_page(connection):
    st.header(":violet[Items List by search]")
    name = st.text_input("Enter the name of the item to show details!")
    cursor = connection.cursor()
    query = "SELECT * FROM pricelist WHERE name LIKE %s"
    cursor.execute(query, ('%' + name + '%',))
    items_data = cursor.fetchall()
    if items_data:
            df = pd.DataFrame(items_data, columns=["ID", "Item Name", "Buy Price", "Selling Price", "Description"])
            st.table(df)
    else:
            st.write("No items found.")
    #To display all existing items
    st.title(":violet[Full List]")
    cursor.execute("SELECT * FROM pricelist ORDER BY name")
    items_data = cursor.fetchall()
    connection.close()
    if items_data:
            df = pd.DataFrame(items_data, columns=["ID", "Item Name", "Buy Price", "Selling Price", "Description"])
            st.table(df)
    else:
            st.write("No items found.")

# Main App
def main():
    #page configuration.
    st.set_page_config(page_title='PRICELIST')
    # Create a connection to the MySQL database
    connection = create_connection()
    if connection:
        # Create tables if they don't exist
        create_pricelist_table(connection)

    st.sidebar.title(':rainbow[Pavan Cycle stores]')
    pages = ["Add Item","View list"]
    selection = st.sidebar.radio("Go to", pages)
    if selection == "Add Item":
        additem_page(connection)
    if selection == "View list":
        view_page(connection)
        

if __name__ == "__main__":
    main()
             
