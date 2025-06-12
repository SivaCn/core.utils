# -*- coding: utf-8 -*-

"""

    Module :mod:``


    LICENSE: The End User license agreement is located at the entry level.

"""

# ----------- START: Native Imports ---------- #
import ast

from abc import ABC, abstractmethod
# ----------- END: Native Imports ---------- #

# ----------- START: Third Party Imports ---------- #
# ----------- END: Third Party Imports ---------- #

# ----------- START: In-App Imports ---------- #
from core.utils.constants import (
    const_states,
)

from core.utils.helpers.utils import (
    Http,
    DotDict,

    string_substitute,
)
# ----------- END: In-App Imports ---------- #

__all__ = [
    # All public symbols go here.
]


class SMSServiceProvider(ABC):

    @abstractmethod
    async def send(self, user, template_name: str, phone: str, **params) -> dict:
        pass


class Ozonetel(SMSServiceProvider):

    PROVIDER = 'ozonetel'

    def __init__(self, session: DotDict):
        self.session = session

    def normalize_phone_number(self, phone: str):
        return phone.replace('-', '')

    async def get_provider_config(self, template_name: str, phone: str, **params) -> dict:

        #
        # Method level imports, DONOT move out
        from core.db.statements import (
            stmt_query_sms_template,
            stmt_query_sms_provider,
            stmt_query_sms_provider_config,
        )

        config = {
            'headers': dict(),
            'data': None,
            'variables': {
                #
                # Destination Phone Number
                'destination_phone': phone
            }
        }

        sms_provider_cursor = await self.session.meta_read.execute(
            stmt_query_sms_provider(name=self.PROVIDER)
        )
        sms_provider = sms_provider_cursor.scalar_one_or_none()

        if not sms_provider:
            raise Exception(
                    f"{self.PROVIDER}: SMS provider does not exist"
            )

        config['sms_provider_id'] = sms_provider.sms_provider_id

        sms_template_cursor = await self.session.meta_read.execute(
            stmt_query_sms_template(name=template_name)
        )
        sms_template = sms_template_cursor.scalar_one_or_none()

        if not sms_template:
            raise Exception(
                f"SMS Template for name '{template_name}', does not exist"
            )

        #
        # Update Variables from SMS Template Config
        config['variables']['external_template_id'] = sms_template.external_template_id
        config['variables']['sms_content'] = sms_template.sms_content
        config['variables']['sms_type'] = sms_template.sms_type

        sms_provider_config_cursor = await self.session.meta_read.execute(
            stmt_query_sms_provider_config(sms_provider_id=sms_provider.sms_provider_id)
        )
        sms_provider_config = sms_provider_config_cursor.scalars().all()

        if not sms_provider_config:
            raise Exception(
                f"Configurations for the SMS Provider {self.PROVIDER} are missing"
            )

        for _config in sms_provider_config:
            if _config.config_type == 'CONFIG':
                config[_config.key] = _config.value

            if _config.config_type == 'HEADER':
                config['headers'][_config.key] = _config.value

            if _config.config_type == 'DATA':
                if config['data'] is not None:
                    raise Exception(
                        'Encountered Duplicate data arguments, recheck the configurations'
                    )

                config['data'] = _config.value

            if _config.config_type == 'VARIABLE':
                config['variables'][_config.key] = _config.value

        config['variables']['sms_content'] = string_substitute(
            config['variables']['sms_content'],
            {
                **config['variables'],
                **params,
            }
        )
        config['data'] = string_substitute(
            config['data'],
            config['variables']
        )

        config['data'] = ast.literal_eval(config['data'])

        return config

    async def send(self,
                   user,
                   template_name: str,
                   phone: str,
                   **params) -> dict:

        #
        # Method level Import
        from core.db.models.tenant import SmsLogModel

        config = await self.get_provider_config(
            template_name=template_name, phone=phone, **params
        )

        http = Http()
        sms_response = http.post(
            url=config['url'], headers=config['headers'], data=config['data']
        ).json()
        '''{'status': 'success', 'message': 'queued', 'refrenceID': '234974722581-ickjatmeltk8aufl26e3nbprv2'}
        '''

        sms_log = SmsLogModel(
            user_id=user.user_id,
            sms_provider_id=config['sms_provider_id'],
            reference_id=sms_response['refrenceID'],
            status=const_states.QUEUED,
            initial_response=sms_response,
        )
        self.session.tenant_write.add(sms_log)
        await self.session.tenant_write.flush()

        return sms_response

    async def send_login_otp(self, user, phone: str, otp: str):

        response = await self.send(
            user=user,
            template_name='LOGINOTP',
            phone=self.normalize_phone_number(phone),
            otp=otp
        )

        return response


def get_sms_provider(session: DotDict) -> SMSServiceProvider:

    return Ozonetel(session=session)

