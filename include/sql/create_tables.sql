
CREATE TABLE IF NOT EXISTS public.tb_process_log (
	id SERIAL PRIMARY key,
    file_name VARCHAR(255) UNIQUE NOT NULL,
    process_status VARCHAR(50) NOT NULL,
    process_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT,
    processed BOOLEAN DEFAULT FALSE
 );

CREATE TABLE IF NOT EXISTS public.tb_evidence_log (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(100) UNIQUE NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    process_status VARCHAR(50) NOT NULL,  
    process_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT,
    processed BOOLEAN DEFAULT FALSE   
);

CREATE TABLE IF NOT EXISTS public.tb_cancellation_reasons (
    id SERIAL PRIMARY KEY,
    reason VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS public.tb_orders (
    order_id SERIAL PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    provider VARCHAR(255),
    technician_email VARCHAR(255),
    cancellation_reason_id INT,
    arrival_date TIMESTAMP,
    deadline_date TIMESTAMP,
    last_modified_date TIMESTAMP,
    FOREIGN KEY (cancellation_reason_id) REFERENCES public.tb_cancellation_reasons(id)
);


CREATE TABLE IF NOT EXISTS public.tb_terminals (
    terminal_id SERIAL PRIMARY KEY,
    terminal_serial_number VARCHAR(255) UNIQUE,
    terminal_model VARCHAR(100),
    terminal_type VARCHAR(50)
);


CREATE TABLE IF NOT EXISTS public.tb_customers (
    customer_id SERIAL PRIMARY KEY,
    customer_phone VARCHAR(20)
);


CREATE TABLE IF NOT EXISTS public.tb_addresses (
    address_id SERIAL PRIMARY KEY,
    customer_id INT,
    city VARCHAR(100),
    country VARCHAR(100),
    country_state VARCHAR(100),
    zip_code VARCHAR(20),
    street_name VARCHAR(255),
    neighborhood VARCHAR(255),
    complement VARCHAR(255),
    FOREIGN KEY (customer_id) REFERENCES public.tb_customers(customer_id)
);


