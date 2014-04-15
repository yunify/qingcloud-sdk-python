=====================
QingCloud Python SDK
=====================

This repository allows you to access `QingCloud <https://www.qingcloud.com>`_
and control your resources from your applications.

This SDK is licensed under
`Apache Licence, Version 2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>`_.

.. note::
  Requires Python 2.6 or higher, for more information please see
  `QingCloud SDK Documentation <https://docs.qingcloud.com/sdk/>`_


------------
Installation
------------

Install via `pip <http://www.pip-installer.org>`_ ::

    $ pip install qingcloud-sdk

Upgrade to the latest version ::

    $ pip install --upgrade qingcloud-sdk

Install from source ::

    git clone https://github.com/yunify/qingcloud-sdk-python.git
    cd qingcloud-sdk-python
    python setup.py install


---------------
Getting Started
---------------

You need apply **access key** on
`qingcloud console <https://console.qingcloud.com>`_ first,
then pass them into method ``connect_to_zone`` to create connection ::

  >>> import qingcloud.iaas
  >>> conn = qingcloud.iaas.connect_to_zone(
          'zone id',
          'access key id',
          'secret access key'
      )

The variable ``conn`` is the instance of ``qingcloud.iaas.connection.APIConnection``,
we can use it to call resource related methods.

Example::

  # launch instances
  >>> ret = conn.run_instances(
          image_id='centos58x64',
          cpu=1,
          memory=1024
        )

  # stop instances
  >>> ret = conn.stop_instances(
          instances=['i-1234abcd'],
          force=True
        )

  # describe instances
  >>> ret = conn.describe_instances(
          image_id='centos58x64',
          status=['running', 'stopped']
        )
