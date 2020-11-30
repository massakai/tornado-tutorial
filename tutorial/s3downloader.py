import os.path
import shutil
import xml.etree.ElementTree
from dataclasses import dataclass
from datetime import datetime

import requests


@dataclass
class Object:
    key: str
    last_modified: datetime


class S3Reader:
    def __init__(self, endpoint_url, namespace):
        self.endpoint_url = endpoint_url
        self.namespaces = {"ns": namespace}

    def list_objects_v2(self, bucket):
        params = {
            "list-type": 2
        }
        response = requests.get(os.path.join(self.endpoint_url, bucket), params=params)
        if response.status_code != 200:
            raise RuntimeError((response.status_code, response.text))

        root = xml.etree.ElementTree.fromstring(response.content)
        return [
            Object(
                key=content.find("ns:Key", self.namespaces).text,
                last_modified=datetime.fromisoformat(
                    content.find("ns:LastModified", self.namespaces).text.replace("Z", "+00:00")))
            for content in root.findall("ns:Contents", self.namespaces)]

    def get_object(self, bucket, key):
        response = requests.get(os.path.join(self.endpoint_url, bucket, key), stream=True)
        return response.raw


def main():
    reader = S3Reader(
        "http://localhost:9000",
        namespace="http://s3.amazonaws.com/doc/2006-03-01/")

    bucket = "data"

    # バケットの一覧を取得する
    objects = reader.list_objects_v2(bucket)
    for obj in objects:
        print(obj)

    # 先頭のオブジェクトを/tmpにダウンロードする
    obj = objects[0]
    content = reader.get_object(bucket, obj.key)
    local_path = os.path.join("/tmp", os.path.basename(obj.key))
    with open(local_path, "wb") as f:
        shutil.copyfileobj(content, f)


if __name__ == "__main__":
    main()
