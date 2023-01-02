import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv('./.env')
    old_mail = os.getenv('EMAIL')
    old_pass = os.getenv('PASSWORD')
    imap = IMAP(old_mail, old_pass, debugging=True)
    folders = imap.get_mailboxes()
    num = imap.select_mailbox(folders[10])
    # headers = imap.fetch_email_headers(num, count=2)
    result = imap.fetch_text_body(num - 6)