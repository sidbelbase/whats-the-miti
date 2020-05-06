$(document).ready(function () {
    $('.change').each(function () {
        $(this).prop('Counter', 0).animate({
            Counter: $(this).text()
        }, {
            duration: 2500,
            easing: 'swing',
            step: function (now) {
                $(this).text(Math.ceil(now));
            }
        });
    });

    function update() {
        $('#live-time').html(moment().tz('Asia/Kathmandu').format('HH.mm.ss'));
    }

    setInterval(update, 200);
});
