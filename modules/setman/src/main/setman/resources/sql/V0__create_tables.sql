CREATE TABLE IF NOT EXISTS main.SETTINGS (
    uuid         TEXT                     PRIMARY KEY,
    name         TEXT                     NOT NULL,
    prefix       TEXT  DEFAULT ''         NOT NULL,
    value        TEXT  DEFAULT ''         NOT NULL,
    stype        TEXT  DEFAULT            'property',
    modified     TEXT  DEFAULT            (CURRENT_TIMESTAMP),

    CONSTRAINT NAME_uk UNIQUE (name)
);

CREATE TABLE IF NOT EXISTS main.SETTINGS_EVENTS (
    uuid         INTEGER        PRIMARY KEY AUTOINCREMENT,
    event        TEXT           NOT NULL,
    setting      TEXT           NOT NULL,
    old_value    TEXT,
    new_value    TEXT,
    created      TEXT  DEFAULT  (CURRENT_TIMESTAMP)
);

-- Create an indexes
CREATE INDEX IF NOT EXISTS idx_settings_uuid ON SETTINGS(uuid);
CREATE INDEX IF NOT EXISTS idx_settings_uuid ON SETTINGS_EVENTS(uuid);
