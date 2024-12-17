from datetime import datetime
import asyncio
from repositories.adds import add_order_details_async
from pandas import DataFrame
import time
import random

class AddService:
    def process_add(self, sale_date: datetime, items: DataFrame, id: int) -> int:
        order_id = random.randint(100, 999)
        warehouse_id = random.randint(1, 3)
        
        items["package_id"] = order_id
        items["date"] = sale_date
        items["user_id"] = id
        items["status"] = "create"
        items["warehouse_id"] = warehouse_id

        print("~~~~~")
        print(items)
        print("~~~~~")
        asyncio.run(add_order_details_async(items))
        # add_order_details(items)
        
        return order_id