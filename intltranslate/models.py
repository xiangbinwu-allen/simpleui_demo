from django.db import models



# app语言包管理类
class LanguageApp(models.Model):
    language = models.CharField(max_length=5, verbose_name='小语种', unique=True)
    total_name = models.CharField(max_length=256, verbose_name='中文描述', null=True, blank=True)
    file_name = models.CharField(max_length=256, verbose_name='文件名称')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now_add=True)

    def save(self, *args, **kwargs):
        # 将Markdown格式 转为html，页面上显示
        super(LanguageApp, self).save(*args, **kwargs)

    def update(self, *args, **kwargs):
        super(LanguageApp, self).update(*args, **kwargs)

    class Meta:
        verbose_name = 'APP语言包'
        verbose_name_plural = 'APP语言包管理'

    def __str__(self):
        return self.language

