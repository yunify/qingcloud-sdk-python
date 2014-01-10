
此项目是 `QingCloud 青云 <https://www.qingcloud.com>`_ 的 Python 开发包
(Software Development Kit)，可以利用它对青云的资源进行查看、创建和操作，
借此开发出更富创造力的产品。

.. note:: 更多文档及样例可查看
  `QingCloud SDK 文档 <https://docs.qingcloud.com/sdk/>`_


------------
Installation
------------

可使用 ``pip`` 安装::

    $ pip install qingcloud-sdk

如果不是在 ``virtualenv`` 上安装，则需要 ``sudo`` ::

    $ sudo pip install qingcloud-sdk

如果你已安装 qingcloud-sdk 并需要更新到最新版本，则可以::

    $ pip install --upgrade qingcloud-sdk


---------------
Getting Started
---------------

使用 qingcloud-sdk 前请先在
`青云控制台 <https://console.qingcloud.com>`_ 申请 access key 。

申请 access key 后，便可开始建立连接::

  >>> import qingcloud.iaas
  >>> conn = qingcloud.iaas.connect_to_zone(
          'pek1',
          'access key id',
          'secret access key'
      )

代码中得到的 ``conn`` 是 APIConnection 的实例，所有操作都可通过它来调用。

APIConnection 中各操作函数的返回值是根据 API 返回的 JSON 数据转换而成的 ``dict`` 。
具体返回内容可参见 `API 文档 <https://docs.qingcloud.com/api/>`_ 中对应指令。

Example::

  # 创建一台主机
  >>> ret = conn.run_instances(
          image_id='centos58x64',
          instance_type='small_b'
        )
