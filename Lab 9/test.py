import os
import tempfile
import unittest
from unittest.mock import patch

from supplier import Supplier
from product import Product
from physicalProduct import PhysicalProduct
from digitalProduct import DigitalProduct
from productFactory import ProductFactory
from inventory import Inventory
from order import Order
from orderLine import OrderLine
from noDiscount import NoDiscount
from percentageDiscount import PercentageDiscount
from bulkDiscount import BulkDiscount
from studentDiscount import StudentDiscount
from main import get_positive_float, load_products

class TestLab9(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "SIT", "SIT@sit.singaporetech.edu.sg")
        self.laptop = ProductFactory.create(
            "physical", "P001", "Laptop", 250.0, 10, self.supplier
        )
        self.ebook = ProductFactory.create(
            "digital", "D001", "Guide", 50.0, 20, self.supplier
        )

    def test_order_discount_strategies(self) -> None:
        order = Order("ORD-01")
        order.add_order_line(self.laptop, 1)  # total = 250.0
        self.assertAlmostEqual(order.calculate_total(), 250.0)

        order.set_discount(BulkDiscount(200, 20))
        self.assertAlmostEqual(order.calculate_total(), 230.0)

        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

        order.set_discount(StudentDiscount())
        self.assertAlmostEqual(order.calculate_total(), 237.5)

        order.set_discount(NoDiscount())
        self.assertAlmostEqual(order.calculate_total(), 250.0)

    def test_product_factory(self) -> None:
        self.assertIsInstance(self.laptop, Product)
        self.assertIsInstance(self.laptop, PhysicalProduct)
        self.assertIsInstance(self.ebook, Product)
        self.assertIsInstance(self.ebook, DigitalProduct)

        with self.assertRaises(ValueError):
            ProductFactory.create(
                "service", "S001", "Installation", 30.0, 5, self.supplier
            )

    def test_validation_rules(self) -> None:
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P002", "BadPrice", 0.0, 5, self.supplier)

        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P003", "NegStock", 10.0, -1, self.supplier)

        with self.assertRaises(ValueError):
            self.laptop.update_stock(-3)

        with self.assertRaises(ValueError):
            OrderLine(self.laptop, 0)

    @patch("builtins.input", side_effect=["abc", "-5", "12.50"])
    def test_get_positive_float(self, _mock_input) -> None:
        self.assertAlmostEqual(get_positive_float("Price: "), 12.50)

    def test_load_products_missing_file(self) -> None:
        inv = Inventory()
        load_products("missing_products.csv", inv, self.supplier)
        self.assertEqual(len(inv.get_products()), 0)

    def test_load_products_skips_bad_rows(self) -> None:
        csv_data = (
            "product_type, product_id,name, price, stock_quantity\n"
            "physical, P001, Desk Lamp, 25.00,10\n"
            "digital, D001, Photo Editor, 49.90,100\n"
            "service, S001, Installation, 30.00,5\n"
            "physical, P002, Office Chair, abc,3\n"
            "physical, P003, Monitor Stand, 39.50,7\n"
        )
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, newline=""
        ) as tmp:
            tmp.write(csv_data)
            tmp_path = tmp.name

        try:
            inv = Inventory()
            load_products(tmp_path, inv, self.supplier)
            self.assertEqual(len(inv.get_products()), 3)
        finally:
            os.remove(tmp_path)

if __name__ == "__main__":
    unittest.main()