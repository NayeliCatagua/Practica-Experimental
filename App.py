from flask import Flask, render_template, request, redirect,  url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#conexion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'opticatriem'
mysql = MySQL(app)

#settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index(): 
    cur = mysql.connection.cursor()
    cur.execute('SELECT ID, NumFactura, Comprador, Vendedor, PrecioTotal, IvaTotal FROM venta')
    data = cur.fetchall()
    return render_template('index.html', venta = data )

@app.route('/add_venta', methods=['POST'])
def add_venta():
    if request.method == 'POST':
        num_factura = request.form['num_factura'] 
        comprador = request.form['comprador']
        vendedor = request.form['vendedor'] 
        precio_total = request.form['precio_total']
        iva_total = request.form['iva_total'] 
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO venta (NumFactura, Comprador, Vendedor, PrecioTotal, IvaTotal) VALUES (%s, %s, %s, %s, %s)',
        (num_factura, comprador, vendedor, precio_total, iva_total))
        mysql.connection.commit()
        flash('Venta Agregada Satisfactoriamente')
        return redirect(url_for('Index'))
    else:
        return render_template('add_venta.html')
    
@app.route('/edit/<id>') 
def get_venta(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT ID, NumFactura, Comprador, Vendedor, PrecioTotal, IvaTotal FROM venta WHERE id = %s',(id,))
    data = cur.fetchall()
    return render_template('editventa.html', venta = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_venta(id):
    if request.method == 'POST':
        numfactura = request.form['num_factura']
        comprador = request.form['comprador']
        vendedor = request.form['vendedor']
        preciototal = request.form['precio_total']
        ivatotal = request.form['iva_total']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE venta
        SET numfactura = %s,
            comprador = %s,
            vendedor = %s,
            preciototal = %s,
            ivatotal = %s
        WHERE id = %s
    """, (numfactura, comprador, vendedor, preciototal, ivatotal, id))
        mysql.connection.commit()
        flash('Venta Actualizada Satisfactoriamente')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_venta(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM venta WHERE id = %s',(id,))
    mysql.connection.commit()
    flash('Venta removida satisfactoriamente')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)