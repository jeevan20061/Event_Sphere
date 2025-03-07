CREATE TABLE events (
    id INT AUTO_INCREMENT PRIMARY KEY,
    evname VARCHAR(255) NOT NULL,
    evdate DATE NOT NULL,
    evloc VARCHAR(255) NOT NULL,
    evwebsite VARCHAR(255) NOT NULL,
    evimage VARCHAR(255) NOT NULL,
    username VARCHAR(100) NOT NULL, -- Foreign key linking to users table
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);
