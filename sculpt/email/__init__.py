from django.conf import settings
from django.core.mail import send_mail as django_send_mail, EmailMultiAlternatives
from django.db import models
from django.template import Context
from django.template.loader import get_template, select_template

import datetime
import os
import os.path

# You will need to define some values in your settings file
# in order to use this, in addition to the regular email
# settings.
#
#   SCULPT_EMAIL_FROM               sender address for email (not the same as mail server username)
#   SCULPT_EMAIL_OVERRIDE_TOLIST    if set, replaces ALL email destination addresses with this list (for debugging)
#   SCULPT_EMAIL_TEMPLATE_BASE      base directory in templates that contains email
#   SCULPT_EMAIL_FAIL_SILENTLY      whether to ignore errors in email; DO NOT set True for production
#   SCULPT_EMAIL_USE_BRANDING       whether to use branding in template paths
#   SCULPT_EMAIL_SITE_HOSTNAME      hostname to pass in context data to templates
#
# Email templates are stored in folders, in this hierarchy:
#
#   <email_template_base>/email/<template_path>/<brand>/subject.txt         subject line of message
#   <email_template_base>/email/<template_path>/<brand>/body.txt            plaintext body of message
#   <email_template_base>/email/<template_path>/<brand>/body.html           HTML body of message (TODO)
#
# The default <brand> is "base". If branding is turned off,
# the brand folder level is omitted.
#
# All templates will be passed the same data, and ONLY
# that data; this is not a RequestContext so will not have
# any template context processors applied to it. You may
# also pass in a Context-derived object and it will be
# passed as-is, so you can pass a RequestContext if you
# like.

# prep and send an email message
def send_mail(template_path, tolist, from_email = None, data = None, brand = None):
    if from_email == None:
        from_email = settings.SCULPT_EMAIL_FROM
    if data == None:
        data = {}

    # make sure the path has been lower-cased
    template_path = os.path.join(settings.SCULPT_EMAIL_TEMPLATE_BASE, 'email', template_path.lower())

    # decide if we're looking for a brand-specific template or not
    if not settings.SCULPT_EMAIL_USE_BRANDING:
        template_paths = [ template_path ]
    elif brand == None:
        template_paths = [ os.path.join(template_path, 'base') ]
    else:
        template_paths = [ os.path.join(template_path, brand), os.path.join(template_path, 'base') ]

    body_list = [ os.path.join(p, 'body.txt') for p in template_paths ]
    body_list.extend([ os.path.join(p, 'body.html') for p in template_paths ])

    # fetch the templates
    subject_template = select_template([ os.path.join(p, 'subject.txt') for p in template_paths ])
    body_template = select_template(body_list)

    # If you include the file html_type inside one of the
    # appropriate folders, then it will render out as an HTML
    # email
    # If the templates do not exist they will throw a template not found error
    html_type = False
    if ody_template.name.endswith('.html'):
        html_type = True

    # fill out the template

    # we'd love to use RequestContext but we don't have request
    # this deep in the call stack; we hope that if someone needs
    # that they will create a RequestContext object and pass it
    # as data
    if not isinstance(data, Context):
        data = Context(data)

    # we have additional data we need to supply, so that all
    # email templates can be rendered appropriately (e.g. HTML
    # templates need to know what external URL to use for any
    # images, if the receiving client permits them)
    data.update({
            'from_email': from_email,
            'site_hostname': settings.SCULPT_EMAIL_SITE_HOSTNAME,
            'site_url': settings.SCULPT_SITE_PROTOCOL + settings.SCULPT_EMAIL_SITE_HOSTNAME + '/',
        })

    # use the same context for subject and body
    subject = subject_template.render(data)
    body = body_template.render(data)

    # send the email
    if settings.SCULPT_EMAIL_OVERRIDE_TOLIST:
        print "[pid:%d]" % os.getpid(), "SENDING EMAIL TO " + repr(settings.SCULPT_EMAIL_OVERRIDE_TOLIST) + " instead of " + repr(tolist)
        tolist = settings.SCULPT_EMAIL_OVERRIDE_TOLIST
    else:
        print "[pid:%d]" % os.getpid(), "SENDING EMAIL TO " + repr(tolist)

    # If it's an html type email then it will need to adjusted so
    # that it's sending it out via the EmailMultiAlternatives type,
    # rather than plain text.
    if html_type:
        msg = EmailMultiAlternatives(subject, body, from_email, tolist)
        msg.content_subtype = 'html'    # Main content is now text/html
        msg.send(fail_silently = settings.SCULPT_EMAIL_FAIL_SILENTLY)

    else:
        django_send_mail(subject, body, from_email, tolist, fail_silently = settings.SCULPT_EMAIL_FAIL_SILENTLY)
