/**
 * Created by stepsame on 2015/12/29.
 */
$('*[data-poload]').mouseenter(function() {
    var e=$(this)
    $.get(e.data('poload'), function(d) {
        e.popover({
            html: true,
            content: d,
            trigger: 'hover',
            container: e
        }).popover('show')
    })
})
