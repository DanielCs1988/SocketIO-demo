$(document).ready(function () {

    // Opening socket. This variable will be used to control the connection from now on.
    // Connect can take the server url as a parameter, leaving it open defaults to localhost.
    let socket = io.connect();

    socket.on('chat', function (msg) {
        let message = `<div class="chat-msg"><b>${msg.nick}:</b> ${msg.message}</div>`;
        $('#chat-space').append(message);
    });

    $('#send-btn').click(function () {
        let message = $('#chat-message');
        socket.emit('chat', message.val(), function (server_reply) {
            console.log(server_reply);
        });
        message.val('');
    });

    socket.on('text-edited', function (newText) {
        $('#editable-text').val(newText);
    });

    $('#editable-text').on('input', function () {
        socket.emit('text-edited', $(this).val());
    });


});