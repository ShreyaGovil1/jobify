from app import app, db

if __name__ == "__main__":
    db.create_all()  # Create tables if not exist
    app.run(debug=True)
