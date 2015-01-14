sculpt-email
============

Email is a pain in the butt. On the one hand it's essential and expected, on the other it's a nuisance to deal with because Django's support for it is very basic.

Features
--------

* With a single configuration setting, capture all outbound email messages and deliver them to a different destination address (e.g. the developer's personal address).
* Template-driven email messages.
    * Automatically look for HTML and plain-text email templates and assemble them correctly. This makes the choice of plain-text vs. HTML dependent on the templates present instead of a programming task, so you can prototype in plain text and build out HTML versions later without revisiting code.
* Allows SSL-wrapped SMTP conversations (e.g. for Amazon SES).
* For tracking email addresses (commonly linked to user accounts), provides an abstract base model class that is useful.
