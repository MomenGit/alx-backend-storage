-- Create users table in the selected database
CREATE TABLE
	IF NOT EXISTS users (
		id INT NOT NULL AUTO_INCREMENT,
		name VARCHAR(255) NOT NULL UNIQUE,
		email VARCHAR(255),
		country ENUM ('US', 'CO', 'TN') NOT NULL,
		PRIMARY KEY (id)
	)