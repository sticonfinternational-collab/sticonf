"""
Custom Django Email Backend that handles SSL certificate verification issues
Useful for development and environments with SSL certificate problems
"""

import ssl
import smtplib
from django.core.mail.backends.smtp import EmailBackend as DjangoSMTPBackend


class InsecureSMTPBackend(DjangoSMTPBackend):
    """
    SMTP backend that disables SSL certificate verification.
    Use this for development or when you have SSL certificate issues.
    
    WARNING: This is less secure. Only use for development or trusted networks.
    """
    
    def _get_connection(self):
        """Override to disable SSL certificate verification"""
        if self.connection is None:
            try:
                # Create SSL context that doesn't verify certificates
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                
                if self.use_tls:
                    # For TLS connections
                    self.connection = smtplib.SMTP(
                        self.host,
                        self.port,
                        timeout=self.timeout
                    )
                    self.connection.starttls(context=ssl_context)
                else:
                    # For SSL connections
                    self.connection = smtplib.SMTP_SSL(
                        self.host,
                        self.port,
                        timeout=self.timeout,
                        context=ssl_context
                    )
                
                if self.username and self.password:
                    self.connection.login(self.username, self.password)
                    
            except (smtplib.SMTPException, OSError) as err:
                if not self.fail_silently:
                    raise
                
        return self.connection


class SecureSMTPBackend(DjangoSMTPBackend):
    """
    SMTP backend with proper SSL certificate verification.
    Use this for production environments.
    """
    
    def _get_connection(self):
        """Override to ensure proper SSL certificate verification"""
        if self.connection is None:
            try:
                # Create SSL context with proper verification
                ssl_context = ssl.create_default_context()
                
                if self.use_tls:
                    # For TLS connections
                    self.connection = smtplib.SMTP(
                        self.host,
                        self.port,
                        timeout=self.timeout
                    )
                    self.connection.starttls(context=ssl_context)
                else:
                    # For SSL connections
                    self.connection = smtplib.SMTP_SSL(
                        self.host,
                        self.port,
                        timeout=self.timeout,
                        context=ssl_context
                    )
                
                if self.username and self.password:
                    self.connection.login(self.username, self.password)
                    
            except (smtplib.SMTPException, OSError) as err:
                if not self.fail_silently:
                    raise
                
        return self.connection
