import numpy as np
from aiw_task_cm.file.file_manager import FileManager

class AwsFileManager(FileManager):

    def read(self, path, value, **kwargs):
        return AwsReader().read(path, value)

    def write(self, data, meta, path, **kwargs):
        return AwsReader().write(data, meta, path)


class AwsReader(object):

    def read(self, path, value):
        f = open(path, 'r')
        idx = 0
        meta = {}
        arr = []
        for line in f.readlines():
            line = line.replace(" ", "").strip().split(",")
            if idx != 0:
                for elm in line:
                    if self.is_number(elm):
                        arr.append(elm)
            else:
                meta_arr = []
                for elm in line:
                    if self.is_number(elm):
                        meta_arr.append(float(elm))
                meta['is_success'] = meta_arr[0]
                meta['stn_size'] = meta_arr[1]
                meta['width'] = meta_arr[2]
                meta['height'] = meta_arr[3]
                meta['resolution'] = meta_arr[6]
            idx += 1
        data = np.asarray(arr)
        data = data.astype(np.float)
        data = data.reshape(int(meta['height']) + 1, int(meta['width']) + 1)
        f.close()
        return data, meta

    def is_number(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def write(self, data, meta, path):
        b = '\n'.join(', '.join('%0.2f' % x for x in y) for y in data)
        f = open(path, 'w')
        f.write(str(b))
        f.close()
