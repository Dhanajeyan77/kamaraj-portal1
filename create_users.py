import sqlite3

def add_students():
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    
    # List: (Roll No, Password, Name, Is_Admin)
    students = [
        ('24UCS003', '24ucs003', 'SHIVA DHARANI P S', 0),
        ('24UCS009', '24ucs009', 'PRAMILA J', 0),
        ('24UCS010', '24ucs010', 'CHANDRAMADAV S', 0),
        ('24UCS011', '24ucs011', 'AAKASH A', 0),
        ('24UCS012', '24ucs012', 'VIGNESHWARAN R', 0),
        ('24UCS016', '24ucs016', 'NAAVNEETH V R', 0),
        ('24UCS022', '24ucs022', 'REHAN SIDDIQ A', 0),
        ('24UCS023', '24ucs023', 'DHANWANTH RAJ N', 0),
        ('24UCS027', '24ucs027', 'PADMA MUNISH DHANAJEYAN T', 1), # ADMIN SET
        ('24UCS028', '24ucs028', 'HARINI B', 0),
        ('24UCS030', '24ucs030', 'SARAVANAKUMAR.M', 0),
        ('24UCS031', '24ucs031', 'PAVITRA DHARNITHA S', 0),
        ('24UCS032', '24ucs032', 'PRAJAN Y', 0),
        ('24UCS033', '24ucs033', 'SARWESVARAN P', 0),
        ('24UCS039', '24ucs039', 'GOBINATH.M', 0),
        ('24UCS049', '24ucs049', 'PRANAVMUTHUVEL.B', 0),
        ('24UCS057', '24ucs057', 'JEGANNAATHAN S J', 0),
        ('24UCS058', '24ucs058', 'NITHYASHREE K', 0),
        ('24UCS059', '24ucs059', 'GURUPRASATH M', 0),
        ('24UCS060', '24ucs060', 'SANJAY I', 0),
        ('24UCS062', '24ucs062', 'NAGAVELRAJAN M', 0),
        ('24UCS068', '24ucs068', 'HEMALATHA S', 0),
        ('24UCS071', '24ucs071', 'DAKSHA MΟΝΙΚΑ ΚΟ', 0),
        ('24UCS072', '24ucs072', 'SYED SHAJEEA S', 0),
        ('24UCS077', '24ucs077', 'PRIYADHARSHINI R', 0),
        ('24UCS083', '24ucs083', 'VAISHNAVIS', 0),
        ('24UCS085', '24ucs085', 'HARI KRISHNAN M', 0),
        ('24UCS087', '24ucs087', 'RENITHA U', 0),
        ('24UCS088', '24ucs088', 'SUJITHA T', 0),
        ('24UCS090', '24ucs090', 'BAVADARINI S', 0),
        ('24UCS093', '24ucs093', 'PAULPANDI K', 0),
        ('24UCS096', '24ucs096', 'HARINATH S', 0),
        ('24UCS098', '24ucs098', 'KIRUTHIKA A', 0),
        ('24UCS101', '24ucs101', 'SUWEDHIKA S', 0),
        ('24UCS108', '24ucs108', 'MANOJKUMAR P', 0),
        ('24UCS109', '24ucs109', 'SHAFINA J', 0),
        ('24UCS114', '24ucs114', 'KARTHIKA S', 0),
        ('24UCS118', '24ucs118', 'BHARATHI MEENA D', 0),
        ('24UCS119', '24ucs119', 'SELVALAKSHMI S', 0),
        ('24UCS122', '24ucs122', 'RASHIKA G', 0),
        ('24UCS127', '24ucs127', 'VAITHEESHWARI S', 0),
        ('24UCS130', '24ucs130', 'SAMEER S', 0),
        ('24UCS136', '24ucs136', 'DHARANIKUMAR M', 0),
        ('24UCS140', '24ucs140', 'YAZHINI K', 0),
        ('24UCS144', '24ucs144', 'SHRI DHARSHINI S', 0),
        ('24UCS145', '24ucs145', 'MOHAMED PARVES M', 0),
        ('24UCS148', '24ucs148', 'DEEPIKA S', 0),
        ('24UCS150', '24ucs150', 'RAKSHIGA BG', 0),
        ('24UCS152', '24ucs152', 'SRI GAYATHRI.S', 0),
        ('24UCS155', '24ucs155', 'SUREKA R', 0),
        ('24UCS159', '24ucs159', 'NETHRA S', 0),
        ('24UCS163', '24ucs163', 'SRIVARSHA T', 0),
        ('24UCS165', '24ucs165', 'VISHWA R', 0),
        ('24UCS169', '24ucs169', 'SANTHOSHKUMAR U', 0),
        ('24UCS171', '24ucs171', 'ARIHARAN N', 0),
        ('24UCS172', '24ucs172', 'ABISHEK M', 0),
        ('24UCS173', '24ucs173', 'VARSHINI PRIYA S', 0),
        ('24UCS174', '24ucs174', 'HARIHARASUDHAN S', 0),
        ('24UCS178', '24ucs178', 'VEERENDHRA PANDDI G', 0),
        ('24UCS184', '24ucs184', 'SRI RANJANI A', 0),
        ('24UCS185', '24ucs185', 'BENOLIN', 0),
        ('24UCS189', '24ucs189', 'AMEERA ALIMA U', 0),
        ('24UCS190', '24ucs190', 'KAVI PRAKASH P', 0),
        ('24UCS191', '24ucs191', 'PRIYAN KUMAR K', 0)
    ]
    
    # Updated to include is_admin column
    cursor.executemany("INSERT OR IGNORE INTO users (roll_no, password, name, is_admin) VALUES (?, ?, ?, ?)", students)
    conn.commit()
    conn.close()
    print("✅ All 64 students added with Admin roles configured.")

if __name__ == "__main__":
    add_students()