from django.shortcuts import render
import json
import urllib.request
import xlsxwriter
import os
import datetime
from pages.models import Course

# Viết phương thức xuất excel

def ghi_tap_tin(duong_dan,list_ghi):
	workbook = xlsxwriter.Workbook(duong_dan)
	worksheet = workbook.add_worksheet()
	# Iterate over the data and write it out row by row
	row = 0
	for item in list_ghi:
		i = 0
		while i < len(item):
			worksheet.write(row,i,item[i])
			i += 1
		row += 1
	workbook.close()
	return


# Viết phương thức chart để gửi dữ liệu tạo biểu đồ

def chart(request):
	pro_list= Course.objects.order_by("name")
	ten = []
	gia = []
	for entry in pro_list:
		ten.append(entry.name)
		gia.append(entry.price)
	gia_1 = {
		"name":"Giá",
		"data":gia,
		"color":"red"
	}
	chart = {
		"chart":{"type":"column"},
		"title":{"text":"Price of Courses"},
		"xAxis":{"categories":ten},
		"series":[gia_1]
	}
	dump = json.dumps(chart)

	# xuất excel
	chuoi_tap_tin = ""
	time_now = datetime.datetime.now()
	list_danh_sach_course = []
	list_tieu_de = ["id","name","price","description"]
	list_danh_sach_course.append(list_tieu_de)
	for item in pro_list:
		coures = [item.id,item.name,item.price,item.description]
		list_danh_sach_course.append(coures)
	if request.method == "POST":
		ten_tap_tin = "danh_sach_course_" + time_now.strftime("%d-%m-%Y-%H-%M-%S" + ".xlsx")
		desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]),"Desktop")
		duong_dan = desktop + "\\" + ten_tap_tin
		ghi_tap_tin(duong_dan,list_danh_sach_course)
		chuoi_tap_tin = "Đã lưu tập tin tại: " + duong_dan


	return render(request,"chart/chart.html",{"chart":dump, "result":chuoi_tap_tin})



