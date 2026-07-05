# PostgreSQL Docker Setup for TodoApplicationServer

This project uses **PostgreSQL 15** with Docker for a containerized database that can be rebuilt and relaunched anytime.

> **Requirements:** Docker Engine v20.10+ or Docker Desktop v4.0+
>
> **Note on Commands:** All examples use `docker compose` (the modern Docker CLI subcommand). If you're using an older Docker installation with the standalone `docker-compose` CLI, simply replace `docker compose` with `docker-compose` in all commands below.

## Quick Start

### 1. Build and Start the Database

```bash
docker compose up -d
```

This command will:
- Pull the PostgreSQL 15 Alpine image
- Create a container named `todoapp-postgres`
- Initialize the database with the schema and seed data from `docker/init.sql`
- Mount a named volume `postgres_data` for data persistence

> **Note:** Use `docker compose` (Docker v20.10+). If using an older Docker version, replace with `docker compose`.

> **⚠️ Important:** `docker/init.sql` only runs the **first** time the container is created against an **empty** `postgres_data` volume. If the container already exists (e.g. you've run `docker compose up -d` before), re-running it will **not** re-seed the database, even after editing `init.sql`. See [Checking and Re-Seeding an Existing Database](#checking-and-re-seeding-an-existing-database) below.

### 2. Verify the Database is Running

```bash
docker compose ps
```

You should see the `todoapp-postgres` service running.

### 3. Connect with PyCharm

In **PyCharm Premium**:

1. Go to **Database** → **Data Sources** → **+** → **PostgreSQL**
2. Fill in the connection details:
   - **Host:** `localhost`
   - **Port:** `5432` (default, or check your `.env`)
   - **Database:** `TodoApplicationServer`
   - **User:** `postgres`
   - **Password:** `postgres`
3. Click **Download missing drivers** if prompted
4. Click **Test Connection** to verify
5. Click **OK** to save

### 4. Install Dependencies

```bash
pip install -e .
# or
uv sync
```

This installs `python-dotenv` and other PostgreSQL-related packages.

### 5. Run the Application

```bash
uvicorn TodoApp.main:app --reload
```

The app will connect to the Docker PostgreSQL database using the `.env` configuration.

---

## Environment Variables

The `.env` file contains default database configuration:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=TodoApplicationServer
DB_PORT=5432
DB_HOST=localhost
DEBUG=True
```

**Customize as needed**, but for local development these defaults work out of the box.

---

## Database Schema

### Tables

#### `users`
- `id` (SERIAL PRIMARY KEY)
- `email` (VARCHAR UNIQUE)
- `username` (VARCHAR UNIQUE)
- `first_name`, `last_name` (VARCHAR)
- `hashed_password` (VARCHAR)
- `is_active` (BOOLEAN, default TRUE)
- `role` (VARCHAR, default 'user')
- `phone_number` (VARCHAR)

#### `todos`
- `id` (SERIAL PRIMARY KEY)
- `title` (VARCHAR)
- `description` (TEXT)
- `priority` (INTEGER, default 1)
- `complete` (BOOLEAN, default FALSE)
- `owner_id` (INTEGER, FOREIGN KEY to users.id)

### Indexes
- `idx_users_email` on `users(email)`
- `idx_users_username` on `users(username)`
- `idx_todos_owner_id` on `todos(owner_id)`

---

## Seed Data

The `docker/init.sql` file includes:

### Sample Users
1. **John Doe** (johndoe) — Admin role
2. **Jane Smith** (janesmith) — User role
3. **Bob Wilson** (bobwilson) — User role
4. **Eric Roby** (codingwithroby) — Admin role

John, Jane, and Bob share the same test password hashed with bcrypt:
- Hashed password: `$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lm`
- Plain password: `secret` (for testing)

Eric's password:
- Plain password: `test1234` (for testing)

### Sample Todos
8 sample todos distributed among users with varying priorities and completion status.

---

## Checking and Re-Seeding an Existing Database

### Is the database already seeded?
```bash
docker compose exec postgres psql -U postgres -d TodoApplicationServer -c "SELECT id, username, email, role FROM users;"
```
If this returns rows, the container was already initialized and `docker/init.sql` will **not** run again on `docker compose up -d` — Postgres only executes files in `/docker-entrypoint-initdb.d/` when the data directory is empty.

### Re-seed without wiping existing data
To (re)apply `docker/init.sql` against an **already-running** container — for example after adding a new sample user to the file — pipe it through `psql` directly. The `ON CONFLICT ... DO NOTHING` clauses in the script make this safe to run repeatedly; existing rows are left untouched and only missing ones are inserted:
```bash
docker compose exec -T postgres psql -U postgres -d TodoApplicationServer < docker/init.sql
```

### Re-seed from scratch (destructive)
To force the full init script to run again exactly as it would on a brand-new setup:
```bash
docker compose down -v   # deletes postgres_data volume — all data is lost
docker compose up -d     # re-creates the container and re-runs docker/init.sql
```

---

## Common Docker Commands

### View Logs
```bash
docker compose logs -f postgres
```

### Stop the Database
```bash
docker compose down
```

### Stop and Remove All Data (Clean Slate)
```bash
docker compose down -v
```

**⚠️ This deletes the `postgres_data` volume and all data!** The next `docker compose up` will reinitialize with seed data.

### Restart the Database
```bash
docker compose restart postgres
```

### Access PostgreSQL CLI Inside Container
```bash
docker compose exec postgres psql -U postgres -d TodoApplicationServer
```

---

## Troubleshooting

### Connection Refused
- Ensure Docker is running
- Check if PostgreSQL is healthy: `docker compose ps`
- Wait 10-15 seconds for the database to be ready after starting

### "Database already exists" Error
- This is normal if running `docker compose up` after `docker compose down`
- The init script uses `IF NOT EXISTS` to prevent duplicate creation

### Port Already in Use
- Change `DB_PORT` in `.env` (e.g., `5433`)
- Update docker compose.yml: `"5433:5432"`

### PyCharm Connection Failed
- Verify the `.env` values match your PyCharm connection settings
- Try the **Test Connection** button in PyCharm to debug
- Ensure the container is running: `docker compose ps`

---

## Development Workflow

1. **Start the database:**
   ```bash
   docker compose up -d
   ```

2. **Run the FastAPI app:**
   ```bash
   uvicorn TodoApp.main:app --reload
   ```

3. **Connect in PyCharm:**
   - Database tab → existing connection (configured above)
   - Inspect tables, run queries, view data

4. **When done (or starting fresh):**
   ```bash
   docker compose down -v  # Clean slate
   docker compose up -d    # Rebuild with fresh seed data
   ```

---

## Notes

- **Persistence:** Data in `postgres_data` volume persists even after `docker compose down`
- **Init Script:** Only runs on first container creation (when volume doesn't exist)
- **Production Use:** In production, use strong passwords and secure environment management (secrets vault, not .env)
