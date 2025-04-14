

class VerifyProcessLog:

    def __init__(self, db_writer):
        self.db_writer = db_writer

    def check_process_log_complete(self):
         
        return self.db_writer.check_process_log_complete()
