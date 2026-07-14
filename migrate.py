import mysql.connector

# ---------- LOCAL DATABASE ----------
local_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="adnu_mosaic"
)

# ---------- RAILWAY DATABASE ----------
remote_conn = mysql.connector.connect(
    host="tokaido.proxy.rlwy.net",
    port=42304,
    user="root",
    password="EltbMSCJRMTyPQBvgwlTvEGwpwAmiDyY",
    database="railway"
)

local = local_conn.cursor(dictionary=True)
remote = remote_conn.cursor()

print("Connected to both databases.")

# Disable foreign key checks
remote.execute("SET FOREIGN_KEY_CHECKS=0")

# Get all local tables
local.execute("SHOW TABLES")
tables = [list(row.values())[0] for row in local.fetchall()]

print(f"Found {len(tables)} tables.")

# Drop existing remote tables
remote.execute("SHOW TABLES")
existing = [row[0] for row in remote.fetchall()]

for table in existing:
    print(f"Dropping {table}...")
    remote.execute(f"DROP TABLE IF EXISTS `{table}`")

remote.execute("SET FOREIGN_KEY_CHECKS=1")

# Create tables and copy data
for table in tables:

    print(f"\nCreating {table}...")

    local.execute(f"SHOW CREATE TABLE `{table}`")
    create_sql = local.fetchone()["Create Table"]

    remote.execute(create_sql)

    local.execute(f"SELECT * FROM `{table}`")
    rows = local.fetchall()

    if rows:

        cols = list(rows[0].keys())

        placeholders = ", ".join(["%s"] * len(cols))
        columns = ", ".join(f"`{c}`" for c in cols)

        insert_sql = f"""
        INSERT INTO `{table}` ({columns})
        VALUES ({placeholders})
        """

        values = [tuple(r[c] for c in cols) for r in rows]

        remote.executemany(insert_sql, values)

        print(f"Inserted {len(rows)} rows.")

remote_conn.commit()

local.close()
remote.close()

local_conn.close()
remote_conn.close()

print("\n🎉 Migration completed successfully!")