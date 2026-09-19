import "./App.css";

import Chat from "./pages/Chat";
import Login from "./pages/Login";

function App() {

    const token = localStorage.getItem("token");

    if (!token) {

        return <Login />;

    }

    return <Chat />;
}

export default App;