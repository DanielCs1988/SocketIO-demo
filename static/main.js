$(document).ready(function () {

    // Opening socket. This variable will be used to control the connection from now on.
    // Connect can take the server url as a parameter, leaving it open defaults to localhost.
    let socket = io.connect();

    // Listening for chat messages and appending them to the DOM.
    socket.on('chat', function (msg) {
        let message = `<div class="chat-msg"><b>${msg.nick}:</b> ${msg.message}</div>`;
        $('#chat-space').append(message);
    });

    // Emitting chat messages to the server so it can broadcast them.
    $('#send-btn').click(function () {
        let message = $('#chat-message');
        socket.emit('chat', message.val(), function (server_reply) {
            // Logging the server return value to demonstrate that we received it.
            console.log(server_reply);
        });
        message.val('');
    });

    // Refreshing the current state of the paragraph.
    socket.on('text-edited', function (newText) {
        $('#editable-text').text(newText);
    });

    // Input event is the only reliable event type for this purpose.
    $('#editable-text').on('input', function () {
        socket.emit('text-edited', $(this).text());
    });


});