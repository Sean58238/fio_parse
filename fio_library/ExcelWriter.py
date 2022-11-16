"""
本文件是对不同fio log文件内的数据写入excel 函数封装
"""
import warnings
import xlsxwriter
import logging
import time, os
from pathlib import Path
warnings.simplefilter("ignore", ResourceWarning)


class ExcelWriter:
    """ 创建Excel 保存fio性能测试log数据
        fio_excel_testlog_name(str): Excel保存文件的名称
        fio_testlog_dir(str): fio testlog日常文件路径 

    """
    def __init__(self, fio_excel_testlog_name=None, fio_testlog_dir=None):
       
        # global log
        # log = logging.getLogger('fio')

        self.log_name = fio_excel_testlog_name
        self.fio_testlog_dir = fio_testlog_dir

        self.workbook = xlsxwriter.Workbook(fio_excel_testlog_name, {'strings_to_numbers': True, 'constant_memory': True})

        print('Excel output file name: {}'.format(fio_excel_testlog_name))
        print('Excel output file name: {}'.format(fio_testlog_dir))
        self.import_test_log_file(fio_excel_testlog_name, fio_testlog_dir)
        # self.import_view('system')

        # self.sort_sheets()

        try:
            start_time = time.time()
            self.workbook.close()
            print('Wrote Excel file in {}'.format(time.time() - start_time))
        except Exception as e:
            print('Error in generating Excel file: {}'.format(e))


    def import_test_log_file(self, name=None, file_path=None):
        '''
         读取test_log.txt 性能数据 写入execl
        '''
        # print(file_path)
        testlog = os.listdir(file_path)[0]
        # print(testlog)
        if not file_path + '/' + testlog or not Path(file_path + '/' + testlog).is_file():
            print('{} file does not exist.'.format(name))
            return

        print('     importing {}'.format(name))
        
        with open(file=file_path + '/' + testlog) as F:
            sheet, fmt = self.get_sheet_and_format(name, '#228B22', 10, '#,##0')
            for row_index, line in enumerate(F, 0):
                print(row_index)
                # print(line)
                log_json = self.testlog_split(line)
                print(log_json)
                # for row in range(row_index + len(log_json)):
                #     for log_json_index in range(len(log_json)):
                #         sheet(row, 1, )

    def testlog_split(self, split_data):
        '''
         分割日志行信息： 待开发
        '''
        split_json = {}
        if 'rw' in split_data and 'bs' in split_data and 'ioengine' in split_data and ' iodepth' in split_data:
            
            split_json['test_name'] = split_data.split(':')[0]
            split_json['g'] = split_data.split(':')[1][-2]
            split_json['rw'] = split_data.split(':')[2].split(',')[0].split('=')[1]
            split_json['bs'] = ''.join(split_data.split(':')[2].split(',')[1:4])[4:]

            split_json['ioengine'] = split_data.split(':')[2].split(',')[-2].split('=')[1]
            split_json['iodepth'] = split_data.split(':')[2].split(',')[-1].split('=')[1].rstrip("\n")

        elif 'fio' in split_data:
            split_json['version'] = split_data.rstrip("\n")

        elif 'groupid' in split_data and 'jobs' in split_data and 'err' in split_data and 'pid' in split_data:
            print(split_data.split(':'))
            
        return  split_json
        
    def get_sheet_and_format(self, name, tab_color, font_size, num_format, font = 'Calibri'):
        '''
         设置excel 表格风格
        '''
        worksheet = self.workbook.add_worksheet(name)
        worksheet.set_tab_color(tab_color)
        format = self.workbook.add_format({'num_format': num_format, 'font_size': font_size, 'font_name': font})
        return worksheet, format