#
# Copyright 2022 DMetaSoul
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import random
import time

import consul


class Consul(object):
    def __init__(self, host, port, token=None):
        self._consul = consul.Consul(host, port, token=token)

    def setConfig(self, key, value):
        return self._consul.kv.put(key, value)

    def getConfig(self, key):
        index, data = self._consul.kv.get(key)
        return data['Value']

    def deletConfig(self, key):
        self._consul.kv.delete(key)


def putServiceConfig(config, host="localhost", port=8500, prefix="config", context="recommend", data_key="data"):
    client = Consul(host, port)
    key = "%s/%s/%s" % (prefix, context, data_key)
    num = 10
    while num > 0:
        if client.setConfig(key, config) and client.getConfig(key):
            print("set config to consul success!")
            break
        time.sleep(random.randint(1, 10))
        num -= 1
    if num <= 0:
        print("set config to consul fail!")

