-- Schema for reporting entities

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'dormant', 'churned')),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(customer_id) ON DELETE CASCADE,
    order_date DATE NOT NULL,
    amount DECIMAL(12,2) NOT NULL CHECK (amount >= 0),
    status TEXT NOT NULL CHECK (status IN ('completed', 'pending', 'cancelled', 'failed')),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    payment_date DATE NOT NULL,
    gateway TEXT NOT NULL,
    amount DECIMAL(12,2) NOT NULL CHECK (amount >= 0),
    success BOOLEAN NOT NULL DEFAULT TRUE,
    failure_code TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    CHECK (success OR failure_code IS NOT NULL)
);
