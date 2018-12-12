from frontend.models import TestResult

# def insert_records():
t = []
for i in range(0,100):
    t.append(TestResult(common_name='hogehoge.com',filename_crt='hogehoge.com_20191031.crt',filename_incrt='hogehoge.com_20191031.incrt',filename_key='hogehoge.com_20191031.key',is_test_result=True))
    t[i].save()
