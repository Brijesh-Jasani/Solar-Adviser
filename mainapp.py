import streamlit as st
import numpy as np

# Main information display
st.title("Solar Project Decision Advisor")

st.header("Overview")
st.write("""
The Solar Project Decision Advisor helps businesses decide between CAPEX (Capital Expenditure) 
and OPEX (Operational Expenditure) models for solar projects. It considers user inputs and calculates 
the Net Present Value (NPV) for both models to provide a recommendation.
""")

st.header("Intended Users")
st.write("""
- Business owners
- Financial managers
- Energy consultants
""")

st.header("How to Use")
st.write("""
1. **Open the Tool**: Access the tool via the provided web application link.
2. **Input Financial Details**: Enter details in the sidebar, including initial investment, annual savings, 
   operational costs, discount rate, and project lifetime.
3. **Answer Questions**: Respond to questions regarding your business's preferences and capabilities.
4. **Receive Recommendation**: View the suggested model (CAPEX or OPEX) and the corresponding NPV calculations.
""")

st.header("Input Information")
st.write("""
- **Initial Investment**: The upfront cost for the CAPEX model.
- **Annual Savings**: Yearly savings from the solar project.
- **Operational Costs**: Yearly costs for maintaining the OPEX model.
- **Discount Rate**: Interest rate used for discounting future cash flows.
- **Project Lifetime**: Number of years the project will last.
""")

st.header("Output Information")
st.write("""
- **Suggested Model**: CAPEX or OPEX based on user inputs.
- **NPV Calculations**: Net Present Value for both CAPEX and OPEX models.
""")

st.header("Questions")
# Define the questions and options for the dropdown
questions = {
    "Capital Availability": [
        "High (Sufficient funds for upfront investment)", 
        "Low (Limited funds for upfront investment)"
    ],
    "Risk Appetite": [
        "High (Willing to take higher financial risks)", 
        "Low (Prefer safer, lower-risk options)"
    ],
    "Tax Benefit Importance": [
        "High (Tax benefits significantly impact financial decisions)", 
        "Low (Tax benefits are not a major consideration)"
    ],
    "Electricity Needs": [
        "High (Large and consistent electricity requirements)", 
        "Low (Smaller or variable electricity needs)"
    ],
    "Growth Projections": [
        "High (Expect significant business growth)", 
        "Low (Do not anticipate much change)"
    ],
    "Space Availability": [
        "High (Adequate space for solar installations)", 
        "Low (Limited space for infrastructure)"
    ],
    "Preference for Ownership": [
        "Yes (Prefer owning assets outright)", 
        "No (Prefer renting or leasing assets)"
    ],
    "Maintenance Capability": [
        "Yes (Can handle maintenance in-house)", 
        "No (Prefer outsourcing maintenance)"
    ]
}

# Financial model inputs
st.sidebar.header("Brijesh Jasani")
website_link = "https://energybrije.com/"
st.sidebar.markdown(f'<a href="{website_link}">Visit My Website</a>', unsafe_allow_html=True)
st.sidebar.header("Financial Model Inputs")
initial_investment = st.sidebar.number_input("Initial Investment (CAPEX)", min_value=0.0, value=10000.0)
annual_savings = st.sidebar.number_input("Annual Savings", min_value=0.0, value=1500.0)
operational_costs = st.sidebar.number_input("Annual Operational Costs (OPEX)", min_value=0.0, value=500.0)
discount_rate = st.sidebar.number_input("Discount Rate (%)", min_value=0.0, max_value=100.0, value=5.0) / 100
project_lifetime = st.sidebar.number_input("Project Lifetime (years)", min_value=1, value=20)

# Initialize a dictionary to store user responses
responses = {}

# Create dropdowns for each question with descriptions
for question, options in questions.items():
    responses[question] = st.selectbox(f"{question}", options)

# Define a function to suggest the model based on responses
def suggest_model(responses):
    capex_count = 0
    opex_count = 0
    weights = {
        "Capital Availability": 2,
        "Risk Appetite": 1.5,
        "Tax Benefit Importance": 1.2,
        "Preference for Ownership": 1.8,
        "Maintenance Capability": 1.5
    }
    
    for question, response in responses.items():
        response = response.split(' ')[0]  # Only consider the first word (High/Low/Yes/No)
        if response == "High" and question in weights:
            capex_count += weights[question]
        elif response == "Low" and question in weights:
            opex_count += weights[question]
        elif response == "Yes" and question == "Preference for Ownership":
            capex_count += weights[question]
        elif response == "No" and question == "Preference for Ownership":
            opex_count += weights[question]

    if capex_count > opex_count:
        return "CAPEX", "Based on your responses, a CAPEX model may be more suitable for your business."
    else:
        return "OPEX", "Based on your responses, an OPEX model might be better for your business."

# Define a function to calculate NPV
def calculate_npv(initial_investment, annual_savings, operational_costs, discount_rate, project_lifetime):
    npv_capex = -initial_investment + sum([annual_savings / ((1 + discount_rate) ** year) for year in range(1, project_lifetime + 1)])
    npv_opex = -sum([operational_costs / ((1 + discount_rate) ** year) for year in range(1, project_lifetime + 1)])
    return npv_capex, npv_opex

# Display the suggestion when the user has made all selections
if all(response != "" for response in responses.values()):
    model, explanation = suggest_model(responses)
    npv_capex, npv_opex = calculate_npv(initial_investment, annual_savings, operational_costs, discount_rate, project_lifetime)  
    st.markdown(f"**<span style='color: green;'>Suggested Model: {model}</span>**", unsafe_allow_html=True)
    st.markdown(f"**<span style='color: green;'>{explanation}</span>**", unsafe_allow_html=True)
    st.markdown(f"**<span style='color: green;'>NPV for CAPEX model: ₹{npv_capex:,.2f}</span>**", unsafe_allow_html=True)
    st.markdown(f"**<span style='color: green;'>NPV for OPEX model: ₹{npv_opex:,.2f}</span>**", unsafe_allow_html=True)

st.header("Assumptions in Financial Model")
st.write("""
**1.Capital Availability and Risk Appetite:** Assumes these directly influence the preference for CAPEX or OPEX models.
         
**2.Tax Benefit Importance:** Assumes higher tax benefits favor the CAPEX model.
         
**3.NPV Calculation:**
         
    3A.CAPEX NPV: Considers initial investment and annual savings over the project lifetime.
    3B.OPEX NPV: Considers annual operational costs over the project lifetime.
         
**4.Discount Rate:** Assumes a constant rate over the project lifetime.
         
**5.Project Lifetime:** Assumes a fixed duration for both models.
         
**6.Annual Savings and Costs:** Assumes consistent savings and costs each year without accounting for inflation or varying energy prices.
""")
