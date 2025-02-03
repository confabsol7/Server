from app import create_app, db
from models import User, ParkingLocation

app = create_app()

with app.app_context():
    # Add users
    users = [
        User(name="Alice Smith", email="alice@example.com", password_hash="hashed_pass", role="car_owner"),
        User(name="Bob Johnson", email="bob@example.com", password_hash="hashed_pass", role="property_manager")
    ]
    db.session.bulk_save_objects(users)

    # Add parking locations
    parking_locations = [
        ParkingLocation(
            manager_id=2, address="456 Elm St", latitude=37.8000, longitude=-122.4000,
            total_spots=100, available_spots=80, hourly_price=10.00
        ),
        ParkingLocation(
            manager_id=2, address="789 Pine St", latitude=37.7600, longitude=-122.4200,
            total_spots=75, available_spots=50, hourly_price=7.50
        )
    ]
    db.session.bulk_save_objects(parking_locations)

    # Commit changes
    db.session.commit()
    print("Database populated!")
