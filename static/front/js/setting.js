var SettingHandler = function () {

}

SettingHandler.prototype.listenAvatarUploadEvent = function () {
    $('#avatar-input').on("change", function () {
        var image = this.files[0]
        console.log(image)
        var formData = new FormData()
        formData.append('image', image)
        zlajax.post({
            url: 'avatar/upload',
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                console.log(result)
                if (result['code'] == 200) {
                    var avatar = result['data']['avatar']
                    var avatar_url = 'media/avatar/' + avatar
                    $('#avatar-img').attr('src', avatar_url)
                }
            }
        })
    })
}
SettingHandler.prototype.listenSubmitEvent = function () {
    $("#submit-btn").on('click', function (event) {
        event.preventDefault()
        var signature = $("#signature-input").val()
        if (!signature) {
            alert('提交成功')
            return
        }
        if (signature && (signature.length > 50 || signature.length < 2)) {
            alert('签名长度在2到50之间')
            return
        }
        zlajax.post({
            url:'profile/edit',
            data: {
                'signature':signature
            },
            success:function (result){
                console.log(result)
            }
        })
    })
}
SettingHandler.prototype.run = function () {
    this.listenAvatarUploadEvent()
    this.listenSubmitEvent()
}

$(function () {
    var handler = new SettingHandler();
    handler.run()
})