-- Sample data for testing the Financial Advisor application
-- Run this after schema.sql to populate the database with test data

-- Insert sample customers
INSERT IGNORE INTO customers (id, name, email, phone, date_of_birth) VALUES
(1, 'Alice Johnson', 'alice.johnson@email.com', '555-0101', '1985-03-15'),
(2, 'Bob Smith', 'bob.smith@email.com', '555-0102', '1990-07-22'),
(3, 'Carol Davis', 'carol.davis@email.com', '555-0103', '1988-11-08');

-- Insert sample transactions for Alice (customer_id = 1)
INSERT IGNORE INTO transactions (customer_id, amount, category, subcategory, description, transaction_date, transaction_type, payment_method) VALUES
-- Income (recent months for trend analysis)
(1, 5000.00, 'Salary', NULL, 'Monthly salary', '2025-03-01', 'income', 'Direct Deposit'),
(1, 5000.00, 'Salary', NULL, 'Monthly salary', '2025-04-01', 'income', 'Direct Deposit'),
(1, 5000.00, 'Salary', NULL, 'Monthly salary', '2025-05-01', 'income', 'Direct Deposit'),
(1, 5000.00, 'Salary', NULL, 'Monthly salary', '2025-06-01', 'income', 'Direct Deposit'),
(1, 5000.00, 'Salary', NULL, 'Monthly salary', '2025-07-01', 'income', 'Direct Deposit'),
(1, 5000.00, 'Salary', NULL, 'Monthly salary', '2025-08-01', 'income', 'Direct Deposit'),

-- Housing expenses (recent months)
(1, 1800.00, 'Housing', 'Rent', 'Monthly rent payment', '2025-03-01', 'expense', 'Bank Transfer'),
(1, 1800.00, 'Housing', 'Rent', 'Monthly rent payment', '2025-04-01', 'expense', 'Bank Transfer'),
(1, 1800.00, 'Housing', 'Rent', 'Monthly rent payment', '2025-05-01', 'expense', 'Bank Transfer'),
(1, 1800.00, 'Housing', 'Rent', 'Monthly rent payment', '2025-06-01', 'expense', 'Bank Transfer'),
(1, 1800.00, 'Housing', 'Rent', 'Monthly rent payment', '2025-07-01', 'expense', 'Bank Transfer'),
(1, 1800.00, 'Housing', 'Rent', 'Monthly rent payment', '2025-08-01', 'expense', 'Bank Transfer'),

-- Utilities (recent months)
(1, 150.00, 'Housing', 'Utilities', 'Electric bill', '2025-03-05', 'expense', 'Credit Card'),
(1, 180.00, 'Housing', 'Utilities', 'Electric bill', '2025-04-05', 'expense', 'Credit Card'),
(1, 140.00, 'Housing', 'Utilities', 'Electric bill', '2025-05-05', 'expense', 'Credit Card'),
(1, 160.00, 'Housing', 'Utilities', 'Electric bill', '2025-06-05', 'expense', 'Credit Card'),
(1, 170.00, 'Housing', 'Utilities', 'Electric bill', '2025-07-05', 'expense', 'Credit Card'),
(1, 155.00, 'Housing', 'Utilities', 'Electric bill', '2025-08-05', 'expense', 'Credit Card'),

-- Food & Dining (recent months)
(1, 400.00, 'Food & Dining', 'Groceries', 'Weekly grocery shopping', '2025-03-07', 'expense', 'Debit Card'),
(1, 350.00, 'Food & Dining', 'Groceries', 'Weekly grocery shopping', '2025-04-07', 'expense', 'Debit Card'),
(1, 380.00, 'Food & Dining', 'Groceries', 'Weekly grocery shopping', '2025-05-07', 'expense', 'Debit Card'),
(1, 420.00, 'Food & Dining', 'Groceries', 'Weekly grocery shopping', '2025-06-07', 'expense', 'Debit Card'),
(1, 390.00, 'Food & Dining', 'Groceries', 'Weekly grocery shopping', '2025-07-07', 'expense', 'Debit Card'),
(1, 410.00, 'Food & Dining', 'Groceries', 'Weekly grocery shopping', '2025-08-07', 'expense', 'Debit Card'),

-- Transportation (recent months)
(1, 350.00, 'Transportation', 'Car Payment', 'Monthly car payment', '2025-03-01', 'expense', 'Bank Transfer'),
(1, 350.00, 'Transportation', 'Car Payment', 'Monthly car payment', '2025-04-01', 'expense', 'Bank Transfer'),
(1, 350.00, 'Transportation', 'Car Payment', 'Monthly car payment', '2025-05-01', 'expense', 'Bank Transfer'),
(1, 350.00, 'Transportation', 'Car Payment', 'Monthly car payment', '2025-06-01', 'expense', 'Bank Transfer'),
(1, 350.00, 'Transportation', 'Car Payment', 'Monthly car payment', '2025-07-01', 'expense', 'Bank Transfer'),
(1, 350.00, 'Transportation', 'Car Payment', 'Monthly car payment', '2025-08-01', 'expense', 'Bank Transfer'),

-- Entertainment (recent months)
(1, 15.99, 'Entertainment', 'Streaming', 'Netflix subscription', '2025-03-01', 'expense', 'Credit Card'),
(1, 12.99, 'Entertainment', 'Streaming', 'Spotify subscription', '2025-03-01', 'expense', 'Credit Card'),
(1, 25.00, 'Entertainment', 'Movies', 'Movie tickets', '2025-03-12', 'expense', 'Credit Card'),

-- Savings (recent months)
(1, 500.00, 'Savings & Investment', 'Emergency Fund', 'Monthly emergency fund contribution', '2025-03-01', 'expense', 'Bank Transfer'),
(1, 500.00, 'Savings & Investment', 'Emergency Fund', 'Monthly emergency fund contribution', '2025-04-01', 'expense', 'Bank Transfer'),
(1, 500.00, 'Savings & Investment', 'Emergency Fund', 'Monthly emergency fund contribution', '2025-05-01', 'expense', 'Bank Transfer'),
(1, 500.00, 'Savings & Investment', 'Emergency Fund', 'Monthly emergency fund contribution', '2025-06-01', 'expense', 'Bank Transfer'),
(1, 500.00, 'Savings & Investment', 'Emergency Fund', 'Monthly emergency fund contribution', '2025-07-01', 'expense', 'Bank Transfer'),
(1, 500.00, 'Savings & Investment', 'Emergency Fund', 'Monthly emergency fund contribution', '2025-08-01', 'expense', 'Bank Transfer'),

-- Additional income sources (recent months)
(1, 200.00, 'Freelance', 'Consulting', 'Side project income', '2025-03-15', 'income', 'PayPal'),
(1, 300.00, 'Freelance', 'Consulting', 'Side project income', '2025-04-15', 'income', 'PayPal'),
(1, 250.00, 'Freelance', 'Consulting', 'Side project income', '2025-05-15', 'income', 'PayPal'),
(1, 350.00, 'Freelance', 'Consulting', 'Side project income', '2025-06-15', 'income', 'PayPal'),
(1, 275.00, 'Freelance', 'Consulting', 'Side project income', '2025-07-15', 'income', 'PayPal'),
(1, 325.00, 'Freelance', 'Consulting', 'Side project income', '2025-08-15', 'income', 'PayPal');

-- Insert sample financial goals for Alice
INSERT IGNORE INTO financial_goals (id, customer_id, goal_name, goal_type, target_amount, current_amount, target_date, priority, status, description) VALUES
(1, 1, 'Emergency Fund', 'savings', 10000.00, 3000.00, '2024-12-31', 'high', 'active', 'Build emergency fund covering 6 months of expenses'),
(2, 1, 'Vacation to Europe', 'purchase', 5000.00, 800.00, '2024-08-15', 'medium', 'active', 'Save for 2-week European vacation'),
(3, 1, 'New Car Down Payment', 'purchase', 8000.00, 1200.00, '2025-06-01', 'medium', 'active', 'Save for down payment on new car'),
(4, 1, 'Retirement Fund', 'investment', 100000.00, 15000.00, '2030-12-31', 'high', 'active', 'Long-term retirement savings goal');

-- Insert sample transactions for Bob (customer_id = 2)
INSERT IGNORE INTO transactions (customer_id, amount, category, subcategory, description, transaction_date, transaction_type, payment_method) VALUES
-- Income (recent months)
(2, 4200.00, 'Salary', NULL, 'Monthly salary', '2025-03-01', 'income', 'Direct Deposit'),
(2, 4200.00, 'Salary', NULL, 'Monthly salary', '2025-04-01', 'income', 'Direct Deposit'),
(2, 4200.00, 'Salary', NULL, 'Monthly salary', '2025-05-01', 'income', 'Direct Deposit'),
(2, 4200.00, 'Salary', NULL, 'Monthly salary', '2025-06-01', 'income', 'Direct Deposit'),
(2, 4200.00, 'Salary', NULL, 'Monthly salary', '2025-07-01', 'income', 'Direct Deposit'),
(2, 4200.00, 'Salary', NULL, 'Monthly salary', '2025-08-01', 'income', 'Direct Deposit'),
(2, 800.00, 'Freelance', NULL, 'Web design project', '2025-03-15', 'income', 'PayPal'),
(2, 750.00, 'Freelance', NULL, 'Web design project', '2025-04-15', 'income', 'PayPal'),
(2, 900.00, 'Freelance', NULL, 'Web design project', '2025-05-15', 'income', 'PayPal'),

-- Expenses (recent months)
(2, 1200.00, 'Housing', 'Rent', 'Monthly rent payment', '2025-03-01', 'expense', 'Bank Transfer'),
(2, 1200.00, 'Housing', 'Rent', 'Monthly rent payment', '2025-04-01', 'expense', 'Bank Transfer'),
(2, 1200.00, 'Housing', 'Rent', 'Monthly rent payment', '2025-05-01', 'expense', 'Bank Transfer'),
(2, 1200.00, 'Housing', 'Rent', 'Monthly rent payment', '2025-06-01', 'expense', 'Bank Transfer'),
(2, 1200.00, 'Housing', 'Rent', 'Monthly rent payment', '2025-07-01', 'expense', 'Bank Transfer'),
(2, 1200.00, 'Housing', 'Rent', 'Monthly rent payment', '2025-08-01', 'expense', 'Bank Transfer'),
(2, 300.00, 'Food & Dining', 'Groceries', 'Monthly groceries', '2025-03-05', 'expense', 'Debit Card'),
(2, 280.00, 'Food & Dining', 'Groceries', 'Monthly groceries', '2025-04-05', 'expense', 'Debit Card'),
(2, 320.00, 'Food & Dining', 'Groceries', 'Monthly groceries', '2025-05-05', 'expense', 'Debit Card'),
(2, 290.00, 'Food & Dining', 'Groceries', 'Monthly groceries', '2025-06-05', 'expense', 'Debit Card'),
(2, 310.00, 'Food & Dining', 'Groceries', 'Monthly groceries', '2025-07-05', 'expense', 'Debit Card'),
(2, 295.00, 'Food & Dining', 'Groceries', 'Monthly groceries', '2025-08-05', 'expense', 'Debit Card'),
(2, 150.00, 'Transportation', 'Public Transport', 'Monthly transit pass', '2025-03-01', 'expense', 'Debit Card'),
(2, 150.00, 'Transportation', 'Public Transport', 'Monthly transit pass', '2025-04-01', 'expense', 'Debit Card'),
(2, 150.00, 'Transportation', 'Public Transport', 'Monthly transit pass', '2025-05-01', 'expense', 'Debit Card'),
(2, 150.00, 'Transportation', 'Public Transport', 'Monthly transit pass', '2025-06-01', 'expense', 'Debit Card'),
(2, 150.00, 'Transportation', 'Public Transport', 'Monthly transit pass', '2025-07-01', 'expense', 'Debit Card'),
(2, 150.00, 'Transportation', 'Public Transport', 'Monthly transit pass', '2025-08-01', 'expense', 'Debit Card');

-- Insert sample financial goals for Bob
INSERT IGNORE INTO financial_goals (id, customer_id, goal_name, goal_type, target_amount, current_amount, target_date, priority, status, description) VALUES
(5, 2, 'Emergency Fund', 'savings', 8000.00, 1500.00, '2024-10-31', 'high', 'active', 'Build emergency fund covering 4 months of expenses'),
(6, 2, 'Home Down Payment', 'purchase', 50000.00, 8000.00, '2026-12-31', 'high', 'active', 'Save for house down payment');

-- Insert some sample advice history
INSERT IGNORE INTO advice_history (customer_id, agent_name, advice_type, advice_content, confidence_score, metadata) VALUES
(1, 'SpendingAnalyzerAgent', 'spending_analysis', 'Your housing costs represent 36% of your income, which is within the recommended 30-40% range. However, your food spending is higher than average at $1,550/month.', 0.85, '{"housing_ratio": 0.36, "food_spending": 1550, "analysis_date": "2024-01-31"}'),
(1, 'GoalPlannerAgent', 'goal_planning', 'Based on your current savings rate of $500/month, you are on track to reach your emergency fund goal by December 2024. Consider increasing contributions to $600/month to build a buffer.', 0.92, '{"current_rate": 500, "recommended_rate": 600, "goal_completion_estimate": "2024-11-15"}'),
(1, 'AdvisorAgent', 'general_advice', 'Overall financial health is good. Priority recommendations: 1) Reduce dining out expenses by $200/month, 2) Increase emergency fund contributions, 3) Consider increasing retirement contributions when emergency fund is complete.', 0.88, '{"priority_actions": ["reduce_dining", "increase_emergency_fund", "increase_retirement"], "overall_score": 7.5}');

-- Insert sample agent interactions
INSERT IGNORE INTO agent_interactions (session_id, customer_id, from_agent, to_agent, interaction_type, message_content, context_data) VALUES
('session_001', 1, 'SpendingAnalyzerAgent', 'GoalPlannerAgent', 'analysis', 'Spending analysis complete. Customer has stable income but high food expenses. Available for savings: $800/month after recommended optimizations.', '{"available_savings": 800, "optimization_potential": 200, "income_stability": "high"}'),
('session_001', 1, 'GoalPlannerAgent', 'AdvisorAgent', 'collaboration', 'Goal feasibility analysis complete. Emergency fund goal is achievable in 10 months with current savings rate. Vacation goal may need timeline adjustment.', '{"emergency_fund_timeline": "10 months", "vacation_feasibility": "challenging", "recommended_adjustments": ["extend_vacation_timeline", "increase_savings_rate"]}'),
('session_001', 1, 'AdvisorAgent', NULL, 'recommendation', 'Comprehensive advice generated based on spending analysis and goal planning. Recommendations prioritized by impact and feasibility.', '{"recommendations_count": 3, "confidence_level": "high", "next_review_date": "2024-04-01"}');
