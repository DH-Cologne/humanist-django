from django.core.management.base import BaseCommand
from ...models import IncomingEmail
from datetime import timedelta
from django.utils import timezone
import os.path
import mailparser

class Command(BaseCommand):
    help = 'Import getmail Mails into Database!'

    def add_arguments(self, parser):
        args = '<import_path import_path ...>'
        parser.add_argument('import_path', nargs='+', type=str)

    def handle(self, *args, **options):
        paths = options["import_path"]

        mail_files = []
        for path in paths: # TODO: only get files
            files = os.listdir(path)
            for file in files:
                mail_files.append(path + file)

        print(mail_files)
        for file in mail_files:
            parsed = mailparser.parse_from_file(file)
            mail = IncomingEmail()
            mail.body = parsed.body

            full_text_body = ""
            for part in parsed.text_plain:
                full_text_body += part
            mail.body = full_text_body.strip()

            full_text_html = ""
            for part in parsed.text_html:
                full_text_html += part
            mail.body_html = full_text_html.strip()

            # TODO: check date error
            mail.date = parsed.date
            mail.raw = parsed.body

            senders = []
            for sender in parsed.from_:
                senders.append('{} <{}>'.format(sender[0], sender[1]))
            mail.sender = ", ".join(senders)

            mail.subject = parsed.subject
            mail.used = False
            mail.deleted = False
            mail.processed = False

            mail.save()