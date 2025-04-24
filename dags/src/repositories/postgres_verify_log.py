from src.interfaces.interface_database import InterfaceDatabase
from src.models import ProcessLog
from src.interfaces.session_manager import SessionManager
from sqlalchemy import desc


class PostgresVerifyLog(InterfaceDatabase):
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

    def check_process_log_complete(self):
        log = (
            self.session.query(ProcessLog)
            .filter(ProcessLog.step == 1)
            .order_by(desc(ProcessLog.process_time))
            .first()
        )

        if not log:
            raise ValueError("Nenhum registro encontrado na tb_process_log.")

        if log.process_status.lower() != "processed":
            raise ValueError(
                f"Último status é '{log.process_status}', esperado: 'processed'."
            )

        return log.process_status
