-- 1. Missing records whose user reference disappeared
SELECT r.record_id, r.user_id
FROM records r
LEFT JOIN users u ON r.user_id = u.user_id
WHERE u.user_id IS NULL;

-- 2. Duplicate records by external identifier
SELECT external_id, COUNT(*) AS occurrences
FROM records
GROUP BY external_id
HAVING COUNT(*) > 1;

-- 3. Null-critical fields inside users table
SELECT *
FROM users
WHERE name IS NULL
   OR username IS NULL
   OR email IS NULL;

-- 4. Orphaned users without a matching api_source entry
SELECT u.user_id, u.api_source_id
FROM users u
LEFT JOIN api_sources s ON u.api_source_id = s.id
WHERE s.id IS NULL;
