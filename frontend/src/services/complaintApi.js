const API_BASE_URL = "http://127.0.0.1:8000";


export async function processComplaint(complaintText) {
    const response = await fetch(
        `${API_BASE_URL}/api/complaints/process`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                complaint_text: complaintText,
            }),
        },
    );

    if (!response.ok) {
        const errorText = await response.text();

        throw new Error(
            `Complaint processing failed: ${response.status} ${errorText}`,
        );
    }

    return response.json();
}


export async function editComplaint(
    currentComplaint,
    editInstruction,
) {
    const response = await fetch(
        `${API_BASE_URL}/api/complaints/edit`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                current_complaint: currentComplaint,
                edit_instruction: editInstruction,
            }),
        },
    );

    if (!response.ok) {
        const errorText = await response.text();

        throw new Error(
            `Complaint edit failed: ${response.status} ${errorText}`,
        );
    }

    return response.json();
}


export async function extractComplaintFromPdf(file) {
    const formData = new FormData();

    formData.append("file", file);

    const response = await fetch(
        `${API_BASE_URL}/api/complaints/extract-document`,
        {
            method: "POST",
            body: formData,
        },
    );

    if (!response.ok) {
        const errorText = await response.text();

        throw new Error(
            `Document extraction failed: ${response.status} ${errorText}`,
        );
    }

    return response.json();
}


export async function checkComplaintCompleteness(
    currentComplaint,
) {
    const response = await fetch(
        `${API_BASE_URL}/api/complaints/check-completeness`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                current_complaint: currentComplaint,
            }),
        },
    );

    if (!response.ok) {
        const errorText = await response.text();

        throw new Error(
            `Completeness check failed: ${response.status} ${errorText}`,
        );
    }

    return response.json();
}


export async function saveComplaint(
    currentComplaint,
    sourceType = "text",
) {
    const response = await fetch(
        `${API_BASE_URL}/api/complaints/save`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                complaint: currentComplaint,
                source_type: sourceType,
            }),
        },
    );

    if (!response.ok) {
        const errorText = await response.text();

        throw new Error(
            `Complaint save failed: ${response.status} ${errorText}`,
        );
    }

    return response.json();
}