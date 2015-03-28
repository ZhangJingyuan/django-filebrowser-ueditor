# coding: utf-8

# DJANGO IMPORTS
from django.template.loader import render_to_string
from django.forms.widgets import ClearableFileInput as DjangoClearableFileInput
from django.forms.widgets import CheckboxInput
from django.utils.translation import ugettext_lazy
from django.utils.safestring import mark_safe

# UEDITOR IMPORTS
from django import forms
from django.conf import settings
from django.contrib.admin.widgets import AdminTextareaWidget
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.http import urlencode
from  filebrowser_ueditor.commands import *

# FILEBROWSER IMPORTS
from filebrowser_ueditor.base import FileObject

#following import used by both apps
from filebrowser_ueditor.settings import ADMIN_THUMBNAIL


class FileInput(DjangoClearableFileInput):

    initial_text = ugettext_lazy('Currently')
    input_text = ugettext_lazy('Change')
    clear_checkbox_label = ugettext_lazy('Clear')
    template_with_initial = u'%(input)s %(preview)s'

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'preview': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'
        substitutions['input'] = super(DjangoClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            preview_template = render_to_string('filebrowser/widgets/fileinput.html', {
                'value': FileObject(value.name),
                'ADMIN_THUMBNAIL': ADMIN_THUMBNAIL,
            })
            substitutions["preview"] = preview_template

        return mark_safe(template % substitutions)


class ClearableFileInput(DjangoClearableFileInput):
    """
    A FileField Widget that shows its current value if it has one.
    If value is an Image, a thumbnail is shown.
    """

    initial_text = ugettext_lazy('Currently')
    input_text = ugettext_lazy('Change')
    clear_checkbox_label = ugettext_lazy('Clear')

    template_with_initial = u'<p class="file-upload">%(initial_text)s: %(initial)s<span class="clearable-file-input">%(clear_template)s</span><br />%(input_text)s: %(input)s %(preview)s</p>'
    template_with_clear = u'%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'preview': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'
        substitutions['input'] = super(DjangoClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = (u'<a target="_blank" href="%s">%s</a>' % (value.url, value))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = checkbox_name
                substitutions['clear_checkbox_id'] = checkbox_id
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        if value and hasattr(value, "url"):
            preview_template = render_to_string('filebrowser/widgets/clearablefileinput.html', {
                'value': FileObject(value.name),
                'ADMIN_THUMBNAIL': ADMIN_THUMBNAIL,
            })
            substitutions["preview"] = preview_template

        return mark_safe(template % substitutions)


# Widget for ueditor
# 修正输入的文件路径,输入路径的标准格式：abc,不需要前后置的路径符号
#如果输入的路径参数是一个函数则执行，否则可以拉接受时间格式化，用来生成如file20121208.bmp的重命名格式
def calc_path(OutputPath, instance=None):
    if callable(OutputPath):
        try:
            OutputPath = OutputPath(instance)
        except:
            OutputPath = ""
    else:
        try:
            import datetime
            OutputPath = datetime.datetime.now().strftime(OutputPath)
        except:
            pass

    return OutputPath

#width=600, height=300, toolbars="full", imagePath="", filePath="", upload_settings={},
                # settings={},command=None,event_handler=None
class UEditorWidget(forms.Textarea):
    def __init__(self,attrs=None):

        params=attrs.copy()

        width=params.pop("width")
        height=params.pop("height")
        toolbars=params.pop("toolbars","full")
        imagePath=params.pop("imagePath","")
        filePath=params.pop("filePath","")
        upload_settings=params.pop("upload_settings",{})
        settings=params.pop("settings",{})
        command=params.pop("command",None)
        event_handler=params.pop("event_handler",None)

        #扩展命令
        self.command=command
        self.event_handler=event_handler
        #上传路径
        self.upload_settings = upload_settings.copy()
        self.upload_settings.update({
            "imagePathFormat": imagePath,
            "filePathFormat": filePath
        })
        #保存
        self._upload_settings =self.upload_settings.copy()
        self.recalc_path(None)

        self.ueditor_settings ={
            'toolbars':toolbars,
            'initialFrameWidth':width,
            'initialFrameHeight':height
        }
        #以下处理工具栏设置，将normal,mini等模式名称转化为工具栏配置值
        try:
            if type(toolbars)==str:
                if toolbars =="full":
                    del self.ueditor_settings['toolbars']
                else:
                    self.ueditor_settings["toolbars"]=ADMIN_THUMBNAIL.TOOLBARS_SETTINGS[toolbars]
        except:
            pass
        self.ueditor_settings.update(settings)
        super(UEditorWidget, self).__init__(attrs)

    def recalc_path(self, model_inst):
        """计算上传路径,允许是function"""
        try:
            ADMIN_THUMBNAIL = self.upload_settings
            if self._upload_settings.has_key("filePathFormat"):
                ADMIN_THUMBNAIL['filePathFormat'] = calc_path(self._upload_settings['filePathFormat'], model_inst)
            if self._upload_settings.has_key("imagePathFormat"):
                ADMIN_THUMBNAIL['imagePathFormat'] = calc_path(self._upload_settings['imagePathFormat'], model_inst)
            if self._upload_settings.has_key("scrawlPathFormat"):
                ADMIN_THUMBNAIL['scrawlPathFormat'] = calc_path(self._upload_settings['scrawlPathFormat'], model_inst)
            if self._upload_settings.has_key("videoPathFormat"):
                ADMIN_THUMBNAIL['videoPathFormat'] = calc_path(self._upload_settings['videoPathFormat'], model_inst),
            if self._upload_settings.has_key("snapscreenPathFormat"):
                ADMIN_THUMBNAIL['snapscreenPathFormat'] = calc_path(self._upload_settings['snapscreenPathFormat'], model_inst)
            if self._upload_settings.has_key("catcherPathFormat"):
                ADMIN_THUMBNAIL['catcherPathFormat'] = calc_path(self._upload_settings['catcherPathFormat'], model_inst)
            if self._upload_settings.has_key("imageManagerListPath"):
                ADMIN_THUMBNAIL['imageManagerListPath'] = calc_path(self._upload_settings['imageManagerListPath'], model_inst)
            if self._upload_settings.has_key("fileManagerListPath"):
                ADMIN_THUMBNAIL['fileManagerListPath'] = calc_path(self._upload_settings['fileManagerListPath'], model_inst)
            #设置默认值，未指定涂鸦、截图、远程抓图、图片目录时,默认均等于imagePath
            if ADMIN_THUMBNAIL['imagePathFormat']!="":
                ADMIN_THUMBNAIL['scrawlPathFormat']=ADMIN_THUMBNAIL['scrawlPathFormat'] if self._upload_settings.has_key("scrawlPathFormat") else ADMIN_THUMBNAIL['imagePathFormat']
                ADMIN_THUMBNAIL['videoPathFormat']=ADMIN_THUMBNAIL['videoPathFormat'] if self._upload_settings.has_key("videoPathFormat") else ADMIN_THUMBNAIL['imagePathFormat']
                ADMIN_THUMBNAIL['snapscreenPathFormat']=ADMIN_THUMBNAIL['snapscreenPathFormat'] if self._upload_settings.has_key("snapscreenPathFormat") else ADMIN_THUMBNAIL['imagePathFormat']
                ADMIN_THUMBNAIL['catcherPathFormat']=ADMIN_THUMBNAIL['catcherPathFormat'] if self._upload_settings.has_key("catcherPathFormat") else ADMIN_THUMBNAIL['imagePathFormat']
                ADMIN_THUMBNAIL['imageManagerListPath']=ADMIN_THUMBNAIL['imageManagerListPath'] if self._upload_settings.has_key("imageManagerListPath") else ADMIN_THUMBNAIL['imagePathFormat']
            if ADMIN_THUMBNAIL['filePathFormat']!="":
                ADMIN_THUMBNAIL['fileManagerListPath']=ADMIN_THUMBNAIL['fileManagerListPath'] if self._upload_settings.has_key("fileManagerListPath") else ADMIN_THUMBNAIL['filePathFormat']
        except:
            pass


    def render(self, name, value, attrs=None):
        if value is None: value = ''
        #传入模板的参数
        editor_id="id_%s" % name.replace("-", "_")
        ADMIN_THUMBNAIL={
            "name": name,
            "id": editor_id,
            "value":value
        }
        if isinstance(self.command,list):
            cmdjs=""
            if isinstance(self.command,list):
                for cmd in self.command:
                    cmdjs=cmdjs+cmd.render(editor_id)
            else:
                cmdis=self.command.render(editor_id)
            ADMIN_THUMBNAIL["commands"]=cmdjs


        ADMIN_THUMBNAIL["settings"] = self.ueditor_settings.copy()
        ADMIN_THUMBNAIL["settings"].update({
            "serverUrl": "/ueditor/controller/?%s" % urlencode(self._upload_settings)
        })
        #生成事件侦听
        if self.event_handler:
            ADMIN_THUMBNAIL["bindEvents"]=self.event_handler.render(editor_id)

        context = {
            'UEditor': ADMIN_THUMBNAIL,
            'STATIC_URL': settings.STATIC_URL,
            'STATIC_ROOT': settings.STATIC_ROOT,
            'MEDIA_URL': settings.MEDIA_URL,
            'MEDIA_ROOT': settings.MEDIA_ROOT
        }
        return mark_safe(render_to_string('ueditor.html', context))

    class Media:
        js = ("ueditor/ueditor.config.js",
              "ueditor/ueditor.all.min.js")


class AdminUEditorWidget(AdminTextareaWidget,UEditorWidget ):
    def __init__(self, **kwargs):
        super(AdminUEditorWidget, self).__init__(**kwargs)

