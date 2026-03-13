class Inventory():
    def __init__(self, item_id, item_name, item_category, quantity=0, reorder_level=10, item_cost=0.00):

        self.item_id = item_id
        self.item_name = item_name
        self.item_category = item_category
        self.quantity = quantity
        self.reorder_level = reorder_level
        self.item_cost = item_cost

    def __str__(self):
        return f"Item({self.item_id}) - {self.item_name} | {self.item_category} | {self.item_cost}"    