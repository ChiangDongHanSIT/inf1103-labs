from supplier import Supplier
from product import Product
from physicalProduct import PhysicalProduct
from digitalProduct import DigitalProduct
from inventory import Inventory
from order import Order

def show_product_details(product: Product) -> None:
    product.display_information()
    print("Fulfilment:", product.get_fulfilment_info())

supplier = Supplier("S01", "TechDistributors", "sales@techdist.com")
p1 = PhysicalProduct("P001", "Laptop", 1200.00, 10, supplier, 2.5)
p2 = DigitalProduct("P002", "Antivirus", 45.00, 50, supplier, 250.0)

del supplier
p1.get_supplier().display_information()
p2.get_supplier().display_information()

inv_a = Inventory()
inv_b = Inventory()

inv_a.add_product(p1)
inv_a.remove_product("P001")  
p1.display_information()      
inv_b.add_product(p1)        

order1 = Order("ORD-101")
order1.add_order_line(p1, 2)
order1.add_order_line(p2, 1)
print(f"Order 1 Total: ${order1.calculate_total():.2f}")

order2 = Order("ORD-102")
order2.add_order_line(p1, 3)

line1 = order1.get_order_lines()[0]
line2 = order2.get_order_lines()[0]
print("Same OrderLine object?", line1 is line2)                 
print("Same Product object?", line1.get_product() is line2.get_product())  

order1.remove_order_line("P002") 

inv_b.add_product(p2) 
for prod in inv_b.get_products():
    show_product_details(prod)