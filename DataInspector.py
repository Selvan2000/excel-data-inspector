import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Inspector Dashboard", layout="wide")

st.title("📊 Excel Data Inspector")
st.write("Upload your Excel file to get an immediate breakdown of your dataset.")

# 1. File Upload
uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        # Load the dataframe
        df = pd.read_excel(uploaded_file)
        
        # --- Overview Section ---
        st.header("📌 Dataset Overview")
        col1, col2, col3 = st.columns(3)
        
        num_rows = df.shape[0]
        num_cols = df.shape[1]
        
        col1.metric("Total Rows", num_rows)
        col2.metric("Total Columns", num_cols)
        col3.metric("Duplicate Rows", df.duplicated().sum())

        # --- Detailed Column Analysis ---
        st.header("🔍 Column-by-Column Insights")
        
        analysis_data = []
        
        for col in df.columns:
            dtype = df[col].dtype
            nunique = df[col].nunique()
            null_count = df[col].isnull().sum()
            null_pct = (null_count / num_rows) * 100
            
            # Logic for unique values list
            if nunique < 20:
                unique_vals = df[col].unique().tolist()
            else:
                unique_vals = "More than 20 unique values"
            
            analysis_data.append({
                "Column Name": col,
                "Data Type": dtype,
                "Unique Count": nunique,
                "Unique Values": unique_vals,
                "Null Values": null_count,
                "Null Percentage": f"{null_pct:.2f}%"
            })
            
        # Display as a clean table
        analysis_df = pd.DataFrame(analysis_data)
        st.dataframe(analysis_df, use_container_width=True)

        # --- Additional Useful Insights ---
        with st.expander("📈 Advanced Statistics & Memory"):
            st.subheader("Numerical Summary")
            # Only show describe for numeric columns
            if not df.select_dtypes(include=['number']).empty:
                st.write(df.describe())
            else:
                st.info("No numerical columns found for statistical summary.")
            
            st.divider()
            
            st.subheader("Memory Usage")
            mem_usage = df.memory_usage(deep=True).sum() / 1024  # Convert to KB
            st.write(f"Total Memory Consumption: **{mem_usage:.2f} KB**")

        # --- Data Preview ---
        st.header("👀 Data Preview")
        st.dataframe(df.head(10))

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please upload an Excel file to begin.")