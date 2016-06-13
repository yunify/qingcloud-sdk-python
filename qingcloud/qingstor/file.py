# =========================================================================
# Copyright 2015 Yunify, Inc.
# -------------------------------------------------------------------------
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this work except in compliance with the License.
# You may obtain a copy of the License in the LICENSE file, or at:
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =========================================================================

from StringIO import StringIO
import os
import sys

from qingcloud.qingstor.bucket import Bucket
from qingcloud.qingstor.connection import QSConnection


try:
    from errno import EINVAL
except ImportError:
    EINVAL = 22

try:
    from errno import EEXIST
except ImportError:
    EEXIST = 47

try:
    from errno import ENOENT
except ImportError:
    ENOENT = 2

try:
    from errno import EIO
except ImportError:
    EIO = 5


class QSFileError(IOError):

    def __init__(self, errno=0, strerror=''):
        IOError.__init__(self, errno, strerror)


class FileBase(object):
    '''Base class of InputFile and OutputFile,
    implement some common functions.
    '''

    def __init__(self, zone=None, access_key_id=None, access_key=None):
        self.zone = zone
        self.access_key_id = access_key_id
        self.access_key = access_key
        self._closed = True
        self.key = None

        if not zone:
            raise QSFileError(EINVAL, 'zone must be specified')

        self.conn = QSConnection(
            qy_access_key_id=access_key_id, qy_secret_access_key=access_key,
            host=zone + ".qingstor.com")

    def open(self, bucket=None, key=None, create=False):
        if not bucket:
            raise QSFileError(EINVAL, 'bucket must be specified')

        if not key:
            raise QSFileError(EINVAL, 'key must be specified')

        self.bucket = Bucket(self.conn, bucket)
        self.key = self.bucket.get_key(key, validate=False)
        self._closed = False

    def _reset(self):
        '''  Response data will be buffered in the connection,
        so we cannot abandon the response and reuse the connection without
        reading all response. Sometimes the response is huge.
          Abandon the connection and reset it to another one,
        we can issue a new request immediately.
        '''
        self._complain_ifclosed()

        conn = QSConnection(
            qy_access_key_id=self.access_key_id, qy_secret_access_key=self.access_key,
            host=self.zone + ".qingstor.com")
        self.bucket = Bucket(conn, self.bucket.name)
        self.key = self.bucket.get_key(self.key.name, validate=False)

    def close(self):
        self.bucket = None
        self.key = None
        self._closed = True

    def _complain_ifclosed(self):
        if self._closed:
            raise ValueError, "I/O operation on closed file"


class InputFile(FileBase):

    def __init__(self, zone=None, access_key_id=None, access_key=None):
        '''Create a file object to read from QingStor.
        '''
        FileBase.__init__(self,
                          zone=zone, access_key_id=access_key_id, access_key=access_key)
        self.length = None
        self.offset = 0
        self.response = None

        self.debug_inject = None

        if '__QINGSTOR_FILE_DEBUG_INJECT' in os.environ:
            self.debug_inject = os.environ['__QINGSTOR_FILE_DEBUG_INJECT']

    def open(self, bucket=None, key=None):
        '''Open the file object to read with given key in QingStor.
        '''
        FileBase.open(self, bucket=bucket, key=key, create=False)
        try:
            self.length = None
            self.offset = 0
            self._request(self.offset)
        except Exception:
            self.close()
            raise

    def read(self, size=None):
        '''Read data from QingStor.
        Return empty string at the end of file.
        '''
        self._complain_ifclosed()

        if size is not None and size <= 0:
            raise QSFileError(EINVAL, 'size must be a positive value')

        retry = 3

        while True:
            amt = self.length - self.offset

            if size is not None:
                amt = amt if amt < size else size

            if amt == 0:
                return ''

            if not self.response:
                self._request(self.offset)

            try:
                if self.debug_inject and retry == 3:
                    self._inject_exception()

                data = self.response.read(amt)
                self.offset += len(data)
                return data
            except Exception as e:
                self._reset()
                retry = retry - 1

                if retry <= 0:
                    raise QSFileError(EIO, str(e))

    def _request(self, offset):
        if offset == 0:
            self.key.open_read()
        else:
            headers = {"Range": "bytes=%d-" % offset}
            self.key.open_read(headers)

        self.response = self.key.resp
        length = offset + int(self.response.getheader('content-length'))

        if self.length is not None and self.length != length:
            raise RuntimeError('file length changed')

        self.length = length

    def _inject_exception(self):
        if self.offset % int(self.debug_inject) == 0:
            sys.stderr.write(
                "inject exception, offset: %s\n" % str(self.offset))
            raise QSFileError(EIO, "fault injection")

    def _reset(self):
        FileBase._reset(self)

        if self.response:
            self.response.close()
            self.response = None

    def close(self):
        '''Close the file.
        '''
        if self.response:
            self.response.close()
            self.response = None

        self.offset = 0
        FileBase.close(self)


class OutputFile(FileBase):

    def __init__(self, zone=None, access_key_id=None, access_key=None):
        '''Create a file object to write into QingStor.
        '''
        FileBase.__init__(self,
                          zone=zone, access_key_id=access_key_id, access_key=access_key)
        self.uploader = None
        self.buffer = None
        self.current_part = 0
        self.parts = None

    def open(self, bucket=None, key=None):
        '''Open the file object to write with given key in QingStor.
        '''
        FileBase.open(self, bucket=bucket, key=key, create=True)
        try:
            self.buffer = StringIO()
            self.uploader = self.bucket.initiate_multipart_upload(key_name=key)
            self.current_part = 0
            self.parts = []
        except Exception:
            self.abort()
            raise

    def write(self, str):
        '''Write data into QingStor.
        '''
        self._complain_ifclosed()

        self.buffer.write(str)

        if self.buffer.tell() >= 4 * 1024 * 1024:
            self._upload()

    def _upload(self):
        try:
            self.buffer.seek(0)
            self.parts.append(self.uploader.upload_part_from_file(
                self.buffer.getvalue(), self.current_part))
            self.buffer.truncate(0)
            self.current_part += 1
        except Exception:
            self.abort()
            raise

    def abort(self):
        '''Abort the write, delete the partial object on QingStor.
        '''
        if self.buffer:
            self.buffer.close()

        self.buffer = None

        if self.uploader:
            try:
                self.uploader.cancel_upload()
            except Exception:
                pass

        self.uploader = None
        self.current_part = 0
        self.parts = None
        FileBase.close(self)

    def close(self):
        '''Close the file and finish the write.
        Object will finally be created on QingStor after close.
        '''
        try:
            if self.buffer and self.buffer.tell() > 0:
                self._upload()

            if self.uploader:
                self.uploader.complete_upload(self.parts)
                self.uploader = None

            if self.buffer:
                self.buffer.close()
                self.buffer = None

            self.current_part = 0
            self.parts = None
            FileBase.close(self)
        except Exception:
            self.abort()
            raise
