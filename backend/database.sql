CREATE DATABASE IF NOT EXISTS tour_ai_db;
USE tour_ai_db;

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(30),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS admins (
    id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tour_packages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    destination VARCHAR(120) NOT NULL,
    category VARCHAR(50) NOT NULL,
    duration INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description TEXT,
    available_slots INT DEFAULT 10,
    rating DECIMAL(3,2) DEFAULT 4.50,
    image_url VARCHAR(255)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS bookings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    package_id INT NOT NULL,
    travel_date DATE NOT NULL,
    num_people INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'Confirmed',
    booking_status VARCHAR(50) DEFAULT 'Pending',
    payment_status VARCHAR(50) DEFAULT 'Pending',
    payment_deadline DATETIME,
    cancellation_reason TEXT,
    journey_start_date DATE,
    journey_end_date DATE,
    booking_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (package_id) REFERENCES tour_packages(id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'Paid',
    paid_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    package_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT NOT NULL,
    comment TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (package_id) REFERENCES tour_packages(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS ai_predictions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    prediction_label VARCHAR(80) NOT NULL,
    recommended_category VARCHAR(80) NOT NULL,
    confidence DECIMAL(5,4),
    features_json TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS itinerary_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    destination VARCHAR(120) NOT NULL,
    days INT NOT NULL,
    budget DECIMAL(10,2) NOT NULL,
    interests TEXT,
    travel_type VARCHAR(80),
    response_text LONGTEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

INSERT IGNORE INTO tour_packages (title, destination, category, duration, price, description, available_slots, rating, image_url) VALUES
('Goa Adventure Escape', 'Goa', 'Adventure', 4, 9500, 'Coastal rides, water sports, and student-friendly stay options.', 12, 4.7, 'https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=900&q=80'),
('Family Rajasthan Heritage', 'Jaipur', 'Family', 5, 11800, 'A gentle family tour with forts, local food, and comfortable hotels.', 8, 4.8, 'https://images.unsplash.com/photo-1516483638261-f4dbaf036963?auto=format&fit=crop&w=900&q=80'),
('Honeymoon in Kerala', 'Kerala', 'Honeymoon', 4, 14500, 'Backwater cruise, romantic stays, and peaceful natural scenery.', 6, 4.9, 'https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=900&q=80'),
('Budget Himachal Trail', 'Manali', 'Budget', 3, 6400, 'A low-cost travel plan with scenic cafes and mountain views.', 15, 4.4, 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=900&q=80'),
('Luxury Maldives Getaway', 'Maldives', 'Luxury', 5, 26000, 'Premium resort stay with private transfers and luxury dining.', 4, 4.9, 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=900&q=80');
