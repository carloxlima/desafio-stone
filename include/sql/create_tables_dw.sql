CREATE TABLE IF NOT EXISTS public.dim_customers (
    customer_sk SERIAL PRIMARY KEY,
    customer_id INT UNIQUE NOT NULL,  -- ID original
    customer_phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS public.dim_addresses (
    address_sk SERIAL PRIMARY KEY,
    customer_id INT,
    city VARCHAR(100),
    country VARCHAR(100),
    country_state VARCHAR(100),
    zip_code VARCHAR(20),
    street_name VARCHAR(255),
    neighborhood VARCHAR(255),
    complement VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS public.dim_cancellation_reasons (
    cancellation_reason_sk SERIAL PRIMARY KEY,
    cancellation_reason_id INT UNIQUE NOT NULL,
    reason VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS public.dim_terminals (
    terminal_sk SERIAL PRIMARY KEY,
    terminal_serial_number VARCHAR(255) UNIQUE,
    terminal_model VARCHAR(100),
    terminal_type VARCHAR(50)
);


CREATE TABLE IF NOT EXISTS public.dim_technicians (
    technician_sk SERIAL PRIMARY KEY,
    technician_email VARCHAR(255) UNIQUE
);


CREATE TABLE IF NOT EXISTS public.fct_orders (
    order_sk SERIAL PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    provider VARCHAR(255),

    technician_sk INT REFERENCES public.dim_technicians(technician_sk),
    customer_sk INT REFERENCES public.dim_customers(customer_sk),
    address_sk INT REFERENCES public.dim_addresses(address_sk),
    terminal_sk INT REFERENCES public.dim_terminals(terminal_sk),
    cancellation_reason_sk INT REFERENCES public.dim_cancellation_reasons(cancellation_reason_sk),

    arrival_date TIMESTAMP,
    deadline_date TIMESTAMP,
    last_modified_date TIMESTAMP
);
