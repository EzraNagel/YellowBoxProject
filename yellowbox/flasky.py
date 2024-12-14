from app import db, create_app

app = create_app('config.Config')


if __name__ == "__main__":
    with app.app_context():
        try:
            db.create_all()
            print("Database tables created successfully.")
        except Exception as e:
            print(f"Error creating database tables: {e}")
    app.run(host='0.0.0.0', port=5000)
