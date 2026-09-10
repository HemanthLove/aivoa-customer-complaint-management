import { useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";

import {
  checkComplaintCompleteness,
  editComplaint,
  extractComplaintFromPdf,
  processComplaint,
} from "./services/complaintApi";

import { setComplaintResult } from "./features/complaint/complaintSlice";


function App() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [selectedFileName, setSelectedFileName] = useState("");
  const [completenessResult, setCompletenessResult] = useState(null);

  const fileInputRef = useRef(null);

  const dispatch = useDispatch();

  const complaint = useSelector(
    (state) => state.complaint.complaint,
  );

  const riskAssessment = useSelector(
    (state) => state.complaint.risk_assessment,
  );

  const hasExistingComplaint =
    Boolean(complaint.product_name) ||
    Boolean(complaint.batch_number) ||
    Boolean(complaint.customer_name);


  function looksLikeEdit(instruction) {
    const editWords = [
      "sorry",
      "correct",
      "correction",
      "change",
      "changed",
      "update",
      "updated",
      "actually",
      "instead",
      "wrong",
      "incorrect",
      "should be",
    ];

    const normalizedText = instruction.toLowerCase();

    return editWords.some((word) =>
      normalizedText.includes(word),
    );
  }


  async function handleSubmit(event) {
    event.preventDefault();

    if (!message.trim() || isProcessing) {
      return;
    }

    const userMessage = message.trim();

    setMessages((current) => [
      ...current,
      {
        role: "user",
        content: userMessage,
      },
    ]);

    setMessage("");
    setIsProcessing(true);
    setCompletenessResult(null);

    try {
      let result;

      const isEdit =
        hasExistingComplaint &&
        looksLikeEdit(userMessage);

      if (isEdit) {
        result = await editComplaint(
          {
            complaint,
            risk_assessment: riskAssessment,
          },
          userMessage,
        );

        dispatch(setComplaintResult(result));

        setMessages((current) => [
          ...current,
          {
            role: "assistant",
            content:
              "Complaint information updated successfully. The risk assessment has also been reassessed.",
          },
        ]);
      } else {
        result = await processComplaint(userMessage);

        dispatch(setComplaintResult(result));

        setMessages((current) => [
          ...current,
          {
            role: "assistant",
            content:
              "Complaint information extracted successfully.",
          },
        ]);
      }
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content:
            `Unable to process the complaint: ${error.message}`,
        },
      ]);
    } finally {
      setIsProcessing(false);
    }
  }


  async function handleCheckCompleteness() {
    if (!hasExistingComplaint || isProcessing) {
      return;
    }

    setIsProcessing(true);

    setMessages((current) => [
      ...current,
      {
        role: "user",
        content: "Check complaint completeness",
      },
    ]);

    try {
      const result = await checkComplaintCompleteness({
        complaint,
        risk_assessment: riskAssessment,
      });

      setCompletenessResult(result);

      const missingText =
        result.missing_fields.length > 0
          ? ` Missing information: ${result.missing_fields.join(", ")}.`
          : " No core information is missing.";

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content:
            `Complaint completeness: ${result.completeness_score}%.${missingText}`,
        },
      ]);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content:
            `Unable to check complaint completeness: ${error.message}`,
        },
      ]);
    } finally {
      setIsProcessing(false);
    }
  }


  function handleFileButtonClick() {
    if (!isProcessing) {
      fileInputRef.current?.click();
    }
  }


  async function handleFileChange(event) {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setSelectedFileName(file.name);

    setMessages((current) => [
      ...current,
      {
        role: "user",
        content: `Uploaded document: ${file.name}`,
      },
    ]);

    setIsProcessing(true);
    setCompletenessResult(null);

    try {
      const result = await extractComplaintFromPdf(file);

      dispatch(setComplaintResult(result));

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content:
            "Complaint document processed successfully. The complaint form and AI risk assessment have been populated.",
        },
      ]);
    } catch (error) {
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content:
            `Unable to extract the document: ${error.message}`,
        },
      ]);
    } finally {
      setIsProcessing(false);

      event.target.value = "";
    }
  }


  return (
    <div className="app-shell">

      <header className="app-header">

        <div>
          <div className="brand">
            AIVOA
          </div>

          <div className="subtitle">
            Customer Complaint Management System
          </div>
        </div>

        <div className="status-badge">
          <span className="status-dot" />
          Pending Triage
        </div>

      </header>


      <main className="workspace">

        <section className="complaint-panel">

          <div className="panel-header">

            <div>

              <p className="eyebrow">
                COMPLAINT MANAGEMENT
              </p>

              <h1>
                Log Customer Complaint
              </h1>

              <p>
                Complaint details are populated by the AIVOA Copilot.
              </p>

            </div>

          </div>


          <div className="section-title">
            Product &amp; Batch Identification
          </div>


          <div className="form-grid">

            <ReadOnlyField
              label="Customer Name"
              value={complaint.customer_name}
            />

            <ReadOnlyField
              label="Customer Source"
              value={complaint.customer_source}
            />

            <ReadOnlyField
              label="Product Name"
              value={complaint.product_name}
            />

            <ReadOnlyField
              label="Product Strength"
              value={complaint.product_strength}
            />

            <ReadOnlyField
              label="Batch / Lot Number"
              value={complaint.batch_number}
            />

            <ReadOnlyField
              label="Manufacturing Date"
              value={complaint.manufacturing_date}
            />

            <ReadOnlyField
              label="Expiry Date"
              value={complaint.expiry_date}
            />

            <ReadOnlyField
              label="Affected Quantity"
              value={
                complaint.affected_quantity
                  ? `${complaint.affected_quantity} ${complaint.affected_quantity_unit ?? ""}`
                  : null
              }
            />

          </div>


          <div className="section-title">
            Complaint Details
          </div>


          <div className="form-grid">

            <ReadOnlyField
              label="Defect Type"
              value={complaint.defect_type}
            />

            <ReadOnlyField
              label="Facility"
              value={complaint.facility_name}
            />

            <ReadOnlyField
              label="Material Impact"
              value={complaint.material_impact}
            />

            <ReadOnlyField
              label="Defect Description"
              value={complaint.defect_description}
            />

          </div>


          <ReadOnlyTextArea
            label="Complaint Description"
            value={complaint.complaint_description}
          />


          <div className="risk-card">

            <div className="risk-card-header">

              <div>

                <p className="eyebrow">
                  AI COPILOT
                </p>

                <h2>
                  Risk Assessment
                </h2>

              </div>

              <span className="ai-badge">
                AI
              </span>

            </div>


            <div className="risk-grid">

              <ReadOnlyField
                label="Severity"
                value={riskAssessment.severity}
              />

              <ReadOnlyField
                label="Risk Level"
                value={riskAssessment.risk_level}
              />

            </div>


            <ReadOnlyTextArea
              label="Recommended Action"
              value={riskAssessment.recommended_action}
            />


            <ReadOnlyTextArea
              label="Rationale"
              value={riskAssessment.rationale}
            />

          </div>


          {completenessResult && (

            <div className="completeness-card">

              <div className="risk-card-header">

                <div>

                  <p className="eyebrow">
                    AI COPILOT
                  </p>

                  <h2>
                    Complaint Completeness
                  </h2>

                </div>

                <span className="ai-badge">
                  AI
                </span>

              </div>


              <div className="completeness-score">
                <span className="score-number">
                  {completenessResult.completeness_score}%
                </span>

                <span className="score-label">
                  {completenessResult.is_complete
                    ? "Complete"
                    : "Incomplete"}
                </span>
              </div>


              <div className="completeness-section">

                <div className="completeness-label">
                  Information Present
                </div>

                {completenessResult.present_fields.length > 0 ? (
                  <ul>
                    {completenessResult.present_fields.map((field) => (
                      <li key={field}>
                        ✓ {field}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>No core fields identified.</p>
                )}

              </div>


              {completenessResult.missing_fields.length > 0 && (

                <div className="completeness-section">

                  <div className="completeness-label">
                    Missing Information
                  </div>

                  <ul>
                    {completenessResult.missing_fields.map((field) => (
                      <li key={field}>
                        ⚠ {field}
                      </li>
                    ))}
                  </ul>

                </div>

              )}


              <p className="completeness-notes">
                {completenessResult.notes}
              </p>

            </div>

          )}

        </section>


        <section className="copilot-panel">

          <div className="copilot-header">

            <div className="copilot-avatar">
              AI
            </div>


            <div>

              <h2>
                AIVOA Copilot
              </h2>

              <p>
                AI Assistant · Complaint Processing
              </p>

            </div>


            <span className="online-badge">
              Online
            </span>

          </div>


          <div className="chat-area">

            {messages.length === 0 ? (

              <div className="empty-chat">

                <div className="empty-icon">
                  ✦
                </div>

                <h3>
                  Ready to process a complaint
                </h3>

                <p>
                  Describe the customer complaint in natural language
                  or upload a complaint PDF.
                </p>


                <div className="example-box">

                  <span>
                    Example
                  </span>

                  <p>
                    “Apollo Pharmacy reported discolored Amoxicillin
                    Capsules 500 mg. Batch BMX240602, 48 capsules affected.”
                  </p>

                </div>

              </div>

            ) : (

              messages.map((item, index) => (

                <div
                  className={`message ${item.role}`}
                  key={`${item.role}-${index}`}
                >

                  <div className="message-label">

                    {item.role === "user"
                      ? "You"
                      : "AIVOA Copilot"}

                  </div>


                  <div className="message-content">
                    {item.content}
                  </div>

                </div>

              ))

            )}


            {isProcessing && (

              <div className="message assistant">

                <div className="message-label">
                  AIVOA Copilot
                </div>

                <div className="message-content processing">
                  Analyzing complaint...
                </div>

              </div>

            )}

          </div>


          <form
            className="chat-input-area"
            onSubmit={handleSubmit}
          >

            <textarea
              value={message}
              onChange={(event) =>
                setMessage(event.target.value)
              }
              placeholder="Describe the customer complaint..."
              rows={4}
              disabled={isProcessing}
            />


            <div className="input-footer">

              <div className="input-actions">

                <button
                  type="button"
                  className="upload-button"
                  onClick={handleFileButtonClick}
                  disabled={isProcessing}
                >
                  Upload PDF
                </button>

                <button
                  type="button"
                  className="completeness-button"
                  onClick={handleCheckCompleteness}
                  disabled={!hasExistingComplaint || isProcessing}
                >
                  Check Completeness
                </button>

                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={handleFileChange}
                  hidden
                />

                {selectedFileName && (
                  <span className="file-name">
                    {selectedFileName}
                  </span>
                )}

              </div>


              <button
                type="submit"
                disabled={
                  !message.trim() ||
                  isProcessing
                }
              >

                {isProcessing
                  ? "Processing..."
                  : "Process Complaint"}

              </button>

            </div>

          </form>

        </section>

      </main>

    </div>
  );
}


function ReadOnlyField({
  label,
  value,
}) {
  return (
    <div className="field">

      <label>
        {label}
      </label>

      <input
        type="text"
        value={value ?? ""}
        placeholder="Not available"
        readOnly
      />

    </div>
  );
}


function ReadOnlyTextArea({
  label,
  value,
}) {
  return (
    <div className="field full-width">

      <label>
        {label}
      </label>

      <textarea
        value={value ?? ""}
        placeholder="Not available"
        rows={3}
        readOnly
      />

    </div>
  );
}


export default App;