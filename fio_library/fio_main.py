

import ExcelWriter

'''

'''

test_log_name = 'test_log'
test_log_path = '/home/zdc/libaio/read/nvme0n1_SSD_test/2022-11-13/Seqread/bs4k/ssd_testLogNumjobs1/QD1/time12000/test_log'

def main():
    ExcelWriter.ExcelWriter(
            test_log_name,
            test_log_path

    )
    return 'Pass'


if __name__ == '__main__':
    result_main = main()

    print(result_main)