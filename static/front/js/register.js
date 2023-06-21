var RegisterHandler = function () {

}

RegisterHandler.prototype.listenSendCaptchaEvent = function () {
    $('#email-captcha-btn').on('click',function (event){
        event.preventDefault()
        var email = $('input[name="email"]').val()
        if (!email) {
            alert("请输入正确格式的邮箱")
            return;
        }
    zlajax.get({
        url: "email/captcha?email=" + email,
        success: function (result) {
            console.log(result)
        }
    })
    });
}

RegisterHandler.prototype.run = function () {
    this.listenSendCaptchaEvent()
}

$(function () {
    var handler = new RegisterHandler()
    handler.run()
})