const API_BASE_URL = "https://hobbyfi-copilot-o38r.onrender.com";

export interface ApprovalPreview {
    user?: string;
    crm_id?: string;
    days?: number;
    current_end_date?: string;
    new_end_date?: string;
}

export interface ChatResponse {
    type?: string;
    approval_id?: number | string;
    message?: string;
    plan?: {
        type?: string;
        tool?: string;
        query?: unknown;
    };
    preview?: ApprovalPreview;
    response?: string;
}

function getHeaders() {

    const token = localStorage.getItem("token");

    return {

        "Content-Type": "application/json",

        ...(token && {
            Authorization: `Bearer ${token}`,
        }),

    };
}

export async function sendMessage(
    message: string
): Promise<ChatResponse> {

    const response = await fetch(
        `${API_BASE_URL}/chat`,
        {
            method: "POST",

            headers: getHeaders(),

            body: JSON.stringify({
                message,
            }),
        }
    );

    if (!response.ok) {

        const error = await response.text();

        console.error(
            "CHAT API ERROR:",
            error
        );

        throw new Error(
            "Failed to send message"
        );
    }

    const data = await response.json();

    if (
        typeof data.response === "string"
    ) {

        try {

            const parsed = JSON.parse(
                data.response
            );

            if (
                parsed.type ===
                "approval_required"
            ) {

                return parsed as ChatResponse;

            }

        } catch {

            // Normal response

        }

    }

    return data as ChatResponse;
}

export async function approveRequest(
    approvalId: number | string
) {

    const response = await fetch(
        `${API_BASE_URL}/approval/${approvalId}/approve`,
        {
            method: "POST",

            headers: getHeaders(),
        }
    );

    if (!response.ok) {

        const error = await response.text();

        console.error(
            "APPROVAL API ERROR:",
            error
        );

        throw new Error(
            "Failed to approve request"
        );
    }

    return response.json();
}

export async function rejectRequest(
    approvalId: number | string
) {

    const response = await fetch(
        `${API_BASE_URL}/approval/${approvalId}/reject`,
        {
            method: "POST",

            headers: getHeaders(),
        }
    );

    if (!response.ok) {

        const error = await response.text();

        console.error(
            "REJECTION API ERROR:",
            error
        );

        throw new Error(
            "Failed to reject request"
        );
    }

    return response.json();
}

export async function login(
    email: string,
    password: string
) {

    const response = await fetch(
        `${API_BASE_URL}/auth/login`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                email,
                password,
            }),
        }
    );

    if (!response.ok) {

        throw new Error(
            "Invalid email or password"
        );
    }

    const data = await response.json();

    localStorage.setItem(
        "token",
        data.access_token
    );

    localStorage.setItem(
        "vendor",
        JSON.stringify(data.vendor)
    );

    return data;
}

export function logout() {

    localStorage.removeItem("token");

    localStorage.removeItem("vendor");
}

export function isLoggedIn() {

    return localStorage.getItem("token") !== null;
}