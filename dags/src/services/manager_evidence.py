class ManagerEvidence:
    def __init__(self, db_writer):
        self.db_writer = db_writer

    def manager_evidence(self, files):
        tfiles = [link.split("/")[-1].split(".")[0] for link in files]
        self.db_writer.insert_evidence_logs(tfiles)
        self.db_writer.update_evidence_status_from_orders(tfiles)
        return True
