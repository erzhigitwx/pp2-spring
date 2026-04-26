CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INT;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE name = p_contact_name;
    IF v_id IS NULL THEN
        RAISE EXCEPTION 'contact % not found', p_contact_name;
    END IF;
    INSERT INTO phones(contact_id, phone, type) VALUES (v_id, p_phone, p_type);
END;
$$;


CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    v_gid INT;
BEGIN
    SELECT id INTO v_gid FROM groups WHERE name = p_group_name;
    IF v_gid IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group_name) RETURNING id INTO v_gid;
    END IF;
    UPDATE contacts SET group_id = v_gid WHERE name = p_contact_name;
END;
$$;


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(id INT, name VARCHAR, email VARCHAR, group_name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT c.id, c.name, c.email, g.name, p.phone
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;
