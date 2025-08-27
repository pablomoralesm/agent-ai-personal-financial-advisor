-- Financial Advisor Database Schema

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Transactions table
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    transaction_date DATE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

-- Financial Goals table
CREATE TABLE IF NOT EXISTS goals (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    goal_type VARCHAR(50) NOT NULL,
    target_amount DECIMAL(10, 2) NOT NULL,
    current_amount DECIMAL(10, 2) DEFAULT 0.00,
    target_date DATE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

-- Advice History table
CREATE TABLE IF NOT EXISTS advice_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    agent_name VARCHAR(50) NOT NULL,
    advice_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX idx_transactions_customer ON transactions(customer_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_goals_customer ON goals(customer_id);
CREATE INDEX idx_advice_customer ON advice_history(customer_id);

-- Sample data for testing (optional - comment out for production)
INSERT INTO customers (name, email) VALUES 
('John Doe', 'john@example.com'),
('Jane Smith', 'jane@example.com');

INSERT INTO transactions (customer_id, amount, category, transaction_date, description) VALUES
(1, 120.50, 'Groceries', '2025-08-01', 'Weekly shopping'),
(1, 45.00, 'Dining', '2025-08-02', 'Restaurant dinner'),
(1, 1200.00, 'Rent', '2025-08-03', 'Monthly rent payment'),
(1, 60.00, 'Entertainment', '2025-08-05', 'Movie tickets'),
(1, 35.75, 'Transportation', '2025-08-06', 'Fuel'),
(2, 89.99, 'Shopping', '2025-08-01', 'New clothes'),
(2, 1500.00, 'Rent', '2025-08-02', 'Monthly rent payment'),
(2, 42.30, 'Groceries', '2025-08-04', 'Food shopping'),
(2, 120.00, 'Utilities', '2025-08-05', 'Electricity bill');

INSERT INTO goals (customer_id, goal_type, target_amount, current_amount, target_date, description) VALUES
(1, 'Emergency Fund', 5000.00, 2000.00, '2025-12-31', 'Build emergency fund'),
(1, 'Vacation', 3000.00, 500.00, '2026-06-30', 'Summer vacation'),
(2, 'Down Payment', 20000.00, 5000.00, '2027-01-31', 'House down payment'),
(2, 'New Car', 15000.00, 3000.00, '2026-03-31', 'Purchase new car');
