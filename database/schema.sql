-- Financial Advisor Database Schema
-- This schema supports the Agentic AI Personal Financial Advisor application

-- Create database (run this manually if needed)
-- CREATE DATABASE financial_advisor;
-- USE financial_advisor;

-- Table for customer profiles
CREATE TABLE IF NOT EXISTS customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(50),
    date_of_birth DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table for financial transactions
CREATE TABLE IF NOT EXISTS transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    amount DECIMAL(12,2) NOT NULL,
    category VARCHAR(100) NOT NULL,
    subcategory VARCHAR(100),
    description TEXT,
    transaction_date DATE NOT NULL,
    transaction_type ENUM('income', 'expense') NOT NULL,
    payment_method VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    INDEX idx_customer_date (customer_id, transaction_date),
    INDEX idx_category (category),
    INDEX idx_type (transaction_type)
);

-- Table for financial goals
CREATE TABLE IF NOT EXISTS financial_goals (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    goal_name VARCHAR(255) NOT NULL,
    goal_type VARCHAR(100) NOT NULL, -- 'savings', 'investment', 'debt_payoff', 'purchase'
    target_amount DECIMAL(12,2) NOT NULL,
    current_amount DECIMAL(12,2) DEFAULT 0.00,
    target_date DATE,
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
    status ENUM('active', 'completed', 'paused', 'cancelled') DEFAULT 'active',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    INDEX idx_customer_status (customer_id, status),
    INDEX idx_priority (priority),
    INDEX idx_target_date (target_date)
);

-- Table for storing advice history from agents
CREATE TABLE IF NOT EXISTS advice_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    agent_name VARCHAR(100) NOT NULL,
    advice_type VARCHAR(100) NOT NULL, -- 'spending_analysis', 'goal_planning', 'general_advice'
    advice_content TEXT NOT NULL,
    confidence_score DECIMAL(3,2), -- 0.00 to 1.00
    metadata JSON, -- Additional structured data from agents
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    INDEX idx_customer_type (customer_id, advice_type),
    INDEX idx_agent (agent_name),
    INDEX idx_created_at (created_at)
);

-- Table for tracking agent interactions and collaboration
CREATE TABLE IF NOT EXISTS agent_interactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    session_id VARCHAR(255) NOT NULL,
    customer_id INT,
    from_agent VARCHAR(100) NOT NULL,
    to_agent VARCHAR(100),
    interaction_type VARCHAR(50) NOT NULL, -- 'analysis', 'collaboration', 'recommendation'
    message_content TEXT NOT NULL,
    context_data JSON, -- Session state and context information
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    INDEX idx_session (session_id),
    INDEX idx_customer (customer_id),
    INDEX idx_agents (from_agent, to_agent),
    INDEX idx_created_at (created_at)
);

-- Table for spending categories (predefined and custom)
CREATE TABLE IF NOT EXISTS spending_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    parent_category VARCHAR(100),
    description TEXT,
    is_income BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default spending categories
INSERT IGNORE INTO spending_categories (category_name, parent_category, description, is_income) VALUES
-- Income categories
('Salary', NULL, 'Regular salary and wages', TRUE),
('Freelance', NULL, 'Freelance and contract work', TRUE),
('Investment Income', NULL, 'Dividends, interest, capital gains', TRUE),
('Other Income', NULL, 'Other sources of income', TRUE),

-- Expense categories
('Housing', NULL, 'Rent, mortgage, utilities, maintenance', FALSE),
('Transportation', NULL, 'Car payments, gas, public transport', FALSE),
('Food & Dining', NULL, 'Groceries, restaurants, takeout', FALSE),
('Healthcare', NULL, 'Medical, dental, insurance', FALSE),
('Entertainment', NULL, 'Movies, games, subscriptions', FALSE),
('Shopping', NULL, 'Clothing, electronics, personal items', FALSE),
('Education', NULL, 'Tuition, books, courses', FALSE),
('Savings & Investment', NULL, 'Retirement, emergency fund, investments', FALSE),
('Debt Payments', NULL, 'Credit cards, loans, other debt', FALSE),
('Insurance', NULL, 'Life, auto, home insurance', FALSE),
('Taxes', NULL, 'Income tax, property tax', FALSE),
('Other Expenses', NULL, 'Miscellaneous expenses', FALSE);

-- Create indexes for better performance
CREATE INDEX idx_categories_active ON spending_categories (is_active);
CREATE INDEX idx_categories_income ON spending_categories (is_income);
