#!/usr/bin/env python3
"""
Script to create database tables on Render deployment
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Import your app and database
    from app import create_app
    from app.models import db

    app=create_app()
    
    # Create application context
    with app.app_context():
        print("Creating database tables...")
        
        # Create all tables
        db.create_all()
        
        print("Database tables created successfully!")
        
        # Optional: Print table names to verify
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"Tables created: {tables}")
        
except Exception as e:
    print(f"Error creating tables: {e}")
    sys.exit(1)