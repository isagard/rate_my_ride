$(document).ready(function() {
    $('#like_btn').click(function() {
        var reviewIdVar;
        reviewIdVar = $(this).attr('data-reviewid');

        $.get('/ride/like_review/',
            {'review_id': reviewIdVar},
            function(data) {
                $('#like_count').html(data);
                $('#like_btn').hide();
            })
    });
});
    