from extensions import db
from datetime import datetime

# Users Table
class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pa_user_id = db.Column(db.String(50))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(15))
    role = db.Column(db.Enum('car_owner', 'property_manager'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    parking_locations = db.relationship('ParkingLocation', backref='manager', lazy=True)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    # def __repr__(self):
    #     return f"<User {self.name}, Role: {self.role}>"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "pa_user_id": self.pa_user_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "role": self.role,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Parking Locations Table
class ParkingLocation(db.Model):
    __tablename__ = 'parking_locations'
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Numeric(10, 8), nullable=False)
    longitude = db.Column(db.Numeric(11, 8), nullable=False)
    total_spots = db.Column(db.Integer, nullable=False)
    available_spots = db.Column(db.Integer, nullable=False)
    hourly_price = db.Column(db.Numeric(10, 2))
    daily_price = db.Column(db.Numeric(10, 2))
    weekly_price = db.Column(db.Numeric(10, 2))
    monthly_price = db.Column(db.Numeric(10, 2))
    zipcode = db.Column(db.Integer, nullable=False)
    category = db.Column(db.Enum('Free', 'Paid'), nullable=False)
    rating = db.Column(db.Numeric(3, 2))

    # Relationships
    bookings = db.relationship('Booking', backref='parking_location', lazy=True)
    reviews = db.relationship('Review', backref='parking_location', lazy=True)

    def to_dict(self):
        return {
            "location_id": self.location_id,
            "manager_id": self.manager_id,
            "address": self.address,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "total_spots": self.total_spots,
            "available_spots": self.available_spots,
            "hourly_price": self.hourly_price,
            "daily_price": self.daily_price,
            "weekly_price": self.weekly_price,
            "monthly_price": self.monthly_price,
            "category": self.category,
            "zipcode": self.zipcode,
            "rating": self.rating
        }

    # def __repr__(self):
    #     return f"<ParkingLocation {self.address}, Manager: {self.manager_id}>"

# Bookings Table
class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.pa_user_id', ondelete='CASCADE'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('parking_locations.location_id', ondelete='CASCADE'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    booking_type = db.Column(db.Enum('hourly', 'daily', 'weekly', 'monthly'), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.Enum('pending', 'paid', 'failed'), default='pending')
    payment_id = db.Column(db.String(255), nullable=True)  # Razorpay/Stripe transaction ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    payment = db.relationship('Payment', backref='booking', lazy=True)

    #def __repr__(self):
    #    return f"<Booking {self.booking_id}, User: {self.user_id}>"
    def to_dict(self):
        return {
            "booking_id": self.booking_id,
            "user_id": self.user_id,
            "location_id": self.location_id,
	    "booking_type":self.booking_type,
            "start_time": self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            "duration": self.duration,
            "total_price": float(self.total_price),
            "payment_status": self.payment_status,
            "payment_id": self.payment_id,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

# Payments Table
class Payment(db.Model):
    __tablename__ = 'payments'
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id', ondelete='CASCADE'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.Enum('credit_card', 'debit_card', 'upi', 'wallet'), nullable=False)
    status = db.Column(db.Enum('success', 'failed', 'pending'), nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Payment {self.payment_id}, Amount: {self.amount}, Status: {self.status}>"

# Reviews Table
class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('parking_locations.location_id', ondelete='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Review {self.review_id}, Rating: {self.rating}>"

# mycars Table
class mycars(db.Model):
    __tablename__ = 'mycars'
    carid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    model = db.Column(db.Text, nullable=False)
    carnumber = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "carid": self.carid,
            "model": self.model,
            "carnumber": self.carnumber,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        
    #def __repr__(self):
    #    return f"<mycars {self.carid}, CarNumber: {self.carnumber}>"
        
# Advertisements Table
class Advertisement(db.Model):
    __tablename__ = 'advertisements'
    ad_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    advertiser_name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    display_start_date = db.Column(db.Date, nullable=False)
    display_end_date = db.Column(db.Date, nullable=False)
    target_audience = db.Column(db.Enum('car_owner', 'property_manager', 'all'), default='all')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Advertisement {self.advertiser_name}, Audience: {self.target_audience}>"


