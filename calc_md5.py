# coding:utf8
import os
from datetime import datetime
from hashlib import md5


class CalcMd5:
    def __init__(self):
        self.stop = 0
        self.count = 0
        self.total_size = 0
        self.s_size = 0
        self.run_size = 0

    def calc_md5(self, file_list):
        self.stop = 0
        self.count = 0
        self.total_size = 0
        calc = md5()
        f = []
        for value in file_list:
            if os.path.isdir(value):
                for root, dirs, files in os.walk(value):
                    if self.stop == 1:
                        break
                    for file in files:
                        name = os.path.join(root, file)
                        file_info = os.stat(name)
                        size = file_info.st_size
                        time = datetime.fromtimestamp(file_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S', )
                        f.append([name, size, time])
                        self.total_size += size
            else:
                name = os.path.join(value)
                file_info = os.stat(name)
                size = file_info.st_size
                time = datetime.fromtimestamp(file_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S', )
                f.append([name, size, time])
                self.total_size += size
        for file in f:
            self.s_size = file[1]
            self.run_size = 0
            try:
                with open(file[0], "rb") as f1:
                    while True:
                        if self.stop == 1:
                            break
                        chunk = f1.read(8192)
                        if not chunk:
                            break
                        calc.update(chunk)
                        self.run_size += len(chunk)
                        self.count += len(chunk)
            except:
                m = None
                self.count += file[1]
            m = calc.hexdigest().upper()
            yield file[0], file[1], file[2], m

    def set_stop(self, value):
        self.stop = value


if __name__ == '__main__':
    q = CalcMd5()
    for i in q.calc_md5(["d:\\"]):
        print(i)
    print(q.count)
    print(q.total_size)
