var RegisterHandler = function () {

}
var callback = function (event){
    var $this = $(this)
    event.preventDefault()
    var email = $('input[name="email"]').val()
    if (!email) {
        alert("请输入正确格式的邮箱")
        return;
    }
    zlajax.get({
        url: "email/captcha?email=" + email,
        success: function (result) {
            if(result['code'] == 200) {
                $this.off("click")
                $this.attr("disabled",'disabled');
                var countDown = 60;
                var interval = setInterval(function(){
                    if(countDown > 0){
                        $this.text(countDown)
                    } else {
                        $this.text('发送验证码')
                        $this.attr('disabled', false)
                        $this.on('click',callback)
                        clearInterval(interval)
                    }
                    countDown--
                },1000)

            }
        }
    })
}

RegisterHandler.prototype.listenSendCaptchaEvent = function () {
    $('#email-captcha-btn').on('click',callback);
}

RegisterHandler.prototype.listenGraphCaptchaEvent = function() {
    $('#captcha-img').on("click", function(){
        var $this = $(this);
        var src = $this.attr('src');
        var new_src = zlparam.setParam(src, 'sign', Math.random())
        $this.attr('src', new_src)
    })
}

RegisterHandler.prototype.listenSubmitEvent = function() {
    $('#submit-btn').on('click', function(event){
        event.preventDefault();
        var email = $('input[name="email"]').val()
        var username = $('input[name="username"]').val()
        var password = $('input[name="password"]').val()
        var password_repeat = $('input[name="password_repeat"]').val()
        var graph_captcha = $('input[name="graph_captcha"]').val()
        var email_captcha = $('input[name="email_captcha"]').val()
        zlajax.post({
            url: '/register',
            data: {
                'email':email,
                'username':username,
                'password':password,
                'repeat_password':password_repeat,
                'graph_captcha':graph_captcha,
                'email_captcha':email_captcha,
            },
            success : function(result){
                console.log(result)
            },
        })
    })
}

RegisterHandler.prototype.run = function () {
    this.listenSendCaptchaEvent();
    this.listenGraphCaptchaEvent()
    this.listenSubmitEvent()
}

$(function () {
    var handler = new RegisterHandler()
    handler.run()
})