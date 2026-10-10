"""
Moon Beverages Pvt. Ltd.
Plant Maintenance Management System - Free Web App
Built with Streamlit (100% Free)
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import json

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="Moon Beverages | Plant Maintenance",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1B4F72, #2E86AB);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 1.5rem;
    }
    .kpi-card {
        background: white;
        border: 2px solid #1B4F72;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1B4F72;
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #555;
        font-weight: 600;
    }
    .stDataFrame {
        border: 1px solid #ddd;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA STORAGE ====================
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

FILES = {
    "maintenance": f"{DATA_DIR}/maintenance.csv",
    "spares": f"{DATA_DIR}/spares.csv",
    "spare_txn": f"{DATA_DIR}/spare_transactions.csv",
    "pm": f"{DATA_DIR}/pm_schedule.csv",
    "master": f"{DATA_DIR}/master.json"
}

# Default Master Data
DEFAULT_MASTER = {
    "shifts": ["General", "A (Morning)", "B (Evening)", "C (Night)"],
    "engineers": ["Rahul Sharma", "Amit Verma", "Suresh Patel", "Priya Singh", "Vikram Yadav", "Neha Gupta", "Rajesh Kumar", "Anita Desai"],
    "areas": ["Filling Line 1", "Filling Line 2", "Filling Line 3", "Filling Line 4", "Filling Line 5",
              "Packaging Area", "Process Area", "Utilities / Boiler", "ETP / WTP", "Warehouse", "Mezzanine Floor", "Other"],
    "statuses": ["Completed", "Pending", "In Progress", "On Hold"],
    "priorities": ["Critical", "High", "Medium", "Low"],
    "work_types": ["Breakdown", "Corrective", "Preventive", "Inspection", "Other"],
    "pending_reasons": ["Material Not Available", "Waiting for Spares", "Waiting for Specialist", "Production Running", "Tools Not Available", "Other"]
}

def load_master():
    if os.path.exists(FILES["master"]):
        with open(FILES["master"], "r") as f:
            return json.load(f)
    return DEFAULT_MASTER.copy()

def save_master(data):
    with open(FILES["master"], "w") as f:
        json.dump(data, f, indent=2)

def load_df(key, columns):
    if os.path.exists(FILES[key]):
        df = pd.read_csv(FILES[key])
        return df
    return pd.DataFrame(columns=columns)

def save_df(key, df):
    df.to_csv(FILES[key], index=False)

# ==================== LOAD DATA ====================
master = load_master()

maint_cols = ["JobID", "ReportDate", "Shift", "Engineer", "Area", "Equipment", "Problem",
              "WorkType", "Priority", "Status", "StartTime", "EndTime", "Downtime",
              "SpareCode", "SpareQty", "PendingReason", "NextAction", "ActionTaken", "VerifiedBy", "Remarks"]
spare_cols = ["PartCode", "PartName", "Category", "Unit", "MinStock", "MaxStock", "ReorderLevel", "CurrentStock", "Location"]
txn_cols = ["TxnID", "Date", "Type", "PartCode", "PartName", "Qty", "Unit", "JobID", "By", "Remarks"]
pm_cols = ["PMID", "AreaEquipment", "Description", "Frequency", "LastDone", "NextDue", "AssignedTo", "Status", "Remarks"]

df_maint = load_df("maintenance", maint_cols)
df_spares = load_df("spares", spare_cols)
df_txn = load_df("spare_txn", txn_cols)
df_pm = load_df("pm", pm_cols)

# ==================== SIDEBAR ====================
st.sidebar.image("https://via.placeholder.com/220x60/1B4F72/FFFFFF?text=Moon+Beverages", use_container_width=True)
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Dashboard", "📝 Maintenance Entry", "🔧 Spare Parts", "📅 PM Schedule", "⚙️ Master Data", "ℹ️ About"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info("**Main Entry:** Maintenance Entry page se daily jobs add karein.\n\nBaaki sab automatic update hota hai.")

# ==================== DASHBOARD ====================
if page == "🏠 Dashboard":
    st.markdown('<div class="main-header"><h2>🏭 Plant Maintenance Executive Dashboard</h2><p>Moon Beverages Pvt. Ltd. | Live Overview</p></div>', unsafe_allow_html=True)
    
    # Maintenance KPIs
    st.subheader("1. Maintenance Performance")
    total = len(df_maint)
    completed = len(df_maint[df_maint["Status"] == "Completed"]) if total > 0 else 0
    pending = len(df_maint[df_maint["Status"] == "Pending"]) if total > 0 else 0
    inprog = len(df_maint[df_maint["Status"] == "In Progress"]) if total > 0 else 0
    onhold = len(df_maint[df_maint["Status"] == "On Hold"]) if total > 0 else 0
    completion = (completed / total * 100) if total > 0 else 0
    
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Jobs", total)
    c2.metric("Completed", completed)
    c3.metric("Pending", pending)
    c4.metric("In Progress", inprog)
    c5.metric("On Hold", onhold)
    c6.metric("Completion %", f"{completion:.1f}%")
    
    st.markdown("---")
    
    # Spares + PM
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("2. Spare Parts Status")
        if len(df_spares) > 0:
            ok = len(df_spares[df_spares["CurrentStock"] > df_spares["ReorderLevel"]])
            low = len(df_spares[(df_spares["CurrentStock"] <= df_spares["ReorderLevel"]) & (df_spares["CurrentStock"] > df_spares["MinStock"])])
            reorder = len(df_spares[df_spares["CurrentStock"] <= df_spares["MinStock"]])
            st.write(f"**Total Parts:** {len(df_spares)}")
            st.success(f"OK Stock: {ok}")
            st.warning(f"LOW Stock: {low}")
            st.error(f"REORDER Required: {reorder}")
        else:
            st.info("Abhi koi spare master entry nahi hai. Spare Parts page se add karein.")
    
    with col2:
        st.subheader("3. PM Compliance")
        if len(df_pm) > 0:
            # Calculate status
            today = datetime.now().date()
            overdue = 0
            duesoon = 0
            ok_pm = 0
            for _, row in df_pm.iterrows():
                try:
                    nd = pd.to_datetime(row["NextDue"]).date()
                    if nd < today:
                        overdue += 1
                    elif nd <= today + timedelta(days=7):
                        duesoon += 1
                    else:
                        ok_pm += 1
                except:
                    pass
            st.write(f"**Total PM Tasks:** {len(df_pm)}")
            st.success(f"On Track: {ok_pm}")
            st.warning(f"Due Soon: {duesoon}")
            st.error(f"OVERDUE: {overdue}")
            compliance = (ok_pm / len(df_pm) * 100) if len(df_pm) > 0 else 0
            st.metric("Compliance %", f"{compliance:.1f}%")
        else:
            st.info("Abhi koi PM Schedule nahi hai.")
    
    st.markdown("---")
    st.subheader("Recent Maintenance Jobs")
    if len(df_maint) > 0:
        st.dataframe(df_maint.tail(10).iloc[::-1], use_container_width=True, hide_index=True)
    else:
        st.info("Abhi koi maintenance record nahi hai. Maintenance Entry page se pehli entry karein.")

# ==================== MAINTENANCE ENTRY ====================
elif page == "📝 Maintenance Entry":
    st.markdown('<div class="main-header"><h2>📝 Daily Maintenance Record</h2><p>Main data entry sheet – yahan se jobs add karein</p></div>', unsafe_allow_html=True)
    
    with st.form("maint_form", clear_on_submit=True):
        st.subheader("New Job Entry")
        c1, c2, c3 = st.columns(3)
        with c1:
            report_date = st.date_input("Report Date", datetime.now())
            shift = st.selectbox("Shift", master["shifts"])
            engineer = st.selectbox("Shift Engineer", master["engineers"])
        with c2:
            area = st.selectbox("Area", master["areas"])
            equipment = st.text_input("Equipment / Machine")
            work_type = st.selectbox("Work Type", master["work_types"])
        with c3:
            priority = st.selectbox("Priority", master["priorities"])
            status = st.selectbox("Status", master["statuses"])
            problem = st.text_input("Problem Description")
        
        c4, c5, c6 = st.columns(3)
        with c4:
            start_time = st.time_input("Start Time")
            end_time = st.time_input("End Time")
        with c5:
            spare_code = st.text_input("Spare Part Code (optional)")
            spare_qty = st.number_input("Spare Qty Used", min_value=0, value=0)
        with c6:
            pending_reason = st.selectbox("Pending Reason (if Pending)", [""] + master["pending_reasons"])
            next_action = st.text_input("Next Action")
        
        action_taken = st.text_area("Action Taken")
        c7, c8 = st.columns(2)
        with c7:
            verified = st.text_input("Verified By")
        with c8:
            remarks = st.text_input("Remarks")
        
        submitted = st.form_submit_button("✅ Save Job", use_container_width=True)
        
        if submitted:
            # Generate Job ID
            date_str = report_date.strftime("%Y%m%d")
            existing = df_maint[df_maint["JobID"].str.contains(date_str, na=False)] if len(df_maint) > 0 else pd.DataFrame()
            seq = len(existing) + 1
            job_id = f"MB-{date_str}-{seq:03d}"
            
            # Downtime calculation
            downtime = ""
            try:
                t1 = datetime.combine(report_date, start_time)
                t2 = datetime.combine(report_date, end_time)
                if t2 > t1:
                    diff = t2 - t1
                    hours = int(diff.total_seconds() // 3600)
                    mins = int((diff.total_seconds() % 3600) // 60)
                    downtime = f"{hours}h {mins}m"
            except:
                downtime = ""
            
            new_row = {
                "JobID": job_id,
                "ReportDate": report_date.strftime("%Y-%m-%d"),
                "Shift": shift,
                "Engineer": engineer,
                "Area": area,
                "Equipment": equipment,
                "Problem": problem,
                "WorkType": work_type,
                "Priority": priority,
                "Status": status,
                "StartTime": start_time.strftime("%H:%M"),
                "EndTime": end_time.strftime("%H:%M"),
                "Downtime": downtime,
                "SpareCode": spare_code,
                "SpareQty": spare_qty,
                "PendingReason": pending_reason,
                "NextAction": next_action,
                "ActionTaken": action_taken,
                "VerifiedBy": verified,
                "Remarks": remarks
            }
            df_maint = pd.concat([df_maint, pd.DataFrame([new_row])], ignore_index=True)
            save_df("maintenance", df_maint)
            st.success(f"✅ Job saved successfully! Job ID: **{job_id}** | Downtime: {downtime}")
            st.rerun()
    
    st.markdown("---")
    st.subheader("All Maintenance Records")
    if len(df_maint) > 0:
        st.dataframe(df_maint.iloc[::-1], use_container_width=True, hide_index=True)
        
        # Download
        csv = df_maint.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download as CSV", csv, "maintenance_records.csv", "text/csv")
    else:
        st.info("Abhi koi record nahi hai.")

# ==================== SPARE PARTS ====================
elif page == "🔧 Spare Parts":
    st.markdown('<div class="main-header"><h2>🔧 Spare Parts Management</h2></div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Spare Master", "Transaction (Receipt/Issue)", "Stock Status"])
    
    with tab1:
        st.subheader("Add / View Spare Master")
        with st.form("spare_master_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                pcode = st.text_input("Part Code")
                pname = st.text_input("Part Name")
            with c2:
                pcat = st.text_input("Category")
                punit = st.selectbox("Unit", ["Nos", "Set", "Kg", "Ltr", "Can", "Mtr"])
            with c3:
                min_s = st.number_input("Min Stock", min_value=0, value=2)
                max_s = st.number_input("Max Stock", min_value=0, value=20)
                reorder = st.number_input("Reorder Level", min_value=0, value=5)
                loc = st.text_input("Location", value="Store-A")
            
            if st.form_submit_button("Add Spare"):
                if pcode and pname:
                    new_s = {
                        "PartCode": pcode, "PartName": pname, "Category": pcat, "Unit": punit,
                        "MinStock": min_s, "MaxStock": max_s, "ReorderLevel": reorder,
                        "CurrentStock": 0, "Location": loc
                    }
                    df_spares = pd.concat([df_spares, pd.DataFrame([new_s])], ignore_index=True)
                    save_df("spares", df_spares)
                    st.success("Spare added!")
                    st.rerun()
        
        if len(df_spares) > 0:
            st.dataframe(df_spares, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Spare Transaction")
        with st.form("txn_form"):
            c1, c2, c3 = st.columns(3)
            with c1:
                tdate = st.date_input("Date", datetime.now())
                ttype = st.selectbox("Type", ["Receipt", "Issue"])
            with c2:
                tcode = st.selectbox("Part Code", df_spares["PartCode"].tolist() if len(df_spares) > 0 else [""])
                tqty = st.number_input("Qty", min_value=1, value=1)
            with c3:
                tjob = st.text_input("Reference Job ID (optional)")
                tby = st.text_input("By")
            
            tremarks = st.text_input("Remarks")
            if st.form_submit_button("Save Transaction"):
                if tcode:
                    txn_id = f"ST-{len(df_txn)+1:03d}"
                    pname = df_spares[df_spares["PartCode"]==tcode]["PartName"].values[0] if len(df_spares) > 0 else ""
                    unit = df_spares[df_spares["PartCode"]==tcode]["Unit"].values[0] if len(df_spares) > 0 else ""
                    
                    new_t = {
                        "TxnID": txn_id, "Date": tdate.strftime("%Y-%m-%d"), "Type": ttype,
                        "PartCode": tcode, "PartName": pname, "Qty": tqty, "Unit": unit,
                        "JobID": tjob, "By": tby, "Remarks": tremarks
                    }
                    df_txn = pd.concat([df_txn, pd.DataFrame([new_t])], ignore_index=True)
                    save_df("spare_txn", df_txn)
                    
                    # Update stock
                    if len(df_spares) > 0:
                        idx = df_spares[df_spares["PartCode"]==tcode].index
                        if len(idx) > 0:
                            if ttype == "Receipt":
                                df_spares.loc[idx, "CurrentStock"] += tqty
                            else:
                                df_spares.loc[idx, "CurrentStock"] -= tqty
                            save_df("spares", df_spares)
                    
                    st.success(f"Transaction {txn_id} saved & stock updated!")
                    st.rerun()
        
        if len(df_txn) > 0:
            st.dataframe(df_txn.iloc[::-1], use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("Current Stock Status")
        if len(df_spares) > 0:
            def status(row):
                if row["CurrentStock"] <= row["MinStock"]:
                    return "REORDER"
                elif row["CurrentStock"] <= row["ReorderLevel"]:
                    return "LOW"
                return "OK"
            df_spares["Status"] = df_spares.apply(status, axis=1)
            st.dataframe(df_spares, use_container_width=True, hide_index=True)
        else:
            st.info("No spares yet.")

# ==================== PM SCHEDULE ====================
elif page == "📅 PM Schedule":
    st.markdown('<div class="main-header"><h2>📅 Preventive Maintenance Schedule</h2></div>', unsafe_allow_html=True)
    
    with st.form("pm_form"):
        c1, c2 = st.columns(2)
        with c1:
            pmid = st.text_input("PM ID (e.g. PM-001)")
            area_eq = st.text_input("Area / Equipment")
            desc = st.text_input("PM Description")
            freq = st.selectbox("Frequency", ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"])
        with c2:
            last_done = st.date_input("Last Done Date")
            assigned = st.selectbox("Assigned To", master["engineers"])
            remarks = st.text_input("Remarks")
        
        if st.form_submit_button("Add PM Task"):
            # Calculate Next Due
            if freq == "Daily":
                next_due = last_done + timedelta(days=1)
            elif freq == "Weekly":
                next_due = last_done + timedelta(days=7)
            elif freq == "Monthly":
                next_due = last_done + timedelta(days=30)
            elif freq == "Quarterly":
                next_due = last_done + timedelta(days=90)
            else:
                next_due = last_done + timedelta(days=365)
            
            today = datetime.now().date()
            if next_due < today:
                status = "OVERDUE"
            elif next_due <= today + timedelta(days=7):
                status = "DUE SOON"
            else:
                status = "OK"
            
            new_pm = {
                "PMID": pmid, "AreaEquipment": area_eq, "Description": desc, "Frequency": freq,
                "LastDone": last_done.strftime("%Y-%m-%d"), "NextDue": next_due.strftime("%Y-%m-%d"),
                "AssignedTo": assigned, "Status": status, "Remarks": remarks
            }
            df_pm = pd.concat([df_pm, pd.DataFrame([new_pm])], ignore_index=True)
            save_df("pm", df_pm)
            st.success(f"PM Task added! Next Due: {next_due} | Status: {status}")
            st.rerun()
    
    st.markdown("---")
    if len(df_pm) > 0:
        st.dataframe(df_pm, use_container_width=True, hide_index=True)
    else:
        st.info("No PM tasks yet.")

# ==================== MASTER DATA ====================
elif page == "⚙️ Master Data":
    st.markdown('<div class="main-header"><h2>⚙️ Master Data (Dropdown Lists)</h2><p>Yahan se lists manage karein – changes automatic dropdowns mein aa jayenge</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Shifts")
        new_shift = st.text_input("Add new Shift")
        if st.button("Add Shift") and new_shift:
            master["shifts"].append(new_shift)
            save_master(master)
            st.success("Added!")
            st.rerun()
        st.write(master["shifts"])
        
        st.subheader("Shift Engineers")
        new_eng = st.text_input("Add new Engineer")
        if st.button("Add Engineer") and new_eng:
            master["engineers"].append(new_eng)
            save_master(master)
            st.success("Added!")
            st.rerun()
        st.write(master["engineers"])
        
        st.subheader("Areas")
        new_area = st.text_input("Add new Area")
        if st.button("Add Area") and new_area:
            master["areas"].append(new_area)
            save_master(master)
            st.success("Added!")
            st.rerun()
        st.write(master["areas"])
    
    with col2:
        st.subheader("Statuses")
        st.write(master["statuses"])
        st.subheader("Priorities")
        st.write(master["priorities"])
        st.subheader("Work Types")
        st.write(master["work_types"])
        st.subheader("Pending Reasons")
        st.write(master["pending_reasons"])

# ==================== ABOUT ====================
else:
    st.markdown('<div class="main-header"><h2>ℹ️ About This System</h2></div>', unsafe_allow_html=True)
    st.write("""
    ### Moon Beverages Pvt. Ltd. – Plant Maintenance Management System
    
    **Free Web Application** built with Streamlit.
    
    #### Features:
    - Daily Maintenance Record with Auto Job ID & Downtime
    - Spare Parts Master + Receipt/Issue + Auto Stock
    - Preventive Maintenance Schedule with Auto Due Date & Status
    - Live Executive Dashboard
    - Master Data for dynamic dropdowns
    - Data saved locally (CSV files)
    
    #### How to use:
    1. **Maintenance Entry** se daily jobs add karein
    2. Spare aaye/jaaye to **Spare Parts** section use karein
    3. PM planning **PM Schedule** mein karein
    4. Dashboard automatic update hota rahega
    
    #### Deploy Free:
    - Streamlit Community Cloud par free host kar sakte ho
    - Ya apne computer par `streamlit run app.py` se chalao
    """)
    st.success("This app is 100% free to use and deploy.")
PYEOF