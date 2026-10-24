
import "./App.css";

import Login from "./pages/Login";
import Workspace from "./pages/Workspace";

/**
 * Render the login screen or authenticated workspace.
 */
function App() {
    const token = localStorage.getItem("token");

    if (!token) {
        return <Login />;
    }

    return <Workspace />;
}

export default App;
