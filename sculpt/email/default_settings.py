# you should include these settings before overriding
# them with your project's settings; here is some
# example code:
#
# extra_settings = [
#     'sculpt.email.default_settings',
# ]
# import pkgutil
# for es in extra_settings:
#     pkg_loader = pkgutil.get_loader(es)
#     exec open(pkg_loader.filename, 'r') in globals()

# if this is set to True, then attempts to send email that
# fail will be quietly ignored; this should NEVER be set to
# True as a default, but it may be useful to do this during
# development until email credentials are properly set
SCULPT_EMAIL_FAIL_SILENTLY = False

# set this to a list of email addresses to capture all
# outbound email and direct it to the list instead (for
# debugging)
SCULPT_EMAIL_OVERRIDE_TOLIST = None

# by default email will appear to originate from a single
# (typically non-replyable) address; you can use a different
# setting from SERVER_EMAIL if you like so that your error
# emails can have a different origin address than your other
# user-facing emails
SCULPT_EMAIL_FROM = SERVER_EMAIL

# Email messages often need to refer to the site; this will
# require the hostname and the protocol. The default for
# this is the first permitted host name.
SCULPT_EMAIL_SITE_HOSTNAME = ALLOWED_HOSTS[0]

