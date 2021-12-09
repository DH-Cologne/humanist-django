from django.core.management.base import BaseCommand
from ...models import IncomingEmail
from datetime import timedelta
from django.utils import timezone
import os.path
import mailparser
import email
from datetime import datetime
from bs4 import BeautifulSoup
from base64 import b64decode


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

                mail.date = email.utils.parsedate_to_datetime(parsed.message.get('Date'))
                mail.raw = parsed.message_as_string

                # Finding text
                plain_text = "".join(parsed.text_plain).strip()
                html_text = "".join(parsed.text_html).strip()

                has_plain_text = len(plain_text) > 0
                has_html_text = len(html_text) > 0

                if has_html_text and not has_plain_text:
                    # Only html text content
                    mail.body_html = html_text
                    soup = BeautifulSoup(mail.body_html, features="html.parser")
                    cleaned = "\n".join([text.strip() for text in soup.text.strip().split("\n")])
                    mail.body = cleaned
                elif has_plain_text and not has_html_text:
                    # Only plain text content
                    mail.body = plain_text
                    mail.body_html = plain_text
                elif has_html_text and has_plain_text:
                    # Both plain text and html text content
                    mail.body = plain_text
                    mail.body_html = html_text
                else:
                    # No plain or html text content
                    # Try base64 content, otherwise abort
                    encoding_header = parsed.headers.get("Content-Transfer-Encoding", None)
                    if encoding_header != "base64":
                        continue
                    base64content = parsed.message_as_string.split("\n\n").pop()
                    decoded = b64decode(base64content).decode('utf-8')
                    cleaned = "\n".join([text.strip() for text in decoded.split("\n")]).strip()
                    if len(cleaned) == 0:
                        continue
                    mail.body = cleaned
                    mail.body_html = cleaned

                senders = []
                for sender in parsed.from_:
                    senders.append('{} <{}>'.format(sender[0], sender[1]))
                mail.sender = ", ".join(senders)

                mail.subject = parsed.subject
                mail.used = False
                mail.deleted = False
                mail.processed = True

                mail.save()
                os.rename(file, "{}.used".format(file))
            except Exception as e:
                print("Failed parsing {}".format(file))
                print(e)
