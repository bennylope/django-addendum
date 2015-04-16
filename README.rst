===============
Django Addendum
===============

.. image:: https://api.travis-ci.org/bennylope/django-addendum.svg?branch=master
    :alt: Build Status
    :target: http://travis-ci.org/bennylope/django-addendum

.. image:: https://pypip.in/v/django-addendum/badge.svg
    :alt: Current PyPI release
    :target: https://crate.io/packages/django-addendum

.. image:: https://pypip.in/d/django-addendum/badge.svg
    :alt: Download count
    :target: https://crate.io/packages/django-addendum

Change snippets of copy on your site, on the fly, for any application, and
without a full-fledged CMS.

Solving queries like:

    Hey, we need to change the greeting on login from "Hi!" to "Sup?"

And:

    The footer copy needs to be updated.

And:

    The marketing team would really like to be able to change that message on a
    monthly basis. I don't care that that's a third-party appliwhoozitz!

This is all simple stuff and it's probably coded right into your templates.
Changing it is easy enough, but requires a developer and then a release. Boo!

Usage
=====

Just add `addendum_tags` to your templates::

    {% load addendum_tags %}

    {% snippet 'home:greeting' %}Hi!{% endsnippet %} {{ user.first_name }}

    <footer>
      {% snippet 'home:footer' %}&copy; 2011 by Acme Corp.{% endsnippet %}
    </footer>

Now you can edit content for these placeholders from the admin interface. If
you don't add anything or you delete text, the site text will always revert to
what is in the template.

Use it for small bits of user modifiable text from any template on your site,
and for swapping out -lorem ipsum- text when prototyping.

Find some more `information in the docs <https://django-addendum.readthedocs.org/en/latest/>`_

Installation
============

Install the package from PyPI::

    pip install django-addendum

Add it to your `INSTALLED_APPS` tuple::

    INSTALLED_APPS += ('addendum')

Sync your database or migrate if you have `South <south.readthedocs.org/en/latest/>`_ installed.

.. note::
    Django Addendum is not compatible with South versions prior to 1.0.

See the docs for upgrade notes.

Contributing
============

Contributions are welcome but should follow some basic guidelines to make life
easier:

- Pull requests should be made from distinct branches that include only the requested changes branched from the canonical master branch.
- Include tests for bug fixes and new features. Ensure that your Travis build is passing before submitting the pull request.
- Include documentation for any new features.
- For multi-commit updates please squash commits so the packager maintainer only has at most a few commits to review.
- Please limit changes to your specific pull request (excluding extraneous changes and please do not bump the version for your own changes).

License
=======

BSD licensed.
