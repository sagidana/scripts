CREATE FUNCTION helper(value integer) RETURNS integer AS $$
  SELECT value + 1;
$$ LANGUAGE SQL;

CREATE FUNCTION greet(value integer) RETURNS integer AS $$
  SELECT helper(value) * 2;
$$ LANGUAGE SQL;

CREATE FUNCTION runner() RETURNS integer AS $$
  SELECT greet(3);
$$ LANGUAGE SQL;
