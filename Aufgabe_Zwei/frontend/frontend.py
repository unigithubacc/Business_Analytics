import streamlit as st

st.set_page_config(page_title="Analytics", layout="wide")

p1 = st.Page("pages/page1.py", title="Page 1", icon=":material/query_stats:")
p2 = st.Page("pages/page2.py", title="Page 2", icon=":material/query_stats:")
p3 = st.Page("pages/page3.py", title="Page 3", icon=":material/query_stats:")
p4 = st.Page("pages/page4.py", title="Page 4", icon=":material/query_stats:")
p5 = st.Page("pages/page5.py", title="Page 5 Linien", icon=":material/query_stats:")
p6 = st.Page("pages/page6.py", title="Page 6 Balken", icon=":material/query_stats:")
p7 = st.Page("pages/page7.py", title="Page 7", icon=":material/query_stats:")
p8 = st.Page("pages/page8.py", title="Page 8 Balken von 4", icon=":material/query_stats:")

# install Multipage
pg = st.navigation({
    "Pages": [p1, p2, p3, p4, p5, p6, p7, p8],
})
pg.run()

