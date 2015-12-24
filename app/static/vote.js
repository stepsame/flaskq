/**
 * Created by stepsame on 2015/12/24.
 */
$(".upvote").click(function(event){
    event.preventDefault()
    up = $(this)
    url = up.attr("href")
    $.get(url, {type: 'up'}, function(data) {
        up.attr("href", data.url)
        if (up.hasClass("active")) {
            up.removeClass("active")
            up.html("Upvote | " + data.upvotes)
        } else {
            up.addClass("active")
            up.html("Upvoted | " + data.upvotes)
            down = up.next()
            if (down.hasClass("active")) {
                down.removeClass("active")
                down.html("Downvote")
                down.attr("href", url)
            }
        }
    })
})
$(".downvote").click(function(event){
    event.preventDefault()
    down = $(this)
    url = down.attr("href")
    $.get(url, {type: 'down'}, function(data) {
        down.attr("href", data.url)
        if (down.hasClass("active")) {
            down.removeClass("active")
            down.html("Downvote")
        } else {
            down.addClass("active")
            down.html("Downvoted")
            up = down.prev()
            if (up.hasClass("active")) {
                up.removeClass("active")
                up.html("Upvote | " + data.upvotes)
                up.attr("href", url)
            }
        }
    })
})
