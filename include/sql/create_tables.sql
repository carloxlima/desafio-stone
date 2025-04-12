CREATE TABLE IF NOT EXISTS process_log (
	id SERIAL PRIMARY key,
    file_name VARCHAR(255) NOT NULL,
    process_status VARCHAR(50) NOT NULL,
    process_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_hash VARCHAR(255),
    error_message TEXT,
    processed BOOLEAN DEFAULT FALSE
    UNIQUE (file_name)
);

CREATE TABLE IF NOT EXISTS evidence_log (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(100) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    process_status VARCHAR(50) NOT NULL,  
    process_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT,
    processed BOOLEAN DEFAULT FALSE,
    UNIQUE (order_number)  
);
