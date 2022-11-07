from datetime import datetime

# a = time.asctime()
# format_time = a.split()
# months = dict(zip(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], [i for i in range(1,13)]))
# format_time[2] = format_time[2].rjust(2,'0')
# print(format_time[4],months[format_time[1]],format_time[2])

a = datetime.today() - datetime(2022, 11, 6)
print(a.days)
