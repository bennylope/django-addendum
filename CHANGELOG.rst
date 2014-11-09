Changes
=======

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
