from django.core.management.base import BaseCommand
from ...models import IncomingEmail
from datetime import timedelta
from django.utils import timezone
import os.path
import mailparser
import email
from datetime import datetime
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = 'Import getmail Mails into Database!'

    def add_arguments(self, parser):
        args = '<import_path import_path ...>'
        parser.add_argument('import_path', nargs='+', type=str)

    def parse_mail(self, path):
        encoding_modes = ["latin1", "utf8"]
        for mode in encoding_modes:
            try:
                with open(path, "r", encoding=mode) as f:
                    return mailparser.parse_from_file_obj(f)
            except Exception as e:
                print("Failed opening {} with mode {}".format(path, mode))
                print(e)
        return None

    def handle(self, *args, **options):
        paths = options["import_path"]

        mail_files = set()

        for path in paths:
            for root, directories, filenames in os.walk(path):
                for filename in filenames:
                    if filename.endswith('.used'):
                        continue
                    mail_files.add(os.path.join(root, filename))

        print("Processing {} new mails".format(len(mail_files)))
        for file in mail_files:
            try:
                parsed = self.parse_mail(file)
                if not parsed:
                    continue
                mail = IncomingEmail()

                mail.body = "".join(parsed.text_plain).strip()
                mail.body_html = "".join(parsed.text_html).strip()

                mail.date = email.utils.parsedate_to_datetime(parsed.message.get('Date'))
                mail.raw = parsed.body

                senders = []
                for sender in parsed.from_:
                    senders.append('{} <{}>'.format(sender[0], sender[1]))
                mail.sender = ", ".join(senders)

                mail.subject = parsed.subject
                mail.used = False
                mail.deleted = False
                mail.processed = True

                if len(mail.body) == 0:
                    soup = BeautifulSoup(mail.body_html, features="html.parser")
                    cleaned = "\n".join([text.strip() for text in soup.text.strip().split("\n")])
                    mail.body = cleaned

                mail.save()
                os.rename(file, "{}.used".format(file))
            except Exception as e:
                print("Failed parsing {}".format(file))
                print(e)
