$(function () {
    $('#comment-btn').on('click', function (event) {
        event.preventDefault();
        var content = $('#comment-textarea').val()
        var post_id = $('#comment-btn').attr('data-post-id')
        zlajax.post({
            'url': '/comment',
            'data': {content, post_id},
            'success': function (result) {
                if (result['code'] === 200) {
                    window.location.reload();
                } else {
                    console.log(result['message'])
                }
            }
        })
    })
})