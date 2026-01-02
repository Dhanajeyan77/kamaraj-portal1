import os
import psycopg2

def add_students():
    # 1. Get the Neon URL from the environment variable
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL is not set. Run 'export DATABASE_URL=...' first.")
        return

    try:
        # 2. Connect to Neon
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # List: (Roll No, Password, Name, Is_Admin)
        # We do NOT include 'id' here so the database can auto-increment it
        students = [('24CP001','24cp001','MOHANA M',True),
            ('24UCS003', '24ucs003', 'SHIVA DHARANI P S', False),
            ('24UCS009', '24ucs009', 'PRAMILA J', False),
            ('24UCS010', '24ucs010', 'CHANDRAMADAV S', False),
            ('24UCS011', '24ucs011', 'AAKASH A', False),
            ('24UCS012', '24ucs012', 'VIGNESHWARAN R', False),
            ('24UCS016', '24ucs016', 'NAAVNEETH V R', False),
            ('24UCS022', '24ucs022', 'REHAN SIDDIQ A', False),
            ('24UCS023', '24ucs023', 'DHANWANTH RAJ N', False),
            ('24UCS027', '24ucs027', 'PADMA MUNISH DHANAJEYAN T', True), 
            ('24UCS028', '24ucs028', 'HARINI B', False),
            ('24UCS030', '24ucs030', 'SARAVANAKUMAR.M', False),
            ('24UCS031', '24ucs031', 'PAVITRA DHARNITHA S', False),
            ('24UCS032', '24ucs032', 'PRAJAN Y', False),
            ('24UCS033', '24ucs033', 'SARWESVARAN P', False),
            ('24UCS039', '24ucs039', 'GOBINATH.M', False),
            ('24UCS049', '24ucs049', 'PRANAVMUTHUVEL.B', False),
            ('24UCS057', '24ucs057', 'JEGANNAATHAN S J', False),
            ('24UCS058', '24ucs058', 'NITHYASHREE K', False),
            ('24UCS059', '24ucs059', 'GURUPRASATH M', False),
            ('24UCS060', '24ucs060', 'SANJAY I', False),
            ('24UCS062', '24ucs062', 'NAGAVELRAJAN M', False),
            ('24UCS068', '24ucs068', 'HEMALATHA S', False),
            ('24UCS071', '24ucs071', 'DAKSHA MΟΝΙΚΑ ΚΟ', False),
            ('24UCS072', '24ucs072', 'SYED SHAJEEA S', False),
            ('24UCS077', '24ucs077', 'PRIYADHARSHINI R', False),
            ('24UCS083', '24ucs083', 'VAISHNAVIS', False),
            ('24UCS085', '24ucs085', 'HARI KRISHNAN M', False),
            ('24UCS087', '24ucs087', 'RENITHA U', False),
            ('24UCS088', '24ucs088', 'SUJITHA T', False),
            ('24UCS090', '24ucs090', 'BAVADARINI S', False),
            ('24UCS093', '24ucs093', 'PAULPANDI K', False),
            ('24UCS096', '24ucs096', 'HARINATH S', False),
            ('24UCS098', '24ucs098', 'KIRUTHIKA A', False),
            ('24UCS101', '24ucs101', 'SUWEDHIKA S', False),
            ('24UCS108', '24ucs108', 'MANOJKUMAR P', False),
            ('24UCS109', '24ucs109', 'SHAFINA J', False),
            ('24UCS114', '24ucs114', 'KARTHIKA S', False),
            ('24UCS118', '24ucs118', 'BHARATHI MEENA D', False),
            ('24UCS119', '24ucs119', 'SELVALAKSHMI S', False),
            ('24UCS122', '24ucs122', 'RASHIKA G', False),
            ('24UCS127', '24ucs127', 'VAITHEESHWARI S', False),
            ('24UCS130', '24ucs130', 'SAMEER S', False),
            ('24UCS136', '24ucs136', 'DHARANIKUMAR M', False),
            ('24UCS140', '24ucs140', 'YAZHINI K', False),
            ('24UCS144', '24ucs144', 'SHRI DHARSHINI S', False),
            ('24UCS145', '24ucs145', 'MOHAMED PARVES M', False),
            ('24UCS148', '24ucs148', 'DEEPIKA S', False),
            ('24UCS150', '24ucs150', 'RAKSHIGA BG', False),
            ('24UCS152', '24ucs152', 'SRI GAYATHRI.S', False),
            ('24UCS155', '24ucs155', 'SUREKA R', False),
            ('24UCS159', '24ucs159', 'NETHRA S', False),
            ('24UCS163', '24ucs163', 'SRIVARSHA T', False),
            ('24UCS165', '24ucs165', 'VISHWA R', False),
            ('24UCS169', '24ucs169', 'SANTHOSHKUMAR U', False),
            ('24UCS171', '24ucs171', 'ARIHARAN N', False),
            ('24UCS172', '24ucs172', 'ABISHEK M', False),
            ('24UCS173', '24ucs173', 'VARSHINI PRIYA S', False),
            ('24UCS174', '24ucs174', 'HARIHARASUDHAN S', False),
            ('24UCS178', '24ucs178', 'VEERENDHRA PANDDI G', False),
            ('24UCS184', '24ucs184', 'SRI RANJANI A', False),
            ('24UCS185', '24ucs185', 'BENOLIN', False),
            ('24UCS189', '24ucs189', 'AMEERA ALIMA U', False),
            ('24UCS190', '24ucs190', 'KAVI PRAKASH P', False),
            ('24UCS191', '24ucs191', 'PRIYAN KUMAR K', False)
        ]
        
        # We specify exactly which columns to insert into
        # This allows the 'id' column to handle itself
        query = """
            INSERT INTO users (roll_no, password, name, is_admin) 
            VALUES (%s, %s, %s, %s) 
            ON CONFLICT (roll_no) DO NOTHING
        """
        
        cursor.executemany(query, students)
        conn.commit()
        print(f"✅ Successfully added {len(students)} students to Neon.")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    add_students()