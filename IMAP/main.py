from socket import *
import ssl
import quopri
import re
import unicodedata
import os
import base64
import getpass
import html
from dotenv import load_dotenv
from bs4 import BeautifulSoup


# Functions             Functionality
# -----------------------------------------------------------------------------------------------------------
# Constructor           Logs in to the imap server using provided email and pasword
# get_mailboxes         Gets all the mailboxes available for user.
# select_mailbox        Selects particular mailbox to use
# fetch_email_headers   Fetches number of email headers from selected mailbox
# get_boundary_id       Get boundary id of body
# fetch_whole_body      Fetch body of selected email

class IMAP:
    '''Class which does all the part of IMAP Protocol

    Arguements: \t
    email: User email \t
    password: User password\t
    imap_server: Url of imap server (default: gmail)\t
    debugging: Utility variable to print sent and received messages
    '''

    # <------------------------------------------------------Variables------------------------------------------>
    # Main socket which does all the work
    __main_socket = None

    __email = ""
    __password = ""

    # Stores the imap server address and port for each domain
    __HOST_EMAIL_PAIR = [
        {
            'domain': 'gmail.com',
            'imap_server': 'imap.gmail.com',
            'port': 993
        },
        {
            'domain': 'coep.ac.in',
            'imap_server': 'outlook.office365.com',
            'port': 993
        },
        {
            'domain': 'outlook.com',
            'imap_server': 'outlook.office365.com',
            'port': 993
        }
    ]

    __AUTH_MSG = "a01 LOGIN"  # Authentication message
    __MAIL_NEW_LINE = "\r\n"

    __SSL_PORT = 993  # Port for gmail imap server
    __HOST = 'imap.gmail.com'
    __TIMEOUT = 15  # 15 seconds for now

    __debugging = False

    # <-----------------------------------------------------Constructor------------------------------------------>

    def __init__(self, email, password, debugging=False):
        self.__email = email
        self.__password = password
        email_domain = email.split('@')[1].lower()

        # Determine host and ssl port using domain name
        for email in self.__HOST_EMAIL_PAIR:
            if email['domain'] == email_domain:
                self.__HOST = email['imap_server']
                self.__SSL_PORT = email['port']
                break

        self.__debugging = debugging

        try:
            # Connect to imap server
            self.__connect()
        except Exception as e:
            raise Exception(e)