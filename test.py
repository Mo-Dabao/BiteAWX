from BiteAWX import AWX
path_awx = './test_data/C002_20190302081500_FY4A.AWX'
awx = AWX(path_awx)
print(awx.head1, '\n')
print(awx.head2, '\n')
print(awx.head3)
awx.DataArray()