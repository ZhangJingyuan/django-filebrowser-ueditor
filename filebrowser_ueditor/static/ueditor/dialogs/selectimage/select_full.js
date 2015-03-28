/**
 * User: Zhang Jingyuan
 * Date: 15-03-26
 * Time: 下午16:34
 * Full js of select image
 */

(function () {

    var remoteImage,
    
    window.onload = function () {
        //initTabs();
        //initAlign();
        remoteImage = remoteImage || new RemoteImage();
        initButtons();
    };

    /* 初始化onok事件 */
    function initButtons() {

        dialog.onok = function () {
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


    /* 初始化对其方式的点击事件 */
     /* 点击align图标 */
    function initAlign(){
        domUtils.on($G("alignIcon"), 'click', function(e){
            var target = e.target || e.srcElement;
            if(target.className && target.className.indexOf('-align') != -1) {
                setAlign(target.getAttribute('data-align'));
            }
        });
    }

    /* 设置对齐方式 */
   function setAlign(align){
        align = align || 'none';
        var aligns = $G("alignIcon").children;
        for(i = 0; i < aligns.length; i++){
            if(aligns[i].getAttribute('data-align') == align) {
                domUtils.addClass(aligns[i], 'focus');
                $G("align").value = aligns[i].getAttribute('data-align');
            } else {
                domUtils.removeClasses(aligns[i], 'focus');
            }
        }
    }
    /* 获取对齐方式 */
    function getAlign(){
        var align = $G("align").value || 'none';
        return align == 'none' ? '':align;
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
                'width': $G('width'),
                'height': $G('height'),
                'border': $G('border'),
                'vhSpace': $G('vhSpace'),
                'title': $G('title'),
                'align': $G('align')*/
            };
            var img = editor.selection.getRange().getClosedNode();
            if (img) {
                this.setImage(img);
            }
        },
        initEvents: function () {
            var _this = this,
                locker = $G('lock');

            /* 改变url */
            domUtils.on($G("ueditor_url"), 'keyup', updatePreview);
            domUtils.on($G("border"), 'keyup', updatePreview);
            domUtils.on($G("title"), 'keyup', updatePreview);

            domUtils.on($G("width"), 'keyup', function(){
                updatePreview();
                if(locker.checked) {
                    var proportion =locker.getAttribute('data-proportion');
                    $G('height').value = Math.round(this.value / proportion);
                } else {
                    _this.updateLocker();
                }
            });
            domUtils.on($G("height"), 'keyup', function(){
                updatePreview();
                if(locker.checked) {
                    var proportion =locker.getAttribute('data-proportion');
                    $G('width').value = Math.round(this.value * proportion);
                } else {
                    _this.updateLocker();
                }
            });
            domUtils.on($G("lock"), 'change', function(){
                var proportion = parseInt($G("width").value) /parseInt($G("height").value);
                locker.setAttribute('data-proportion', proportion);
            });

            function updatePreview(){
                _this.setPreview();
            }
        },
       updateLocker: function(){
            var width = $G('width').value,
                height = $G('height').value,
                locker = $G('lock');
            if(width && height && width == parseInt(width) && height == parseInt(height)) {
                locker.disabled = false;
                locker.title = '';
            } else {
                locker.checked = false;
                locker.disabled = 'disabled';
                locker.title = lang.remoteLockError;
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
                $G("width").value = img.width || '';
                $G("height").value = img.height || '';
                $G("border").value = img.getAttribute("border") || '0';
                $G("vhSpace").value = img.getAttribute("vspace") || '0';
                $G("title").value = img.title || img.alt || '';
                setAlign(align);
                this.updateLocker();
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
                ow = $G('width').value,
                oh = $G('height').value,
                border = $G('border').value,
                title = $G('title').value,*/
                preview = $G('preview'),
                width,
                height;

            width = ((!ow || !oh) ? preview.offsetWidth:Math.min(ow, preview.offsetWidth));
            width = width+(border*2) > preview.offsetWidth ? width:(preview.offsetWidth - (border*2));
            height = (!ow || !oh) ? '':width*oh/ow;

            if(url) {
                preview.innerHTML = '<img src="' + url + '" width="' + width + '" height="' + height + '" border="' + border + 'px solid #000" title="' + title + '" />';
            }
        },
        getInsertList: function () {
            var data = this.getData();
            if(data['ueditor_url']) {
                return [{
                    src: data['ueditor_url'],
                    _src: data['ueditor_url'],
                   width: data['width'] || '',
                    height: data['height'] || '',
                    border: data['border'] || '',
                    floatStyle: data['align'] || '',
                    vspace: data['vhSpace'] || '',
                    title: data['title'] || '',
                    alt: data['title'] || '',
                    style: "width:" + data['width'] + "px;height:" + data['height'] + "px;"
                }];
            } else {
                return [];
            }
        }
    };

})();
