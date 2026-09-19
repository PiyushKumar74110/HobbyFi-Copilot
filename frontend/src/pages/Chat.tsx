import { useEffect, useRef, useState } from "react";

import ChatBox from "../components/ChatBox";
import { logout } from "../api/client";

import {
    FiMoreVertical,
    FiLogOut,
    FiUser,
    FiMail,
    FiHash,
} from "react-icons/fi";

function Chat() {

    const vendor = JSON.parse(
        localStorage.getItem("vendor") || "{}"
    );

    const [menuOpen, setMenuOpen] = useState(false);

    const menuRef = useRef<HTMLDivElement>(null);

    useEffect(() => {

        function handleClick(e: MouseEvent) {

            if (
                menuRef.current &&
                !menuRef.current.contains(e.target as Node)
            ) {
                setMenuOpen(false);
            }

        }

        window.addEventListener("click", handleClick);

        return () =>
            window.removeEventListener(
                "click",
                handleClick
            );

    }, []);

    function handleLogout() {

        logout();

        window.location.reload();

    }

    const initials =
        vendor?.name
            ?.split(" ")
            ?.map((v: string) => v[0])
            ?.join("")
            ?.slice(0, 2)
            ?.toUpperCase() || "V";

    return (

        <main className="chat-page">

    <div className="chat-wrapper">


            <header className="top-header">

    <div className="brand">

        <div className="brand-logo">

            ✦

        </div>

        <div>

            <h1>

                HobbyFi Copilot

            </h1>

            <p>

                AI CRM Assistant for Vendors

            </p>

        </div>

    </div>

    <div
        className="profile-section"
        ref={menuRef}
    >

        <button
            className="profile-button"
            onClick={() =>
                setMenuOpen(!menuOpen)
            }
        >

            <div className="profile-avatar">

                {initials}

            </div>

            <FiMoreVertical size={20} />

        </button>

        {menuOpen && (

            <div className="profile-menu">

                <div className="menu-user">

                    <div className="profile-avatar large">

                        {initials}

                    </div>

                    <div className="menu-user-info">

                        <strong>

                            {vendor.name}

                        </strong>

                        <div className="menu-item-text">

                            <FiMail size={14}/>

                            {vendor.email}

                        </div>

                        <div className="menu-item-text">

                            <FiHash size={14}/>

                            Vendor #{vendor.id}

                        </div>

                    </div>

                </div>

                <hr/>

                <button className="menu-button">

                    <FiUser/>

                    Profile

                </button>

                <button
                    className="menu-button logout"
                    onClick={handleLogout}
                >

                    <FiLogOut/>

                    Logout

                </button>

            </div>

        )}

    </div>

</header>

            <ChatBox />

            </div>

        </main>

    );

}

export default Chat;