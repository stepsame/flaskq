/**
 * Created by stepsame on 2015/12/29.
 */
$('.answer-body').each(function(event) {

    var max_length = 350
    /* set the max content length before a read more link will be added */

    if ($(this).html().length > max_length) { /* check for content length */

        var short_content = $(this).html().substr(0, max_length)
        /* split the content in two parts */
        var long_content = $(this).html().substr(max_length)

        $(this).html('<div>'+short_content+'...</div>' + '<a href="#" class="read_more">(more)</a>' +
                '<div class="more_text" style="display:none;">' + long_content + '</div>')
        /* Alter the html to allow the read more functionality */

        $(this).find('a.read_more').click(function (event) { /* find the a.read_more element within the new html and bind the following code to it */

            event.preventDefault()
            /* prevent the a from changing the url */
            $(this).hide()
            /* hide the read more button */
            $(this).parents('.answer-body').find('.more_text').show();
            /* show the .more_text span */

        })
    }
})
