class DatabaseRouter:
    def db_for_read(self, model, **hints):
        """Direct read operations."""
        if model._meta.app_label in [
            "auth",
            "contenttypes",
            "sessions",
            "admin",
            "user_db",
        ]:
            return "user_db"  # Use the shared user database for user-related models
        return "default"  # Use the default app-specific database

    def db_for_write(self, model, **hints):
        """Direct write operations."""
        if model._meta.app_label in [
            "auth",
            "contenttypes",
            "sessions",
            "admin",
            "user_db",
        ]:
            return "user_db"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        """Allow relationships if both models are in the same database."""
        db_set = {"default", "user_db"}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Route migrations."""
        if app_label in ["auth", "contenttypes", "sessions", "admin", "user_db"]:
            return db == "user_db"  # Send auth-related migrations to the user_db
        return db == "default"  # Send other migrations to the default database
