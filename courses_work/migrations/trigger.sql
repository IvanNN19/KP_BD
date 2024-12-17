CREATE OR REPLACE FUNCTION log_user_activity()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO UsersLog (user_id, operation_status)
    VALUES (NEW.user_id, 'Регистрация в системе');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER log_user_login
AFTER INSERT ON Users
FOR EACH ROW
EXECUTE FUNCTION log_user_activity();
