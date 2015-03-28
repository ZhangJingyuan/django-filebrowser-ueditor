# coding: utf-8

# PYTHON IMPORTS
import os
import re

# DJANGO IMPORTS
from django import forms
from django.utils.translation import ugettext_lazy as _

#  UEDITOR IMPORTS
from filebrowser_ueditor.widgets import UEditorWidget
from filebrowser_ueditor.models import UEditorField as ModelUEditorField

# FILEBROWSER IMPORTS
from filebrowser_ueditor.settings import FOLDER_REGEX
from filebrowser_ueditor.utils import convert_filename

# FILEBROWSER FORM
ALNUM_NAME_RE = re.compile(FOLDER_REGEX, re.U)
# CHOICES
TRANSPOSE_CHOICES = (
    ("", u"-----"),
    ("0", _(u"Flip horizontal")),
    ("1", _(u"Flip vertical")),
    ("2", _(u"Rotate 90° CW")),
    ("4", _(u"Rotate 90° CCW")),
    ("3", _(u"Rotate 180°")),
)


class CreateDirForm(forms.Form):
    """
    Form for creating a folder.
    """

    name = forms.CharField(widget=forms.TextInput(attrs=dict({'class': 'vTextField'}, max_length=50, min_length=3)), label=_(u'Name'), help_text=_(u'Only letters, numbers, underscores, spaces and hyphens are allowed.'), required=True)

    def __init__(self, path, *args, **kwargs):
        self.path = path
        self.site = kwargs.pop("filebrowser_site", None)
        super(CreateDirForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        "validate name"
        if self.cleaned_data['name']:
            # only letters, numbers, underscores, spaces and hyphens are allowed.
            if not ALNUM_NAME_RE.search(self.cleaned_data['name']):
                raise forms.ValidationError(_(u'Only letters, numbers, underscores, spaces and hyphens are allowed.'))
            # Folder must not already exist.
            if self.site.storage.isdir(os.path.join(self.path, convert_filename(self.cleaned_data['name']))):
                raise forms.ValidationError(_(u'The Folder already exists.'))
        return convert_filename(self.cleaned_data['name'])


class ChangeForm(forms.Form):
    """
    Form for renaming a file/folder.
    """

    custom_action = forms.ChoiceField(label=_(u'Actions'), required=False)
    name = forms.CharField(widget=forms.TextInput(attrs=dict({'class': 'vTextField'}, max_length=50, min_length=3)), label=_(u'Name'), help_text=_(u'Only letters, numbers, underscores, spaces and hyphens are allowed.'), required=True)

    def __init__(self, *args, **kwargs):
        self.path = kwargs.pop("path", None)
        self.fileobject = kwargs.pop("fileobject", None)
        self.site = kwargs.pop("filebrowser_site", None)
        super(ChangeForm, self).__init__(*args, **kwargs)

        # Initialize choices of custom action
        choices = [("", u"-----")]
        for name, action in self.site.applicable_actions(self.fileobject):
            choices.append((name, action.short_description))
        self.fields['custom_action'].choices = choices

    def clean_name(self):
        "validate name"
        if self.cleaned_data['name']:
            # only letters, numbers, underscores, spaces and hyphens are allowed.
            if not ALNUM_NAME_RE.search(self.cleaned_data['name']):
                raise forms.ValidationError(_(u'Only letters, numbers, underscores, spaces and hyphens are allowed.'))
            #  folder/file must not already exist.
            if self.site.storage.isdir(os.path.join(self.path, convert_filename(self.cleaned_data['name']))) and os.path.join(self.path, convert_filename(self.cleaned_data['name'])) != self.fileobject.path:
                raise forms.ValidationError(_(u'The Folder already exists.'))
            elif self.site.storage.isfile(os.path.join(self.path, convert_filename(self.cleaned_data['name']))) and os.path.join(self.path, convert_filename(self.cleaned_data['name'])) != self.fileobject.path:
                raise forms.ValidationError(_(u'The File already exists.'))
        return convert_filename(self.cleaned_data['name'])

# UEDITOR FORM
class UEditorField(forms.CharField):
    def __init__(self,label,width=600, height=300, toolbars="full",imagePath="", filePath="",upload_settings={},settings={},command=None ,event_handler=None,*args,**kwargs):
        uSettings=locals().copy()
        del uSettings["self"],uSettings["label"],uSettings["args"],uSettings["kwargs"]
        kwargs["widget"]=UEditorWidget(attrs=uSettings)
        kwargs["label"]=label
        super(UEditorField,self).__init__( *args, **kwargs)

def UpdateUploadPath(model_form,model_inst=None):
    """ 遍历model字段，如果是UEditorField则需要重新计算路径 """
    if model_inst is not  None:
        try:
            for field in model_inst._meta.fields:
                if isinstance(field, ModelUEditorField):
                    model_form.__getitem__(field.name).field.widget.recalc_path(model_inst)
        except:
            pass

class UEditorModelForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(UEditorModelForm,self).__init__(*args,**kwargs)
        try:
            if kwargs.has_key("instance"):
                UpdateUploadPath(self,kwargs["instance"])
            else:
                UpdateUploadPath(self,None)
        except Exception:
            pass

