/**
 * Created by stepsame on 2015/12/21.
 */
$(".comments-link").click(function(event){
    event.preventDefault()
    comment_box = $(this).parent().parent().siblings(".comment-box")
    comment_box.toggle()

    url = $(this).attr("href")
    $.get(url, function(data){
        comment_box.html(data)
    })
})

$(".comment-box").on("submit", ".comment-form form", function(event){
    event.preventDefault()
    comment_box = $(this).parent().parent()
    comments_link = comment_box.prev().find(".comments-link")
    url = comments_link.attr("href")

    $.post(url, $(this).serialize(), function(data){
        comment_box.html(data)
        comment_box.find("#body").val("")
    })
})

