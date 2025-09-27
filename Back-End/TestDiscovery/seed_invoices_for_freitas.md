docker exec -i meu_postgres2 psql -U postgres -d meubanco <<'SQL'
-- seed_invoices_for_freitas.sql
BEGIN;

-- 1) garante que o usuário exista (insere se não existir) e retorna id em CTE
WITH upsert_user AS (
  INSERT INTO users (email, username, password_hash, created_at, plan_name, limit_monthly_tokens, tokens_used, acess_token, expires_at)
  VALUES (
    'freitasalexandre815@gmail.com',
    'freitasalexandre',
    '<bcrypt-placeholder>',
    NOW(),
    'Pro',
    1000000,
    1234,
    'testtoken-inv-5000',
    NOW() + INTERVAL '30 days'
  )
  ON CONFLICT (email) DO UPDATE
    SET username = EXCLUDED.username
  RETURNING id
), uid AS (
  SELECT id FROM upsert_user
  UNION ALL
  SELECT id FROM users WHERE email = 'freitasalexandre815@gmail.com' LIMIT 1
)

-- 2) Insere 3 faturas somente se não existirem com o mesmo número para esse usuário
INSERT INTO invoices (user_id, number, date, amount, currency, status, plan_name, pdf_path, pdf_url, lines, created_at, updated_at)
SELECT uid.id, v.number, v.date, v.amount, v.currency, v.status, v.plan_name, v.pdf_path, v.pdf_url, v.lines, v.created_at, v.updated_at
FROM uid
CROSS JOIN (
  VALUES
    ('INV-2025-0001', NOW() - INTERVAL '10 days', 49.90, 'BRL', 'paid', 'Pro', 'invoice-2025-0001.pdf', NULL, '[{"description":"Assinatura mensal Pro","qty":1,"price":49.90}]', NOW() - INTERVAL '10 days', NOW() - INTERVAL '10 days'),
    ('INV-2025-0002', NOW() - INTERVAL '5 days', 49.90, 'BRL', 'pending', 'Pro', NULL, NULL, '[{"description":"Renovação pendente - Pro","qty":1,"price":49.90}]', NOW() - INTERVAL '5 days', NOW() - INTERVAL '5 days'),
    ('INV-2025-0003', NOW() - INTERVAL '30 days', 249.00, 'BRL', 'paid', 'Business', NULL, 'https://example-bucket.s3.amazonaws.com/invoice-2025-0003.pdf', '[{"description":"Assinatura anual Business","qty":1,"price":249.00}]', NOW() - INTERVAL '30 days', NOW() - INTERVAL '30 days')
) AS v(number, date, amount, currency, status, plan_name, pdf_path, pdf_url, lines, created_at, updated_at)
WHERE NOT EXISTS (
  SELECT 1 FROM invoices i WHERE i.number = v.number AND i.user_id = uid.id
);

-- 3) Ajusta sequences
SELECT setval(pg_get_serial_sequence('users','id'), (SELECT COALESCE(MAX(id),1) FROM users));
SELECT setval(pg_get_serial_sequence('invoices','id'), (SELECT COALESCE(MAX(id),1) FROM invoices));

COMMIT;
SQL
