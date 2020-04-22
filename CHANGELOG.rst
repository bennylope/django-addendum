Changes
=======

0.6.0
-----

* Drop Python 2 and Django 1.11 support
* Add Django 2, 3 support

0.5.2
-----

* Fix issue in which variables may be explicitly boolean in render method

0.5.1
-----

* Fix a packaging error

0.5.0
-----

* Removes South support!
* Django 1.8 and 1.11 support only for now
* MAJOR: updates behavior for templated snippets to prevent template errors
  from bubbling up.

0.4.0
-----

* Drop support for Django 1.4
* Packaging fix
* Automatically create missing Snippet instances
* Bug fixes for cache invalidation, admin langauges, text autoescaping

0.3.5
-----

* Fixes migration issue (possibly breaking for some users): the field choices
  as provided in the SnippetTranslation model populated a new migration when
  installed in a project, and these noticeably changed after an update to the
  project's testing framework. This was 'fixed' by removing the choices from
  the model to a ModelForm class, but users with 0.3.4 installed might have an
  extra migration. Only affects Django 1.8+.

0.3.4
-----

* Address bad data included in Wheel package

0.3.3
-----

* Fix project homepage URL

0.3.2
-----

* Bug fix in cache value return
* Adds Django 1.8 testing

0.3.1
-----

* Formatting fixes

0.3.0
-----

* Adds multilingual (i18n) support
* Adds management command for updating cache
* Removes support for Python 2.6 and Django 1.5

0.2.0
-----

* Length key from 100 chars to 250
* Test against Django 1.7

0.1.0
-----

* Updated docs
* Explicitly allow template variable names to be passed as snippet key
  arguments.

0.0.5
-----

* Added template rendering for snippet content.
* Changed keyword argument from 'richtext' to 'safe' to better align with
  Django templating conventions. 'richtext' is still allowed though.

0.0.4
-----

* **WARNING** wipes out migrations to remove key swapping migration, start from
  scratch
