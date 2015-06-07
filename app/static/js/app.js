$('document').ready(function() {
    // Tooltips
    $("[data-toggle='tooltip']").tooltip(); 
    
    // Like functionlity with ajax request
    $('#answers').on('click', function(e) {
        e.preventDefault();
        var element = $(e.target);
        var answer_id = element.data('id');
        if (answer_id) {
            //we clicked on right html element :)
            $.post('/like', {
                answer_id: answer_id
            }).done(function(result) {
                var likes = result.likes;
                var str = '';
                if (likes == 0) {
                    str = 'Like';
                } else {
                    str = 'Like (' + likes + ')';
                }
                element.html(str);
            }).fail(function(xhr, textStatus, errorThrown) {
                console.log('Something went wrong!');
            });
        }
    })
});