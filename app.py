import os
from flask import Flask
from extensions import db, cors
from routes.auth import auth_routes
from routes.profile import profile_routes
from routes.parking import parking_routes
from routes.bookings import booking_routes
from routes.payments import payment_routes
from routes.reviews import review_routes
from routes.ads import ad_routes
from routes.mycars import mycars_routes
#import googlemaps  # Correct library for Google Places API
from config import Config
from models import User, ParkingLocation, Booking, Payment, Review, Advertisement, mycars

app = Flask(__name__)

def create_app():
    
    # Configure the SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    # Initialize extensions
    # db = SQLAlchemy(app)
    db.init_app(app)
    cors.init_app(app)

    # Initialize Google Maps API client
    #api_key = Config.GOOGLE_API_KEY
    #if not api_key:
    #    raise ValueError("Google API key not found in environment variables.")
    #gmaps_client = googlemaps.Client(key=api_key)  # Google Maps Client

    # Register blueprints
    app.register_blueprint(auth_routes, url_prefix='/auth')
    app.register_blueprint(profile_routes, url_prefix='/profile')
    app.register_blueprint(parking_routes, url_prefix='/parking')
    app.register_blueprint(booking_routes, url_prefix='/bookings')
    app.register_blueprint(payment_routes, url_prefix='/payments')
    app.register_blueprint(review_routes, url_prefix='/reviews')
    app.register_blueprint(ad_routes, url_prefix='/ads')
    app.register_blueprint(mycars_routes, url_prefix='/mycars')

    # Pass the gmaps_client to routes if needed (e.g., dependency injection)
    #app.config['GOOGLE_MAPS_CLIENT'] = gmaps_client
    #db.create_all()
    @app.route('/')
    def home():
        return "Hello, Google App Engine!"
    
    @app.route('/routes')
    def list_routes():
        output = []
        for rule in app.url_map.iter_rules():
            methods = ', '.join(rule.methods)
            output.append(f"{rule.endpoint}: {rule.rule} ({methods})")
        return "<br>".join(output)
    
    return app

app = create_app()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize the database
        print("tables created")
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000   , debug=True)
