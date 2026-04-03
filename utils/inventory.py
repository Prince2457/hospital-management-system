from utils.db_helpers import execute_query

def get_all_inventory():
    """Fetch all inventory from th databese .Return a list of dictionary """
    return execute_query("SELECT * FROM inventory", fetch="all") or []


def get_inventory_by_id(item_id):
    """ Fetch ivnetory from database using item id . """
    return execute_query("SELECT * FROM inventory WHERE item_id=%s",(item_id,), fetch="one")


def create_inventory(item_name, item_category, quantity, reorder_level, item_cost):
    """Insert into database to create inventory."""
    return execute_query("""INSERT INTO inventory (item_name, item_category, quantity, reorder_level, item_cost)
                        VALUES (%s,%s,%s,%s,%s)""",
                        (item_name, item_category, quantity, reorder_level, item_cost), commit=True)


def update_inventory(item_id, item_name, item_category, quantity, reorder_level, item_cost):
    """Update set inventory in database."""
    return execute_query(
        """UPDATE inventory SET
            item_name=%s,
            item_category=%s,
            quantity=%s,
            reorder_level=%s,
            item_cost=%s
            WHERE item_id=%s""",
            (item_name, item_category, quantity, reorder_level, item_cost, item_id), commit=True)

def delete_inventory(item_id):
    """Delete inventory from database."""
    return execute_query("DELETE FROM inventory WHERE item_id=%s",(item_id,), commit=True)

def get_low_stock_items():
    """ Fetch from low stock from inventory by fetching from inventory where quantity is less than reorder level."""
    return execute_query(
        """ SELECT * FROM inventory
        WHERE quantity <= reorder_level
        ORDER BY quantity ASC""",
        fetch="all"
    ) or []