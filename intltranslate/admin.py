import os

from django.http import JsonResponse
from django.contrib import admin, messages
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin
from simpleui.admin import AjaxAdmin
from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse

from intltranslate import views
from intltranslate.models import LanguageApp
from intltranslate.utils import git_util, json_util


# APP语言包管理
@admin.register(LanguageApp)
class LanguageAppAdmin(ImportExportActionModelAdmin, AjaxAdmin):
    list_display = ('language', 'total_name', 'file_name', 'create_time', 'update_time')
    list_per_page = 20

    actions = ('get_remote_file', 'compare_file', 'download_compare_file','upload_translation_file', 'download_whole_file')

    # 从git拉取最新语言包
    def get_remote_file(self, request, queryset):
        app_url = 'https://gitee.com/wuxiangbin/simpleui/raw/master/'
        # 这里的upload 就是和params中配置的key一样
        ids = request.POST.getlist('_selected_action')
        for id in ids:
            employe = LanguageApp.objects.get(id=id)
            git_util.download_file_from_git(app_url, employe.file_name, "templates\\app_file\\")

        messages.add_message(request, messages.SUCCESS, '同步成功')


    get_remote_file.short_description = '更新语言包(从git拉取覆盖本地)'
    get_remote_file.type = 'success'
    get_remote_file.icon = 'el-icon-upload'
    get_remote_file.enable = True

    # 上传翻译好的文件,比对更新
    def upload_translation_file(self, request, queryset):
        idstr = request.POST.get('_selected')
        if idstr == None:
            return JsonResponse(data={
                'status': 'failed',
                'msg': '请选择1种需要更新的语言包!'
            })
        ids = idstr.split(",")
        print(len(ids))
        if len(ids) != 1:
            return JsonResponse(data={
                'status': 'failed',
                'msg': '请选择1种需要更新的语言包!'
            })

        employe = LanguageApp.objects.get(id=int(ids[0]))
        if employe == None:
            return JsonResponse(data={
                'status': 'failed',
                'msg': '当前语言语言包不存在!'
            })

        obj = request.FILES.get('upload')
        if obj == None:
            return JsonResponse(data={
                'status': 'warning',
                'msg': '请选择要上传的文件'
            })

        # 解析文件并写入本地
        json_util._update_file_data_from_excel(employe.file_name, obj)

    upload_translation_file.short_description = '上传翻译完成的文件'
    upload_translation_file.type = 'success'
    upload_translation_file.icon = 'el-icon-upload'
    upload_translation_file.enable = True

    upload_translation_file.layer = {
        'params': [{
            'type': 'file',
            'key': 'upload',
            'label': '文件'
        }]
    }

    # 比对两个语言包,并生成生成比对后的差异文件, 使用弹窗来做
    def compare_file(self, request, queryset):
        app_url = 'https://gitee.com/wuxiangbin/simpleui/raw/master/'
        # 这里的upload 就是和params中配置的key一样
        ids = request.POST.getlist('_selected_action')
        if len(ids) != 2:
            return JsonResponse(data={
                'status': 'failed',
                'msg': '请选择需要比对的两种语言'
            })
        for id in ids:
            employe = LanguageApp.objects.get(id=id)
            git_util.download_file_from_git(app_url, employe.file_name, "templates\\app_file\\")
            # Language.objects.create(
            #     name=employe.name,
            #     idCard=employe.idCard,
            #     phone=employe.phone,
            #     birthday=employe.birthday,
            #     department_id=employe.department_id
            # )

        messages.add_message(request, messages.SUCCESS, '同步成功')


    compare_file.short_description = '比对语言包'
    compare_file.type = 'success'
    compare_file.icon = 'el-icon-upload'
    compare_file.enable = True

    # 导出比对语言的结果
    def download_compare_file(self, request, queryset):
        app_url = 'https://gitee.com/wuxiangbin/simpleui/raw/master/'
        # 这里的upload 就是和params中配置的key一样
        ids = request.POST.getlist('_selected_action')
        if len(ids) != 2:
            return JsonResponse(data={
                'status': 'failed',
                'msg': '请选择需要比对的两种语言'
            })
        for id in ids:
            employe = LanguageApp.objects.get(id=id)
            git_util.download_file_from_git(app_url, employe.file_name, "templates\\app_file\\")
            # Language.objects.create(
            #     name=employe.name,
            #     idCard=employe.idCard,
            #     phone=employe.phone,
            #     birthday=employe.birthday,
            #     department_id=employe.department_id
            # )

        messages.add_message(request, messages.SUCCESS, '同步成功')


    download_compare_file.short_description = '导出语言包比对结果'
    download_compare_file.type = 'success'
    download_compare_file.icon = 'el-icon-upload'
    download_compare_file.enable = True

    # 导出完整语言包
    def download_whole_file(self, request, queryset):
        idstr = request.POST.get('_selected_action')
        ids = idstr.split(",")
        print(len(ids))
        if len(ids) != 1:
            return JsonResponse(data={
                'status': 'failed',
                'msg': '只能选择一种语言包!'
            })

        employe = LanguageApp.objects.get(id=int(ids[0]))
        if employe == None:
            return JsonResponse(data={
                'status': 'failed',
                'msg': '当前语言语言包不存在!'
            })
        file_name = employe.file_name
        return render(request, "download.html", {"file_name":file_name})

    download_whole_file.short_description = '导出完整语言包'
    download_whole_file.type = 'success'
    download_whole_file.icon = 'el-icon-upload'
    download_whole_file.enable = True