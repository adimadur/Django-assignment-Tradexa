import threading
from django.core.management.base import BaseCommand
from core.models import User, Product, Order
from django.db import IntegrityError, transaction


# Given Input data
users_data = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
    {"id": 4, "name": "David", "email": "david@example.com"},
    {"id": 5, "name": "Eve", "email": "eve@example.com"},
    {"id": 6, "name": "Frank", "email": "frank@example.com"},
    {"id": 7, "name": "Grace", "email": "grace@example.com"},
    {"id": 8, "name": "Alice", "email": "alice@example.com"},
    {"id": 9, "name": "Henry", "email": "henry@example.com"},
    {"id": 10, "name": "", "email": "jane@example.com"},
]

products_data = [
    {"id": 1, "name": "Laptop", "price": 1000.00},
    {"id": 2, "name": "Smartphone", "price": 700.00},
    {"id": 3, "name": "Headphones", "price": 150.00},
    {"id": 4, "name": "Monitor", "price": 300.00},
    {"id": 5, "name": "Keyboard", "price": 50.00},
    {"id": 6, "name": "Mouse", "price": 30.00},
    {"id": 7, "name": "Laptop", "price": 1000.00},
    {"id": 8, "name": "Smartwatch", "price": 250.00},
    {"id": 9, "name": "Gaming Chair", "price": 500.00},
    {"id": 10, "name": "Earbuds", "price": -50.00},
]

orders_data = [
    {"id": 1, "user_id": 1, "product_id": 1, "quantity": 2},
    {"id": 2, "user_id": 2, "product_id": 2, "quantity": 1},
    {"id": 3, "user_id": 3, "product_id": 3, "quantity": 5},
    {"id": 4, "user_id": 4, "product_id": 4, "quantity": 1},
    {"id": 5, "user_id": 5, "product_id": 5, "quantity": 3},
    {"id": 6, "user_id": 6, "product_id": 6, "quantity": 4},
    {"id": 7, "user_id": 7, "product_id": 7, "quantity": 2},
    {"id": 8, "user_id": 8, "product_id": 8, "quantity": 0},
    {"id": 9, "user_id": 9, "product_id": 1, "quantity": -1},
    {"id": 10, "user_id": 10, "product_id": 11, "quantity": 2},
]

# Thread-safe print
print_lock = threading.Lock()

def insert_users():
    for u in users_data:
        try:
            if not u['name'].strip() or '@' not in u['email']:
                raise ValueError("Invalid user data")
            with transaction.atomic(using='users'):
                User.objects.using('users').create(**u)
            with print_lock:
                print(f"[User] Inserted: {u}")
        except Exception as e:
            with print_lock:
                print(f"[User] Failed: {u} => {str(e)}")

def insert_products():
    for p in products_data:
        try:
            if p['price'] < 0:
                raise ValueError("Price cannot be negative")
            with transaction.atomic(using='products'):
                Product.objects.using('products').create(**p)
            with print_lock:
                print(f"[Product] Inserted: {p}")
        except Exception as e:
            with print_lock:
                print(f"[Product] Failed: {p} => {str(e)}")

def insert_orders():
    for o in orders_data:
        try:
            if o['quantity'] <= 0:
                raise ValueError("Quantity must be positive")

            # Check user and product exist
            user_exists = User.objects.using('users').filter(id=o['user_id']).exists()
            product_exists = Product.objects.using('products').filter(id=o['product_id']).exists()
            if not user_exists or not product_exists:
                raise ValueError("Invalid user_id or product_id")

            with transaction.atomic(using='orders'):
                Order.objects.using('orders').create(**o)
            with print_lock:
                print(f"[Order] Inserted: {o}")
        except Exception as e:
            with print_lock:
                print(f"[Order] Failed: {o} => {str(e)}")

class Command(BaseCommand):
    help = 'Insert test data into users, products, and orders databases concurrently'

    def handle(self, *args, **kwargs):
        threads = [
            threading.Thread(target=insert_users),
            threading.Thread(target=insert_products),
            threading.Thread(target=insert_orders),
        ]

        print("Starting concurrent insertions...\n")

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        print("\nAll insertions complete.")
