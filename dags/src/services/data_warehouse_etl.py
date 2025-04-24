from collections import namedtuple


class DataWarehouseETL:
    """
    Calcula o valor com desconto aplicado.

    Args:
        valor (float): O valor original do produto.
        desconto (float): A porcentagem de desconto a ser aplicada.

    Returns:
        float: O valor após a aplicação do desconto.
    """

    def __init__(self, db_writer):
        self.db_writer = db_writer

    def extract(self):
        return self.db_writer.extract_normalize_database()
        # Logic to extract data from the source
        print(f"Extracting data from {self.source_data}")

    def transform_and_load_dims(self, data):
        OrderDW = namedtuple(
            "OrderDW",
            [
                "order_number",
                "provider",
                "technician_email",
                "arrival_date",
                "deadline_date",
                "last_modified_date",
                "cancellation_reason",
                "terminal_model",
                "terminal_type",
                "customer_phone",
                "city",
                "country",
                "country_state",
                "zip_code",
                "street_name",
                "neighborhood",
                "complement",
                "file_name",
            ],
        )

        base = [OrderDW(*row) for row in data]

        self.db_writer.insert_unique_technicians(base)
        self.db_writer.insert_unique_customers(base)
        self.db_writer.insert_unique_addresses(base)
        self.db_writer.insert_unique_cancellations(base)
        self.db_writer.insert_unique_terminals(base)

        print("Loading data into the dimension tables")

    def load_fct(self, data):
        OrderDW = namedtuple(
            "OrderDW",
            [
                "order_number",
                "provider",
                "technician_email",
                "arrival_date",
                "deadline_date",
                "last_modified_date",
                "cancellation_reason",
                "terminal_model",
                "terminal_type",
                "customer_phone",
                "city",
                "country",
                "country_state",
                "zip_code",
                "street_name",
                "neighborhood",
                "complement",
                "file_name",
            ],
        )

        base = [OrderDW(*row) for row in data]

        self.db_writer.insert_fact_orders(base)
        print("Loading data into the fact table")

    def load(self):
        # Logic to load the transformed data into the destination
        print(f"Loading data into {self.destination_data}")

    def run_etl(self):
        self.extract()
        self.transform()
        self.load()
