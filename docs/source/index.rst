.. swingmusic documentation master file, created by
   sphinx-quickstart on Mon May 19 14:36:22 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

swingmusic documentation
========================

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.



Quickstart
----------

.. tab-set::


   .. tab-item:: Download

      Download the latest build for your system from `swingmusic Github <https://github.com/swingmx/swingmusic/releases>`_
      You can now start swingmusic with launching your build file.

   .. tab-item:: Pypi

      Open a terminal and type:

      .. code-block:: bash

         pip install swingmusic
         swingmusic


   .. tab-item:: Github releases

         Download the latest wheel from `here <https://github.com/swingmx/swingmusic/releases>`_ and then:

         .. code-block:: bash

            pip install swingmusic-<version>-py3-none-any.whl
            swingmusic

   .. tab-item:: By source

      .. code-block:: bash

         git clone https://github.com/swingmx/swingmusic.git
         cd swingmusic
         pip install .
         swingmusic


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   architecture
   apidocs/index



.. todo::
   :collapsible: open

   * Installation from build, pypi, source
   * How to launch
   * Config file location
   * Configs
   * * Streaming
   * * Watchdog
   * Project architecture
   * What is executed when and why