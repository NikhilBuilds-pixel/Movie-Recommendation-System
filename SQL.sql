CREATE DATABASE IF NOT EXISTS movie_recommendation;
USE movie_recommendation;

CREATE TABLE IF NOT EXISTS movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(100) NOT NULL,
    language VARCHAR(100) NOT NULL,
    rating DECIMAL(3,1) NOT NULL,
    description TEXT
);

INSERT INTO movies (title, genre, language, rating, description) VALUES
('3 Idiots','Comedy','Hindi',9.2,'Comedy drama about engineering students'),
('Dangal','Sports','Hindi',8.8,'Sports biographical movie'),
('Inception','Sci-Fi','English',8.8,'Dream within dreams'),
('Interstellar','Sci-Fi','English',8.7,'Space exploration'),
('Parasite','Thriller','Korean',8.6,'Oscar winning thriller'),
('Train to Busan','Thriller','Korean',8.5,'Zombie survival movie'),
('Your Name','Comedy','Japanese',8.4,'Romantic anime movie'),
('Suzume','Comedy','Japanese',7.9,'Fantasy adventure');