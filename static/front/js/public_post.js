var PublicPostHandler = function () {
    var csrf_token = $('meta[name="csrf-token"]').attr('content');
    var editor = new window.wangEditor('#editor')
    editor.config.uploadImgServer = '/post/image/upload';
    editor.config.uploadImgHeaders = {
        'X-CSRFToken': csrf_token,
    };
    editor.config.uploadFileName = 'image';
    editor.config.uploadImgMaxSize = 1024 * 1024 * 5;
    editor.create();
    this.editor = editor;
}

PublicPostHandler.prototype.run = function () {
}

$(function () {
    var handler = new PublicPostHandler()
    handler.run()
})