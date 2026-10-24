
import { useCallback, useEffect, useState } from "react";
import { Bot, MessageCircle, Database } from "lucide-react";
import Chat from "./Chat";

type DatabaseRecord = Record<string, unknown>;

type TableResponse = {
    tables: string[];
};

type RecordsResponse = {
    table: string;
    total: number;
    limit: number;
    offset: number;
    records: DatabaseRecord[];
};

const API_BASE_URL =
    "https://hobbyfi-copilot-o38r.onrender.com" || "http://localhost:8000";

/**
 * Display the main workspace with Chat and Database navigation.
 */
function Workspace() {
    const [activeView, setActiveView] = useState<"chat" | "database">("chat");
    const [tables, setTables] = useState<string[]>([]);
    const [activeTable, setActiveTable] = useState("users");
    const [search, setSearch] = useState("");
    const [records, setRecords] = useState<DatabaseRecord[]>([]);
    const [total, setTotal] = useState(0);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    /**
     * Retrieve the saved authentication token.
     */
    const getToken = useCallback((): string => {
        return localStorage.getItem("token") || "";
    }, []);

    /**
     * Fetch the tables available to the authenticated vendor.
     */
    const fetchTables = useCallback(async () => {
        const response = await fetch(`${API_BASE_URL}/database/tables`, {
            headers: {
                Authorization: `Bearer ${getToken()}`,
            },
        });

        if (!response.ok) {
            throw new Error(`Could not load tables (${response.status}).`);
        }

        const data: TableResponse = await response.json();
        setTables(data.tables);

        setActiveTable((current) =>
            data.tables.includes(current) ? current : data.tables[0] || ""
        );
    }, [getToken]);

    /**
     * Fetch real records for the selected database table.
     */
    const fetchRecords = useCallback(async () => {
        if (!activeTable) {
            setRecords([]);
            setTotal(0);
            return;
        }

        setLoading(true);
        setError("");

        try {
            const params = new URLSearchParams({
                search,
                limit: "100",
                offset: "0",
            });

            const response = await fetch(
                `${API_BASE_URL}/database/${encodeURIComponent(activeTable)}?${params}`,
                {
                    headers: {
                        Authorization: `Bearer ${getToken()}`,
                    },
                }
            );

            if (!response.ok) {
                const body = await response.json().catch(() => null);
                throw new Error(
                    body?.detail || `Could not load records (${response.status}).`
                );
            }

            const data: RecordsResponse = await response.json();
            setRecords(data.records);
            setTotal(data.total);
        } catch (err) {
            setRecords([]);
            setTotal(0);
            setError(
                err instanceof Error ? err.message : "An unexpected error occurred."
            );
        } finally {
            setLoading(false);
        }
    }, [activeTable, getToken, search]);

    useEffect(() => {
        fetchTables().catch((err: unknown) => {
            setError(
                err instanceof Error ? err.message : "Could not load database tables."
            );
        });
    }, [fetchTables]);

    useEffect(() => {
        if (activeView === "database" && activeTable) {
            fetchRecords();
        }
    }, [activeView, activeTable, fetchRecords]);

    /**
     * Convert database values into readable table-cell text.
     */
    const formatValue = (value: unknown): string => {
        if (value === null || value === undefined) return "—";
        if (typeof value === "object") return JSON.stringify(value);
        return String(value);
    };

    const columns = records.length > 0 ? Object.keys(records[0]) : [];

    return (
        <div className="workspace">
            <header className="workspace-header">
                <div className="workspace-brand">
                    <Bot size={16} />
                    <span>HobbyFi Copilot</span>
                </div>
                <span className="workspace-status">Connected UI</span>
            </header>

            <nav className="workspace-nav">
                <button
                    type="button"
                    className={`workspace-tab ${activeView === "chat" ? "active" : ""}`}
                    onClick={() => setActiveView("chat")}
                >
                    <MessageCircle size={14} />
                    <span>AI Chat</span>
                </button>

                <button
                    type="button"
                    className={`workspace-tab ${activeView === "database" ? "active" : ""}`}
                    onClick={() => setActiveView("database")}
                >
                    <Database size={14} />
                    <span>Database</span>
                </button>
            </nav>

            <main className="workspace-content">
                {activeView === "chat" ? (
                    <Chat />
                ) : (
                    <section className="database-layout">
                        <aside className="database-sidebar">
                            <p className="database-sidebar-title">TABLES</p>

                            {tables.map((table) => (
                                <button
                                    key={table}
                                    type="button"
                                    className={`database-table-button ${
                                        activeTable === table ? "active" : ""
                                    }`}
                                    onClick={() => {
                                        setActiveTable(table);
                                        setSearch("");
                                        setError("");
                                    }}
                                >
                                    {table.replaceAll("_", " ").replace(/\b\w/g, (c) =>
                                        c.toUpperCase()
                                    )}
                                </button>
                            ))}
                        </aside>

                        <div className="database-main">
                            <h2>
                                {activeTable
                                    .replaceAll("_", " ")
                                    .replace(/\b\w/g, (c) => c.toUpperCase())}
                            </h2>

                            <p className="database-description">
                                Search records and inspect available fields
                            </p>

                            <div className="database-panel">
                                <input
                                    className="database-search"
                                    type="search"
                                    placeholder={`⌕  Search ${activeTable}...`}
                                    aria-label={`Search ${activeTable}`}
                                    value={search}
                                    onChange={(event) => setSearch(event.target.value)}
                                />

                                {loading ? (
                                    <p className="database-description" style={{ padding: 8 }}>
                                        Loading database records...
                                    </p>
                                ) : error ? (
                                    <p className="database-description" style={{ padding: 8 }}>
                                        {error}
                                    </p>
                                ) : records.length === 0 ? (
                                    <p className="database-description" style={{ padding: 8 }}>
                                        No records found.
                                    </p>
                                ) : (
                                    <div className="database-table-wrapper">
                                        <table className="database-table">
                                            <thead>
                                                <tr>
                                                    {columns.map((column) => (
                                                        <th key={column}>
                                                            {column
                                                                .replaceAll("_", " ")
                                                                .replace(/\b\w/g, (c) =>
                                                                    c.toUpperCase()
                                                                )}
                                                        </th>
                                                    ))}
                                                </tr>
                                            </thead>

                                            <tbody>
                                                {records.map((record, index) => (
                                                    <tr key={String(record.id ?? index)}>
                                                        {columns.map((column) => (
                                                            <td key={column}>
                                                                {formatValue(record[column])}
                                                            </td>
                                                        ))}
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                    </div>
                                )}
                            </div>

                            <p className="database-caption">
                                {loading
                                    ? "Fetching live data..."
                                    : `${total} record${total === 1 ? "" : "s"} found`}
                            </p>
                        </div>
                    </section>
                )}
            </main>
        </div>
    );
}

export default Workspace;
