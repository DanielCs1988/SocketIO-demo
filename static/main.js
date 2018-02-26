$(document).ready(function () {

    // Opening socket. This variable will be used to control the connection from now on.
    // Connect can take the server url as a parameter, leaving it open defaults to localhost.
    let socket = io.connect();

    socket.on('chat', function (msg) {
        let message = `<div class="chat-msg"><b>${msg.nick}:</b> ${msg.message}</div>`;
        $('#chat-space').append(message);
    });

    $('#send-btn').click(function () {
        let message = $('#chat-message').val();
        socket.emit('chat', message);
    });

});