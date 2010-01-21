Definition of Done
==================

All code SHOULD be in Python.

All necessary steps to run the code MUST be defined in the package. This SHOULD
be done in code (i.e., have a script to download all the necessary database
files and what not. If not convenient, this should be a part of INSTALL).

Python Standards
-----------------

- Follow PEP 8 http://www.python.org/dev/peps/pep-0008/. The parts marked "pet
  peeves" is optional as is limiting yourself to 79 chars per line.

- All functions must be documented, except if they are internal. Internal
  functions MUST be named with a leading underscore (for ``_example``) and MUST
  never be used outside of the file that defines them (or they stop being
  internal).


Doc strings
-----------

Doc strings should be of the form::

    def function(arg1, arg2=None):
        '''
        ret_value = function(arg1, arg2={+infinity})

        Computes something

        ``function`` computes a very useful....
        ..........

        For details see http://my.reference.to/the/algorithm

        Parameters
        ----------
          arg1 : integer
          arg2 : string (default: +infinity)
        Returns
        -------
           ret_value : integer
        '''

This is:

- text is restructured text
- first line is an example function call. Some guides recommend *against* this
  as redundant, but it is more consistent and you can add information. In this
  case, I added the fact that there is a return value and that ``arg2`` is, by
  default, + infinity even that is implemented as a None.
- Second line is a one to two-line description.
- Then as much text as you want. Include references if any.
- Parameter section and Return value section. They must be named ``Parameter``
  and ``Returns`` and must have the form ``xx : explanation``.
  
There is software to process these, which is why we need to adhere so closely to
a fixed standard.

Try to give hard instead of soft documentation (i.e., what are the types, the
corner cases, instead of generalities like "you can use this function in your
programmable toaster" which would belong in more general documentation).

Testing
-------

Each public function with more than 3 lines should have at least a test to
verify that it runs. These catch at least the typos, which is surprisingly
helpful.

Any bug we catch should be turned into a test case for regression testing.

We are going to use `nosetest
<http://somethingaboutorange.com/mrl/projects/nose/>`_ as a framework. Tests
should be in a separate directory called ``test``.

Tests cannot be deleted unless they become irrelevant (if they test a function
that is removed or if we decided to change the functionality of something).
Milestones are not reached unless all tests are clean.

