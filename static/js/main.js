$(document).ready(function () {

    function clock() {
        $('#live-time').html(moment().tz('Asia/Kathmandu').format('HH.mm.ss'));
    }

    function date() {
        $('#date-today').html(moment().tz('Asia/Kathmandu').format('MMMM D, dddd'));
    }

    function nepalimiti() {
        $.ajax('/api').done(function (getthat) {
            $('#nepalimiti').text(getthat.nepali_miti);
        });
    }

    setInterval(clock, 500);
    setInterval(date, 1000);
    setInterval(nepalimiti, 30000);

});