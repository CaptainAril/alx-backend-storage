-- creates a function `SafeDiv` that takes two arguments, `a, INT`, and `b, INT`
-- and returns the a / b or 0 if b == 0

DELIMITER $$
CREATE FUNCTION SafeDiv (a INT, b INT)
RETURNS FLOAT
DETERMINISTIC

BEGIN
    IF b = 0 THEN
        RETURN (0);
    ELSE
        RETURN (a / b);
    END IF;
END $$
