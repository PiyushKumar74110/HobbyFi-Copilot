import {
    useEffect,
    useRef,
    useState,
} from "react";

import Message from "./Message";
import ApprovalCard from "./ApprovalCard";

import {
    sendMessage,
    type ApprovalPreview,
} from "../api/client";


interface ApprovalData {
    id: number | string;

    message: string;

    plan?: {
        type?: string;
        tool?: string;
        query?: unknown;
    };

    preview?: ApprovalPreview;
}


interface TextMessage {
    id: number;

    type: "message";

    role: "user" | "assistant";

    content: string;
}


interface ApprovalMessage {
    id: number;

    type: "approval";

    approval: ApprovalData;
}


type ChatItem =
    | TextMessage
    | ApprovalMessage;


function ChatBox() {

    const [messages, setMessages] =
        useState<ChatItem[]>([
            {
                id: 1,

                type: "message",

                role: "assistant",

                content:
                    "Hi! I'm HobbyFi Copilot. How can I help you today?",
            },
        ]);


    const [input, setInput] =
        useState("");


    const [loading, setLoading] =
        useState(false);


    const messagesEndRef =
        useRef<HTMLDivElement | null>(
            null
        );


    useEffect(() => {

        messagesEndRef.current
            ?.scrollIntoView({
                behavior: "smooth",
            });

    }, [
        messages,
        loading,
    ]);


    const handleSend = async () => {

        const query = input.trim();


        if (
            !query ||
            loading
        ) {

            return;

        }


        const userMessage: TextMessage = {

            id: Date.now(),

            type: "message",

            role: "user",

            content: query,

        };


        setMessages(
            (previous) => [

                ...previous,

                userMessage,

            ]
        );


        setInput("");

        setLoading(true);


        try {

            const response =
                await sendMessage(
                    query
                );


            if (
                response.type ===
                "approval_required"
            ) {

                const approvalMessage:
                    ApprovalMessage = {

                    id:
                    Date.now() + 1,

                    type:
                    "approval",

                    approval: {

                        id:
                        response.approval_id!,

                        message:
                        response.message ??
                        "This action requires approval.",

                        plan:
                        response.plan,

                        preview:
                        response.preview,

                    },

                };


                setMessages(
                    (previous) => [

                        ...previous,

                        approvalMessage,

                    ]
                );

            } else {

                const assistantMessage:
                    TextMessage = {

                    id:
                    Date.now() + 1,

                    type:
                    "message",

                    role:
                    "assistant",

                    content:
                    response.response ??
                    response.message ??
                    "I could not process the request.",

                };


                setMessages(
                    (previous) => [

                        ...previous,

                        assistantMessage,

                    ]
                );

            }

        } catch {

            const errorMessage:
                TextMessage = {

                id:
                Date.now() + 1,

                type:
                "message",

                role:
                "assistant",

                content:
                "Unable to connect to the server.",

            };


            setMessages(
                (previous) => [

                    ...previous,

                    errorMessage,

                ]
            );

        } finally {

            setLoading(false);

        }
    };


    const handleKeyDown = (
        event:
        React.KeyboardEvent<HTMLInputElement>
    ) => {

        if (
            event.key === "Enter"
        ) {

            handleSend();

        }
    };


    return (

        <div className="chat-container">


            <div className="chat-header">

                <div>

                    <h2>
                        HobbyFi Copilot
                    </h2>

                    <span>
                        AI assistant for your CRM
                    </span>

                </div>


                <div className="online-status">

                    <span
                        className="status-dot"
                    />

                    Online

                </div>

            </div>


            <div className="messages-container">


                {messages.map(
                    (item) => {


                        if (
                            item.type ===
                            "approval"
                        ) {

                            return (

                                <ApprovalCard

                                    key={
                                        item.id
                                    }

                                    approvalId={
                                        item
                                            .approval
                                            .id
                                    }

                                    message={
                                        item
                                            .approval
                                            .message
                                    }

                                    plan={
                                        item
                                            .approval
                                            .plan
                                    }

                                    preview={
                                        item
                                            .approval
                                            .preview
                                    }

                                />

                            );

                        }


                        return (

                            <Message

                                key={
                                    item.id
                                }

                                role={
                                    item.role
                                }

                                content={
                                    item.content
                                }

                            />

                        );

                    }
                )}


                {loading && (

                    <div className="typing-indicator">

                        <span />

                        <span />

                        <span />

                    </div>

                )}


                <div
                    ref={
                        messagesEndRef
                    }
                />

            </div>


            <div className="chat-input-container">


                <input

                    type="text"

                    value={input}

                    placeholder=
                    "Ask about users, memberships, revenue..."

                    onChange={
                        (event) =>
                            setInput(
                                event.target.value
                            )
                    }

                    onKeyDown={
                        handleKeyDown
                    }

                    disabled={
                        loading
                    }

                />


                <button

                    className="send-button"

                    onClick={
                        handleSend
                    }

                    disabled={
                        loading ||
                        !input.trim()
                    }

                    aria-label=
                    "Send message"

                >

                    ➜

                </button>

            </div>

        </div>

    );
}


export default ChatBox;