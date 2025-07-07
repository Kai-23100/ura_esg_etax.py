import streamlit as st

st.set_page_config(page_title="URA eTax ESG Declaration", layout="centered")

st.title("URA eTax Portal – ESG Data Declaration Module")
st.write("Step 5 of 8: ESG Declarations (Optional for Small Taxpayers)")

# --- Environmental Data ---
with st.expander("Environmental Data", expanded=True):
    st.subheader("1. Renewable Energy Investments")
    renewable_invested = st.radio("Did your company invest in renewable energy this year?", options=["No", "Yes"])
    if renewable_invested == "Yes":
        asset_types = st.multiselect(
            "Asset type (select all that apply):",
            options=["Solar", "Wind", "Hydro", "Biomass"]
        )
        renewable_amount = st.number_input("Total investment amount (UGX)", min_value=0, step=1000)
        vat_exempt = st.radio("VAT-exempt?", options=["Yes", "No"])
        renewable_invoice = st.file_uploader(
            "Upload invoice or import certificate (PDF/JPG/PNG)", type=["pdf", "jpg", "png"]
        )
        if renewable_invoice is not None:
            st.write(f"Uploaded file: {renewable_invoice.name}")
    else:
        asset_types = []
        renewable_amount = 0
        vat_exempt = "No"
        renewable_invoice = None

    st.subheader("2. Plastic Packaging or Material Use")
    plastic_use = st.radio("Did your company import or manufacture plastic packaging?", options=["No", "Yes"])
    if plastic_use == "Yes":
        plastic_amount = st.number_input("Plastic material used/imported (kg or tonnes)", min_value=0.0, step=0.1)
        excise_code = st.text_input("Excise duty code used")
        plastic_report = st.file_uploader(
            "Upload customs or packaging report (PDF/JPG/PNG)", type=["pdf", "jpg", "png"]
        )
        if plastic_report is not None:
            st.write(f"Uploaded file: {plastic_report.name}")
    else:
        plastic_amount = 0
        excise_code = ""
        plastic_report = None

# --- Social Data ---
with st.expander("Social Data", expanded=False):
    st.subheader("3. Disability-Inclusive Employment")
    disability_employees = st.number_input(
        "Number of full-time employees with certified disabilities", min_value=0, step=1
    )
    ncpd_certificates = st.file_uploader(
        "Attach NCPD certificates (multiple allowed, PDF/JPG/PNG)",
        accept_multiple_files=True,
        type=["pdf", "jpg", "png"]
    )
    if ncpd_certificates:
        st.write(f"{len(ncpd_certificates)} file(s) uploaded:")
        for file in ncpd_certificates:
            st.write(f"- {file.name}")

    st.subheader("4. Staff Training & Upskilling")
    training_spend = st.number_input("Total annual training expenditure (UGX)", min_value=0, step=1000)
    training_certified = st.selectbox("Was training certified by:", options=["None", "NITA-U", "Ministry of Education"])
    training_receipts = st.file_uploader(
        "Attach provider TIN or receipts (multiple allowed, PDF/JPG/PNG)",
        accept_multiple_files=True,
        type=["pdf", "jpg", "png"]
    )
    if training_receipts:
        st.write(f"{len(training_receipts)} file(s) uploaded:")
        for file in training_receipts:
            st.write(f"- {file.name}")

# --- Governance Data ---
with st.expander("Governance Data", expanded=False):
    st.subheader("5. Total Tax Contribution (TTC) — [Large Taxpayers Only]")
    ttc_upload = st.file_uploader(
        "Upload completed Form TTC-01 (Excel/PDF)", type=["pdf", "xls", "xlsx"]
    )
    if ttc_upload is not None:
        st.write(f"Uploaded file: {ttc_upload.name}")

    ttc_income_tax = st.number_input("Corporate Income Tax (UGX)", min_value=0, step=1000)
    ttc_paye = st.number_input("PAYE (UGX)", min_value=0, step=1000)
    ttc_vat = st.number_input("VAT (UGX)", min_value=0, step=1000)
    ttc_withholding = st.number_input("Withholding Tax (UGX)", min_value=0, step=1000)
    ttc_excise = st.number_input("Excise Duty (UGX)", min_value=0, step=1000)
    ttc_nssf = st.number_input("NSSF Contributions (UGX)", min_value=0, step=1000)

# --- Submission Confirmation ---
st.markdown("---")
confirm = st.checkbox("I confirm that the information provided is accurate and complete.")

if st.button("Submit ESG Data"):
    if not confirm:
        st.error("Please confirm that your information is accurate before submitting.")
    else:
        # Basic validation examples
        errors = []
        if renewable_invested == "Yes" and renewable_amount == 0:
            errors.append("Renewable energy investment amount must be greater than zero.")
        if plastic_use == "Yes" and plastic_amount == 0:
            errors.append("Plastic material amount must be greater than zero.")
        if disability_employees == 0:
            st.warning("You have indicated zero employees with disabilities.")
        if training_spend == 0:
            st.warning("You have indicated zero training expenditure.")
        if errors:
            for err in errors:
                st.error(err)
        else:
            st.success("ESG data submitted successfully!")
            st.markdown("### Summary of your submission:")
            st.write(f"Renewable energy investment: {renewable_amount} UGX, assets: {asset_types}, VAT-exempt: {vat_exempt}")
            st.write(f"Plastic use/imported: {plastic_amount} kg/tonnes, Excise code: {excise_code}")
            st.write(f"Disability-inclusive employees: {disability_employees}")
            st.write(f"Training expenditure: {training_spend} UGX, Certified by: {training_certified}")
            st.write(f"TTC uploaded: {'Yes' if ttc_upload else 'No'}")
            st.write(f"TTC Breakdown (UGX): Income Tax={ttc_income_tax}, PAYE={ttc_paye}, VAT={ttc_vat}, Withholding Tax={ttc_withholding}, Excise={ttc_excise}, NSSF={ttc_nssf}")

            # TODO: Save data to database or file system here
            # Example:
            # save_to_db({...})


