var PublicPostHandler = function () {
    this.editor = new window.wangEditor('#editor')
    this.editor.create()
}

PublicPostHandler.prototype.run = function () {
}

$(function () {
    var handler = new PublicPostHandler()
    handler.run()
})