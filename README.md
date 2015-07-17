sculpt-email
============

Email is a pain in the butt. On the one hand it's essential and expected, on the other it's a nuisance to deal with because Django's support for it is very basic.

Special Note
------------

This is not a complete project. There are no unit tests, and the only documentation is within the code itself. I don't really expect anyone else to use this code... yet. All of those things will be addressed at some point.

That said, the code _is_ being used. This started with work I did while at Caxiam (and I obtained a comprehensive license to continue with the code) so here and there are references to Caxiam that I am slowly replacing. I've done quite a bit of refactoring since then and expect to do more.

Features
--------

* With a single configuration setting, capture all outbound email messages and deliver them to a different destination address (e.g. the developer's personal address). Exceptionally useful for testing.
* Template-driven email messages.
    * Automatically look for HTML and plain-text email templates and assemble them correctly. This makes the choice of plain-text vs. HTML dependent on the templates present instead of a programming task, so you can prototype in plain text and build out HTML versions later without revisiting code.
* Allows SSL-wrapped SMTP conversations (e.g. for Amazon SES).
