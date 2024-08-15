import xmlrpc.client
import ssl
from datetime import datetime, timedelta

# Odoo server configuration
DB = ''
URL = ''
USERNAME = ''
PASSWORD = ''

# Disable SSL verification
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def connect_to_odoo():
    try:
        common = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/common', context=ctx)
        uid = common.authenticate(DB, USERNAME, PASSWORD, {})
        models = xmlrpc.client.ServerProxy(f'{URL}/xmlrpc/2/object', context=ctx)
        return uid, models
    except xmlrpc.client.ProtocolError as e:
        print(f"Error connecting to Odoo: {e}")
        return None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None

def fetch_sales_data(uid, models):
    try:
        end_date = datetime.now()
        # Define time frame 
        start_date = end_date - timedelta(days=90)

        sales_domain = [
            ('date_order', '>=', start_date.strftime('%Y-%m-%d')),
            ('date_order', '<=', end_date.strftime('%Y-%m-%d')),
            ('state', 'in', ['sale', 'done'])
        ]

        sale_order_ids = models.execute_kw(DB, uid, PASSWORD, 'sale.order', 'search', [sales_domain])
        sale_orders = models.execute_kw(DB, uid, PASSWORD, 'sale.order', 'read', [sale_order_ids], {'fields': ['order_line']})
        
        product_ids = set()
        for order in sale_orders:
            order_line_ids = order['order_line']
            order_lines = models.execute_kw(DB, uid, PASSWORD, 'sale.order.line', 'read', [order_line_ids], {'fields': ['product_id']})
            product_ids.update(line['product_id'][0] for line in order_lines)
        
        return list(product_ids)
    except xmlrpc.client.Fault as e:
        print(f"Error fetching sales data: {e}")
        return []

def main():
    uid, models = connect_to_odoo()
    if not uid or not models:
        return

    product_ids = fetch_sales_data(uid, models)
    if not product_ids:
        return

    print(product_ids)

if __name__ == "__main__":
    main()
    
# [6784, 2111]
