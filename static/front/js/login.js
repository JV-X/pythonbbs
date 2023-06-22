var LoginHandler = function () {

}

LoginHandler.prototype.listenSubmitEvent = function () {
    $('#submit-btn').on('click', function (event) {
        event.preventDefault();
        var email = $('input[name="email"]').val()
        var password = $('input[name="password"]').val()
        var remember = $('input[name="remember"]').prop('checked')
        console.log(email, password, remember)
        zlajax.post({
            url: '/login',
            data:{
                'email': email,
                'password': password,
                'remember': remember ? 1 : 0,
            },
            success:function (result){
                console.log(result)
            }
        })
    })
}

LoginHandler.prototype.run = function () {
    this.listenSubmitEvent()
}

$(function () {
    var handler = new LoginHandler()
    handler.run()
})