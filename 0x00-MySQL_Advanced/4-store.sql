-- Creates a trigger that decreases the quantity of an item
-- after add a new order
DELIMITER $$
CREATE
TRIGGER decr_qnty 
AFTER INSERT ON orders 
FOR EACH ROW
BEGIN
UPDATE items SET quantity = quantity - NEW.number
WHERE name=NEW.item_name;
END$$
