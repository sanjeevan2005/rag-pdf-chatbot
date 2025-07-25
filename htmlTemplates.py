css = '''
<style>
.chat-message {
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: flex-start;
}
.chat-message.user {
    background-color: #2b313e;
}
.chat-message.bot {
    background-color: #475063;
}
.chat-message .avatar {
    width: 20%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.chat-message .avatar img {
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
}
.chat-message .message {
    width: 80%;
    padding: 0 1.5rem;
    color: #ffffff;
    word-break: break-word;
}
@media (max-width: 600px) {
    .chat-message .avatar {
        width: 15%;
    }
    .chat-message .message {
        width: 85%;
        font-size: 15px;
        padding: 0 1rem;
    }
}
</style>
'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.ibb.co/qWBwpNb/Photo-logo-5.png" alt="Bot Avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.ibb.co/3mfFPSxC/me.jpg" alt="User Avatar">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''
