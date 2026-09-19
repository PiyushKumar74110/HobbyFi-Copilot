interface MessageProps {
    role: "user" | "assistant";
    content: string;
}


function Message({
    role,
    content,
}: MessageProps) {

    const isUser = role === "user";


    return (
        <div
            className={
                `message-row ${
                    isUser
                        ? "user-row"
                        : "assistant-row"
                }`
            }
        >
            <div
                className={
                    `message ${
                        isUser
                            ? "user-message"
                            : "assistant-message"
                    }`
                }
            >
                <span className="message-label">
                    {isUser
                        ? "You"
                        : "HobbyFi Copilot"}
                </span>

                <p className="message-content">
    {content}
</p>
            </div>
        </div>
    );
}


export default Message;