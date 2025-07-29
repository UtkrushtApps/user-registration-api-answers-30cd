# Solution Steps

1. Create a requirements.txt file declaring FastAPI, SQLAlchemy (asyncio), asyncpg, uvicorn, alembic, and any other required dependencies.

2. Write a Dockerfile to install dependencies and run the FastAPI app using uvicorn.

3. Write a docker-compose.yml with two services: api (your app) and db (PostgreSQL), set environment variables, ports, and volumes.

4. Define the SQLAlchemy User model in models.py with unique email constraint (both column-level and UniqueConstraint).

5. Define Pydantic schemas in schemas.py for user creation (input) and reading (output), including validation (email, password length).

6. Set up database connection logic and dependency in db.py with an async engine and session local.

7. Implement FastAPI routes in main.py: /register for user registration (POST) and /users for listing (GET).

8. In the /register endpoint, check for an existing email in the DB before trying to add, returning a 400 error if found (API layer).

9. On user creation, catch database IntegrityError (for unique constraint violations) and return a 400 error (DB layer).

10. On /users, list all users (select), serialize using the output schema without passwords.

11. On startup, ensure database tables are created (auto-migrate).

12. Test end-to-end: registration succeeds for unique emails, fails for duplicates, and users can be listed.

13. Add .dockerignore to ignore non-essential files in your container contexts.

