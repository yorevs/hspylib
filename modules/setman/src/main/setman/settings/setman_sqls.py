SETMAN_SQLS = [
    """
    CREATE TABLE IF NOT EXISTS main.SETTINGS (
        uuid         TEXT                     PRIMARY KEY,
        name         TEXT                     NOT NULL,
        prefix       TEXT  DEFAULT ''         NOT NULL,
        value        TEXT  DEFAULT ''         NOT NULL,
        stype        TEXT  DEFAULT            'property',
        modified     TEXT  DEFAULT            (CURRENT_TIMESTAMP),

        CONSTRAINT NAME_uk UNIQUE (name)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS main.SETTINGS_EVENTS (
        uuid         INTEGER        PRIMARY KEY AUTOINCREMENT,
        event        TEXT           NOT NULL,
        setting      TEXT           NOT NULL,
        old_value    TEXT,
        new_value    TEXT,
        created      TEXT  DEFAULT  (CURRENT_TIMESTAMP)
    )
    """,
    """
    -- Create an indexes
    CREATE INDEX IF NOT EXISTS idx_settings_uuid ON SETTINGS(uuid)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_settings_uuid ON SETTINGS_EVENTS(uuid)
    """,
    """
    -- INSERT trigger
    CREATE TRIGGER after_settings_insert
    AFTER INSERT ON SETTINGS
    FOR EACH ROW
    BEGIN
        INSERT INTO SETTINGS_EVENTS (uuid, event, setting, old_value, new_value, created)
        VALUES (NULL, 'INSERT', NEW.name, NULL, NEW.value, CURRENT_TIMESTAMP);
    END
    """,
    """
    -- UPDATE trigger
    CREATE TRIGGER after_settings_update
    AFTER UPDATE ON SETTINGS
    FOR EACH ROW
    BEGIN
        INSERT INTO SETTINGS_EVENTS (uuid, event, setting, old_value, new_value, created)
        VALUES (NULL, 'UPDATE', OLD.name, OLD.value, NEW.value, CURRENT_TIMESTAMP);
    END
    """,
    """
    -- DELETE trigger
    CREATE TRIGGER after_settings_delete
    AFTER DELETE ON SETTINGS
    FOR EACH ROW
    BEGIN
        INSERT INTO SETTINGS_EVENTS (uuid, event, setting, old_value, new_value, created)
        VALUES (NULL, 'DELETE', OLD.name, OLD.value, NULL, CURRENT_TIMESTAMP);
    END
    """
]
