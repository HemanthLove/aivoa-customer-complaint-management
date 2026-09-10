import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    complaint: {
        customer_name: null,
        customer_source: null,
        product_name: null,
        product_strength: null,
        batch_number: null,
        manufacturing_date: null,
        expiry_date: null,
        affected_quantity: null,
        affected_quantity_unit: null,
        complaint_description: null,
        facility_name: null,
        material_impact: null,
        defect_type: null,
        defect_description: null,
    },

    risk_assessment: {
        severity: null,
        risk_level: null,
        recommended_action: null,
        rationale: null,
    },

    status: "Pending Triage",
};

const complaintSlice = createSlice({
    name: "complaint",
    initialState,

    reducers: {
        setComplaintResult: (state, action) => {
            state.complaint = action.payload.complaint;
            state.risk_assessment = action.payload.risk_assessment;
            state.status = "AI Processed";
        },

        updateComplaint: (state, action) => {
            state.complaint = {
                ...state.complaint,
                ...action.payload,
            };
        },

        clearComplaint: () => initialState,
    },
});

export const {
    setComplaintResult,
    updateComplaint,
    clearComplaint,
} = complaintSlice.actions;

export default complaintSlice.reducer;