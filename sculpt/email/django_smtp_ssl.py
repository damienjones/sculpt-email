# this code comes from the net, as part of an explanation of how to
# get SMTP working with Amazon (which requires SSL)

# NOTE: Django supposedly supports SSL- and TLS-wrapped email, but
# their code doesn't seem to work with Amazon SES. This does.

import smtplib

from django.core.mail.utils import DNS_NAME
from django.core.mail.backends.smtp import EmailBackend

class SSLEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False
        try:
            self.connection = smtplib.SMTP_SSL(
                    self.host, self.port,
                    local_hostname = DNS_NAME.get_fqdn(),
                )
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except:
            if not self.fail_silently:
                raise
