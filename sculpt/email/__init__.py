from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import TemplateDoesNotExist
from django.template.loader import get_template, select_template

from sculpt.common import Enumeration

import datetime
import re
import os
import os.path

# You will need to define some values in your settings file
# in order to use this, in addition to the regular email
# settings. See default_settings.py for instructions.
#
# Email templates are specified by folder; each folder is
# inspected to see what format the email message should be
# in. This makes it easy to prototype using plaintext mail
# and upgrade to HTML mail later. Within each folder:
#
#   subject.txt         subject line of message
#   body.txt            plain text body of message
#   body.html           HTML body of message
#
# All templates will be passed the same data. If you pass
# a request object, it will be given to the template to
# use for rendering.
#
# A list of template paths may be given instead of a
# single path. This is useful if there are multiple
# versions of an email template (for branding, translation,
# etc.)

# prep and send an email message
def send_mail(template_path, tolist, from_email = None, data = None, attachments = None, request = None):
    if not isinstance(tolist, (list,tuple)):
        tolist = [ tolist ]
    if from_email == None:
        from_email = settings.SCULPT_EMAIL_FROM
    if data == None:
        data = {}

    # make sure we have a list of template paths
    if isinstance(template_path, (list, tuple)):
        template_paths = template_path
    else:
        template_paths = [ template_path ]

    # create a full list of body templates we're looking for
    body_list = []
    for p in template_paths:
        body_list.append(os.path.join(p, 'body.html'))
        body_list.append(os.path.join(p, 'body.txt'))

    # fetch the templates
    subject_template = select_template([ os.path.join(p, 'subject.txt') for p in template_paths ])
    try:
        body_html_template = select_template([ os.path.join(p, 'body.html') for p in template_paths ])
    except TemplateDoesNotExist:
        body_html_template = None
    try:
        body_text_template = select_template([ os.path.join(p, 'body.txt') for p in template_paths ])
    except TemplateDoesNotExist:
        body_text_template = None

    if body_html_template is None and body_text_template is None:
        raise Exception('neither plain text nor HTML body could be found')

    # fill out the templates

    # we have additional data we need to supply, so that all
    # email templates can be rendered appropriately (e.g. HTML
    # templates need to know what external URL to use for any
    # images)
    data.update({
            'from_email': from_email,
            'site_hostname': settings.SCULPT_EMAIL_SITE_HOSTNAME,
            'site_url': settings.SCULPT_SITE_PROTOCOL + settings.SCULPT_EMAIL_SITE_HOSTNAME + '/',
            # these may not be available
            'MEDIA_URL': settings.MEDIA_URL,
            'STATIC_URL': settings.STATIC_URL,
        })

    # use the same context for subject and body
    subject = subject_template.render(data, request)

    if body_html_template is not None:
        body_html = body_html_template.render(data, request)
    else:
        body_html = None

    if body_text_template is not None:
        body_text = body_text_template.render(data, request)
    else:
        body_text = None

    # determine who to send it to
    if settings.SCULPT_EMAIL_OVERRIDE_TOLIST:
        print "[pid:%d]" % os.getpid(), "SENDING EMAIL TO " + repr(settings.SCULPT_EMAIL_OVERRIDE_TOLIST) + " instead of " + repr(tolist)
        tolist = settings.SCULPT_EMAIL_OVERRIDE_TOLIST
    else:
        print "[pid:%d]" % os.getpid(), "SENDING EMAIL TO " + repr(tolist)

    # generate the message
    message = EmailMultiAlternatives(
            subject = subject,
            body = body_text if body_text is not None else body_html,
            from_email = from_email,
            to = tolist,
        )
    if body_text is None:
        # we only have an HTML type
        message.content_subtype = 'html'    # main type is always 'text'
    
    elif body_html is not None:
        # we used the plain text, but we also have
        # an HTML version
        message.attach_alternative(body_html, 'text/html')

    # attach any files
    if attachments is not None:
        for a in attachments:
            message.attach(**a)

    # send the message
    message.send(fail_silently = settings.SCULPT_EMAIL_FAIL_SILENTLY)
