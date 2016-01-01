/**
 * Created by stepsame on 2015/12/29.
 */
var popoverTimeout
var e
$('*[data-poload]').mouseenter(function() {
    e=$(this)
    popoverTimeout = setTimeout(showPopover,1000)
}).mouseleave(function() {
    $(this).popover('hide')
    clearTimeout(popoverTimeout)
})

function showPopover(){
    e.off('hover')
    $.get(e.data('poload'), function(d) {
        e.popover({
            html: true,
            content: d,
            container: e
        }).popover('show')
    })
}
