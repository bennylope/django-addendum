===============
Django Addendum
===============

Change snippets of copy on your site, on the fly, for any application, and
without a full-fledged CMS.

Solving queries like:

    Hey, we need to change the greeting on login from "Hi!" to "Sup?"

And:

    The footer copy needs to be udpated.

And:

    The marketing team would really like to be able to change that message on a
    monthly basis. I don't care that that's a third-party appliwhoozitz!

This is all simple stuff and it's probably coded right into your templates.
Changing it is easy enough, but requires a developer and then a release. Boo!

Usage
=====

Just add `addendum_tags` to your templates:

::

    {% load addendum_tags %}

    {% editable 'home:greeting' %}Hi!{% endeditable %} {{ user.first_name }}

    <footer>
      {% editable 'home:footer' %}&copy; 2011 by Acme Corp.{% endeditable %}
    </footer>

Now you can edit content for these placeholders from the admin interface. If
you don't add anything or you delete text, the site text will always revert to
what is in the template.

Use it for small bits of user modifiable text from any template on your site,
and for swapping out *lorem ipsum* text when prototyping.

Installation
============

Install the package from PyPI::

    pip install django-addendum

Add it to your `INSTALLED_APPS` tuple::

    INSTALLED_APPS += ('addendum')

Sync your database or migrate if you have `South
<south.readthedocs.org/en/latest/>`_ installed.

License
=======

BSD licensed.
