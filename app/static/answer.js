/**
 * Created by stepsame on 2015/12/23.
 */
$(".answer-edit").click(function(event){
    event.preventDefault()
    answer_conent = $(this).parent().parent()
    answer_conent.hide()
    answer_editor = answer_conent.next()
    answer_editor.show()
    url = $(this).attr("href")
    $.get(url, function(data){
        answer_editor.html(data)
    })
})
$(".answer-editor").on("click", ".answer-cancel", function(event){
    event.preventDefault()
    answer_editor = $(this).parent().parent().parent()
    answer_editor.hide()
    answer_conent = answer_editor.prev()
    answer_conent.show()
})


$(".answer-write").click(function(event){
    event.preventDefault()
    answer_creator = $(this).parent().next()
    answer_creator.toggle()
    if (answer_creator.attr("display") != "none"){
        url = $(this).attr("href")
        $.get(url, function(data){
            answer_creator.html(data)
            $(".answer-cancel").hide()
        })
    }
})



