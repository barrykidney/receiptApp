DROP DATABASE IF EXISTS receipts;
CREATE DATABASE receipts;
USE receipts;

CREATE TABLE [IF NOT EXISTS] receipts(
   receipt_id INT AUTO_INCREMENT PRIMARY KEY,
   store_name varchar(255) DEFAULT "unknown",
   receipt_total DECIMAL DEFAULT 0.0,
   receipt_text varchar(2048) DEFAULT "unknown",
   taxable BOOLEAN DEFAULT FALSE,
   receipt_date DATETIME DEFAULT NULL,
   PRIMARY KEY (receipt_id),
)

CREATE TABLE [IF NOT EXISTS] items(
   item_id INT AUTO_INCREMENT,
   price DECIMAL DEFAULT 0.0,
   receipt_id INT,
   item_category ENUM('unknown') NOT NULL,
   item_subcategory ENUM('unknown') NOT NULL,
   item_description varchar(255) DEFAULT "unknown",
   PRIMARY KEY (item_id),
   FOREIGN KEY (receipt_id) REFERENCES receipts(receipt_id)
)

