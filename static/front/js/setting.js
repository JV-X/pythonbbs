var SettingHandler = function (){

}

SettingHandler.prototype.listenAvatarUploadEvent = function (){
    $('#avatar-input').on("change",function (){
        var image= this.files[0]
        console.log(image)
        var formData = new FormData()
        formData.append('image',image)
        zlajax.post({
            url:'avatar/upload',
            data:formData,
            processData: false,
            contentType: false,
            success:function (result){
                console.log(result)
                if(result['code']==200){
                    var avatar = result['data']['avatar']
                    var avatar_url = 'media/avatar/' + avatar
                    $('#avatar-img').attr('src',avatar_url)
                }
            }
        })
    })
}
SettingHandler.prototype.run=function (){
    this.listenAvatarUploadEvent()
}

$(function (){
    var handler = new SettingHandler();
    handler.run()
})