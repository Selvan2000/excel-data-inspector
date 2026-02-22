import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Inspector Dashboard", layout="wide")

st.title("📊 Excel Data Inspector")
st.write("Upload your Excel file to get an immediate breakdown of your dataset.")

uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        # Load the data
        df = pd.read_excel(uploaded_file)
        
        # --- Overview Section ---
        st.header("📌 Dataset Overview")
        col1, col2, col3 = st.columns(3)
        
        num_rows = df.shape[0]
        num_cols = df.shape[1]
        
        col1.metric("Total Rows", num_rows)
        col2.metric("Total Columns", num_cols)
        col3.metric("Duplicate Rows", int(df.duplicated().sum()))

        # --- Column Insights ---
        st.header("🔍 Column-by-Column Insights")
        
        analysis_data = []
        
        for col in df.columns:
            # Explicitly force everything to native Python types
            col_dtype = str(df[col].dtype)
            nunique = int(df[col].nunique())
            null_count = int(df[col].isnull().sum())
            null_pct = (null_count / num_rows) * 100
            
            if nunique < 20:
                unique_list = df[col].unique().tolist()
                unique_vals = ", ".join(map(str, unique_list))
            else:
                unique_vals = "More than 20 unique values"
            
            analysis_data.append({
                "Column Name": str(col),
                "Data Type": col_dtype,
                "Unique Count": nunique,
                "Unique Values": unique_vals,
                "Null Values": null_count,
                "Null Percentage": f"{null_pct:.2f}%"
            })
            
        # Create DataFrame
        analysis_df = pd.DataFrame(analysis_data)
        
        # THE ARROW FIX: Force columns that cause issues to be string-only
        # This prevents PyArrow from getting confused by "Object" types
        columns_to_fix = ["Column Name", "Data Type", "Unique Values"]
        for c in columns_to_fix:
            analysis_df[c] = analysis_df[c].astype(str)

        st.dataframe(analysis_df, use_container_width=True)

        # --- Advanced Stats ---
        with st.expander("📈 Advanced Statistics & Memory"):
            st.subheader("Numerical Summary")
            numeric_df = df.select_dtypes(include=['number'])
            if not numeric_df.empty:
                st.write(numeric_df.describe())
            else:
                st.info("No numerical columns found.")
            
            st.divider()
            mem_usage = df.memory_usage(deep=True).sum() / 1024
            st.write(f"Total Memory Consumption: **{mem_usage:.2f} KB**")

        # --- Data Preview ---
        st.header("👀 Data Preview")
        st.dataframe(df.head(10))

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.info("Tip: This often happens if the Excel file has very complex formatting or hidden characters.")
else:
    st.info("Please upload an Excel file to begin.")
