import streamlit as st
from agent import generate_query
from db_handler import run_query

st.set_page_config(page_title="University DB Assistant", page_icon="🎓")
st.title("University Database Assistant (LangChain + MySQL)")
st.write("Ask questions in natural language and get answers from your database.")

user_input = st.text_input("Ask a question about the university data:")

if st.button("Run Query"):
    if user_input:
        try:
            with st.spinner("Generating SQL and executing..."):
                # Call the agent
                sql_query = generate_query(user_input)  # no traceback

                st.code(sql_query, language="sql")

                # Execute query
                result = run_query(sql_query)

                if result:
                    st.success("✅ Query executed.")
                    st.dataframe(result)
                else:
                    st.warning("No data found.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    else:
        st.warning("Please enter a question.")
