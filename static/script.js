
const form = document.getElementById("url-form");
const input = document.getElementById("url-input");
const message = document.getElementById("message");
const results = document.getElementById("results");
const resultBody = document.getElementById("result-body");

const labels = [
    ["protocol", "Protocol"],
    ["domain", "Domain name"],
    ["subdomain", "Subdomain"],
    ["path", "Path"],
    ["file_page_name", "File / page name"],
    ["query_parameters", "Query parameters"],
    ["fragment", "Fragment"]
];

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    message.textContent = "";
    results.hidden = true;

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: input.value })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Could not analyze URL.");
        }

        resultBody.replaceChildren();

        labels.forEach(([key, label]) => {
            const row = document.createElement("tr");
            const nameCell = document.createElement("td");
            const valueCell = document.createElement("td");

            nameCell.textContent = label;

            let value = data[key];

            if (key === "query_parameters") {
                value = Object.entries(value || {})
                    .map(([name, values]) =>
                        `${name}=${values.join(", ")}`)
                    .join("&");
            }

            valueCell.textContent =
                value === null || value === undefined || value === ""
                    ? "Not present"
                    : String(value);

            row.append(nameCell, valueCell);
            resultBody.appendChild(row);
        });

        results.hidden = false;
    } catch (error) {
        message.textContent = error.message;
    }
});
