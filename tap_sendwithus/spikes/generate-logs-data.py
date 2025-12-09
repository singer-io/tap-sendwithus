"""
A script to send emails using Sendwithus API.
This script generates email payloads and sends them using the provided API key and ESP account key.
It will assist end user in generating data for below mentioned streams for the platform
    >>> logs
    >>> log_events

    Usage:
    -----
        python generate-logs-data.py --num-mails 5

    Note:
    -----
        You may also need to install dotenv package if not already installed:
            pip install python-dotenv

        Ensure you have the following environment variables set:
        - SENDWITHUS_API_KEY
        - SENDWITHUS_ESP_ACCOUNT_KEY

"""

import argparse
import os
import random
import time

import requests
import singer
from dotenv import load_dotenv

LOGGER = singer.get_logger()


class SessionAuth:
    """ Adapter class for handling different authentication methods for requests.Session
        This can be extended with more functionalities later if needed :)
    """

    def __init__(self, session: requests.Session, token: str = None, username: str = None):
        self._session = session
        self._username = username
        self._token = token

    def _basic_auth(self):
        """ Sets up basic authentication for the session. """
        auth = (self._username, "")
        self._session.auth = auth

    def _bearer_auth(self):
        """ Sets up bearer token authentication for the session. """
        self._session.headers.update({"Authorization": f"Bearer {self._token}"})


class SendwithusDataGenerator:
    """ Class to generate and send emails using Sendwithus API """

    def __init__(self, number_of_mails: int, esp_key: str = None):
        self._mail_url = "https://api.sendwithus.com/api/v1/send"
        self._mail_ctr = number_of_mails

        # Email ids and templates are hardcoded for now. Please modify as per your requirements.
        self._mail_ids = ["tempuser@mail.com", "tempuser2@mail.com", "tempuser3@mail.com"]
        self._template_ids = ["tem_XrPrQQKVhK876X94986J644G", "tem_wqSdjk3kkrkyMdPV76jQbCG4",
                              "tem_GvTyGGfykXrfmqT8JJqVhqD7", "tem_Y8Hm9VBhxPdPGVRmGJ7cfq48"]
        self._template_data_options = [
            {"first_name": "Alice", "button_text": "Click Here"},
            {"first_name": "Bob", "button_text": "Join Now"},
            {"first_name": "Charlie", "button_text": "Sign Up Today"}
        ]

        self._http_method = "POST"
        self._esp_account = esp_key

    def generate_mail_payload(self):
        """ Function to generate a random mail payload.

        Returns:
            dict: The generated mail payload.
        """

        address = random.choice(self._mail_ids)
        user = address

        payload = {
            "template": random.choice(self._template_ids),
            "recipient": {
                "name": user,
                "address": address
            },
            "template_data": random.choice(self._template_data_options),
            "locale": "en-US",
            "esp_account": self._esp_account,
            "version_name": "New Version"
        }

        return payload

    def generate_mail_data(self):
        """ Generator function to yield mail data payloads.

        Yields:
            dict: The generated mail payload.
        """

        for _ in range(self._mail_ctr):
            yield self.generate_mail_payload()
            # Wait for some time between mails if needed
            time.sleep(5)  # This is done to avoid creating log_events with same timestamp

    def send_mails(self, api_key: str):
        """ Entry point to send mails using Sendwithus API.

        Args:
            api_key (str): The API key for authentication.
        """

        session = requests.Session()
        SessionAuth(session=session, username=api_key)._basic_auth()

        for mail_data in self.generate_mail_data():
            response = session.post(self._mail_url, json=mail_data)
            if response.status_code == 200:
                LOGGER.info(f"Email sent successfully to {mail_data['recipient']['address']}")
                LOGGER.info(f"Response: {response.json()}")
            else:
                LOGGER.info(f"Failed to send email to {mail_data['recipient']['address']}: {response.text}")


def main():
    load_dotenv()

    api_key = os.getenv("SENDWITHUS_API_KEY")
    esp_key = os.getenv("SENDWITHUS_ESP_ACCOUNT_KEY")

    if not api_key:
        raise ValueError("SENDWITHUS_API_KEY environment variable is not set")

    if not esp_key:
        raise ValueError("SENDWITHUS_ESP_ACCOUNT_KEY environment variable is not set")

    # Get number of mails to send from the sys arguments or default to 3
    argparser = argparse.ArgumentParser(description="Send emails using Sendwithus API")
    argparser.add_argument("--num-mails", type=int, default=3, help="Number of emails to send defaults to 3")
    args = argparser.parse_args()

    if not args.num_mails or args.num_mails <= 0:
        raise ValueError("Number of mails must be a positive integer")

    LOGGER.info(f"Sending {args.num_mails} emails using Sendwithus API")
    mail_generator = SendwithusDataGenerator(number_of_mails=args.num_mails, esp_key=esp_key)
    mail_generator.send_mails(api_key)


if __name__ == "__main__":
    main()
