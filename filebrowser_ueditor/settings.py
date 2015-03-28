# coding: utf-8

# django imports
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.conf import settings as gSettings   #global settings ueditor

# PATH AND URL SETTINGS

# Main Media Settings
# WARNING: FILEBROWSER_MEDIA_ROOT and FILEBROWSER_MEDIA_URL will be removed with Filebrowser 3.6.
# Read the documentation on FileBrowser's storages (http://readthedocs.org/docs/django-filebrowser/en/latest/file_storages.html)
MEDIA_ROOT = getattr(settings, "FILEBROWSER_MEDIA_ROOT", settings.MEDIA_ROOT)
MEDIA_URL = getattr(settings, "FILEBROWSER_MEDIA_URL", settings.MEDIA_URL)
# Main FileBrowser Directory. This has to be a directory within MEDIA_ROOT.
# Leave empty in order to browse all files under MEDIA_ROOT.
# DO NOT USE A SLASH AT THE BEGINNING, DO NOT FORGET THE TRAILING SLASH AT THE END.
DIRECTORY = getattr(settings, "FILEBROWSER_DIRECTORY", 'uploads/')

# EXTENSIONS AND FORMATS
# Allowed Extensions for File Upload. Lower case is important.
EXTENSIONS = getattr(settings, "FILEBROWSER_EXTENSIONS", {
    'Folder': [''],
    'Image': ['.jpg', '.jpeg', '.gif', '.png', '.tif', '.tiff'],
    'Document': ['.pdf', '.doc', '.rtf', '.txt', '.xls', '.csv', '.docx'],
    'Video': ['.mov', '.wmv', '.mpeg', '.mpg', '.avi', '.rm'],
    'Audio': ['.mp3', '.mp4', '.wav', '.aiff', '.midi', '.m4p']
})
# Define different formats for allowed selections.
# This has to be a subset of EXTENSIONS.
# e.g., add ?type=image to the browse-URL ...
SELECT_FORMATS = getattr(settings, "FILEBROWSER_SELECT_FORMATS", {
    'file': ['Folder', 'Image', 'Document', 'Video', 'Audio'],
    'image': ['Image'],
    'document': ['Document'],
    'media': ['Video', 'Audio'],
})

# VERSIONS

# Directory to Save Image Versions (and Thumbnails). Relative to site.storage.location.
# If no directory is given, versions are stored within the Image directory.
# VERSION URL: VERSIONS_BASEDIR/original_path/originalfilename_versionsuffix.extension
VERSIONS_BASEDIR = getattr(settings, 'FILEBROWSER_VERSIONS_BASEDIR', '')
# Versions Format. Available Attributes: verbose_name, width, height, opts
VERSIONS = getattr(settings, "FILEBROWSER_VERSIONS", {
    'admin_thumbnail': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop'},
    'thumbnail': {'verbose_name': 'Thumbnail (1 col)', 'width': 60, 'height': 60, 'opts': 'crop'},
    'small': {'verbose_name': 'Small (2 col)', 'width': 140, 'height': '', 'opts': ''},
    'medium': {'verbose_name': 'Medium (4col )', 'width': 300, 'height': '', 'opts': ''},
    'big': {'verbose_name': 'Big (6 col)', 'width': 460, 'height': '', 'opts': ''},
    'large': {'verbose_name': 'Large (8 col)', 'width': 680, 'height': '', 'opts': ''},
})
# Quality of saved versions
VERSION_QUALITY = getattr(settings, 'FILEBROWSER_VERSION_QUALITY', 90)
# Versions available within the Admin-Interface.
ADMIN_VERSIONS = getattr(settings, 'FILEBROWSER_ADMIN_VERSIONS', ['thumbnail', 'small', 'medium', 'big', 'large'])
# Which Version should be used as Admin-thumbnail.
ADMIN_THUMBNAIL = getattr(settings, 'FILEBROWSER_ADMIN_THUMBNAIL', 'admin_thumbnail')

# PLACEHOLDER

# Path to placeholder image (relative to storage location)
PLACEHOLDER = getattr(settings, "FILEBROWSER_PLACEHOLDER", "")
# Show Placeholder if the original image does not exist
SHOW_PLACEHOLDER = getattr(settings, "FILEBROWSER_SHOW_PLACEHOLDER", False)
# Always show placeholder (even if the original image exists)
FORCE_PLACEHOLDER = getattr(settings, "FILEBROWSER_FORCE_PLACEHOLDER", False)

# EXTRA SETTINGS

# If set to True, the FileBrowser will not try to import a mis-installed PIL.
STRICT_PIL = getattr(settings, 'FILEBROWSER_STRICT_PIL', False)
# PIL's Error "Suspension not allowed here" work around:
# s. http://mail.python.org/pipermail/image-sig/1999-August/000816.html
IMAGE_MAXBLOCK = getattr(settings, 'FILEBROWSER_IMAGE_MAXBLOCK', 1024 * 1024)
# Exclude files matching any of the following regular expressions
# Default is to exclude 'thumbnail' style naming of image-thumbnails.
EXTENSION_LIST = []
for exts in EXTENSIONS.values():
    EXTENSION_LIST += exts
EXCLUDE = getattr(settings, 'FILEBROWSER_EXCLUDE', (r'_(%(exts)s)_.*_q\d{1,3}\.(%(exts)s)' % {'exts': ('|'.join(EXTENSION_LIST))},))
# Max. Upload Size in Bytes.
MAX_UPLOAD_SIZE = getattr(settings, "FILEBROWSER_MAX_UPLOAD_SIZE", 10485760)
# Normalize filename and remove all non-alphanumeric characters
# except for underscores, spaces & dashes.
NORMALIZE_FILENAME = getattr(settings, "FILEBROWSER_NORMALIZE_FILENAME", False)
# Convert Filename (replace spaces and convert to lowercase)
CONVERT_FILENAME = getattr(settings, "FILEBROWSER_CONVERT_FILENAME", True)
# Max. Entries per Page
# Loading a Sever-Directory with lots of files might take a while
# Use this setting to limit the items shown
LIST_PER_PAGE = getattr(settings, "FILEBROWSER_LIST_PER_PAGE", 50)
# Default Sorting
# Options: date, filesize, filename_lower, filetype_checked
DEFAULT_SORTING_BY = getattr(settings, "FILEBROWSER_DEFAULT_SORTING_BY", "date")
# Sorting Order: asc, desc
DEFAULT_SORTING_ORDER = getattr(settings, "FILEBROWSER_DEFAULT_SORTING_ORDER", "desc")
# regex to clean dir names before creation
FOLDER_REGEX = getattr(settings, "FILEBROWSER_FOLDER_REGEX", r'^[\w._\ /-]+$')
# Traverse directories when searching
SEARCH_TRAVERSE = getattr(settings, "FILEBROWSER_SEARCH_TRAVERSE", False)
# Default Upload and Version Permissions
DEFAULT_PERMISSIONS = getattr(settings, "FILEBROWSER_DEFAULT_PERMISSIONS", 0o755)
# Overwrite existing files on upload
OVERWRITE_EXISTING = getattr(settings, "FILEBROWSER_OVERWRITE_EXISTING", True)

# EXTRA TRANSLATION STRINGS

# The following strings are not availabe within views or templates
_('Folder')
_('Image')
_('Video')
_('Document')
_('Audio')

#UEDITOR SETTINGS
#工具栏样式，可以添加任意多的模式
TOOLBARS_SETTINGS={
    "besttome":[['source','undo', 'redo','bold', 'italic', 'underline','forecolor', 'backcolor','superscript','subscript',"justifyleft","justifycenter","justifyright","insertorderedlist","insertunorderedlist","blockquote",'formatmatch',"removeformat",'autotypeset','inserttable',"pasteplain","wordimage","searchreplace","map","preview","fullscreen"], ['insertcode','paragraph',"fontfamily","fontsize",'link', 'unlink','insertimage','insertvideo','attachment','emotion',"date","time"]],
    "mini":[['source','|','undo', 'redo', '|','bold', 'italic', 'underline','formatmatch','autotypeset', '|', 'forecolor', 'backcolor','|', 'link', 'unlink','|','simpleupload','attachment']],
    "normal":[['source','|','undo', 'redo', '|','bold', 'italic', 'underline','removeformat', 'formatmatch','autotypeset', '|', 'forecolor', 'backcolor','|', 'link', 'unlink','|','simpleupload', 'emotion','attachment', '|','inserttable', 'deletetable', 'insertparagraphbeforetable', 'insertrow', 'deleterow', 'insertcol', 'deletecol', 'mergecells', 'mergeright', 'mergedown', 'splittocells', 'splittorows', 'splittocols']]
}

#默认的Ueditor设置，请参见ueditor.config.js
UEditorSettings={
    "toolbars":TOOLBARS_SETTINGS["normal"],
    "autoFloatEnabled":False,
    "defaultPathFormat":"%(basename)s_%(datetime)s_%(rnd)s.%(extname)s"   #默认保存上传文件的命名方式
}
#请参阅php文件夹里面的config.json进行配置
UEditorUploadSettings={
   #上传图片配置项
    "imageActionName": "uploadimage", #执行上传图片的action名称
    "imageMaxSize": 10485760, #上传大小限制，单位B,10M
    "imageFieldName": "upfile", #* 提交的图片表单名称 */
    "imageUrlPrefix":"",
    "imagePathFormat":"",
    "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"], #上传图片格式显示

    #涂鸦图片上传配置项 */
    "scrawlActionName": "uploadscrawl", #执行上传涂鸦的action名称 */
    "scrawlFieldName": "upfile", #提交的图片表单名称 */
    "scrawlMaxSize": 10485760, #上传大小限制，单位B  10M
    "scrawlUrlPrefix":"",
    "scrawlPathFormat":"",

    #截图工具上传 */
    "snapscreenActionName": "uploadimage", #执行上传截图的action名称 */
    "snapscreenPathFormat":"",
    "snapscreenUrlPrefix":"",

    #抓取远程图片配置 */
    "catcherLocalDomain": ["127.0.0.1", "localhost", "img.baidu.com"],
    "catcherPathFormat":"",
    "catcherActionName": "catchimage", #执行抓取远程图片的action名称 */
    "catcherFieldName": "source", #提交的图片列表表单名称 */
    "catcherMaxSize": 10485760, #上传大小限制，单位B */
    "catcherAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"], #抓取图片格式显示 */
    "catcherUrlPrefix":"",
    #上传视频配置 */
    "videoActionName": "uploadvideo", #执行上传视频的action名称 */
    "videoPathFormat":"",
    "videoFieldName": "upfile", # 提交的视频表单名称 */
    "videoMaxSize": 102400000, #上传大小限制，单位B，默认100MB */
    "videoUrlPrefix":"",
    "videoAllowFiles": [
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid"], #上传视频格式显示 */

    #上传文件配置 */
    "fileActionName": "uploadfile", #controller里,执行上传视频的action名称 */
    "filePathFormat":"",
    "fileFieldName": "upfile",#提交的文件表单名称 */
    "fileMaxSize": 204800000, #上传大小限制，单位B，200MB */
    "fileUrlPrefix": "",#文件访问路径前缀 */
    "fileAllowFiles": [
        ".png", ".jpg", ".jpeg", ".gif", ".bmp",
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
        ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml"
    ], #上传文件格式显示 */

    #列出指定目录下的图片 */
    "imageManagerActionName": "listimage", #执行图片管理的action名称 */
    "imageManagerListPath":"",
    "imageManagerListSize": 30, #每次列出文件数量 */
    "imageManagerAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"], #列出的文件类型 */
    "imageManagerUrlPrefix": "",#图片访问路径前缀 */

    #列出指定目录下的文件 */
    "fileManagerActionName": "listfile", #执行文件管理的action名称 */
    "fileManagerListPath":"",
    "fileManagerUrlPrefix": "",
    "fileManagerListSize": 30, #每次列出文件数量 */
    "fileManagerAllowFiles": [
        ".png", ".jpg", ".jpeg", ".gif", ".bmp",".tif",".psd"
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
        ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml",
        ".exe",".com",".dll",".msi"
    ] #列出的文件类型 */
}


#更新配置：从用户配置文件settings.py重新读入配置UEDITOR_SETTINGS,覆盖默认
def UpdateUserSettings():
    UserSettings=getattr(gSettings,"UEDITOR_SETTINGS",{}).copy()
    if UserSettings.has_key("config"):UEditorSettings.update(UserSettings["config"])
    if UserSettings.has_key("upload"):UEditorUploadSettings.update(UserSettings["upload"])

#读取用户Settings文件并覆盖默认配置
UpdateUserSettings()


#取得配置项参数
def GetUeditorSettings(key,default=None):
    if UEditorSettings.has_key(key):
        return UEditorSettings[key]
    else:
        return default
