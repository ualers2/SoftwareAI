# Simple check to confirm the database connection is minimally functional
from Modules.ChatKit.postgres_store import Thread
from api import app
with app.app_context():
    Thread.query.count() 
print("Database connection verified: Thread table queried successfully.")
