# -*- coding: utf-8 -*-

"""

    Module :mod:``

    This Module is created to...

    LICENSE: The End User license agreement is located at the entry level.

"""

# ----------- START: Native Imports ---------- #
import os

from typing import Optional, List, Any
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
import mandrill
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.error import BadArgumentError

from core.utils.helpers.environ import (
    get_build_config,
)
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


email_config = get_build_config(section='email-config')
yellow_config = get_build_config(section='yellow-config')


class EmailRecipientType:
    email: str
    name: Optional[str] = None


def send_email(
        recipients: List[EmailRecipientType],
        subject: str,
        html_content: Optional[str]=None,
        text_content: Optional[str]=None,
        tags: Optional[List[str]]=None,
) -> List[Any]:

    if not html_content and not text_content:
        raise BadArgumentError(
            'Argument either html_content or text_content should be supplied, Got None'
        )

    recipients_detail = [
        {
            'type': 'to',
            'email': recipient['email'],
            'name': recipient['name'] or '',
        }
        for recipient in recipients
    ]

    result = list()

    for retry_attempt in range(3):

        # Initialize Mandrill client
        mandrill_client = mandrill.Mandrill(os.getenv('MANDRILL_API_KEY'))

        # Send email through Mandrill
        message = {
            'html': html_content,
            'text': text_content,
            'subject': subject,
            'from_email': email_config.sender_email_id,
            'from_name': yellow_config.company_name,
            'to': recipients_detail,
            'important': True,
            'track_opens': True,
            'track_clicks': True,
            'tags': tags or list(),
            'metadata': {
                'website': yellow_config.yellow_website
            }
        }

        try:
            # Send the message
            result = mandrill_client.messages.send(message=message)
            '''
            >>> result
            [{'email': 'siva@getyellow.in', 'status': 'sent', '_id': '8e5b579530c84724997119f8296a1bd8', 'reject_reason': None, 'queued_reason': None}]
            '''

            #
            # Skip re-attempt when succeeded
            break

        except mandrill.Error:
            if retry_attempt == 2:
                raise

    return result

