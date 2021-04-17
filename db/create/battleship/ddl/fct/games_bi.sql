CREATE FUNCTION games_bi() RETURNS trigger
AS $$
  BEGIN
    if NEW.id is null then
        NEW.id := nextval('games_s');
    end if;
	NEW.created_at := current_timestamp;
    NEW.created_by := current_user;
    NEW.updated_at := NEW.created_at;
    NEW.updated_by := NEW.created_by;
    RETURN NEW;
  END;
$$ LANGUAGE plpgsql;
