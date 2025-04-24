from datetime import datetime
from src.interfaces.interface_database import InterfaceDatabase
from src.interfaces.session_manager import SessionManager
from airflow.providers.postgres.hooks.postgres import PostgresHook
from src.models import (
    DimCustomer,
    DimAddress,
    DimTechnician,
    DimTerminal,
    DimCancellationReason,
    FctOrder,
    ProcessLog,
)


class PostgresWriterDw(InterfaceDatabase):
    def __init__(self, connection: str):
        """
        Initialize the PostgreDatabase class.

        :param connection_string: The connection string to connect to the PostgreSQL database.
        Connection configured on Airflow UI.
        This connection used on PostgresHook.
        """
        self.connection = connection
        self.engine = self._create_connection()

        with SessionManager() as session:
            self.session = session

    def _create_connection(self):
        self.hook = PostgresHook(postgres_conn_id=self.connection)
        engine = self.hook.get_sqlalchemy_engine()
        return engine

    def extract_normalize_database(self):
        sql = """
            SELECT 
    o.order_number,
    o.provider,
    o.technician_email,
    o.arrival_date,
    o.deadline_date,
    o.last_modified_date,
    c.reason as cancellation_reason,
    o.terminal_model,
    o.terminal_type,
    cust.customer_phone,
    addr.city,
    addr.country,
    addr.country_state,
    addr.zip_code, 
    addr.street_name, 
    addr.neighborhood, 
    addr.complement,
    o.file_name
FROM tb_orders o
LEFT JOIN tb_cancellation_reasons c ON o.cancellation_reason_id = c.id
LEFT JOIN tb_customers cust ON cust.customer_id =  o.customer_id 
LEFT JOIN (select distinct customer_id, city, country, country_state, zip_code, street_name, neighborhood, complement from tb_addresses ) as addr on addr.customer_id =  o.customer_id limit 1000;
        """

        records = self.hook.get_records(sql)

        return records

    def insert_unique_technicians(self, data):
        emails = {row.technician_email for row in data if row.technician_email}
        existing = {
            email
            for (email,) in self.session.query(DimTechnician.email)
            .filter(DimTechnician.email.in_(emails))
            .all()
        }
        to_insert = [
            DimTechnician(email=email) for email in emails if email not in existing
        ]
        self.session.bulk_save_objects(to_insert)
        self.session.commit()

    def insert_unique_customers(self, data):
        phones = {row.customer_phone for row in data if row.customer_phone}
        existing = {
            phone
            for (phone,) in self.session.query(DimCustomer.customer_phone)
            .filter(DimCustomer.customer_phone.in_(phones))
            .all()
        }
        to_insert = [
            DimCustomer(customer_phone=phone)
            for phone in phones
            if phone not in existing
        ]
        self.session.bulk_save_objects(to_insert)
        self.session.commit()

    def insert_unique_addresses(self, data):
        addresses = {(row.city, row.country_state, row.country, row.zip_code,
                      row.street_name, row.neighborhood, row.complement) for row in data}

        existing = {
            (addr.city, addr.country_state, addr.country, addr.zip_code,
             addr.street_name, addr.neighborhood, addr.complement)
            for addr in self.session.query(DimAddress).all()
        }
        to_insert = [
            DimAddress(city=city, country_state=country_state, country=country, zip_code=zip_code,
                       street_name=street_name, neighborhood=neighborhood, complement=complement)
            for (city, country_state, country, zip_code, street_name, neighborhood, complement) in addresses
            if (city, country_state, country, zip_code, street_name, neighborhood, complement) not in existing
        ]
        self.session.bulk_save_objects(to_insert)
        self.session.commit()

    def insert_unique_cancellations(self, data):
        reasons = {
            row.cancellation_reason for row in data if row.cancellation_reason}
        existing = {
            reason
            for (reason,) in self.session.query(DimCancellationReason.reason)
            .filter(DimCancellationReason.reason.in_(reasons))
            .all()
        }
        to_insert = [
            DimCancellationReason(reason=reason)
            for reason in reasons
            if reason not in existing
        ]
        self.session.bulk_save_objects(to_insert)
        self.session.commit()

    def insert_unique_terminals(self, data):
        terminals = {(row.terminal_model, row.terminal_type) for row in data}
        existing = {
            (term.model, term.type) for term in self.session.query(DimTerminal).all()
        }
        to_insert = [
            DimTerminal(model=model, type=type)
            for (model, type) in terminals
            if (model, type) not in existing
        ]
        self.session.bulk_save_objects(to_insert)
        self.session.commit()

    def insert_fact_orders(self, data):
        for row in data:
            # Buscar os IDs das dimensões com base nos valores da linha

            technician_id = (
                self.session.query(DimTechnician.technician_id)
                .filter_by(email=row.technician_email)
                .scalar()
            )
            customer_id = (
                self.session.query(DimCustomer.customer_id)
                .filter_by(customer_phone=row.customer_phone)
                .scalar()
            )
            address_id = (
                self.session.query(DimAddress.address_id)
                .filter_by(
                    city=row.city, country_state=row.country_state, country=row.country, zip_code=row.zip_code, street_name=row.street_name, neighborhood=row.neighborhood, complement=row.complement

                )
                .scalar()
            )
            cancellation_id = (
                self.session.query(DimCancellationReason.id)
                .filter_by(reason=row.cancellation_reason)
                .scalar()
            )
            terminal_id = (
                self.session.query(DimTerminal.terminal_id)
                .filter_by(model=row.terminal_model, type=row.terminal_type)
                .scalar()
            )

            # Checar se já existe o pedido (por segurança, evita duplicidade na fato)
            exists = (
                self.session.query(FctOrder.order_id)
                .filter_by(order_number=row.order_number)
                .first()
            )
            if exists:
                continue

            fato = FctOrder(
                order_number=row.order_number,
                provider=row.provider,
                arrival_date=row.arrival_date,
                deadline_date=row.deadline_date,
                last_modified_date=row.last_modified_date,
                technician_id=technician_id,
                customer_id=customer_id,
                address_id=address_id,
                cancellation_reason_id=cancellation_id,
                terminal_id=terminal_id,
                file_name=row.file_name,
            )

            self.session.add(fato)

        self.session.commit()


def insert_process_log(
    self,
    file_name: str,
    process_status: str,
    step: int,
    error_message: str = None,
    processed: bool = False,
):
    new_log = ProcessLog(
        file_name=file_name,
        process_status=process_status,
        process_time=datetime.now(),
        error_message=error_message,
        processed=processed,
        step=step,
    )
    self.session.add(new_log)
    self.session.commit()
