import constants
import sys
from model import Model
from PyPDF2 import PdfFileReader, PdfFileWriter

class Controller:
    def __init__(self, view, model=Model()):
        self.view = view
        self.model = model

        self.view.bind_file_changed(self.handle_file_changed)
        self.view.bind_close(self.handle_close)
        self.view.bind_protect(self.handle_password_protect)
        
        self.view.in_path = self.model.in_file
        self.view.out_path = self.model.out_file
        self.view.status_text = constants.STATUSBAR_SELECT

    def handle_close(self, evt):
        sys.exit(0)
    
    def handle_password_protect(self, evt):
        first_run = self.view.show_password_dialog(constants.PROMPT_FIRST_PASSWORD)
        second_run = self.view.show_password_dialog(constants.PROMPT_SECOND_PASSWORD)

        if first_run != second_run:
            self.view.show_error_dialog(constants.ERROR_PASSWORD_NOMATCH)
            return

        password = first_run
        self.model.in_file = self.view.in_path
        self.model.out_file = self.view.out_path

        try:
            self.view.status_text = constants.STATUSBAR_PROCESSING
            self.password_protect_pdf_file(password)
            self.view.show_message_dialog(constants.NOTIFICATION_SUCCESS)
            self.view.clear()
            self.view.status_text = constants.STATUSBAR_SELECT

        except:
            exec_info = sys.exc_info()
            message = exec_info[0] if len(exec_info) == 1 else exec_info[1]
            self.view.show_error_dialog(f"{message}")
            self.view.status_text = constants.STATUSBAR_ERROR

    def handle_file_changed(self, evt):
        self.model.in_file = self.view.in_path
        self.model.out_file = self.view.out_path

        if self.model.in_file.strip() == "" or self.model.out_file.strip() == "":
            self.view.protect_enabled = False
            self.view.status_text = constants.STATUSBAR_SELECT
        else:
            self.view.protect_enabled = True
            self.view.status_text = constants.STATUSBAR_PROTECT

    def password_protect_pdf_file(self, password):
        with open(self.model.in_file, "rb") as in_file, open(self.model.out_file, "wb") as out_file:
            input_pdf = PdfFileReader(in_file)

            output_pdf = PdfFileWriter()   
            output_pdf.appendPagesFromReader(input_pdf)
            output_pdf.encrypt(password)
            output_pdf.write(out_file)
