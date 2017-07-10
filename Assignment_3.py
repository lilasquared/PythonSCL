class InventoryItem(object):
    def __init__(self, description, cost, quanity):
        self.description = description
        self.cost = cost
        self.quantity = quanity


inventoryList = [
    InventoryItem('Monitor', 149.99, 5),
    InventoryItem('Keyboard', 29.99, 12),
    InventoryItem('Mouse', 24.99, 13),
    InventoryItem('USB Drive (32gb)', 26.99, 23),
]
print('+----------------------------------------------------+')
print('| {:<20} | {:>12} | {:>12} |'.format('Description', 'Cost ($)', 'Quantity'))
print('|----------------------------------------------------|')
for item in inventoryList:
    print('| {:<20} | {:>12} | {:>12} |'.format(item.description, item.cost, item.quantity))
print('+----------------------------------------------------+')
