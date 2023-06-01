import pandas as pd
from sqlalchemy import create_engine

# create a connection to the SQLite database
engine = create_engine('sqlite:///your_database.db')

# define the SQL query in multiple steps for readability
query = """
SELECT 
    pbd_prod_code,
    psd_stk_qty + psd_booked_qty,
    pbd_prod_name || ' ' || COALESCE(pbd_prod_unit, '') || ' ' ||
    CASE 
        WHEN LENGTH(pbd_prod_ptr) = 5 THEN 
            CASE 
                WHEN SUBSTR(pbd_prod_ptr, 3) <= 700 THEN 
                    (SELECT TRIM(aca_cu_name) 
                    FROM admin.sffaca_details 
                    WHERE aca_cu_no = 'PTX0' || SUBSTR(pbd_prod_ptr, 1, 2) 
                    AND aca_addr_no = SUBSTR(pbd_prod_ptr, 3))
                ELSE 
                    (SELECT TRIM(aca_txt_l1) 
                    FROM admin.sffaca_other 
                    WHERE aca_cu_no = 'PTX0' || SUBSTR(pbd_prod_ptr, 1, 2) 
                    AND aca_addr_no = SUBSTR(pbd_prod_ptr, 3)) 
            END 
        WHEN LENGTH(pbd_prod_ptr) = 6 THEN 
            CASE 
                WHEN SUBSTR(pbd_prod_ptr, 4) <= 700 THEN 
                    (SELECT TRIM(aca_cu_name) 
                    FROM admin.sffaca_details 
                    WHERE aca_cu_no = 'PTX' || SUBSTR(pbd_prod_ptr, 1, 3) 
                    AND aca_addr_no = SUBSTR(pbd_prod_ptr, 4))
                ELSE 
                    (SELECT TRIM(aca_txt_l1) 
                    FROM admin.sffaca_other 
                    WHERE aca_cu_no = 'PTX' || SUBSTR(pbd_prod_ptr, 1, 3) 
                    AND aca_addr_no = SUBSTR(pbd_prod_ptr, 4)) 
            END 
    END AS Description,
    pbd_prod_pack, 
    pbd_vat_code, 
    pbd_split_price, 
    pbd_trade_price, 
    pbd_retail_price, 
    pbd_layer_qty, 
    pbd_pallet_size, 
    pxd_ean_code, 
    pbd_maj_grp, 
    pbd_min_grp, 
    pxd_flags_1, 
    pxd_flags_2, 
    pbd_prod_ptr, 
    CASE pbd_prod_unit WHEN 'Single' THEN '' ELSE pbd_prod_unit END, 
    psd_po_qty
FROM 
    admin.sffpbd 
LEFT JOIN 
    admin.sffpsd ON pbd_prod_ptr = psd_prod_ptr 
LEFT JOIN 
    admin.sffpxd_details ON pbd_prod_ptr = pxd_prod_ptr
WHERE 
    psd_stk_qty + psd_booked_qty + psd_po_qty > 0
ORDER BY 
    pbd_maj_grp ASC,
    pbd_min_grp ASC,
    pbd_prod_name ASC
"""

# execute the query and convert the result into a DataFrame
df = pd.read_sql_query(query, engine)
