/**
 * User: Zhang Jingyuan
 * Date: 15-03-26
 * Time: 下午16:34
 * Select image from django-filebrowser
 */

(function () {

    var remoteImage;

    window.onload = function () {
        initButtons();
    };

    /* 初始化onok事件 */
    function initButtons() {

        dialog.onok = function () {
            remoteImage = remoteImage || new RemoteImage();
            var remote = false, list = [], id, tabs = $G('tabhead').children;
            for (var i = 0; i < tabs.length; i++) {
                if (domUtils.hasClass(tabs[i], 'focus')) {
                    id = tabs[i].getAttribute('data-content-id');
                    break;
                }
            }
            list = remoteImage.getInsertList();

            if(list) {
                editor.execCommand('insertimage', list);
                remote && editor.fireEvent("catchRemoteImage");
            }
        };
    }


    /* 在线图片 */
    function RemoteImage(target) {
        this.container = utils.isString(target) ? document.getElementById(target) : target;
        this.init();
    }
    RemoteImage.prototype = {
        init: function () {
            this.initContainer();
            this.initEvents();
        },
        initContainer: function () {
            this.dom = {
                'ueditor_url': $G('ueditor_url'),
            };
            var img = editor.selection.getRange().getClosedNode();
            if (img) {
                this.setImage(img);
            }
        },
        initEvents: function () {

            /* 改变url */
            domUtils.on($G("ueditor_url"), 'keyup', updatePreview);

            function updatePreview(){
                _this.setPreview();
            }
        },
        setImage: function(img){
            /* 不是正常的图片 */
            if (!img.tagName || img.tagName.toLowerCase() != 'img' && !img.getAttribute("src") || !img.src) return;

            var wordImgFlag = img.getAttribute("word_img"),
                src = wordImgFlag ? wordImgFlag.replace("&amp;", "&") : (img.getAttribute('_src') || img.getAttribute("src", 2).replace("&amp;", "&")),
                align = editor.queryCommandValue("imageFloat");

            /* 防止onchange事件循环调用 */
            if (src !== $G("ueditor_url").value) $G("ueditor_url").value = src;
            if(src) {
                /* 设置表单内容 */
                this.setPreview();
            }
        },
        getData: function(){
            var data = {};
            for(var k in this.dom){
                data[k] = this.dom[k].value;
            }
            return data;
        },
        setPreview: function(){
            var url = $G('ueditor_url').value,
                preview = $G('preview');

            if(url) {
                preview.innerHTML = '<img src="' + url + '"/>';
            }
        },
        getInsertList: function () {
            var data = this.getData();
            if(data['ueditor_url']) {
                return [{
                    src: data['ueditor_url'],
                    _src: data['ueditor_url'],
                }];
            } else {
                return [];
            }
        }
    };

})();
