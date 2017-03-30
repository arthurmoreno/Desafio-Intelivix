/********************************/
/*  Java Script do app de urls  */
/********************************/


// Renderização da resposta da pesquisa de uma url
$(document).ready(function(){
    $(function(){
        $('#search-form').submit(function(e){
            e.preventDefault();
            var form = $(this);
            var post_url = form.attr('action');
            var post_data = form.serialize();
            $.ajax({
                type: 'POST',
                url: post_url,
                data: post_data,
                success: function(data) {
                    $("#search-table-div").html(data);
                }
            });
        });
    });
});

