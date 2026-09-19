import { useState } from "react";

import {
    approveRequest,
    rejectRequest,
    type ApprovalPreview,
} from "../api/client";


interface ApprovalPlan {
    type?: string;
    tool?: string;
    query?: unknown;
}


interface ApprovalCardProps {
    approvalId: number | string;
    message: string;
    plan?: ApprovalPlan;
    preview?: ApprovalPreview;
}


function ApprovalCard({
    approvalId,
    message,
    plan,
    preview,
}: ApprovalCardProps) {

    const [status, setStatus] = useState<
        "pending" | "approved" | "rejected"
    >("pending");

    const [loading, setLoading] =
        useState(false);


    const query =
        typeof plan?.query === "object" &&
        plan.query !== null
            ? plan.query as Record<
                string,
                unknown
            >
            : {};


    const formatDate = (
        date?: string
    ) => {

        if (!date) {
            return null;
        }


        const parsedDate = new Date(
            date
        );


        if (
            Number.isNaN(
                parsedDate.getTime()
            )
        ) {

            return date;

        }


        return parsedDate.toLocaleDateString(
            "en-IN",
            {
                day: "numeric",
                month: "long",
                year: "numeric",
            }
        );
    };


    const getActionTitle = () => {

        switch (plan?.tool) {

            case "extend_trial":

                return (
                    "Extend Membership Trial"
                );


            default:

                return "CRM Modification";

        }
    };


    const getProposedChange = () => {

        switch (plan?.tool) {

            case "extend_trial":

                return `Extend ${
                    String(
                        preview?.crm_id ??
                        query.user ??
                        query.crm_id ??
                        "user"
                    )
                }'s membership by ${
                    String(
                        preview?.days ??
                        query.days ??
                        7
                    )
                } days`;


            default:

                return "Modify CRM data";

        }
    };


    const getEffect = () => {

        switch (plan?.tool) {

            case "extend_trial": {

                const currentDate =
                    formatDate(
                        preview?.current_end_date
                    );


                const newDate =
                    formatDate(
                        preview?.new_end_date
                    );


                if (
                    currentDate &&
                    newDate
                ) {

                    return (
                        `The membership expiry date ` +
                        `will be extended from ` +
                        `${currentDate} to ${newDate}.`
                    );

                }


                return (
                    `The membership expiry date ` +
                    `will be extended by ${
                        String(
                            preview?.days ??
                            query.days ??
                            7
                        )
                    } days.`
                );

            }


            default:

                return (
                    "CRM data will be updated " +
                    "after approval."
                );

        }
    };


    const handleApprove = async () => {

        try {

            setLoading(true);


            await approveRequest(
                approvalId
            );


            setStatus(
                "approved"
            );

        } catch {

            alert(
                "Failed to approve request"
            );

        } finally {

            setLoading(false);

        }
    };


    const handleReject = async () => {

        try {

            setLoading(true);


            await rejectRequest(
                approvalId
            );


            setStatus(
                "rejected"
            );

        } catch {

            alert(
                "Failed to reject request"
            );

        } finally {

            setLoading(false);

        }
    };


    return (

        <div className="approval-card">


            <span className="approval-title">

                Approval Required

            </span>


            <p className="approval-message">

                {message}

            </p>


            <div className="approval-details">


                <div className="approval-detail">

                    <span>
                        Action
                    </span>

                    <strong>
                        {getActionTitle()}
                    </strong>

                </div>


                <div className="approval-detail">

                    <span>
                        Proposed Change
                    </span>

                    <strong>
                        {getProposedChange()}
                    </strong>

                </div>


                <div className="approval-detail">

                    <span>
                        Effect After Approval
                    </span>

                    <strong>
                        {getEffect()}
                    </strong>

                </div>


            </div>


            {status === "pending" ? (

                <div className="approval-actions">


                    <button
                        className="reject-button"
                        onClick={handleReject}
                        disabled={loading}
                    >

                        Reject

                    </button>


                    <button
                        className="approve-button"
                        onClick={handleApprove}
                        disabled={loading}
                    >

                        {loading
                            ? "Processing..."
                            : "Approve"}

                    </button>


                </div>

            ) : (

                <div
                    className={
                        `approval-status ${status}`
                    }
                >

                    Request {status}

                </div>

            )}


        </div>

    );
}


export default ApprovalCard;