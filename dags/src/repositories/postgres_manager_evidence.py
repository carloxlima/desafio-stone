from src.interfaces.interface_database import InterfaceDatabase
from src.models import EvidenceLog, Order
from datetime import datetime
from src.interfaces.session_manager import SessionManager


class PostgresManagerEvidence(InterfaceDatabase):
    """
    Class to create a PostgreSQL database.
    This class is used to create a new database in PostgreSQL.
    """

    def __init__(self, connection: str):
        self.connection = connection
        self.engine = self._create_connection()

        with SessionManager() as session:
            self.session = session

    def _create_connection(self):
        """
        Create a connection to the database.
        :return: A connection object.
        """
        pass

    def insert_evidence_logs(self, order_numbers: list[str], status: str = "pending"):

        evidence_existing = [
            evidence.order_number for evidence in self.session.query(EvidenceLog).all()
        ]

        to_insert_evidence = {
            order_number for order_number in order_numbers if order_number not in evidence_existing
        }

        logs = [
            EvidenceLog(
                order_number=order_number,
                file_name=f"{order_number}.jpg",
                process_status=status,
                process_time=datetime.now(),
                processed=False,
            )
            for order_number in to_insert_evidence
        ]

        self.session.bulk_save_objects(logs)
        self.session.commit()

    def update_evidence_status_from_orders(
        self, order_numbers: list[str], new_status: str = "completed"
    ):
        existing_orders = (
            self.session.query(Order.order_number)
            .filter(Order.order_number.in_(order_numbers))
            .all()
        )

        found_order_numbers = [row.order_number for row in existing_orders]

        if not found_order_numbers:
            print("Nenhum order_number encontrado na tb_orders.")
            return

        self.session.query(EvidenceLog).filter(
            EvidenceLog.order_number.in_(found_order_numbers)
        ).update(
            {EvidenceLog.process_status: new_status, EvidenceLog.processed: True},
            synchronize_session=False,
        )

        self.session.commit()
        print(
            f"Atualizados {len(found_order_numbers)} registros na tb_evidence_log.")
