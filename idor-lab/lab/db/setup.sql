-- create database
CREATE DATABASE IF NOT EXISTS vuln_platform;

-- set vuln_platform as active database
use vuln_platform;

-- create users table
CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT PRIMARY KEY,
	first_name VARCHAR(255) NOT NULL,
	last_name VARCHAR(255) NOT NULL,
	email VARCHAR(255) NOT NULL,
	password VARCHAR(255) NOT NULL,
	user_hash VARCHAR(255) NOT NULL,
	phone_number VARCHAR(255),
	address VARCHAR(255),
	access_token VARCHAR(255),
	birth_place VARCHAR(255),
	posts_count INT,
	joined_at VARCHAR(255)
);

-- insert test data for proof-of-concept

-- first user
INSERT INTO users (first_name, last_name, email, password, user_hash, phone_number, address, access_token, birth_place, posts_count, joined_at) VALUES ("john", "doe", "johndoe@gmail.com", "b7a875fc1ea228b9061041b7cec4bd3c52ab3ce3", "04b829dd0ac626aba079837753ecd25b3e58b2808d8076926c30d5aaa720ac70", "+00112233445566778899", "super secret street in london", "J0HN_SUP3R_S3CR37_4CC355_70K3N", "london", 1, "2018");
-- second user
INSERT INTO users (first_name, last_name, email, password, user_hash, phone_number, address, access_token, birth_place, posts_count, joined_at) VALUES ("sam", "young", "samyoung@gmail.com", "cbfdac6008f9cab4083784cbd1874f76618d2a97", "eff4869acd4ee1ce2a33ae20306623003f7fd33ae9ae15bb34061485b054cfbc", "+99887766554433221100", "super secret street in new york", "S4M_SUP3R_S3CR37_4CC355_70K3N", "new york", 1, "2019");
-- third user
INSERT INTO users (first_name, last_name, email, password, user_hash, phone_number, address, access_token, birth_place, posts_count, joined_at) VALUES ("pedro", "morata", "pedromorata@gmail.com", "e5e9fa1ba31ecd1ae84f75caaa474f3a663f05f4", "9772119375391c534ebc096afbfa62a20b75d2da8631e4f43a09b91c7a010af7", "+01233210456654789987", "super secret street in madrid", "P3DR0_SUP3R_S3CR37_4CC355_70K3N", "madrid", 1, "2020");