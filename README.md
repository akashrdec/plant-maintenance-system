# Moon Beverages – Plant Maintenance Management System (Free Web App)

## Yeh kya hai?
Excel wale system ka **free Web Application** version.  
Browser mein chalega, phone se bhi use kar sakte ho.

---

## Kaise Chalaye (3 Tarike)

### Tarika 1: Apne Computer / Laptop par (Sabse Easy)

1. Pehle **Python** install ho hona chahiye (python.org se free download)
2. Is folder ko open karein
3. Command Prompt / Terminal mein yeh commands chalayein:

```bash
pip install -r requirements.txt
streamlit run app.py
```

4. Browser automatic khul jayega → App ready

---

### Tarika 2: Free Online Hosting (Streamlit Cloud) – Recommended

1. https://share.streamlit.io par free account banayein (GitHub se login)
2. Is pure folder ko GitHub par upload karein
3. Streamlit Cloud mein “New App” → apna GitHub repo select karein
4. Main file: `app.py` select karein
5. Deploy dabayein
6. Kuch minute mein aapka **live website link** mil jayega
7. Link kisi ko bhi de sakte ho – bilkul free

---

### Tarika 3: Phone se use
- Tarika 2 se jo link milega, usko phone browser mein open karein
- Ya laptop par chalaye aur same WiFi par phone se access karein

---

## App mein kya-kya hai

| Page | Kaam |
|------|------|
| Dashboard | Poora overview (Maintenance + Spare + PM) |
| Maintenance Entry | Daily jobs add karo (Auto Job ID + Downtime) |
| Spare Parts | Master + Receipt/Issue + Stock status |
| PM Schedule | Preventive maintenance planning |
| Master Data | Dropdown lists manage karo |

---

## Data kahan save hota hai?
- App ke andar `data` folder mein CSV files banti hain
- Aapka data aapke computer / hosting par hi rehta hai

---

Moon Beverages Pvt. Ltd. | Free Plant Maintenance System
