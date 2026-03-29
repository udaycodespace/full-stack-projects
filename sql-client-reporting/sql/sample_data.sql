-- Seed data for reporting and validation

INSERT INTO customers (name, email, status, created_at) VALUES
('Acme Corporation', 'ops@acme.com', 'active', '2023-01-05T12:00:00Z'),
('Borealis Ventures', 'info@borealis.ventures', 'active', '2023-04-16T08:30:00Z'),
('Canyon Retail', 'hello@canyonretail.com', 'dormant', '2022-09-22T16:45:00Z'),
('Delta Logistics', 'finance@deltalogistics.com', 'churned', '2021-07-01T09:15:00Z');

INSERT INTO orders (customer_id, order_date, amount, status, created_at) VALUES
(1, '2024-01-10', 12500.00, 'completed', '2024-01-10T11:00:00Z'),
(1, '2024-01-25', 7500.50, 'completed', '2024-01-25T17:20:00Z'),
(2, '2024-01-12', 0.00, 'completed', '2024-01-12T14:00:00Z'), -- zero-dollar order stays for validation
(2, '2024-02-05', -150.00, 'completed', '2024-02-05T10:10:00Z'), -- negative order for validation
(2, '2024-02-14', 3890.75, 'failed', '2024-02-14T09:42:00Z'),
(3, '2024-01-30', 4500.00, 'completed', '2024-01-30T13:55:00Z'),
(3, '2024-03-08', 1200.00, 'pending', '2024-03-08T08:27:00Z'),
(4, '2024-02-17', 8200.00, 'completed', '2024-02-17T18:05:00Z');

INSERT INTO payments (order_id, payment_date, gateway, amount, success, failure_code, created_at) VALUES
(1, '2024-01-11', 'stripe', 12500.00, TRUE, NULL, '2024-01-11T09:00:00Z'),
(2, '2024-01-26', 'stripe', 7500.50, TRUE, NULL, '2024-01-26T12:00:00Z'),
(3, '2024-01-13', 'paypal', 0.00, TRUE, NULL, '2024-01-13T15:40:00Z'),
(4, '2024-02-06', 'stripe', -150.00, TRUE, NULL, '2024-02-06T09:05:00Z'), -- matching negative order
(5, '2024-02-15', 'paypal', 3890.75, FALSE, 'CARD_DECLINED', '2024-02-15T14:18:00Z'),
(6, '2024-01-31', 'stripe', 4500.00, TRUE, NULL, '2024-01-31T11:11:00Z'),
(7, '2024-03-09', 'ach', 1200.00, FALSE, 'NETWORK_ERROR', '2024-03-09T10:44:00Z'),
(8, '2024-02-18', 'stripe', 8200.00, TRUE, NULL, '2024-02-18T16:02:00Z');
