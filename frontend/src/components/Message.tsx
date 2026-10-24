
import { useMemo, useState } from "react";

interface MessageProps {
    role: "user" | "assistant";
    content: string;
}

type CrmRecord = Record<string, string>;

/**
 * Normalize field labels into readable table headings.
 */
function normalizeLabel(label: string): string {
    const normalizedLabels: Record<string, string> = {
        "crm id": "CRM ID",
        "crm_id": "CRM ID",
        "payment id": "Payment ID",
        "payment_id": "Payment ID",
        "user id": "User ID",
        "created at": "Created At",
        "created_at": "Created At",
        "phone number": "Phone",
    };

    const normalized = label.trim().toLowerCase();

    return (
        normalizedLabels[normalized] ??
        label.trim().replaceAll("_", " ").replace(/\b\w/g, (c) => c.toUpperCase())
    );
}

/**
 * Parse pipe-separated CRM records or labeled single-record details.
 */
function parseCrmRecords(content: string): CrmRecord[] {
    const records: CrmRecord[] = [];

    for (const line of content.split(/\r?\n/)) {
        const recordLine = line.replace(/^\s*\d+\.\s*/, "").trim();

        if (!recordLine.includes("|")) continue;

        const record: CrmRecord = {};

        for (const field of recordLine.split("|")) {
            const separator = field.indexOf(":");
            if (separator < 1) continue;

            const key = normalizeLabel(field.slice(0, separator));
            const value = field.slice(separator + 1).trim();

            if (key && value) record[key] = value;
        }

        if (Object.keys(record).length >= 2) records.push(record);
    }

    if (records.length > 0) return records;

    const details: CrmRecord = {};

    for (const line of content.split(/\r?\n/)) {
        const match = line.match(/^\s*([^:]+):\s*(.*?)\s*$/);
        if (!match) continue;

        const key = normalizeLabel(match[1]);
        const value = match[2].trim();

        if (key && value) details[key] = value;
    }

    return Object.keys(details).length >= 2 ? [details] : [];
}

/**
 * Split a timestamp into date and HH:MM time columns.
 */
function formatRecord(record: CrmRecord): CrmRecord {
    const formatted = { ...record };
    const timestamp = formatted["Created At"];

    if (timestamp) {
        const match = timestamp.match(
            /^(\d{4}-\d{2}-\d{2})\s+(\d{2}):(\d{2})/
        );

        if (match) {
            formatted["Date"] = match[1];
            formatted["Time"] = `${match[2]}:${match[3]}`;
            delete formatted["Created At"];
        }
    }

    return formatted;
}

/**
 * Display an assistant message with searchable and sortable CRM data.
 */
function Message({ role, content }: MessageProps) {
    const isUser = role === "user";
    const records = useMemo(
        () => (isUser ? [] : parseCrmRecords(content).map(formatRecord)),
        [content, isUser]
    );

    const [search, setSearch] = useState("");
    const [sortColumn, setSortColumn] = useState("");
    const [ascending, setAscending] = useState(true);

    const columns = useMemo(
        () => Array.from(new Set(records.flatMap(Object.keys))),
        [records]
    );

    const filteredRecords = useMemo(() => {
        const query = search.trim().toLowerCase();

        const filtered = records.filter((record) =>
            Object.values(record).some((value) =>
                value.toLowerCase().includes(query)
            )
        );

        if (!sortColumn) return filtered;

        return [...filtered].sort((a, b) => {
            const left = a[sortColumn] ?? "";
            const right = b[sortColumn] ?? "";

            const comparison = left.localeCompare(right, undefined, {
                numeric: true,
                sensitivity: "base",
            });

            return ascending ? comparison : -comparison;
        });
    }, [records, search, sortColumn, ascending]);

    function handleSort(column: string) {
        if (sortColumn === column) {
            setAscending(!ascending);
        } else {
            setSortColumn(column);
            setAscending(true);
        }
    }

    return (
        <div className={`message-row ${isUser ? "user-row" : "assistant-row"}`}>
            <div className={`message ${isUser ? "user-message" : "assistant-message"}`}>
                <span className="message-label">
                    {isUser ? "You" : "HobbyFi Copilot"}
                </span>

                {records.length > 0 ? (
                    <div className="crm-table-card">
                        <div className="crm-table-toolbar">
                            <div>
                                <h3>CRM Results</h3>
                                <span className="crm-table-count">
                                    {filteredRecords.length} of {records.length} records
                                </span>
                            </div>

                            <input
                                className="crm-table-search"
                                type="search"
                                placeholder="Search records..."
                                aria-label="Search CRM records"
                                value={search}
                                onChange={(event) => setSearch(event.target.value)}
                            />
                        </div>

                        <div className="message-table-wrapper">
                            <table className="message-table">
                                <thead>
                                    <tr>
                                        {columns.map((column) => (
                                            <th key={column}>
                                                <button
                                                    type="button"
                                                    className="crm-sort-button"
                                                    onClick={() => handleSort(column)}
                                                >
                                                    {column}
                                                    <span aria-hidden="true">
                                                        {sortColumn === column
                                                            ? ascending ? " ↑" : " ↓"
                                                            : " ↕"}
                                                    </span>
                                                </button>
                                            </th>
                                        ))}
                                    </tr>
                                </thead>

                                <tbody>
                                    {filteredRecords.map((record, index) => (
                                        <tr key={`${record["Payment ID"] ?? record["CRM ID"] ?? "row"}-${index}`}>
                                            {columns.map((column) => (
                                                <td key={column}>
                                                    {record[column] || "—"}
                                                </td>
                                            ))}
                                        </tr>
                                    ))}

                                    {filteredRecords.length === 0 && (
                                        <tr>
                                            <td colSpan={columns.length} className="crm-table-empty">
                                                No matching records found.
                                            </td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                ) : (
                    <p className="message-content">{content}</p>
                )}
            </div>
        </div>
    );
}

export default Message;
