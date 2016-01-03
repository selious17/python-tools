#!/usr/bin/python
# -*- coding: utf-8 -*-
# vim: fileencoding=utf-8
# パイソンスクリプト

import os , sys , codecs , re , csv

TARGET_ENCODINGS = [
    'utf-8',
    'shift-jis',
    'euc-jp',
    'iso2022-jp'
]
FLAG_STDOUT = True
OUTPUT_FILE_NAME = 'result.csv'

def guess_charset(data):
    file = lambda d, encoding: d.decode(encoding) and encoding
    for enc in TARGET_ENCODINGS:
        try:
            file(data, enc)
            return enc
        except:
            pass
    return 'binary'


def search_keyword(dir_name, keyword):

    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
    std_out = sys.stdout.write

    f_out = codecs.open(OUTPUT_FILE_NAME, 'w', 'utf-8')
    f_out.write('file_name,file_full_path,line_number,target_line\n')

    for dirpath, dirs, files in os.walk(dir_name):
        for fn in files:
            path = os.path.join(dirpath, fn)
            fobj = file(path, 'rU')
            data = fobj.read()
            fobj.close()
            base, ext = os.path.splitext(fn)
            try:
                enc = guess_charset(data)
            except:
                continue
            if enc == 'binary':
                continue
            count = 0
            try:
                for l in codecs.open(path, 'r', enc):
                    count = count + 1
                    if keyword in l:
                        out_w = ''
                        try:
                            out_w = fn + "," + path  + "," + str(count) + "," + l.strip() + '\n'
                        except:
                            continue
                        if FLAG_STDOUT:
                            std_out(out_w)
                        f_out.write(out_w)
            except:
                continue
    f_out.close()


if __name__ == "__main__":

    params = sys.argv # コマンドライン引数を取得
    argc = len(params) # コマンドライン引数の個数を取得

    if (argc < 3): # コマンドライン引数の個数が２つ未満の場合、使い方を出力して終了
        print 'Usage: # python %s directory_name search_keyword' % params[0]
        quit()

    search_keyword(params[1], params[2])

