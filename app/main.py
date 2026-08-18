import streamlit as st
from prediction_helper import predict

# ==============================================================================
# Page Configuration
# ==============================================================================

st.set_page_config(
    page_title="Credit Risk Modelling System",
    page_icon="📊",
    layout="wide"
)

# ==============================================================================
# Custom Styling
# ==============================================================================

st.markdown("""
<style>

/* Reduce White Space */

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
    padding-left:2rem;
    padding-right:2rem;
}

div[data-testid="stVerticalBlock"] > div{
    gap:0.10rem;
}

/* Button Styling */

div.stButton > button:first-child {
    background-color: #0B3D91;
    color: white;
    border-radius: 8px;
    height: 2.3rem;
    font-weight: 600;
    border: none;
    transition: all 0.2s ease;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

div.stButton > button:first-child:hover {
    background-color: #1557C0;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ==============================================================================
# Header
# ==============================================================================

st.title("Credit Risk Modelling System")

st.markdown(
    "<p style='font-size:0.9rem; color:#666;'>"
    "Assess loan applicants by predicting default risk, generating credit scores, and assigning credit ratings."
    "</p>",
    unsafe_allow_html=True
)

# ==============================================================================
# Applicant Information
# ==============================================================================

with st.container(border=True):

    st.markdown("##### Applicant Information")

    col1, col2 = st.columns([1, 1])

    with col1:
        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=28,
            step=1
        )

    with col2:
        residence_type = st.selectbox(
            "Residence Type",
            [
                "Owned",
                "Rented",
                "Mortgage"
            ]
        )

# ==============================================================================
# Loan Information
# ==============================================================================

with st.container(border=True):

    st.markdown("##### Loan Information")

    col1, col2, col3, col4, col5 = st.columns(
        [1.3, 1.3, 1.0, 1.2, 1.0]
    )

    with col1:
        income_lakhs = st.number_input(
            "Annual Income (INR Lakhs)",
            min_value=0.0,
            value=12.0,
            step=0.5,
            help="""
            Enter the amount in INR Lakhs.

            Example:
            12.00 INR Lakhs = 12,00,000 INR

            Reference:
            1 Lakh = 1,00,000 = 100K
            """
                )

        income = income_lakhs * 100000

    with col2:
        loan_amount_lakhs = st.number_input(
            "Loan Amount (INR Lakhs)",
            min_value=0.0,
            value=30.0,
            step=0.5,
            help="""
            Enter the amount in INR Lakhs.

            Example:
            30.00 INR Lakhs = 30,00,000 INR

            Reference:
            1 Lakh = 1,00,000 = 100K
            """
                )

        loan_amount = loan_amount_lakhs * 100000

    with col3:
        loan_tenure_months = st.number_input(
            "Tenure (Months)",
            min_value=1,
            value=36,
            step=1
        )

    with col4:
        loan_purpose = st.selectbox(
            "Loan Purpose",
            [
                "Education",
                "Home",
                "Auto",
                "Personal"
            ]
        )

    with col5:
        loan_type = st.selectbox(
            "Loan Type",
            [
                "Secured",
                "Unsecured"
            ]
        )

# ==============================================================================
# Credit History
# ==============================================================================

with st.container(border=True):

    st.markdown("##### Credit History")

    col1, col2, col3, col4 = st.columns(
        [1, 1.3, 1.2, 1.3]
    )

    with col1:
        num_open_accounts = st.number_input(
            "Open Accounts",
            min_value=1,
            max_value=4,
            value=2,
            step=1
        )

    with col2:
        credit_utilization_ratio = st.number_input(
            "Credit Utilization (%)",
            min_value=0,
            max_value=100,
            value=30,
            step=1
        )

    with col3:
        delinquency_ratio = st.number_input(
            "Delinquency Ratio (%)",
            min_value=0,
            max_value=100,
            value=30,
            step=1
        )

    with col4:
        avg_dpd_per_delinquency = st.number_input(
            "Average DPD",
            min_value=0,
            value=20,
            step=1
        )

# ==============================================================================
# Calculate Loan-to-Income Ratio
# ==============================================================================

loan_to_income_ratio = (
    loan_amount / income
    if income > 0
    else 0
)

# ==============================================================================
# Loan-to-Income Ratio & Prediction
# ==============================================================================

left_col, right_col = st.columns([1, 2])

# ------------------------------------------------------------------------------
# Loan-to-Income Ratio
# ------------------------------------------------------------------------------

with left_col:

    with st.container(border=True):

        st.markdown("##### Loan-to-Income Ratio")

        st.metric(
            label="Loan-to-Income Ratio",
            value=f"{loan_to_income_ratio:.2f}",
            help="""
Calculated as:

Loan Amount ÷ Annual Income

Higher values indicate a larger loan relative to annual income.
"""
        )

# ------------------------------------------------------------------------------
# Prediction Button
# ------------------------------------------------------------------------------

with right_col:

    with st.container(border=True):

        st.markdown("##### Credit Risk Assessment")

        st.markdown(
            "<p style='font-size:0.9rem; color:#666;'>"
            "Click the button below to evaluate the applicant's probability of default, "
            "credit score, and credit rating."
            "</p>",
            unsafe_allow_html=True
        )

        assess_risk = st.button(
            "Assess Credit Risk",
            use_container_width=True,
            type="primary"
        )

# ==============================================================================
# Generate Prediction
# ==============================================================================

if assess_risk:

    probability, credit_score, rating = predict(
        age,
        income,
        loan_amount,
        loan_tenure_months,
        avg_dpd_per_delinquency,
        delinquency_ratio,
        credit_utilization_ratio,
        num_open_accounts,
        residence_type,
        loan_purpose,
        loan_type
    )

# ==============================================================================
# Credit Assessment Results
# ==============================================================================

if assess_risk:

    with st.container(border=True):

        st.markdown("##### Credit Assessment Results")

        col1, col2, col3 = st.columns(3)

        # ----------------------------------------------------------------------
        # Default Probability
        # ----------------------------------------------------------------------

        with col1:

            st.metric(
                label="Default Probability",
                value=f"{probability:.2%}",
                help="""
Estimated probability that a borrower will fail to repay a loan.

Lower probabilities indicate lower credit risk.
"""
            )

        # ----------------------------------------------------------------------
        # Credit Score
        # ----------------------------------------------------------------------

        with col2:

            st.metric(
                label="Credit Score",
                value=f"{credit_score}",
                help="""
Normalized credit score ranging from 300 to 900.

Higher scores indicate stronger creditworthiness and lower default risk.
"""
            )

        # ----------------------------------------------------------------------
        # Credit Rating
        # ----------------------------------------------------------------------

        with col3:

            st.metric(
                label="Credit Rating",
                value=rating,
                help="""
Creditworthiness category determined from the calculated credit score.

• Poor: 300–499

• Average: 500–649

• Good: 650–749

• Excellent: 750–900

"""
            )

