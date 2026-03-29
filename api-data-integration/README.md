# API-Based Data Integration Pipeline

## Overview
This repository captures a backend-driven ingestion and validation workflow that centralizes data from public REST APIs into a relational store. The service acts as an internal integration tool, translating API responses into a normalized schema so downstream analytics and automation teams can trust the source of truth.

## Data Flow
1. `api_client` pulls JSON payloads from stable REST endpoints (JSONPlaceholder users and posts) while handling pagination, HTTP failures, and parsing issues.
2. `data_ingestion` transforms the responses into relational records, inserts them into PostgreSQL (trackable by the `api_sources`, `users`, and `records` tables), and emits ingestion metrics per source.
3. `data_validation` executes predefined SQL checks via `validation_queries.sql`, surfaces missing relationships or dirty data, and logs the results through pandas before handoffs.

## Tech Stack
- Python 3.11+ standard library plus `requests`, `psycopg2`, and `pandas`
- PostgreSQL for relational persistence
- Plain SQL scripts for schema definition and validation rules
- Environment-variable driven config for credentials and host information

## Running Locally
1. Provision a PostgreSQL instance and set the required env vars: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.
2. Apply `sql/schema.sql` to create the relational tables before ingestion.
3. Install dependencies (`requests`, `psycopg2`, `pandas`).
4. Execute `python/python/data_ingestion.py` to sync API payloads into the database.
5. Run `python/python/data_validation.py` to verify the integrated data remains clean.

## Validation Approach
All logical checks live in `sql/validation_queries.sql`. The Python runner opens a managed connection, executes each query, and uses pandas to format the resultset counts. It focuses on missing foreign keys, duplicates, null-critical fields, and orphan records so every run can serve as a gate before downstream consumers access the data.

## Example Use Cases
- Synchronizing third-party CRM user metadata with an internal analytics warehouse for reporting audits.
- Daily ingestion of marketing campaign data and validating referential integrity before joins reach BI dashboards.
- Proof-of-concept for integrating loosely coupled REST sources into a transactional, schema-bound backend service.
