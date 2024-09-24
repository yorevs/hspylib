-- INSERT trigger
CREATE TRIGGER after_settings_insert
AFTER INSERT ON SETTINGS
FOR EACH ROW
BEGIN
    INSERT INTO SETTINGS_EVENTS (uuid, event, setting, old_value, new_value, created)
    VALUES (NULL, 'INSERT', NEW.name, NULL, NEW.value, CURRENT_TIMESTAMP);
END;


-- UPDATE trigger
CREATE TRIGGER after_settings_update
AFTER UPDATE ON SETTINGS
FOR EACH ROW
BEGIN
    INSERT INTO SETTINGS_EVENTS (uuid, event, setting, old_value, new_value, created)
    VALUES (NULL, 'UPDATE', OLD.name, OLD.value, NEW.value, CURRENT_TIMESTAMP);
END;

-- DELETE trigger
CREATE TRIGGER after_settings_delete
AFTER DELETE ON SETTINGS
FOR EACH ROW
BEGIN
    INSERT INTO SETTINGS_EVENTS (uuid, event, setting, old_value, new_value, created)
    VALUES (NULL, 'DELETE', OLD.name, OLD.value, NULL, CURRENT_TIMESTAMP);
END;
