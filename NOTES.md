# 🛡️ Production Scaling & Legal Compliance (GoBD / WORM)

For deploying this engine in enterprise production environments, the following architectural upgrades are recommended:

## 1. Database Scaling (Migrating to PostgreSQL)
SQLite locks the database file on writes, making it vulnerable under high transaction loads (concurrent billing cycles). For multi-instance, horizontal setups, migrate the database layer to **PostgreSQL**. Since SQLModel is built on SQLAlchemy, this transition only requires changing the connection string in `database/db.py`.

## 2. Large Object Decoupling
To avoid database bloat and performance degradation, do not store invoice PDF/XML binaries in the SQL database. 
* Store files in a dedicated **Object Storage** service (e.g., AWS S3, Google Cloud Storage, or an on-premise MinIO cluster).
* Save only the document URI and the file's SHA-256 cryptographic hash in the PostgreSQL table.

## 3. Legal Compliance: WORM Storage (GoBD)
In German-speaking and EU regions, finalized invoice documents must be kept in their original form and be **unalterable** for 10 years (compliant with GoBD regulations).
* **Object Lock in Compliance Mode**: Configure AWS S3 or MinIO buckets with Object Lock in **Compliance Mode**. When enabled, the storage layer physically blocks files from being updated, overwritten, or deleted by any user (including root administrators) for the specified retention duration.
* **Database Constraints**: Disable any `DELETE` or `UPDATE` handlers on finalized `InvoiceOrder` records within the application layer. All corrections must be done strictly via supplementary credit notes (Stornorechnungen).
